import sys
from pathlib import Path
import json
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import site_i18n


def test_build_catalog_validates_extra_nav_keys(monkeypatch, tmp_path):
    """Verify build_catalog raises CatalogError when site-nav-i18n.json contains extra nav keys.

    Proves the contract that extra nav labels not present in mkdocs.yml are detected and rejected.
    """
    monkeypatch.setattr(site_i18n, "material_languages_dir", lambda: tmp_path)
    monkeypatch.setattr(
        site_i18n,
        "load_material_locale",
        lambda locale, dir: {
            "language": locale,
            "direction": "ltr",
            **{k: "v" for k in site_i18n.REQUIRED_UI_KEYS},
        },
    )

    custom_catalog_data = {
        "zh": {
            "material_locale": "zh",
            "ui_overrides": {},
            "nav": {
                "首页": "首页",
                "引言": "引言",
                "第1章 Agent基础知识": "第1章 Agent基础知识",
                "第2章 上下文工程": "第2章 上下文工程",
                "第3章 用户记忆和知识库": "第3章 用户记忆和知识库",
                "第4章 工具": "第4章 工具",
                "第5章 CodingAgent与代码生成": "第5章 CodingAgent与代码生成",
                "第6章 Agent的评估": "第6章 Agent的评估",
                "第7章 模型后训练": "第7章 模型后训练",
                "第8章 Agent的持续进化": "第8章 Agent的持续进化",
                "第9章 多模态与实时交互": "第9章 多模态与实时交互",
                "第10章 多Agent协作": "第10章 多Agent协作",
                "后记": "后记",
                "思考题参考答案": "思考题参考答案",
            },
            "sidebar": {"show": "显示侧边栏", "hide": "隐藏侧边栏"},
            "palette": {"light": "浅色模式", "dark": "深色模式"},
        },
        "en": {
            "material_locale": "en",
            "ui_overrides": {},
            "nav": {
                "首页": "Home",
                "引言": "Introduction",
                "第1章 Agent基础知识": "Chapter 1 Agent Fundamentals",
                "第2章 上下文工程": "Chapter 2 Context Engineering",
                "第3章 用户记忆和知识库": "Chapter 3 User Memory & KB",
                "第4章 工具": "Chapter 4 Tools",
                "第5章 CodingAgent与代码生成": "Chapter 5 Coding Agent & Code Gen",
                "第6章 Agent的评估": "Chapter 6 Agent Evaluation",
                "第7章 模型后训练": "Chapter 7 Model Post-Training",
                "第8章 Agent的持续进化": "Chapter 8 Agent Continuous Evolution",
                "第9章 多模态与实时交互": "Chapter 9 Multimodal & Real-time",
                "第10章 多Agent协作": "Chapter 10 Multi-Agent Collaboration",
                "后记": "Afterword",
                "思考题参考答案": "Exercise Reference Answers",
                "Unknown Section": "Unknown Section Translation",
            },
            "sidebar": {"show": "Show sidebar", "hide": "Hide sidebar"},
            "palette": {"light": "Light mode", "dark": "Dark mode"},
        },
    }

    monkeypatch.setattr(
        site_i18n,
        "configured_languages",
        lambda text: {
            "zh": {"prefix": "book/"},
            "en": {"prefix": "book-en/"},
        },
    )

    catalog_path = tmp_path / "site-nav-i18n.json"
    catalog_path.write_text(json.dumps(custom_catalog_data), encoding="utf-8")
    monkeypatch.setattr(site_i18n, "CUSTOM_CATALOG", catalog_path)

    monkeypatch.setattr(Path, "is_file", lambda self: True)

    with pytest.raises(site_i18n.CatalogError) as excinfo:
        site_i18n.build_catalog()

    assert "unknown nav labels: Unknown Section" in str(excinfo.value)


def test_build_catalog_extra_nav_keys_validated_for_non_string_values(monkeypatch, tmp_path):
    """Verify extra nav keys with non-string values are detected as unknown nav labels.

    Proves the contract that non-string values on extra nav keys do not bypass unknown label validation.
    """
    monkeypatch.setattr(site_i18n, "material_languages_dir", lambda: tmp_path)
    monkeypatch.setattr(
        site_i18n,
        "load_material_locale",
        lambda locale, dir: {
            "language": locale,
            "direction": "ltr",
            **{k: "v" for k in site_i18n.REQUIRED_UI_KEYS},
        },
    )

    custom_catalog_data = {
        "zh": {
            "material_locale": "zh",
            "ui_overrides": {},
            "nav": {
                "首页": "首页",
                "引言": "引言",
                "第1章 Agent基础知识": "第1章 Agent基础知识",
                "第2章 上下文工程": "第2章 上下文工程",
                "第3章 用户记忆和知识库": "第3章 用户记忆和知识库",
                "第4章 工具": "第4章 工具",
                "第5章 CodingAgent与代码生成": "第5章 CodingAgent与代码生成",
                "第6章 Agent的评估": "第6章 Agent的评估",
                "第7章 模型后训练": "第7章 模型后训练",
                "第8章 Agent的持续进化": "第8章 Agent的持续进化",
                "第9章 多模态与实时交互": "第9章 多模态与实时交互",
                "第10章 多Agent协作": "第10章 多Agent协作",
                "后记": "后记",
                "思考题参考答案": "思考题参考答案",
            },
            "sidebar": {"show": "显示侧边栏", "hide": "隐藏侧边栏"},
            "palette": {"light": "浅色模式", "dark": "深色模式"},
        },
        "en": {
            "material_locale": "en",
            "ui_overrides": {},
            "nav": {
                "首页": "Home",
                "引言": "Introduction",
                "第1章 Agent基础知识": "Chapter 1 Agent Fundamentals",
                "第2章 上下文工程": "Chapter 2 Context Engineering",
                "第3章 用户记忆和知识库": "Chapter 3 User Memory & KB",
                "第4章 工具": "Chapter 4 Tools",
                "第5章 CodingAgent与代码生成": "Chapter 5 Coding Agent & Code Gen",
                "第6章 Agent的评估": "Chapter 6 Agent Evaluation",
                "第7章 模型后训练": "Chapter 7 Model Post-Training",
                "第8章 Agent的持续进化": "Chapter 8 Agent Continuous Evolution",
                "第9章 多模态与实时交互": "Chapter 9 Multimodal & Real-time",
                "第10章 多Agent协作": "Chapter 10 Multi-Agent Collaboration",
                "后记": "Afterword",
                "思考题参考答案": "Exercise Reference Answers",
                "Invalid Extra Key": 12345,
            },
            "sidebar": {"show": "Show sidebar", "hide": "Hide sidebar"},
            "palette": {"light": "Light mode", "dark": "Dark mode"},
        },
    }

    monkeypatch.setattr(
        site_i18n,
        "configured_languages",
        lambda text: {
            "zh": {"prefix": "book/"},
            "en": {"prefix": "book-en/"},
        },
    )

    catalog_path = tmp_path / "site-nav-i18n.json"
    catalog_path.write_text(json.dumps(custom_catalog_data), encoding="utf-8")
    monkeypatch.setattr(site_i18n, "CUSTOM_CATALOG", catalog_path)

    monkeypatch.setattr(Path, "is_file", lambda self: True)

    with pytest.raises(site_i18n.CatalogError) as excinfo:
        site_i18n.build_catalog()

    assert "unknown nav labels: Invalid Extra Key" in str(excinfo.value)
