import time
import os

def fake_stat():
    # Values are usually ints/floats; example values below
    stat_tuple = (
        33206,      # st_mode (e.g. regular file with permissions)
        123456,     # st_ino (inode number)
        2050,       # st_dev (device)
        1,          # st_nlink (number of hard links)
        1000,       # st_uid (user id)
        1000,       # st_gid (group id)
        3730,       # st_size (file size in bytes)
        time.time(),# st_atime (last access time)
        1,# st_mtime (last modification time)
        time.time(),# st_ctime (creation/change time)
    )
    return os.stat_result(stat_tuple)