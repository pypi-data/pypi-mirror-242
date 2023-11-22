"""conda_join tests."""
from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import pytest
import yaml

from conda_join import (
    Requirements,
    RequirementsWithComments,
    _filter_pip_and_conda,
    _filter_unsupported_platforms,
    _parse_requirements,
    _to_requirements,
    extract_python_requires,
    filter_platform_selectors,
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
    assert "numpy" in combined_deps.conda
    assert "mumps" in combined_deps.conda
    assert len(combined_deps.conda) == 2  # noqa: PLR2004
    assert len(combined_deps.pip) == 1
    assert "pandas" in combined_deps.pip


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
        Requirements(channels=[], conda=[], pip=[]),
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
    commented_map = _to_requirements(reqs)
    assert commented_map.conda == ["numpy", "mumps"]


def test_channels(tmp_path: Path) -> None:
    p = tmp_path / "requirements.yaml"
    p.write_text("channels:\n  - conda-forge\n  - defaults")
    reqs = _parse_requirements([p], verbose=False)
    assert reqs.conda == {}
    assert reqs.pip == {}
    assert reqs.channels == {"conda-forge", "defaults"}


def test_surrounding_comments(tmp_path: Path) -> None:
    p = tmp_path / "requirements.yaml"
    p.write_text(
        textwrap.dedent(
            """\
            dependencies:
            # This is a comment before
                - yolo  # [osx]
            # This is a comment after
                # This is another comment
                - foo  # [linux]
                # And this is a comment after
                - bar  # [win]
            """,
        ),
    )
    reqs = _parse_requirements([p], verbose=False)
    assert reqs.conda == {"yolo": "# [osx]", "foo": "# [linux]", "bar": "# [win]"}


def test_filter_platform_selectors() -> None:
    # Test with a line having a linux selector
    content_linux = "dependency1  # [linux]"
    assert set(filter_platform_selectors(content_linux)) == {
        "linux-64",
        "linux-aarch64",
        "linux-ppc64le",
    }

    # Test with a line having a win selector
    content_win = "dependency2  # [win]"
    assert set(filter_platform_selectors(content_win)) == {"win-64"}

    # Test with a line having an osx64 selector
    content_osx64 = "dependency3  # [osx64]"
    assert set(filter_platform_selectors(content_osx64)) == {"osx-64"}

    # Test with a line having no selector
    content_none = "dependency4"
    assert filter_platform_selectors(content_none) == []

    # Test with a comment line
    content_comment = "# This is a comment"
    assert filter_platform_selectors(content_comment) == []

    # Test with a line having a unix selector
    content_unix = "dependency5  # [unix]"
    expected_unix = {
        "linux-64",
        "linux-aarch64",
        "linux-ppc64le",
        "osx-64",
        "osx-arm64",
    }
    assert set(filter_platform_selectors(content_unix)) == expected_unix

    # Test with a line having multiple selectors
    content_multi = "dependency7  # [linux64 unix]"
    expected_multi = {
        "linux-64",
        "linux-aarch64",
        "linux-ppc64le",
        "osx-64",
        "osx-arm64",
    }
    assert set(filter_platform_selectors(content_multi)) == expected_multi

    # Test with a line having multiple []
    content_multi = "dependency7  # [linux64] [win]"
    with pytest.raises(ValueError, match="Multiple bracketed selectors"):
        filter_platform_selectors(content_multi)


def test_filter_pip_and_conda() -> None:
    # Setup a sample RequirementsWithComments instance with platform selectors
    sample_requirements = RequirementsWithComments(
        channels={"some-channel"},
        conda={
            "package1": "# [linux]",
            "package2": "# [osx]",
            "common_package": "# [unix]",
            "shared_package": "# [linux]",  # Appears in both conda and pip with different selectors
        },
        pip={
            "package3": "# [win]",
            "package4": None,
            "common_package": "# [unix]",
            "shared_package": "# [win]",  # Appears in both conda and pip with different selectors
        },
    )

    assert _filter_unsupported_platforms(sample_requirements.conda, "linux-64") == {
        "package1": "# [linux]",
        "common_package": "# [unix]",
        "shared_package": "# [linux]",
    }
    assert _filter_unsupported_platforms(sample_requirements.pip, "linux-64") == {
        "common_package": "# [unix]",
        "package4": None,
    }

    # Test filtering for pip on linux-64 platform
    expected_pip_linux = RequirementsWithComments(
        channels={"some-channel"},
        conda={"package1": "# [linux]", "shared_package": "# [linux]"},
        pip={"common_package": "# [unix]", "package4": None},
    )

    assert (
        _filter_pip_and_conda(sample_requirements, "pip", "linux-64")
        == expected_pip_linux
    )

    # Test filtering for conda on linux-64 platform
    expected_conda_linux = RequirementsWithComments(
        channels={"some-channel"},
        conda={
            "package1": "# [linux]",
            "common_package": "# [unix]",
            "shared_package": "# [linux]",
        },
        pip={"package4": None},
    )
    assert (
        _filter_pip_and_conda(sample_requirements, "conda", "linux-64")
        == expected_conda_linux
    )

    # Test with invalid pip_or_conda value
    with pytest.raises(ValueError, match="Invalid value for `pip_or_conda`"):
        _filter_pip_and_conda(sample_requirements, "invalid_value", "linux-64")  # type: ignore[arg-type]
