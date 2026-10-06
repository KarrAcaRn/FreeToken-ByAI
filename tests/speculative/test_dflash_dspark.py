"""DeepSpec "DSpark" drafters (PixelML's Qwen3.8-Flash-Next DFlash): flat config, and the
anchor row predicts the next token, so K query rows give K drafts."""

from freetoken.speculative.dflash.config import DFlashConfig

DSPARK_CFG = {
    "architectures": ["Qwen3DSparkModel"],
    "block_size": 7,
    "mask_token_id": 248077,
    "target_layer_ids": [3, 15, 23, 35, 43],
    "num_target_layers": 48,
    "markov_rank": 0,
    "hidden_size": 2560,
    "num_hidden_layers": 5,
    "head_dim": 256,
    "sliding_window": None,
    "layer_types": ["full_attention"] * 5,
}


def test_dspark_config_reads_the_flat_fields():
    cfg = DFlashConfig.from_hf_config(DSPARK_CFG)
    assert cfg.query_zero_predicts_next
    assert cfg.target_layer_ids == [3, 15, 23, 35, 43]  # not the derived spread
    assert cfg.block_size == 8  # verify block: anchor + 7 drafts
    assert cfg.layer_windows == [None] * 5
    assert not cfg.is_dflash2


def test_zlab_config_keeps_its_convention():
    cfg = DFlashConfig.from_hf_config({"dflash_config": {"block_size": 16, "target_layer_ids": [1, 2]}})
    assert not cfg.query_zero_predicts_next and cfg.block_size == 16
