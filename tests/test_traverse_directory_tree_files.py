from src.script import traverse_directory_tree
from tests.test_helpers import fake_stat


from pathlib import Path
import pytest
from unittest.mock import call

test_data_new_files = [
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir1', [], ['file2.txt']),
        ('E:/mocked_dir/subdir2', [], [])
    ], 
    [
        Path('R:/backup/mocked_dir/file1.txt'),
        Path('R:/backup/mocked_dir/subdir1/file2.txt')
    ]),
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir1', [], ['file2.txt']),
        ('E:/mocked_dir/subdir2', ['subsubdir1'], []),
        ('E:/mocked_dir/subdir2/subsubdir1/', [], ['file3.txt'])
    ], 
    [
        Path('R:/backup/mocked_dir/file1.txt'),
        Path('R:/backup/mocked_dir/subdir1/file2.txt'),
        Path('R:/backup/mocked_dir/subdir2/subsubdir1/file3.txt')
    ])
]

@pytest.mark.parametrize(
    "mock_walk_output,expected_dst_shutil_paths",
    test_data_new_files,
    ids=["simple_new_files", "new_files_deep_tree"]
)
def test_traverse_directory_tree_new_files_should_be_copied(mocker, mock_walk_output, expected_dst_shutil_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    os_stat_mock = mocker.patch('os.stat', return_value=fake_stat())
    os_remove_mock = mocker.patch('os.remove')
    shutil_copy2_mock = mocker.patch('shutil.copy2')

    # Ignore dir handling
    mocker.patch.object(Path, "mkdir", autospec=True)
    mocker.patch('shutil.rmtree')

    # Act
    traverse_directory_tree('E:/mocked_dir')

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))
    
    dst_called_paths = [call_args[0][1] for call_args in shutil_copy2_mock.call_args_list]
    assert sorted(dst_called_paths) == sorted(expected_dst_shutil_paths)

test_data_removed_files = [
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir1', [], ['file2.txt']),
        ('E:/mocked_dir/subdir2', [], [])
    ],
    {
        'mocked_dir/file1.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        },
        'mocked_dir/file3.txt': {
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
        Path('R:/backup/mocked_dir/file3.txt'),
    ]),
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], []),
        ('E:/mocked_dir/subdir1', [], []),
        ('E:/mocked_dir/subdir2', [], [])
    ],
    {
        'mocked_dir/file1.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        },
        'mocked_dir/file3.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        }, 
        'mocked_dir/subdir1/file2.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        },
    },
    [
        Path('R:/backup/mocked_dir/file3.txt'),
        Path('R:/backup/mocked_dir/file1.txt'),
        Path('R:/backup/mocked_dir/subdir1/file2.txt')
    ])
]

@pytest.mark.parametrize(
    "mock_walk_output,last_state_files,expected_os_rm_paths",
    test_data_removed_files,
    ids=["simple_delete_file", "delete_files_deeper"]
)
def test_traverse_directory_tree_removed_files_should_be_removed(mocker, mock_walk_output, last_state_files, expected_os_rm_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    os_stat_mock = mocker.patch('os.stat', return_value=fake_stat())
    os_remove_mock = mocker.patch('os.remove')
    shutil_copy2_mock = mocker.patch('shutil.copy2')

    # Ignore dir handling
    mocker.patch.object(Path, "mkdir", autospec=True)
    mocker.patch('shutil.rmtree')

    # Act
    traverse_directory_tree('E:/mocked_dir', last_state_files=last_state_files)

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))
    
    called_paths = [call_args[0][0] for call_args in os_remove_mock.call_args_list]
    assert sorted(called_paths) == sorted(expected_os_rm_paths)

test_data_renamed_files = [
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir1', [], ['file_renamed.txt']),
        ('E:/mocked_dir/subdir2', [], [])
    ],
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
        Path('R:/backup/mocked_dir/subdir1/file_renamed.txt'),
    ],
    [
        Path('R:/backup/mocked_dir/subdir1/file2.txt'),
    ]),
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], ['file1.txt']),
        ('E:/mocked_dir/subdir1', [], ['file2.txt']),
        ('E:/mocked_dir/subdir2', [], [])
    ],
    {
        'mocked_dir/file1.txt': {
            "mtime": 1,
            "size": 3730,
            "matched": False
        },
        'mocked_dir/subdir1/file2.txt': {
            "mtime": 10,
            "size": 3500,
            "matched": False
        } 
    },
    [
        Path('R:/backup/mocked_dir/subdir1/file2.txt')
    ],
    [])
]

@pytest.mark.parametrize(
    "mock_walk_output,last_state_files,expected_shutil_dst_paths,expected_os_rm_paths",
    test_data_renamed_files,
    ids=["simple_renamed_file", "modified_file"]
)
def test_traverse_directory_tree_modified_files_should_be_copied(mocker, mock_walk_output, last_state_files, expected_shutil_dst_paths, expected_os_rm_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    os_stat_mock = mocker.patch('os.stat', return_value=fake_stat())
    os_remove_mock = mocker.patch('os.remove')
    shutil_copy2_mock = mocker.patch('shutil.copy2')

    # Ignore dir handling
    mocker.patch.object(Path, "mkdir", autospec=True)
    mocker.patch('shutil.rmtree')

    # Act
    traverse_directory_tree('E:/mocked_dir', last_state_files=last_state_files)

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))

    called_paths_copy2 = [call_args[0][1] for call_args in shutil_copy2_mock.call_args_list]
    assert sorted(called_paths_copy2) == sorted(expected_shutil_dst_paths)
    
    called_paths_rm = [call_args[0][0] for call_args in os_remove_mock.call_args_list]
    assert sorted(called_paths_rm) == sorted(expected_os_rm_paths)