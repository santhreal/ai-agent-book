"""Regression: save_path under missing parents must create dirs before savefig."""
import matplotlib

matplotlib.use("Agg")
import numpy as np

from visualization import create_layer_attention_heatmap


def test_layer_heatmap_nested_save(tmp_path):
    out = tmp_path / "plots" / "layer.png"
    create_layer_attention_heatmap(np.eye(2), ["a", "b"], save_path=str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_layer_heatmap_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    create_layer_attention_heatmap(np.eye(2), ["a", "b"], save_path="layer.png")
    assert (tmp_path / "layer.png").exists()
