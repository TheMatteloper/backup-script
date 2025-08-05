from src.script import traverse_directory_tree
from tests.test_helpers import fake_stat


from pathlib import Path
import pytest
from unittest.mock import call

test_data_new_dirs = [
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], []),
        ('E:/mocked_dir/subdir1', [], []),
        ('E:/mocked_dir/subdir2', [], [])
    ], 
    [
        Path('R:/backup/mocked_dir/subdir1'),
        Path('R:/backup/mocked_dir/subdir2')
    ]),
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], []),
        ('E:/mocked_dir/subdir1', ['subsubdir1', 'subsubdir2'], []),
        ('E:/mocked_dir/subdir2', [], []),
        ('E:/mocked_dir/subdir1/subsubdir1', [], []),
        ('E:/mocked_dir/subdir1/subsubdir2', [], [])
    ], 
    [
        Path('R:/backup/mocked_dir/subdir1'),
        Path('R:/backup/mocked_dir/subdir2'),
        Path('R:/backup/mocked_dir/subdir1/subsubdir1'),
        Path('R:/backup/mocked_dir/subdir1/subsubdir2')
    ])
    ]

@pytest.mark.parametrize(
    "mock_walk_output,expected_mkdir_paths",
    test_data_new_dirs,
    ids=["simple_new_dirs", "nested_new_dirs"]
)
def test_traverse_directory_tree_new_dirs_should_be_copied(mocker, mock_walk_output, expected_mkdir_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    path_mkdir_mock = mocker.patch.object(Path, "mkdir", autospec=True)

    # Ignore file handling
    mocker.patch('os.stat', return_value=fake_stat())
    mocker.patch('os.remove')
    mocker.patch('shutil.copy2')
    
    # Act
    traverse_directory_tree('E:/mocked_dir')

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))
    
    called_paths = [call_args[0][0] for call_args in path_mkdir_mock.call_args_list]
    assert sorted(called_paths) == sorted(expected_mkdir_paths)

test_data_rm_dirs = [
    ([
        ('E:/mocked_dir', ['subdir1', 'subdir2'], []),
        ('E:/mocked_dir/subdir1', [], []),
        ('E:/mocked_dir/subdir2', [], []),
    ],
    {
        "mocked_dir/subdir3" : False,
        "mocked_dir/subdir1" : False,
        "mocked_dir/subdir2" : False,
        "mocked_dir/subdir1/subsubdir1" : False,

    },
    [
        call(Path('R:/backup/mocked_dir/subdir1/subsubdir1'), ignore_errors=True),
        call(Path('R:/backup/mocked_dir/subdir3'), ignore_errors=True),    
    ]),
    ([
        ('E:/mocked_dir', ['subdir2'], []),
        ('E:/mocked_dir/subdir2', [], []),
    ],
    {
        "mocked_dir/subdir3" : False,
        "mocked_dir/subdir1" : False,
        "mocked_dir/subdir2" : False,
        "mocked_dir/subdir1/subsubdir1" : False,

    },
    [
        call(Path('R:/backup/mocked_dir/subdir1/subsubdir1'), ignore_errors=True),
        call(Path('R:/backup/mocked_dir/subdir1'), ignore_errors=True),
        call(Path('R:/backup/mocked_dir/subdir3'), ignore_errors=True)
    ])
    ]

@pytest.mark.parametrize(
    "mock_walk_output,last_state_dirs,expected_rmtree_paths",
    test_data_rm_dirs,
    ids=["simple_delete_dirs", "delete_whole_subtree"]
)
def test_traverse_directory_tree_deleted_dirs_should_be_deleted(mocker, mock_walk_output, last_state_dirs, expected_rmtree_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    shutil_rmtree_mock = mocker.patch('shutil.rmtree')
    mocker.patch.object(Path, "mkdir", autospec=True)

    # Ignore file handling
    mocker.patch('os.stat', return_value=fake_stat())
    mocker.patch('os.remove')
    mocker.patch('shutil.copy2')

    # Act
    traverse_directory_tree('E:/mocked_dir', last_state_dirs)

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))

    shutil_rmtree_mock.assert_has_calls(expected_rmtree_paths, any_order = True)

test_data_renamed_dirs = [
    ([
        ('E:/mocked_dir', ['renamed_dir', 'subdir2'], []),
        ('E:/mocked_dir/renamed_dir', [], []),
        ('E:/mocked_dir/subdir2', [], []),
    ],
    {
        "mocked_dir/subdir1" : False,
        "mocked_dir/subdir2" : False,
    },
    [
        call(Path('R:/backup/mocked_dir/subdir1'), ignore_errors=True),    
    ],
    [
        Path('R:/backup/mocked_dir/renamed_dir'),    
    ]),
    ([
        ('E:/mocked_dir', ['renamed_dir', 'subdir2'], []),
        ('E:/mocked_dir/renamed_dir', ['subsubdir1'], []),
        ('E:/mocked_dir/subdir2', [], []),
        ('E:/mocked_dir/renamed_dir/subsubdir1', [], []),
    ],
    {
        "mocked_dir/subdir1" : False,
        "mocked_dir/subdir2" : False,
        "mocked_dir/subdir1/subsubdir1" : False,
    },
    [
        call(Path('R:/backup/mocked_dir/subdir1/subsubdir1'), ignore_errors=True),
        call(Path('R:/backup/mocked_dir/subdir1'), ignore_errors=True)   
    ],
    [
        Path('R:/backup/mocked_dir/renamed_dir/subsubdir1'),
        Path('R:/backup/mocked_dir/renamed_dir')    
    ])
]

@pytest.mark.parametrize(
    "mock_walk_output,last_state_dirs,expected_rmtree_paths,expected_mkdir_paths",
    test_data_renamed_dirs,
    ids=["simple_renamed_subdir","renamed_dir_with_subdir",]
)   
def test_traverse_directory_tree_deleted_renamed_dir_should_be_old_deleted_new_crated(mocker, mock_walk_output, last_state_dirs,
                                                                                       expected_rmtree_paths, expected_mkdir_paths):
    # Mocks
    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    path_mkdir_mock = mocker.patch.object(Path, "mkdir", autospec=True)
    shutil_rmtree_mock = mocker.patch('shutil.rmtree')

    # Ignore file handling
    mocker.patch('os.stat', return_value=fake_stat())
    mocker.patch('os.remove')
    mocker.patch('shutil.copy2')

    # Act
    traverse_directory_tree('E:/mocked_dir', last_state_dirs)

    # Assert
    os_walk_mock.assert_called_once_with(Path('E:/mocked_dir'))

    shutil_rmtree_mock.assert_has_calls(expected_rmtree_paths, any_order = True)
    
    called_mkdir_paths = [call_args[0][0] for call_args in path_mkdir_mock.call_args_list]
    assert sorted(called_mkdir_paths) == sorted(expected_mkdir_paths)