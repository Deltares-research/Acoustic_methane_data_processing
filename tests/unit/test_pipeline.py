from acoustic_methane.pipeline import run_pipeline


def test_run_pipeline_returns_status():
    result = run_pipeline({"a": 1})
    assert result["status"] == "ok"
