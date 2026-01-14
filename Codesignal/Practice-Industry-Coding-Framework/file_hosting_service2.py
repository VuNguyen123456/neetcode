import json
import math
import string
import re
import random
import sys
import traceback
import functools
import copy
from collections import OrderedDict

import numpy
import sortedcontainers
from datetime import datetime

dic = {}
results = []
ts = {}

def FILE_UPLOAD(file_name, size):
    if file_name in dic:
        raise RuntimeError('File already exist')
    dic[file_name] = {'size': int(re.findall(r'-?\d*\.?\d+', size)[0])} # String as size
    results.append(f'uploaded {file_name}')

def FILE_GET(file_name):
    if file_name not in dic:
        return None
    results.append(f'got {file_name}')
    return dic[file_name]['size']

def FILE_COPY(source, dest):
    if source not in dic:
        raise RuntimeError('Source file doesn\'t exist')
    dic[dest] = {'size': dic[source]['size']}
    results.append(f"copied {source} to {dest}")

def FILE_SEARCH(prefix):
    top10 = []
    for file in dic:
        if file.startswith(prefix):
            top10.append((file, dic[file]['size']))
    sortedTop10 = sorted(top10, key=lambda x: (-x[1], x[0]))
    sortedTop10 = sortedTop10[:10]
    res = [ i[0] for i in sortedTop10 ]
    results.append(f"found [{', '.join(res)}]")
    return res

# def FILE_UPLOAD_AT(timestamp, file_name, file_size):
#     if file_name in dic:
#         raise RuntimeError('File already exist')
#     dic[file_name] = {
#                     'size': int(re.findall(r'-?\d*\.?\d+', file_size)[0]),
#                     'timestamp': timestamp
#                       } # String as size
#     results.append(f'uploaded {file_name}')

def FILE_UPLOAD_AT(timestamp, file_name, file_size, ttl = None):
    if file_name in dic:
        raise RuntimeError('File already exist')
    dic[file_name] = {
                    'size': int(re.findall(r'-?\d*\.?\d+', file_size)[0]),
                    'timestamp': timestamp,
                    'ttl': ttl
                      } # String as size
    results.append(f'uploaded at {file_name}')
    ts[timestamp] = copy.deepcopy(dic)

def FILE_GET_AT(timestamp, file_name):
    if file_name not in dic:
        results.append('file not found')
        return None
    if dic[file_name]['ttl'] == None:
        results.append(f'got at {file_name}')
        ts[timestamp] = copy.deepcopy(dic)
        return dic[file_name]['size']

    createdTime = datetime.fromisoformat(dic[file_name]['timestamp'])
    currentTime = datetime.fromisoformat(timestamp)

    if (currentTime - createdTime).total_seconds() > dic[file_name]['ttl']: #Still valid
        results.append('file not found')
        return None
    results.append(f'got at {file_name}')
    ts[timestamp] = copy.deepcopy(dic)
    return dic[file_name]['size']

def FILE_COPY_AT(timestamp, file_from, file_to):
    if file_from not in dic:
        raise RuntimeError('Source file doesn\'t exist')
    if dic[file_from]['ttl'] == None:
        results.append(f"copied at {file_from} to {file_to}")
        dic[file_to] = {
                    'size': dic[file_from]['size'],
                    'timestamp': dic[file_from]['timestamp'],
                    'ttl': dic[file_from]['ttl']
                    }
        ts[timestamp] = copy.deepcopy(dic)
        return
    
    createdTime = datetime.fromisoformat(dic[file_from]['timestamp'])
    currentTime = datetime.fromisoformat(timestamp)

    if (currentTime - createdTime).total_seconds() > dic[file_from]['ttl']:
        return None

    dic[file_to] = {
                    'size': dic[file_from]['size'],
                    'timestamp': dic[file_from]['timestamp'],
                    'ttl': dic[file_from]['ttl']
                    }
    results.append(f"copied at {file_from} to {file_to}")
    ts[timestamp] = copy.deepcopy(dic)

def FILE_SEARCH_AT(timestamp, prefix):
    top10 = []
    for file in dic:
        if file.startswith(prefix):
            if dic[file]['ttl'] == None:
                top10.append((file, dic[file]['size']))
                continue
            createdTime = datetime.fromisoformat(dic[file]['timestamp'])
            currentTime = datetime.fromisoformat(timestamp)
            if (currentTime - createdTime).total_seconds() < dic[file]['ttl']:
                top10.append((file, dic[file]['size']))
    sortedTop10 = sorted(top10, key=lambda x: (-x[1], x[0]))
    sortedTop10 = sortedTop10[:10]
    res = [ i[0] for i in sortedTop10 ]
    results.append(f"found at [{', '.join(res)}]")
    ts[timestamp] = copy.deepcopy(dic)
    return res

def ROLLBACK(timestamp):
    global dic
    dic = copy.deepcopy(ts[timestamp])
    results.append(f"rollback to {timestamp}")
    ts[timestamp] = copy.deepcopy(dic)
    


def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    for command in list_of_lists:
        op = command[0]
        if op == "FILE_UPLOAD":
            FILE_UPLOAD(command[1], command[2])
        elif op == "FILE_GET":
            FILE_GET(command[1])
        elif op == "FILE_COPY":
            FILE_COPY(command[1], command[2])
        elif op == "FILE_SEARCH":
            FILE_SEARCH(command[1])
        elif op == "FILE_UPLOAD_AT":
            if len(command) == 4:
                FILE_UPLOAD_AT(command[1], command[2], command[3])
            else:
                FILE_UPLOAD_AT(command[1], command[2], command[3], int(command[4]))
        elif op == "FILE_GET_AT":
            FILE_GET_AT(command[1], command[2])
        elif op == "FILE_COPY_AT":
            FILE_COPY_AT(command[1], command[2], command[3])
        elif op == "FILE_SEARCH_AT":
            FILE_SEARCH_AT(command[1], command[2])
        elif op == "ROLLBACK":
            ROLLBACK(command[1])
    return results
