"""conda_join tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import yaml
from ruamel.yaml.comments import CommentedMap

from conda_join import (
    _parse_requirements,
    _to_commented_map,
    extract_python_requires,
    generate_conda_env_file,
    parse_requirements,
    scan_requirements,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture()
def setup_test_files(tmp_path: Path) -> tuple[Path, Path]:
    d1 = tmp_path / "dir1"
    d1.mkdir()
    f1 = d1 / "requirements.yaml"
    f1.write_text("dependencies:\n  - numpy\n  - conda: mumps")

    d2 = tmp_path / "dir2"
    d2.mkdir()
    f2 = d2 / "requirements.yaml"
    f2.write_text("dependencies:\n  - pip: pandas")

    return (f1, f2)


def test_scan_requirements(tmp_path: Path, setup_test_files: tuple[Path, Path]) -> None:
    # Make sure to pass the depth argument correctly if your function expects it.
    results = scan_requirements(tmp_path, depth=1, verbose=True)

    # Convert results to absolute paths for comparison
    absolute_results = sorted(str(p.resolve()) for p in results)
    absolute_test_files = sorted(str(p.resolve()) for p in setup_test_files)

    assert absolute_results == absolute_test_files


@pytest.mark.parametrize("verbose", [True, False])
def test_parse_requirements(
    verbose: bool,  # noqa: FBT001
    setup_test_files: tuple[Path, Path],
) -> None:
    combined_deps = parse_requirements(setup_test_files, verbose=verbose)
    assert "numpy" in combined_deps["conda"]
    assert "mumps" in combined_deps["conda"]
    assert len(combined_deps["conda"]) == 2  # noqa: PLR2004
    assert len(combined_deps["pip"]) == 1
    assert "pandas" in combined_deps["pip"]


@pytest.mark.parametrize("verbose", [True, False])
def test_generate_conda_env_file(
    tmp_path: Path,
    verbose: bool,  # noqa: FBT001
    setup_test_files: tuple[Path, Path],
) -> None:
    output_file = tmp_path / "environment.yaml"
    combined_deps = parse_requirements(setup_test_files, verbose=verbose)
    generate_conda_env_file(combined_deps, str(output_file), verbose=verbose)

    with output_file.open() as f:
        env_data = yaml.safe_load(f)
        assert "dependencies" in env_data
        assert "numpy" in env_data["dependencies"]
        assert {"pip": ["pandas"]} in env_data["dependencies"]


def test_generate_conda_env_stdout(
    setup_test_files: tuple[Path, Path],
    capsys: pytest.CaptureFixture,
) -> None:
    combined_deps = parse_requirements(setup_test_files, verbose=False)
    generate_conda_env_file(combined_deps, None)

    captured = capsys.readouterr()
    assert "dependencies" in captured.out
    assert "numpy" in captured.out
    assert "- pandas" in captured.out


def test_verbose_output(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    f = tmp_path / "dir3" / "requirements.yaml"
    f.parent.mkdir()
    f.write_text("dependencies:\n  - scipy")

    scan_requirements(tmp_path, verbose=True)
    captured = capsys.readouterr()
    assert "Scanning in" in captured.out
    assert str(tmp_path / "dir3") in captured.out

    parse_requirements([f], verbose=True)
    captured = capsys.readouterr()
    assert "Parsing" in captured.out
    assert str(f) in captured.out

    generate_conda_env_file(
        {"conda": [], "pip": [], "channels": []},
        verbose=True,
    )
    captured = capsys.readouterr()
    assert "Generating environment file at" in captured.out
    assert "Environment file generated successfully." in captured.out


def test_extract_python_requires(setup_test_files: tuple[Path, Path]) -> None:
    f1, f2 = setup_test_files
    requires1 = extract_python_requires(str(f1))
    assert requires1 == ["numpy"]
    requires2 = extract_python_requires(str(f2))
    assert requires2 == ["pandas"]


def test_extract_comment(tmp_path: Path) -> None:
    p = tmp_path / "requirements.yaml"
    p.write_text("dependencies:\n  - numpy # [osx]\n  - conda: mumps  # [linux]")
    reqs = _parse_requirements([p], verbose=False)
    assert reqs.conda == {"numpy": "# [osx]", "mumps": "# [linux]"}
    commented_map = _to_commented_map(reqs)
    assert commented_map["conda"] == ["numpy", "mumps"]
    assert isinstance(commented_map, CommentedMap)


def test_channels(tmp_path: Path) -> None:
    p = tmp_path / "requirements.yaml"
    p.write_text("channels:\n  - conda-forge\n  - defaults")
    reqs = _parse_requirements([p], verbose=False)
    assert reqs.conda == {}
    assert reqs.pip == {}
    assert reqs.channels == {"conda-forge", "defaults"}
