import numpy as np
from keras_cv_attention_models import backend
from keras_cv_attention_models.backend import layers, models, functional
from keras_cv_attention_models.models import register_model
from keras_cv_attention_models.download_and_load import reload_model_weights
from keras_cv_attention_models.attention_layers import activation_by_name, CausalMask
from keras_cv_attention_models.gpt2.gpt2 import RunPrediction


PRETRAINED_DICT = {
    "llama2_110m": {"tiny_stories": "92b530d129f5b3c70c190669cb48b5bb"},
    "llama2_15m": {"tiny_stories": "b16894b3e40703d941e08b83767dd826"},
    "llama2_42m": {"tiny_stories": "35d924a79d6f8b1e3dcb4af8a9ae6863"},
}


@backend.register_keras_serializable(package="kecam/llama2")
class PositionalEncodingFourierRot1D(layers.Layer):
    def __init__(self, max_block_size, temperature=1e4, **kwargs):
        super().__init__(**kwargs)
        self.temperature, self.max_block_size = float(temperature), max_block_size

    def build(self, input_shape):
        # input: `[batch, ..., attn_height * attn_width, num_heads, channels // num_heads // 2, 2]`.
        # print(input_shape)
        self.channels = input_shape[-2] * input_shape[-1]
        pos_filters = self.channels // 2
        dim_t = self.temperature ** (np.arange(pos_filters, dtype="float32") / pos_filters)  # (filters,)
        grid = np.expand_dims(np.arange(self.max_block_size, dtype="float32"), -1) / dim_t
        pos_sin, pos_cos = np.expand_dims(np.sin(grid), -2), np.expand_dims(np.cos(grid), -2)
        # print(f"{pos_sin.shape = }, {pos_cos.shape = }, {height = }, {width = }, {self.channels = }")

        if hasattr(self, "register_buffer"):  # PyTorch
            self.register_buffer("pos_sin", functional.convert_to_tensor(pos_sin, dtype=self.compute_dtype), persistent=False)
            self.register_buffer("pos_cos", functional.convert_to_tensor(pos_cos, dtype=self.compute_dtype), persistent=False)
        else:
            self.pos_sin = functional.convert_to_tensor(pos_sin, dtype=self.compute_dtype)
            self.pos_cos = functional.convert_to_tensor(pos_cos, dtype=self.compute_dtype)
        super().build(input_shape)

    def call(self, inputs, **kwargs):
        left, right = functional.unstack(inputs, axis=-1)
        pos_cos, pos_sin = self.pos_cos[: left.shape[-3]], self.pos_sin[: left.shape[-3]]
        out = functional.stack([left * pos_cos - right * pos_sin, right * pos_cos + left * pos_sin], axis=-1)
        return out

    def get_config(self):
        base_config = super().get_config()
        base_config.update({"temperature": self.temperature, "max_block_size": self.max_block_size})
        return base_config


@backend.register_keras_serializable(package="kecam/llama2")
class RMSNorm(layers.Layer):
    def __init__(self, epsilon=1e-5, **kwargs):
        super().__init__(**kwargs)
        self.epsilon = epsilon

    def build(self, input_shape):
        self.gamma = self.add_weight(name="gamma", shape=(input_shape[-1],), initializer="ones", trainable=True)
        super().build(input_shape)

    def call(self, inputs):
        norm = inputs * functional.rsqrt(functional.reduce_mean(inputs**2, keepdims=True, axis=-1) + self.epsilon)
        return norm * self.gamma

    def get_config(self):
        base_config = super().get_config()
        base_config.update({"epsilon": self.epsilon})
        return base_config


def apply_positional_encoding_rotary(inputs, pos_emb_layer):
    """Reshape is separated out from PositionalEncodingFourierRot1D for setting as dynamic"""
    num_heads = inputs.shape[-2]
    nn = layers.Reshape([-1, num_heads, inputs.shape[-1] // 2, 2])(inputs)
    nn = pos_emb_layer(nn)
    out = layers.Reshape([-1, num_heads, inputs.shape[-1]])(nn)
    return out


def causal_self_attention(inputs, block_size, num_heads, use_bias=False, dropout=0, name=""):
    input_channels = inputs.shape[-1]
    key_dim = input_channels // num_heads
    qq_scale = 1.0 / (float(key_dim) ** 0.5)

    query = layers.Dense(input_channels, use_bias=use_bias, name=name + "q_proj")(inputs)
    key = layers.Dense(input_channels, use_bias=use_bias, name=name + "k_proj")(inputs)
    value = layers.Dense(input_channels, use_bias=use_bias, name=name + "v_proj")(inputs)

    # Create a new one every time, as there's no weights for this layer
    rope = PositionalEncodingFourierRot1D(max_block_size=block_size, name=name + "rope")
    query = layers.Reshape([-1, num_heads, key_dim])(query)
    query = apply_positional_encoding_rotary(query, rope)
    query = functional.transpose(query, [0, 2, 1, 3])

    key = layers.Reshape([-1, num_heads, key_dim])(key)
    key = apply_positional_encoding_rotary(key, rope)
    key = functional.transpose(key, [0, 2, 3, 1])

    value = functional.transpose(layers.Reshape([-1, num_heads, key_dim])(value), [0, 2, 1, 3])

    attn = (query @ key) * qq_scale
    attn = CausalMask(block_size=block_size)(attn)
    attn = layers.Softmax(axis=-1, name=name + "attention_scores")(attn)
    attn_out = attn @ value

    output = functional.transpose(attn_out, [0, 2, 1, 3])
    output = layers.Reshape([-1, input_channels])(output)
    output = layers.Dense(input_channels, use_bias=use_bias, name=name + "o_proj")(output)
    output = layers.Dropout(dropout)(output)
    return output


def attention_fft_block(inputs, block_size, num_heads, hidden_divisible=32, use_bias=False, dropout=0, activation="swish", name=""):
    input_channels = inputs.shape[-1]
    attn = RMSNorm(name=name + "input_layernorm")(inputs)
    attn = causal_self_attention(attn, block_size, num_heads, use_bias, dropout, name=name + "self_attn.")
    attn_out = inputs + attn

    hidden_dim = 2 * 4 * input_channels // 3
    hidden_dim = hidden_divisible * ((hidden_dim + hidden_divisible - 1) // hidden_divisible)
    # print(f"{input_channels = }, {hidden_divisible = }, {hidden_dim = }")

    fft = RMSNorm(name=name + "post_attention_layernorm")(attn_out)
    fft_1 = layers.Dense(hidden_dim, use_bias=use_bias, name=name + "mlp.gate_proj")(fft)
    fft_1 = activation_by_name(fft_1, activation=activation, name=name + "mlp.gate_proj.")
    fft_3 = layers.Dense(hidden_dim, use_bias=use_bias, name=name + "mlp.up_proj")(fft)
    fft = fft_1 * fft_3
    fft = layers.Dense(input_channels, use_bias=use_bias, name=name + "mlp.down_proj")(fft)
    fft = layers.Dropout(dropout)(fft)

    return layers.Add(name=name + "output")([attn_out, fft])


def LLaMA2(
    num_blocks=12,
    embedding_size=768,
    hidden_divisible=32,
    num_heads=12,
    block_use_bias=False,
    vocab_size=50304,
    max_block_size=2048,
    include_top=True,
    dropout=0.0,
    activation="swish",
    pretrained=None,
    model_name="llama2",
    kwargs=None,
):
    inputs = layers.Input([None], dtype="int64")
    tok_emb = layers.Embedding(vocab_size, embedding_size, name="embed_tokens")(inputs)
    nn = layers.Dropout(dropout)(tok_emb)

    for block_id in range(num_blocks):
        nn = attention_fft_block(nn, max_block_size, num_heads, hidden_divisible, block_use_bias, dropout, activation, name="blocks.{}.".format(block_id))
    nn = RMSNorm(name="norm")(nn)

    if include_top:
        nn = layers.Dense(vocab_size, use_bias=False, dtype="float32", name="lm_head")(nn)

    model = models.Model(inputs, nn, name=model_name)
    model.max_block_size = max_block_size  # or model.get_layer('pos_idx').block_size
    model.run_prediction = RunPrediction(model, tokenizer="SentencePieceTokenizer")
    reload_model_weights(model, PRETRAINED_DICT, "llama2", pretrained)
    return model


@register_model
def LLaMA2_15M(max_block_size=256, vocab_size=32000, include_top=True, activation="swish", pretrained="tiny_stories", **kwargs):
    num_blocks = 6
    embedding_size = 288
    num_heads = 6
    return LLaMA2(**locals(), **kwargs, model_name="llama2_15m")


@register_model
def LLaMA2_42M(max_block_size=1024, vocab_size=32000, include_top=True, activation="swish", pretrained="tiny_stories", **kwargs):
    num_blocks = 8
    embedding_size = 512
    num_heads = 8
    return LLaMA2(**locals(), **kwargs, model_name="llama2_42m")


@register_model
def LLaMA2_110M(max_block_size=1024, vocab_size=32000, include_top=True, activation="swish", pretrained="tiny_stories", **kwargs):
    num_blocks = 12
    embedding_size = 768
    num_heads = 12
    return LLaMA2(**locals(), **kwargs, model_name="llama2_110m")


@register_model
def LLaMA2_7B(max_block_size=2048, vocab_size=32000, include_top=True, activation="swish", pretrained=None, **kwargs):
    num_blocks = 32
    embedding_size = 4096
    hidden_divisible = 256
    num_heads = 32
    return LLaMA2(**locals(), **kwargs, model_name="llama2_7b")


""" Convert pytorch weights to h5 """


def convert_huggingface_weights_to_h5(source_pt_path, save_path="AUTO", name_convert_map={}, to_fp16=False):
    from keras_cv_attention_models.download_and_load import convert_torch_weights_to_h5

    skip_weights = [".num_batches_tracked", ".inv_freq"]
    name_convert_funcs = [
        lambda name: name.replace("layers.", "blocks."),
        lambda name: name[len("model.") :] if name.startswith("model.") else name,
    ]
    weight_convert_funcs = [lambda target_name, weight: weight.T if len(weight.shape) == 2 and "embed_tokens" not in target_name else weight]  # Dense weight
    return convert_torch_weights_to_h5(source_pt_path, save_path, skip_weights, name_convert_funcs, name_convert_map, weight_convert_funcs, to_fp16)


if __name__ == "__test__":
    from keras_cv_attention_models import llama2

    mm = llama2.LLaMA2_42M()
    mm.run_prediction("As evening fell, a maiden stood at the edge of a wood. In her hands,", num_samples=3)
