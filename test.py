from script import traverse_directory_tree

from pathlib import Path
import time
import os
import shutil

# TODO only prototype
def test_traverse_directory_tree_new_dir_should_be_copied(mocker):
    mock_walk_output = [
        ('/mocked_dir', ['subdir'], ['file1.txt', 'file2.txt']),
        ('/mocked_dir/subdir', [], ['file3.txt'])
    ]

    os_walk_mock = mocker.patch('os.walk', return_value=mock_walk_output)
    os_stat_mock = mocker.patch('os.stat', return_value=fake_stat())
    os_remove_mock = mocker.patch('os.remove')
    shutil_copy2_mock = mocker.patch('shutil.copy2')

    path_mkdir_os = mocker.patch.object(Path, 'mkdir')


    traverse_directory_tree('/mocked_dir')

    os_walk_mock.assert_called_once_with(Path('/mocked_dir').resolve())

def fake_stat():
    # Values are usually ints/floats; example values below
    stat_tuple = (
        33206,      # st_mode (e.g. regular file with permissions)
        123456,     # st_ino (inode number)
        2050,       # st_dev (device)
        1,          # st_nlink (number of hard links)
        1000,       # st_uid (user id)
        1000,       # st_gid (group id)
        4096,       # st_size (file size in bytes)
        time.time(),# st_atime (last access time)
        time.time(),# st_mtime (last modification time)
        time.time(),# st_ctime (creation/change time)
    )
    return os.stat_result(stat_tuple)