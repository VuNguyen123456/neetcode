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
    if item_id not in dic:
        results.append("error: item not found")
        return None
    results.append(f"get item {item_id}")
    return dic[item_id]

def ITEM_UPDATE_QTY(item_id, quantity):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    dic[item_id]['quantity'] = quantity
    results.append(f"update quantity item {item_id}")

def ITEM_REMOVE(item_id):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    del dic[item_id]
    results.append(f"del item {item_id}")

# Level 2:
def ITEM_RESTOCK(item_id, amount):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    dic[item_id]['quantity'] += amount
    results.append(f"restock item {item_id}")

def ITEM_SELL(item_id, amount):
    if item_id not in dic:
        results.append("error: item not found")
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

def ITEM_ADD(item_id, name, quantity, category=None, location=None):
    if item_id not in dic:
        dic[item_id] = {'name': name, 'quantity': quantity, 'category': category, 'location': location}
    results.append(f"add item id:{item_id}")

def ITEM_MOVE(item_id, new_location):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    dic[item_id]['location'] = new_location
    results.append(f"relocate item {item_id}")

def ITEM_FILTER(category=None, location=None):
    filtered = []
    for item_id in dic:
        item = dic[item_id]
        if ((category is None or item.get('category') == category) and 
            (location is None or item.get('location') == location)):
            filtered.append(item_id)
    
    sorted_items = sorted(filtered)
    result = ", ".join(sorted_items)
    results.append(f"filtered [{result}]")
    return sorted_items
    
def ITEM_ADD_AMOUNT(item_id, amount):
    if item_id not in dic:
        return False
    dic[item_id]['quantity'] += amount

def ITEM_REDUCE_AMOUNT(item_id, amount):
    if item_id not in dic:
        return False
    if dic[item_id]['quantity'] < amount:
        return False
    dic[item_id]['quantity'] -= amount

def ITEM_TRANSFER(from_location, to_location, item_id, amount):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    
    # Check if item is at source location
    if dic[item_id]['location'] != from_location:
        results.append("error: item not at source location")
        return
    
    # Check if we can reduce the amount
    if not ITEM_REDUCE_AMOUNT(item_id, amount):
        results.append("error: insufficient stock")
        return

    # is there's is an already exist destination you just add the amount in
    dest_found = False
    for iid in dic:
        if (dic[iid]['name'] == dic[item_id]['name'] and 
            dic[iid]['location'] == to_location):
            ITEM_ADD_AMOUNT(iid, amount)
            dest_found = True
            break
    
    # If you didn't found existing destination then make a new item at that location for that transfer
    if not dest_found:
        new_id = f"{item_id}_at_{to_location}"
        dic[new_id] = {
            'name': dic[item_id]['name'],
            'quantity': amount,
            'category': dic[item_id].get('category'),
            'location': to_location
        }
    
    results.append(f"transferred {item_id}")

tsdic = {}

def ITEM_ADD_AT(timestamp, item_id, name, quantity, category=None, location=None):
    if item_id not in dic:
        dic[item_id] = {'name': name, 'quantity': quantity, 'category': category, 'location': location, 'createdTime': timestamp,
                        'history': [
                            {'time': timestamp, 'action': 'added', 'quantity': quantity}
                        ]
                        }
    results.append(f"add item id:{item_id}")
    tsdic[timestamp] = copy.deepcopy(dic)

def ITEM_RESTOCK_AT(timestamp, item_id, amount):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    dic[item_id]['quantity'] += amount
    dic[item_id]['history'].append({'time': timestamp, 'action': 'restocked', 'amount': amount})
    results.append(f"restock item {item_id}")
    tsdic[timestamp] = copy.deepcopy(dic)

def ITEM_SELL_AT(timestamp, item_id, amount):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    if dic[item_id]['quantity'] < amount:
        raise RuntimeError("insufficient")
    dic[item_id]['quantity'] -= amount
    dic[item_id]['history'].append({'time': timestamp, 'action': 'sold', 'amount': amount})
    results.append(f"sell item {item_id}")
    tsdic[timestamp] = copy.deepcopy(dic)

def ITEM_MOVE_AT(timestamp, item_id, location):
    if item_id not in dic:
        results.append("error: item not found")
        return None
    dic[item_id]['location'] = location
    dic[item_id]['history'].append({'time': timestamp, 'action': 'moved', 'location': location})
    results.append(f"relocate item {item_id}")
    tsdic[timestamp] = copy.deepcopy(dic)

def TRANSACTION_LOG(item_id):
    if item_id not in dic:
        results.append("error: item not found")
        return
    
    log_entries = []
    for event in dic[item_id]['history']:
        if event['action'] == 'added':
            log_entries.append(f"{event['time']} added qty={event['quantity']}")
        elif event['action'] == 'restocked':
            log_entries.append(f"{event['time']} restocked +{event['amount']}")
        elif event['action'] == 'sold':
            log_entries.append(f"{event['time']} sold -{event['amount']}")
        elif event['action'] == 'moved':
            log_entries.append(f"{event['time']} moved to {event['location']}")
    
    log_str = ", ".join(log_entries)
    results.append(f"log {item_id}: [{log_str}]")

def ROLLBACK(timestamp):
    global dic
    dic = copy.deepcopy(tsdic[timestamp])
    tsdic[timestamp] = copy.deepcopy(dic)
    results.append(f"rolledBack to {timestamp}")

# Scuff
# def AUDIT(start_time, end_time):
#     changes = []
#     for item in dic:
#         for t in range(len(dic[item]['history'])):
#             if (datetime.fromisoformat(dic[item]['history'][t]['time']) < datetime.fromisoformat(end_time) 
#                 and datetime.fromisoformat(dic[item]['history'][t]['time']) > datetime.fromisoformat(start_time)):
#                 changes.append(dic[item]['history'][t])
#     results.append(f"audited to {changes}")

def AUDIT(start_time, end_time):
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    changes = []
    
    for item_id in dic:
        for t in range(len(dic[item_id]['history'])):
            event = dic[item_id]['history'][t]
            event_time = datetime.fromisoformat(event['time'])
            
            if start < event_time < end:
                # Add to changes based on action type
                if event['action'] == 'restocked':
                    changes.append((event['time'], f"{event['time']} {item_id} restocked +{event['amount']}"))
                elif event['action'] == 'sold':
                    changes.append((event['time'], f"{event['time']} {item_id} sold -{event['amount']}"))
    
    # Sort by timestamp and format
    changes.sort(key=lambda x: x[0])
    audit_str = ", ".join([c[1] for c in changes])
    results.append(f"audit: [{audit_str}]")

def simulate_coding_framework(list_of_lists):
    global dic, results, tsdic
    dic = {}
    results = []
    tsdic = {}
    
    for command in list_of_lists:
        operation = command[0]
        
        # Level 1
        if operation == "ITEM_ADD":
            if len(command) == 6:
                ITEM_ADD(command[1], command[2], command[3], command[4], command[5])
            elif len(command) == 5:
                ITEM_ADD(command[1], command[2], command[3], command[4])
            else:
                ITEM_ADD(command[1], command[2], command[3])
        elif operation == "ITEM_GET":
            ITEM_GET(command[1])
        elif operation == "ITEM_UPDATE_QTY":
            ITEM_UPDATE_QTY(command[1], command[2])
        elif operation == "ITEM_REMOVE":
            ITEM_REMOVE(command[1])
        
        # Level 2
        elif operation == "ITEM_RESTOCK":
            ITEM_RESTOCK(command[1], command[2])
        elif operation == "ITEM_SELL":
            ITEM_SELL(command[1], command[2])
        elif operation == "ITEM_LOW_STOCK":
            ITEM_LOW_STOCK(command[1])
        
        # Level 3
        elif operation == "ITEM_FILTER":
            if len(command) == 3:
                ITEM_FILTER(command[1], command[2])
            elif len(command) == 2:
                ITEM_FILTER(command[1], None)
            else:
                ITEM_FILTER(None, None)
        elif operation == "ITEM_MOVE":
            ITEM_MOVE(command[1], command[2])
        elif operation == "ITEM_TRANSFER":
            ITEM_TRANSFER(command[1], command[2], command[3], command[4])
        
        # Level 4
        elif operation == "ITEM_ADD_AT":
            if len(command) == 7:
                ITEM_ADD_AT(command[1], command[2], command[3], command[4], command[5], command[6])
            elif len(command) == 6:
                ITEM_ADD_AT(command[1], command[2], command[3], command[4], command[5])
            else:
                ITEM_ADD_AT(command[1], command[2], command[3], command[4])
        elif operation == "ITEM_RESTOCK_AT":
            ITEM_RESTOCK_AT(command[1], command[2], command[3])
        elif operation == "ITEM_SELL_AT":
            ITEM_SELL_AT(command[1], command[2], command[3])
        elif operation == "ITEM_MOVE_AT":
            ITEM_MOVE_AT(command[1], command[2], command[3])
        elif operation == "TRANSACTION_LOG":
            TRANSACTION_LOG(command[1])
        elif operation == "ROLLBACK":
            ROLLBACK(command[1])
        elif operation == "AUDIT":
            AUDIT(command[1], command[2])
    
    return results



"""
LEVEL 4 - Transaction Log & Rollback

Requirements:
- All operations now have _AT(timestamp, ...) variants
- TRANSACTION_LOG(item_id) - Return all transactions for an item
- ROLLBACK(timestamp) - Restore inventory to state at timestamp
- AUDIT(start_time, end_time) - Return all changes in time range

Data Structure Suggestion:
dic[item_id] = {
    'name': name,
    'quantity': current_quantity,
    'category': category,
    'location': location,
    'history': [
        {'time': '2024-01-01T10:00:00', 'action': 'added', 'quantity': 100},
        {'time': '2024-01-01T11:00:00', 'action': 'sold', 'quantity': -20},
        {'time': '2024-01-01T12:00:00', 'action': 'restocked', 'quantity': +50}
    ]
}
"""

import unittest
from sim import simulate_coding_framework

class TestInventoryLevel4(unittest.TestCase):
    
    # ========== LEVEL 4 TESTS ==========
    
    def test_level4_add_at(self):
        """Test adding items with timestamps"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_ADD_AT", "2024-01-01T11:00:00", "ITEM002", "Gadget", 50, "Electronics", "WH2"],
            ["ITEM_GET", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "added ITEM002 at 2024-01-01T11:00:00",
            "got ITEM001"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_restock_at(self):
        """Test restocking with timestamps"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_RESTOCK_AT", "2024-01-01T11:00:00", "ITEM001", 50],
            ["ITEM_GET", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "restocked ITEM001 at 2024-01-01T11:00:00",
            "got ITEM001"  # Should show quantity 150
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_sell_at(self):
        """Test selling with timestamps"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_SELL_AT", "2024-01-01T11:00:00", "ITEM001", 30],
            ["ITEM_GET", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "sold ITEM001 at 2024-01-01T11:00:00",
            "got ITEM001"  # Should show quantity 70
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_transaction_log(self):
        """Test transaction log for an item"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_RESTOCK_AT", "2024-01-01T11:00:00", "ITEM001", 50],
            ["ITEM_SELL_AT", "2024-01-01T12:00:00", "ITEM001", 30],
            ["TRANSACTION_LOG", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "restocked ITEM001 at 2024-01-01T11:00:00",
            "sold ITEM001 at 2024-01-01T12:00:00",
            "log ITEM001: [2024-01-01T10:00:00 added qty=100, 2024-01-01T11:00:00 restocked +50, 2024-01-01T12:00:00 sold -30]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_transaction_log_nonexistent(self):
        """Test transaction log for non-existent item"""
        commands = [
            ["TRANSACTION_LOG", "ITEM999"]
        ]
        
        expected = [
            "error: item not found"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_rollback(self):
        """Test rollback to previous state"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_SELL_AT", "2024-01-01T11:00:00", "ITEM001", 30],
            ["ITEM_RESTOCK_AT", "2024-01-01T12:00:00", "ITEM001", 50],
            ["ROLLBACK", "2024-01-01T11:30:00"],
            ["ITEM_GET", "ITEM001"]  # Should show quantity 70 (after sell, before restock)
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "sold ITEM001 at 2024-01-01T11:00:00",
            "restocked ITEM001 at 2024-01-01T12:00:00",
            "rollback to 2024-01-01T11:30:00",
            "got ITEM001"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_rollback_multiple_items(self):
        """Test rollback with multiple items"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T09:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM002", "Gadget", 50, "Electronics", "WH1"],
            ["ITEM_SELL_AT", "2024-01-01T11:00:00", "ITEM001", 30],
            ["ITEM_ADD_AT", "2024-01-01T12:00:00", "ITEM003", "Doohickey", 75, "Tools", "WH2"],
            ["ROLLBACK", "2024-01-01T10:30:00"],
            ["ITEM_GET", "ITEM001"],  # Should exist with qty 100
            ["ITEM_GET", "ITEM002"],  # Should exist with qty 50
            ["ITEM_GET", "ITEM003"]   # Should NOT exist (created after rollback point)
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T09:00:00",
            "added ITEM002 at 2024-01-01T10:00:00",
            "sold ITEM001 at 2024-01-01T11:00:00",
            "added ITEM003 at 2024-01-01T12:00:00",
            "rollback to 2024-01-01T10:30:00",
            "got ITEM001",            # qty 100 (sell hadn't happened yet)
            "got ITEM002",            # qty 50
            "error: item not found"   # ITEM003 doesn't exist yet
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_audit(self):
        """Test audit for time range"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T09:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_SELL_AT", "2024-01-01T10:00:00", "ITEM001", 30],
            ["ITEM_RESTOCK_AT", "2024-01-01T11:00:00", "ITEM001", 50],
            ["ITEM_ADD_AT", "2024-01-01T12:00:00", "ITEM002", "Gadget", 75, "Electronics", "WH2"],
            ["AUDIT", "2024-01-01T09:30:00", "2024-01-01T11:30:00"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T09:00:00",
            "sold ITEM001 at 2024-01-01T10:00:00",
            "restocked ITEM001 at 2024-01-01T11:00:00",
            "added ITEM002 at 2024-01-01T12:00:00",
            "audit: [2024-01-01T10:00:00 ITEM001 sold -30, 2024-01-01T11:00:00 ITEM001 restocked +50]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_audit_empty(self):
        """Test audit with no transactions in range"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T10:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["AUDIT", "2024-01-01T11:00:00", "2024-01-01T12:00:00"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T10:00:00",
            "audit: []"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_complex_scenario(self):
        """Test complex scenario with all Level 4 features"""
        commands = [
            ["ITEM_ADD_AT", "2024-01-01T09:00:00", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_RESTOCK_AT", "2024-01-01T10:00:00", "ITEM001", 50],
            ["ITEM_SELL_AT", "2024-01-01T11:00:00", "ITEM001", 30],
            ["TRANSACTION_LOG", "ITEM001"],
            ["AUDIT", "2024-01-01T09:30:00", "2024-01-01T11:30:00"],
            ["ROLLBACK", "2024-01-01T10:30:00"],
            ["ITEM_GET", "ITEM001"],  # Should be 150 (after restock, before sell)
            ["TRANSACTION_LOG", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001 at 2024-01-01T09:00:00",
            "restocked ITEM001 at 2024-01-01T10:00:00",
            "sold ITEM001 at 2024-01-01T11:00:00",
            "log ITEM001: [2024-01-01T09:00:00 added qty=100, 2024-01-01T10:00:00 restocked +50, 2024-01-01T11:00:00 sold -30]",
            "audit: [2024-01-01T10:00:00 ITEM001 restocked +50, 2024-01-01T11:00:00 ITEM001 sold -30]",
            "rollback to 2024-01-01T10:30:00",
            "got ITEM001",
            "log ITEM001: [2024-01-01T09:00:00 added qty=100, 2024-01-01T10:00:00 restocked +50]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_backward_compatibility(self):
        """Test that non-timestamped operations still work"""
        commands = [
            ["ITEM_ADD", "ITEM001", "Widget", 100, "Electronics", "WH1"],
            ["ITEM_RESTOCK", "ITEM001", 50],
            ["ITEM_SELL", "ITEM001", 30],
            ["ITEM_GET", "ITEM001"]
        ]
        
        expected = [
            "added ITEM001",
            "restocked ITEM001",
            "sold ITEM001",
            "got ITEM001"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
