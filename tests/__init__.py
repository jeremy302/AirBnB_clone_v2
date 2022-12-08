#!/usr/bin/python3
''' airbnb v2 tests'''
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream):
    '''clears a stream'''
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def delete_file(path: str):
    ''' deletes a file '''
    if os.path.isfile(path):
        os.unlink(path)


def reset_store(storage, path='file.json'):
    ''' reset storage '''
    with open(path, 'w') as file:
        file.write('{}')
    if storage:
        storage.reload()


def read_text_file(path):
    ''' reads fine '''
    lines = []
    if os.path.isfile(path):
        with open(path, 'r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def write_text_file(path, v):
    """write to a file"""
    with open(path, 'w') as f:
        f.write(v)
