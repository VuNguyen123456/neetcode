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

import numpy as np
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

# def URL_SHORTEN(long_url, custom_code=None):
#     if custom_code == None:
#         code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
#         while code in dic:
#             code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
#     else:
#         code = custom_code
#         while custom_code in dic:
#             code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))        
    
#     dic[code] = {
#         'url': long_url,
#         'clicks': 0,
#         'created_at': datetime.now().isoformat()  # Use .isoformat() not .time()
#     }
#     results.append(f"shorten {long_url} to {code}")
#     return code

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

def URL_SHORTEN(long_url, custom_code=None, user_id=None, ttl=None):
    if custom_code is None:
        code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
        while code in dic:
            code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6))
    else:
        if custom_code in dic:
            results.append("error: code already exists")
            return
        code = custom_code
    
    dic[code] = {
        'url': long_url,
        'clicks': 0,
        'uid': user_id,
        'created_at': datetime.now().isoformat(),
        'ttl': ttl
    }
    results.append(f"shortened to {code}")
    return code

def URL_USER_LIST(user_id):
    res = []
    for code in dic:
        if dic[code]['uid'] == user_id:
            res.append(code)
    if not res:
        results.append(f"{user_id} doesn't exist")
        return res
    results.append(f"user id: [{res}]")
    return res

def URL_RENEW(short_code, new_ttl):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    dic[short_code]['ttl'] = new_ttl
    results.append(f"new ttl for {short_code}")

def URL_EXPAND_AT(timestamp, short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    checkedTime = datetime.fromisoformat(timestamp)
    createdTime = datetime.fromisoformat(dic[short_code]['created_at'])
    if dic[short_code]['ttl'] != None and (checkedTime - createdTime).total_seconds() > dic[short_code]['ttl']:
        results.append('invalid time')
    else:
        results.append('valid time')

def URL_CREATE_VERSION(short_code, long_url_v2, split_percent):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    dic[short_code]['url_v2'] = long_url_v2
    dic[short_code]['clicks_v2'] = 0
    dic[short_code]['splits'] = split_percent
    results.append(f'version 2 created: {long_url_v2}')

def URL_CLICK(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    if 'url_v2' in dic[short_code]:
        items = ['v1', 'v2']
        weight = [dic[short_code]['splits'], 100 - dic[short_code]['splits']]
        chosen_v = random.choices(items, weights=weight)[0]
        if chosen_v == items[0]:
            dic[short_code]['clicks'] += 1
        else:
            dic[short_code]['clicks_v2'] += 1
        results.append(f'click routed to: {short_code} version: {chosen_v}')
    else:
        dic[short_code]['clicks'] += 1
        results.append(f'click routed to: {short_code} version: v1')

def URL_VERSION_STATS(short_code):
    if short_code not in dic:
        results.append("error: code not found")
        return
    
    v1_clicks = dic[short_code]['clicks']
    
    if 'url_v2' not in dic[short_code]:
        results.append(f"stats {short_code}: {v1_clicks} clicks")
    else:
        v2_clicks = dic[short_code]['clicks_v2']
        results.append(f"stats {short_code}: v1={v1_clicks}, v2={v2_clicks}")

def URL_SET_SPLIT(short_code, split_percent):
    if short_code not in dic:
        results.append("error: code not found")
        return None
    if 'url_v2' not in dic[short_code]:
        results.append("error: no version 2 exists")
        return
    
    dic[short_code]['splits'] = split_percent
    results.append(f"split updated {short_code}")

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
        elif operation == "URL_USER_LIST":
            URL_USER_LIST(command[1])
        elif operation == "URL_RENEW":
            URL_RENEW(command[1], command[2])
        elif operation == "URL_EXPAND_AT":
            URL_EXPAND_AT(command[1], command[2])
        elif operation == "URL_CREATE_VERSION":
            URL_CREATE_VERSION(command[1], command[2], command[3])
        elif operation == "URL_VERSION_STATS":
            URL_VERSION_STATS(command[1])
        elif operation == "URL_SET_SPLIT":
            URL_SET_SPLIT(command[1], command[2])
    
    return results
