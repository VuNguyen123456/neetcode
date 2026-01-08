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

# Level 1:
def ITEM_ADD(item_id, name, quantity):
    if item_id not in dic:
        dic[item_id] = {'name': name, 'quantity': quantity}
    results.append(f"add item id:{item_id}")

def ITEM_GET(item_id):
    if item_id in dic:
        return None
    results.append(f"get item {item_id}")
    return dic[item_id]

def ITEM_UPDATE_QTY(item_id, quantity):
    if item_id in dic:
        return None
    dic[item_id]['quantity'] = quantity
    results.append(f"update quantity item {item_id}")

def ITEM_REMOVE(item_id):
    if item_id in dic:
        return None
    del dic[item_id]
    results.append(f"del item {item_id}")

# Level 2:
def ITEM_RESTOCK(item_id, amount):
    if item_id in dic:
        return None
    dic[item_id]['quantity'] += amount
    results.append(f"restock item {item_id}")

def ITEM_SELL(item_id, amount):
    if item_id in dic:
        return None
    if dic[item_id]['quantity'] < amount:
        raise RuntimeError("insufficient")
    dic[item_id]['quantity'] -= amount
    results.append(f"sell item {item_id}")

def ITEM_LOW_STOCK(threshold):
    lowStockItems = []
    for item in dic:
        if dic[item]['quantity'] < threshold:
            lowStockItems.append(dic[item])
    results.append(f"lowstock items: [{lowStockItems}]")
    return lowStockItems

def ITEM_ADD(item_id, name, quantity, category, location):
    if item_id not in dic:
        dic[item_id] = {'name': name, 'quantity': quantity, 'category': category, 'location': location}
    results.append(f"add item id:{item_id}")

def ITEM_MOVE(item_id, new_location):
    if item_id in dic:
        return None
    dic[item_id]['location'] = new_location
    results.append(f"relocate item {item_id}")

def ITEM_FILTER(category=None, location=None):
    filtered = []
    for item in dic:
        if ((dic[item]['category'] == category or category == None) 
            and (dic[item]['location'] == location or location == None)):
            filtered.append(dic[item])
    results.append(f"filtered items: [{filtered}]")
    return filtered
    
# def ITEM_TRANSFER(from_location, to_location, item_id, amount):
#     if item_id in dic:
#         return None


def simulate_coding_framework(list_of_lists):
    global dic, results
    dic = {}
    results = []
    
    for command in list_of_lists:
        operation = command[0]
        
        if operation == "ITEM_ADD":
            ITEM_ADD(command[1], command[2], command[3])
        elif operation == "ITEM_GET":
            ITEM_GET(command[1])
        elif operation == "ITEM_UPDATE_QTY":
            ITEM_UPDATE_QTY(command[1], command[2])
        elif operation == "ITEM_REMOVE":
            ITEM_REMOVE(command[1])
        elif operation == "ITEM_RESTOCK":
            ITEM_RESTOCK(command[1], command[2])
        elif operation == "ITEM_SELL":
            ITEM_SELL(command[1], command[2])
        elif operation == "ITEM_LOW_STOCK":
            ITEM_LOW_STOCK(command[1])
    
    return results
