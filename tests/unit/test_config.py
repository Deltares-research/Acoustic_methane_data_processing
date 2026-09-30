from acoustic_methane.config import load_config


def test_load_config_empty(tmp_path):
    cfg_file = tmp_path / "empty.yaml"
    cfg_file.write_text("", encoding="utf-8")
    assert load_config(cfg_file) == {}
