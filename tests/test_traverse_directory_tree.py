from src.script import traverse_directory_tree
from tests.test_helpers import fake_stat


from pathlib import Path
import pytest
from unittest.mock import call

test_data_complete_run = [
    ([
        ('E:/mocked_dir', ['subdir_renamed', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir_renamed', [], ['file_renamed.txt']),
        ('E:/mocked_dir/subdir2', [], ['file3.txt'])
    ],
    {
        "mocked_dir/subdir1" : False,
        "mocked_dir/subdir2" : False
    },
    {
        'mocked_dir/file1.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        },
        'mocked_dir/subdir1/file2.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        } 
    },
    [
        call(Path('R:/backup/mocked_dir/subdir1'), ignore_errors=True)   
    ],
    [
        Path('R:/backup/mocked_dir/subdir_renamed')    
    ],
    [
        Path('R:/backup/mocked_dir/subdir_renamed/file_renamed.txt'),
        Path('R:/backup/mocked_dir/subdir2/file3.txt')
    ],
    [
        Path('R:/backup/mocked_dir/subdir1/file2.txt'),
    ])
]

@pytest.mark.parametrize(
    "mock_walk_output,last_state_dirs,last_state_files,expected_rmtree_paths,expected_mkdir_paths,expected_shutil_dst_paths,expected_os_rm_paths",
    test_data_complete_run,
    ids=["renamed_dir_and_renamed_file"]
)
def test_traverse_directory_tree_complete_run(mocker, mock_walk_output, last_state_dirs, last_state_files,
                                                                  expected_rmtree_paths, expected_mkdir_paths,
                                                                  expected_shutil_dst_paths, expected_os_rm_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    os_stat_mock = mocker.patch('os.stat', return_value=fake_stat())
    os_remove_mock = mocker.patch('os.remove')
    shutil_copy2_mock = mocker.patch('shutil.copy2')
    path_mkdir_mock = mocker.patch.object(Path, "mkdir", autospec=True)
    shutil_rmtree_mock = mocker.patch('shutil.rmtree')

    # Act
    traverse_directory_tree('E:/mocked_dir', last_state_dirs, last_state_files)

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))

    shutil_rmtree_mock.assert_has_calls(expected_rmtree_paths, any_order = True)
    
    called_mkdir_paths = [call_args[0][0] for call_args in path_mkdir_mock.call_args_list]
    assert sorted(called_mkdir_paths) == sorted(expected_mkdir_paths)

    called_paths_copy2 = [call_args[0][1] for call_args in shutil_copy2_mock.call_args_list]
    assert sorted(called_paths_copy2) == sorted(expected_shutil_dst_paths)
    
    called_paths_rm = [call_args[0][0] for call_args in os_remove_mock.call_args_list]
    assert sorted(called_paths_rm) == sorted(expected_os_rm_paths)