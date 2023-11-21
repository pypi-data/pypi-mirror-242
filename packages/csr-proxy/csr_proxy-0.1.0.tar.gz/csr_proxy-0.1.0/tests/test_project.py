# ---------------------------------------------------------------------
# Gufo Labs: Project structure tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import inspect
import os
import sys
from typing import Tuple, Union

# Third-party modules
import pytest


def _get_root() -> str:
    mod_path = inspect.getfile(sys.modules[__name__])
    rel_root = os.path.dirname(mod_path)
    return os.path.abspath(os.path.join(rel_root, ".."))


def _get_project() -> str:
    d = [
        f
        for f in os.listdir(os.path.join(ROOT, "src"))
        if not f.startswith(".") and not f.startswith("_")
    ]
    # assert len(d) == 1
    return d[0]


ROOT = _get_root()
PROJECT = _get_project()

REQUIRED_FILES = [
    ".devcontainer/devcontainer.json",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug-report.yml",
    ".github/ISSUE_TEMPLATE/feature-request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".gitignore",
    ".requirements/docs.txt",
    ".requirements/lint.txt",
    ".requirements/test.txt",
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "Dockerfile",
    "LICENSE.md",
    "README.md",
    "SECURITY.md",
    "docs/assets/logo.png",
    "docs/codebase.md",
    "docs/codequality.md",
    "docs/devcommon.md",
    "docs/environment.md",
    "docs/faq.md",
    "docs/index.md",
    ("docs/installation.md", "docs/installation/index.md"),
    "docs/testing.md",
    "mkdocs.yml",
    "pyproject.toml",
    "src/csr_proxy/__init__.py",
    "src/csr_proxy/py.typed",
    "tests/test_docs.py",
    "tests/test_project.py",
]


def test_required_is_sorted() -> None:
    def q(name: Union[str, Tuple[str, ...]]) -> Tuple[str, ...]:
        if isinstance(name, str):
            return (name,)
        return name

    normalized = [q(x) for x in REQUIRED_FILES]
    assert sorted(normalized) == normalized, "REQUIRED_FILES must be sorted"


@pytest.mark.parametrize("name", REQUIRED_FILES)
def test_required_files(name: Union[str, Tuple[str, ...]]) -> None:
    if isinstance(name, str):
        full_path = os.path.join(ROOT, name)
        assert os.path.exists(full_path), f"File {name} is missed"
    else:
        full_paths = [os.path.join(ROOT, n) for n in name]
        present = any(os.path.exists(n) for n in full_paths)
        assert present, f"Any of files {', '.join(full_paths)} must be exist"


def test_version() -> None:
    m = __import__(PROJECT, {}, {}, "*")
    assert hasattr(m, "__version__"), "__init__.py must contain __version__"
