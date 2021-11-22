from tempfile import TemporaryDirectory
from pathlib import Path
import plain_sight.file_io as file_io
from json import dumps


def test_save_load_and_parse() -> None:
    _EXAMPLE_DATA = {
        'a': 123,
        'b': 456
    }
    _EXAMPLE_CONTENT = dumps(_EXAMPLE_DATA).encode()

    with TemporaryDirectory() as temp_dir:
        temp_filename = Path(temp_dir) / 'temporary_file.json'

        file_io.save_file(temp_filename, _EXAMPLE_CONTENT)
        recovered_content = file_io.load_file(temp_filename)

        assert _EXAMPLE_CONTENT == recovered_content

        recovered_data = file_io.load_config(temp_filename)

        assert len(_EXAMPLE_DATA) == len(recovered_data)
        for key in _EXAMPLE_DATA:
            assert key in recovered_data
            assert _EXAMPLE_DATA.get(key) == recovered_data.get(key)


class ExampleClass:
    @staticmethod
    def to_json():
        return True


def test_json_helper() -> None:
    example_object = ExampleClass()
    assert file_io.json_helper(example_object)
