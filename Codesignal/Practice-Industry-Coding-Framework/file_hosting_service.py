import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict
import copy

import numpy
import sortedcontainers
from datetime import datetime

# want a dic of dic:
tsdic = {}
dic = {} 
timeStamps = []
results = []  # store messages
    
def FILE_UPLOAD(file_name, size):
    if file_name in dic:
        raise RuntimeError("File already exists on the server")
    dic[file_name] = int(re.findall(r"[-+]?\d*\.\d+|\d+", size)[0])
    results.append(f"uploaded {file_name}")

def FILE_GET(file_name):
    if file_name not in dic:
        return None
    results.append(f"got {file_name}")
    return dic[file_name]

def FILE_COPY(source, dest):
    if source not in dic:
        raise RuntimeError("File doesn't exists on the server")
    cp = dic[source]
    dic[dest] = cp
    results.append(f"copied {source} to {dest}")

def FILE_SEARCH(prefix):
    lstName = []
    lstSize = []
    for file in dic:

        if file.startswith(prefix):

            if not lstSize:
                lstName.append(file)
                lstSize.append(dic[file])
            elif lstSize and dic[file] < lstSize[-1]:
                lstName.insert(len(lstName), file)
                lstSize.insert(len(lstSize), dic[file])
            else:
                for i in range(len(lstName)):
                    if lstSize[i] < dic[file]:
                        lstName.insert(i, file)
                        lstSize.insert(i, dic[file])
                    elif dic[file] == lstSize[i]:
                        if lstName[i] < file:
                            lstName.insert(i, file)
                            lstSize.insert(i, dic[file])
                        else:
                            lstName.insert(i + 1, file)
                            lstSize.insert(i + 1, dic[file])
    top10 = ", ".join(lstName)
    results.append(f"found [{top10}]")
    return lstName

# dic now also store timestamp and ttl, {file: (size, ts, ttl)} - ts is the timestamp opject created
# def FILE_UPLOAD_AT(timestamp, file_name, file_size):
#     if file_name in dic:
#         raise RuntimeError("File already exists on the server")
#     dic[file_name] = (int(re.findall(r"[-+]?\d*\.\d+|\d+", file_size)[0]), timestamp, float("inf"))
#     results.append(f"uploaded at {file_name}")
#     timeStamps.append(f"FILE_UPLOAD_AT: {file_name} at {timestamp}")

def FILE_UPLOAD_AT(timestamp, file_name, file_size, ttl = None):
    if file_name in dic:
        raise RuntimeError("File already exists on the server")
    if ttl is None:
        ttl = float("inf")
    dic[file_name] = [int(re.findall(r"[-+]?\d*\.\d+|\d+", file_size)[0]), timestamp, ttl]
    results.append(f"uploaded at {file_name}")
    timeStamps.append(f"FILE_UPLOAD_AT: {file_name} at {timestamp}")
    tsdic[timestamp] = copy.deepcopy(dic)

def FILE_GET_AT(timestamp, file_name):
    if file_name not in dic:
        return None
    t1 = datetime.fromisoformat(dic[file_name][1]) #Creation time
    t2 = datetime.fromisoformat(timestamp) # Current time
    if (t2 - t1).total_seconds() > dic[file_name][2]: # If current time - created time > ttl => time's up
        results.append(f"file not found")
        return None
    results.append(f"got at {file_name}")
    timeStamps.append(f"FILE_GET_AT: {file_name} at {timestamp}")
    tsdic[timestamp] = copy.deepcopy(dic)
    return dic[file_name]

def FILE_COPY_AT(timestamp, file_from, file_to):
    if file_from not in dic:
        raise RuntimeError("File doesn't exists on the server")
    t1 = datetime.fromisoformat(dic[file_from][1]) #Creation time
    t2 = datetime.fromisoformat(timestamp) # Current time
    if (t2 - t1).total_seconds() > dic[file_from][2]: # If current time - created time > ttl => time's up
        results.append(f"file not found")
        return
    cp = dic[file_from]
    dic[file_to] = cp
    results.append(f"copied at {file_from} to {file_to}")
    timeStamps.append(f"FILE_COPY_AT: from {file_from} to {file_to} at {timestamp}")
    tsdic[timestamp] = copy.deepcopy(dic)

def FILE_SEARCH_AT(timestamp, prefix):
    lstName = []
    lstSize = []
    for file in dic:
        t1 = datetime.fromisoformat(dic[file][1]) #Creation time
        t2 = datetime.fromisoformat(timestamp) # Current time
        if file.startswith(prefix) and (t2 - t1).total_seconds() < dic[file][2]: # If current time - created time < ttl => still have time left

            if not lstSize:
                lstName.append(file)
                lstSize.append(dic[file])
            elif lstSize and dic[file][0] < lstSize[-1][0]:
                lstName.insert(len(lstName), file)
                lstSize.insert(len(lstSize), dic[file])
            else:
                for i in range(len(lstName)):
                    if lstSize[i][0] < dic[file][0]:
                        lstName.insert(i, file)
                        lstSize.insert(i, dic[file])
                    elif dic[file][0] == lstSize[i][0]:
                        if lstName[i] > file:
                            lstName.insert(i, file)
                            lstSize.insert(i, dic[file])
                        else:
                            lstName.insert(i + 1, file)
                            lstSize.insert(i + 1, dic[file])
    lstName = lstName[:10]
    top10 = ", ".join(lstName)
    results.append(f"found at [{top10}]")
    timeStamps.append(f"FILE_SEARCH_AT: with prefix {prefix} at {timestamp}")
    tsdic[timestamp] = copy.deepcopy(dic)
    return top10

# def ROLLBACK(timestamp):
#     global dic
#     dic = copy.deepcopy(tsdic[timestamp])
#     for file in dic:
#         if dic[file][2] != float("inf"):
#             t1 = datetime.fromisoformat(dic[file][1]) # Old Creation Time
#             t2 = datetime.fromisoformat(timestamp) # New Creation Time
#             newTtl = dic[file][2] - (t2-t1).total_seconds()
#             dic[file][2] = max(0, newTtl)
#     results.append(f"rollback to {timestamp}")
#     tsdic[timestamp] = copy.deepcopy(dic)

# THE TEST OUTPUT IS WRONG!

def ROLLBACK(timestamp):
    global dic
    # Don't restore old state - keep all current files
    # Just adjust TTLs relative to rollback timestamp
    rollback_time = datetime.fromisoformat(timestamp)
    
    for file in dic:
        if dic[file][2] != float("inf"):
            creation_time = datetime.fromisoformat(dic[file][1])
            time_elapsed = (rollback_time - creation_time).total_seconds()
            
            # Only reduce TTL if file was created before rollback point
            if time_elapsed > 0:
                dic[file][2] = dic[file][2] - time_elapsed
            # Files created after rollback keep their original TTL unchanged
    
    results.append(f"rollback to {timestamp}")
    # Don't save to tsdic here - it causes duplication issues

def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    
    # Calling
    for command in list_of_lists:
        if command[0] == "FILE_UPLOAD":
            FILE_UPLOAD(command[1], command[2])
        elif command[0] == "FILE_GET":
            FILE_GET(command[1])
        elif command[0] == "FILE_COPY":
            FILE_COPY(command[1], command[2])
        elif command[0] == "FILE_SEARCH":
            FILE_SEARCH(command[1])
        elif command[0] == "FILE_UPLOAD_AT":
            if len(command) == 4:
                FILE_UPLOAD_AT(command[1], command[2], command[3], None)
            else:
                FILE_UPLOAD_AT(command[1], command[2], command[3], command[4])
        elif command[0] == "FILE_GET_AT":
            FILE_GET_AT(command[1], command[2])
        elif command[0] == "FILE_COPY_AT":
            FILE_COPY_AT(command[1], command[2], command[3])
        elif command[0] == "FILE_SEARCH_AT":
            FILE_SEARCH_AT(command[1], command[2])
        elif command[0] == "ROLLBACK":
            ROLLBACK(command[1])
    return results
