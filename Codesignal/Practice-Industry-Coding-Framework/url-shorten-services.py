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

dic = {}
results = [] 

# def URL_SHORTEN(long_url):
#     code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
#     while code in dic:
#         code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
#     dic[code] = long_url
#     results.append(f"shorten {long_url} to {code}")
#     return code

def URL_EXPAND(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    results.append(f"expanded {short_code}")
    return dic[short_code]['url']

def URL_DELETE(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    results.append(f"deleted {short_code}")
    del dic[short_code]

def URL_SHORTEN(long_url, custom_code=None):
    if custom_code == None:
        code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
        while code in dic:
            code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
    else:
        code = custom_code
        while custom_code in dic:
            code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))        
    
    dic[code] = {
        'url': long_url,
        'clicks': 0,
        'created_at': datetime.now().isoformat()  # Use .isoformat() not .time()
    }
    results.append(f"shorten {long_url} to {code}")
    return code

def URL_CLICK(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    dic[short_code]['clicks'] += 1
    results.append(f"increment click of {short_code}")

def URL_STATS(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    results.append(f"{short_code}: {dic[short_code]['clicks']} clicks, created_at {dic[short_code]['created_at']}")
    return dic[short_code]['clicks'], dic[short_code]['created_at']

def URL_TOP(n):
    temp = []
    res = []
    for url in dic:
        temp.append([dic[url]['url'], dic[url]['clicks']])
    temp = sorted(temp, key = lambda x: x[1])
    for i in range(n):
        res.append(temp[i])
    results.append(f"top clicks [{res}]")
    return res

def simulate_coding_framework(list_of_lists):
    global dic, results, tsdic
    dic = {}
    results = []
    tsdic = {}
    
    for command in list_of_lists:
        operation = command[0]
        
        # Level 1
        if operation == "URL_SHORTEN":
            if len(command) == 2:
                URL_SHORTEN(command[1])
            else:
                URL_SHORTEN(command[1], command[2])
        elif operation == "URL_EXPAND":
            URL_EXPAND(command[1])
        elif operation == "URL_DELETE":
            URL_DELETE(command[1])
        elif operation == "URL_CLICK":
            URL_CLICK(command[1])
        elif operation == "URL_STATS":
            URL_STATS(command[1])
        elif operation == "URL_TOP":
            URL_TOP(command[1])
    
    return results
