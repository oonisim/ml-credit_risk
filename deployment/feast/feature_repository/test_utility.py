# test_utils.py
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import logging
from io import StringIO

# Import your module (adjust import path as needed)
from utility import list_feature_views, get_yaml_value, read_yaml


@pytest.fixture
def sample_yaml_data():
    """Sample YAML data for testing"""
    return {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'testdb'
        },
        'app_name': 'test_app',
        'debug': True,
        'features': ['feature1', 'feature2']
    }


@pytest.fixture
def temp_yaml_file(sample_yaml_data):
    """Create temporary YAML file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_yaml_data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def empty_yaml_file():
    """Create empty YAML file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_path = f.name

    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def invalid_yaml_file():
    """Create invalid YAML file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: [unclosed")
        temp_path = f.name

    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


class TestGetYamlValue:

    def test_get_yaml_value_existing_key(self, temp_yaml_file):
        """Test getting existing key"""
        result = get_yaml_value(temp_yaml_file, 'app_name')
        assert result == 'test_app'

    def test_get_yaml_value_nested_key_not_supported(self, temp_yaml_file):
        """Test that nested keys are not directly supported"""
        # This function only supports top-level keys
        result = get_yaml_value(temp_yaml_file, 'database')
        assert result == {'host': 'localhost', 'port': 5432, 'name': 'testdb'}

    def test_get_yaml_value_nonexistent_key(self, temp_yaml_file):
        """Test getting non-existent key returns default"""
        result = get_yaml_value(temp_yaml_file, 'nonexistent')
        assert result == ""

        result = get_yaml_value(temp_yaml_file, 'nonexistent', 'custom_default')
        assert result == 'custom_default'

    def test_get_yaml_value_file_not_found(self):
        """Test file not found raises exception"""
        with pytest.raises(FileNotFoundError):
            get_yaml_value('nonexistent.yaml', 'key')

    def test_get_yaml_value_invalid_yaml(self, invalid_yaml_file):
        """Test invalid YAML raises exception"""
        with pytest.raises(yaml.YAMLError):
            get_yaml_value(invalid_yaml_file, 'key')

    def test_get_yaml_value_empty_file(self, empty_yaml_file):
        """Test empty file"""
        result = get_yaml_value(empty_yaml_file, 'key', 'default')
        assert result == 'default'

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_get_yaml_value_permission_error(self, mock_open):
        """Test permission error"""
        with pytest.raises(PermissionError):
            get_yaml_value('file.yaml', 'key')


class TestReadYaml:

    def test_read_yaml_success(self, temp_yaml_file, sample_yaml_data):
        """Test successful YAML reading"""
        result = read_yaml(temp_yaml_file)
        assert result == sample_yaml_data

    def test_read_yaml_file_not_exists(self, caplog):
        """Test non-existent file returns default"""
        with caplog.at_level(logging.ERROR):
            result = read_yaml('nonexistent.yaml')
            assert result == {}
            assert "YAML file does not exist" in caplog.text

    def test_read_yaml_custom_default(self):
        """Test custom default value"""
        default_val = {'custom': 'default'}
        result = read_yaml('nonexistent.yaml', default_val)
        assert result == default_val

    def test_read_yaml_empty_file(self, empty_yaml_file, caplog):
        """Test empty file"""
        with caplog.at_level(logging.ERROR):
            result = read_yaml(empty_yaml_file)
            assert result == {}
            assert "YAML file is empty" in caplog.text

    def test_read_yaml_invalid_yaml(self, invalid_yaml_file, caplog):
        """Test invalid YAML content"""
        with caplog.at_level(logging.ERROR):
            result = read_yaml(invalid_yaml_file)
            assert result == {}
            assert "YAML parsing error" in caplog.text

    def test_read_yaml_directory_path(self, tmp_path, caplog):
        """Test passing directory instead of file"""
        with caplog.at_level(logging.ERROR):
            result = read_yaml(str(tmp_path))
            assert result == {}
            assert "Path is not a file" in caplog.text

    def test_read_yaml_non_dict_content(self, caplog):
        """Test YAML with non-dict root"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("- item1\n- item2\n")
            temp_path = f.name

        try:
            with caplog.at_level(logging.ERROR):
                result = read_yaml(temp_path)
                assert result == {}
                assert "YAML root is not a dictionary" in caplog.text
        finally:
            Path(temp_path).unlink(missing_ok=True)

    @patch('builtins.open')
    def test_read_yaml_unicode_error(self, mock_open_func, caplog):
        """Test Unicode decode error"""
        mock_open_func.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')

        with caplog.at_level(logging.ERROR):
            result = read_yaml('test.yaml')
            assert result == {}
            assert "Encoding error" in caplog.text

    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    @patch('builtins.open')
    def test_read_yaml_unexpected_error(self, mock_open_func, mock_is_file, mock_exists, caplog):
        """Test unexpected error handling"""
        mock_open_func.side_effect = RuntimeError("Unexpected error")

        with caplog.at_level(logging.ERROR):
            result = read_yaml('test.yaml')
            assert result == {}
            assert "Unexpected error reading" in caplog.text

    def test_read_yaml_success_logging(self, temp_yaml_file, caplog):
        """Test success logging"""
        with caplog.at_level(logging.INFO):
            result = read_yaml(temp_yaml_file)
            assert result != {}
            assert "Successfully loaded YAML" in caplog.text


class TestParametrized:

    @pytest.mark.parametrize("key,expected", [
        ('app_name', 'test_app'),
        ('debug', True),
        ('features', ['feature1', 'feature2']),
        ('nonexistent', ''),
    ])
    def test_get_yaml_value_parametrized(self, temp_yaml_file, key, expected):
        """Parametrized test for get_yaml_value"""
        result = get_yaml_value(temp_yaml_file, key)
        assert result == expected

    @pytest.mark.parametrize("default_value", [
        {},
        {'default': 'value'},
        [],
        None,
        "string_default"
    ])
    def test_read_yaml_different_defaults(self, default_value):
        """Test read_yaml with different default values"""
        result = read_yaml('nonexistent.yaml', default_value)
        expected = {} if default_value is None else default_value
        assert result == expected
