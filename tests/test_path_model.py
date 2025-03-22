import pytest
from pathlib import Path
from ..models.path_model import PathModel


def test_create_path(tmp_path):
    test_path = tmp_path / "new_dir"
    assert not test_path.exists()
    created_path = PathModel._PathModel__create_path(test_path)
    assert created_path.exists()
    assert created_path.is_dir()

def test_add_json_suffix():
    path_without_suffix = "testfile"
    path_with_suffix = "testfile.json"
    result_path = PathModel._PathModel__add_json_suffix(path_without_suffix)
    assert result_path == Path(path_with_suffix)

    result_path = PathModel._PathModel__add_json_suffix(path_with_suffix)
    assert result_path == Path(path_with_suffix)

def test_verify_path_autocreate(tmp_path):
    test_file = tmp_path / "new_dir" / "testfile"
    assert not test_file.parent.exists()
    verified_path = PathModel.verify_path(test_file, autocreate_path=True)
    assert verified_path == Path(f"{test_file}.json")
    assert verified_path.parent.exists()

def test_verify_path_no_autocreate(tmp_path):
    test_file = tmp_path / "new_dir" / "testfile"
    assert not test_file.parent.exists()
    with pytest.raises(FileNotFoundError):
        PathModel.verify_path(test_file, autocreate_path=False)

def test_verify_path_existing(tmp_path):
    test_file = tmp_path / "existing_dir" / "testfile"
    test_file.parent.mkdir()
    verified_path = PathModel.verify_path(test_file, autocreate_path=False)
    assert verified_path == Path(f"{test_file}.json")
    assert verified_path.parent.exists()
