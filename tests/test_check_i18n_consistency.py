import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_i18n_consistency


def test_discover_locales_deduplicates_zh_cn(tmp_path, monkeypatch):
    """Verify that discover_locales does not duplicate zh-CN if docs/zh-CN/README.md exists.

    Proves the contract that the discovered locales list remains deduplicated even when
    docs/ contains a zh-CN directory with a README.md file.
    """
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "zh-CN").mkdir()
    (docs / "zh-CN" / "README.md").touch()
    (docs / "en").mkdir()
    (docs / "en" / "README.md").touch()

    monkeypatch.setattr(check_i18n_consistency, "ROOT", tmp_path)

    locales = check_i18n_consistency.discover_locales()
    assert locales == ["zh-CN", "en"]

def test_main_readme_path_locale_validation():
    """Verify main_readme_path maps zh-CN to root README.md and other locales to docs/<locale>/README.md."""
    assert check_i18n_consistency.main_readme_path("zh-CN") == check_i18n_consistency.ROOT / "README.md"
    assert check_i18n_consistency.main_readme_path("en") == check_i18n_consistency.ROOT / "docs" / "en" / "README.md"


def test_project_count_in_table_nonexistent(tmp_path):
    """Verify project_count_in_table returns -1 for nonexistent files."""
    p = tmp_path / "nonexistent.md"
    assert check_i18n_consistency.project_count_in_table(p) == -1


def test_count_git_clones_nonexistent(tmp_path):
    """Verify count_git_clones returns -1 for nonexistent files."""
    p = tmp_path / "nonexistent.md"
    assert check_i18n_consistency.count_git_clones(p) == -1


def test_toc_table_columns_nonexistent(tmp_path):
    """Verify toc_table_columns returns -1 for nonexistent files."""
    p = tmp_path / "nonexistent.md"
    assert check_i18n_consistency.toc_table_columns(p) == -1
