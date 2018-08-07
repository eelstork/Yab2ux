from unittest.mock import patch, MagicMock as mock
from yab2ux import *


def test_export_path(path, config, root):
    expected = '/project/Assets/models/turnip.fbx'
    assert (get_export_path(path, config, root) == expected)
    config = {"path": "Assets/"}
    assert (get_export_path(path, config, root) == expected)
    root = "/project/"
    assert (get_export_path(path, config, root) == expected)


def test_export_fbx(outpath, config, root):
    with patch("yab2ux.makedirs", mock()) as makedirs:
        with patch("yab2ux.bl_to_fbx", mock()) as bl_to_fbx:
            do_export_fbx(outpath, config, root)
    makedirs.assert_called_with('/project/models', exist_ok=True)
    bl_to_fbx.assert_called_with('/project/models/turnip.fbx')


def test_export_fbx(outpath, config_with_params, root):
    with patch("yab2ux.makedirs", mock()) as makedirs:
        with patch("yab2ux.bl_to_fbx", mock()) as bl_to_fbx:
            do_export_fbx(outpath, config_with_params, root)
    makedirs.assert_called_with('/project/models', exist_ok=True)
    bl_to_fbx.assert_called_with('/project/models/turnip.fbx', foo='bar')


def test_config_not_found(path):
    with patch('yab2ux.load_config_file', mock(return_value=None)):
        assert load_config(path) == (None, None)


def test_load_single_config(path):
    with patch('yab2ux.load_config_file', mock_load_config_file):
        assert load_config(path) == (CONFIG, '/project')


def test_load_multi_config(path):
    with patch('yab2ux.load_config_file', mock_load_config_file_multi):
        assert load_config(path) == (COMPOSITE_CONFIG, '/project')


def test_skip_assets_dir():
    path = '/project/Assets/Media/Models/Foo.blend'
    with patch('yab2ux.load_config_file', mock_load_config_file):
        assert load_config(path) == (None, None)
    path = '/project/Media/Models/Foo.blend'
    with patch('yab2ux.load_config_file', mock_load_config_file):
        assert load_config(path) == (CONFIG, '/project')

# -----------------------------------------------------------------------------

import pytest

CONFIG = {"path": "Assets"}
CONFIG_WITH_PARAM = {"path": "Assets", "foo": "bar"}
SUB_CONFIG = {"foo": "sharp"}
COMPOSITE_CONFIG = {"path": "Assets", "foo": "sharp"}

# Mocks -----------------------------------------------------------------------


def mock_load_config_file(path):
    return CONFIG if path == '/project' else None


def mock_load_config_file_multi(path):
    if path == '/project': return CONFIG_WITH_PARAM
    if path == '/project/models': return SUB_CONFIG
    return None


# Fixtures --------------------------------------------------------------------


@pytest.fixture
def config():
    return CONFIG


@pytest.fixture
def config_with_params():
    return CONFIG_WITH_PARAM


@pytest.fixture
def path():
    return '/project/models/turnip.blend'


@pytest.fixture
def outpath():
    return '/project/models/turnip.fbx'


@pytest.fixture
def root():
    return '/project'
