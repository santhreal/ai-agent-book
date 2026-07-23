"""fit() on an empty extract list must return an empty model, not ValueError."""
from archetypes import fit


def test_fit_empty_results_returns_empty_model():
    schema = {"core_factors": [], "extensions": {"盗窃罪": []}}
    model = fit(schema, [], save=False, verbose=False)
    assert model["n_samples"] == 0
    assert model["n_archetypes"] == 0
    assert model["archetypes"] == []
    assert model["columns"] == []
    assert model["global_importance"] == []


def test_fit_single_sample_still_returns_model():
    """One sample cannot cluster but must not crash (sibling of empty-list guard)."""
    schema = {"core_factors": [], "extensions": {"盗窃罪": []}}
    results = [{"extracted": {"charge": "盗窃罪"}, "label_months": 12}]
    model = fit(schema, results, save=False, verbose=False)
    assert model["n_samples"] == 1
    assert model["n_archetypes"] == 0
    assert isinstance(model["columns"], list)
