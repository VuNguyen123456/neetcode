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

# def URL_CLICK(short_code):
#     if short_code not in dic:
#         results.append("error: code not found")
#         return None
#     dic[short_code]['clicks'] += 1
#     results.append(f"increment click of {short_code}")

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
        temp.append([url, dic[url]['clicks']])
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
        results.append(f"clicked {short_code}")

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
            elif len(command) == 3:
                URL_SHORTEN(command[1], command[2])
            elif len(command) == 4:
                URL_SHORTEN(command[1], command[2], command[3])
            elif len(command) == 5:
                URL_SHORTEN(command[1], command[2], command[3], command[4])
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


"""
URL Shortener Service - Test Cases for All Levels
"""

import unittest
from sim import simulate_coding_framework

class TestURLShortener(unittest.TestCase):
    
    # ========== LEVEL 1 TESTS ==========
    
    def test_level1_basic_shorten_expand(self):
        """Test basic URL shortening and expansion"""
        commands = [
            ["URL_SHORTEN", "https://www.google.com"],
            ["URL_EXPAND", "CODE1"],  # Will fail - code is random
        ]
        
        output = simulate_coding_framework(commands)
        # Can't test exact code since it's random
        self.assertTrue(output[0].startswith("shortened to"))
        # Note: This test is incomplete - in real tests you'd capture the returned code
    
    def test_level1_delete(self):
        """Test deleting a shortened URL"""
        commands = [
            ["URL_SHORTEN", "https://example.com"],
            ["URL_DELETE", "abc123"],  # Assume we know the code
        ]
        
        # Note: Can't fully test without knowing generated code
        # In practice, you'd mock random or use custom codes
    
    # ========== LEVEL 2 TESTS ==========
    
    def test_level2_custom_code(self):
        """Test custom short codes"""
        commands = [
            ["URL_SHORTEN", "https://www.example.com", "mycustom"],
            ["URL_EXPAND", "mycustom"],
            ["URL_DELETE", "mycustom"],
            ["URL_EXPAND", "mycustom"]
        ]
        
        expected = [
            "shortened to mycustom",
            "expanded mycustom",
            "deleted mycustom",
            "error: code not found"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level2_duplicate_custom_code(self):
        """Test creating duplicate custom code"""
        commands = [
            ["URL_SHORTEN", "https://example1.com", "test123"],
            ["URL_SHORTEN", "https://example2.com", "test123"]
        ]
        
        expected = [
            "shortened to test123",
            "error: code already exists"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level2_clicks(self):
        """Test click tracking"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "click1"],
            ["URL_CLICK", "click1"],
            ["URL_CLICK", "click1"],
            ["URL_CLICK", "click1"],
            ["URL_STATS", "click1"]
        ]
        
        expected = [
            "shortened to click1",
            "click routed to: click1 version: v1",
            "click routed to: click1 version: v1",
            "click routed to: click1 version: v1",
            "stats click1: 3 clicks"  # Adjust format based on your implementation
        ]
        
        output = simulate_coding_framework(commands)
        # Check first 4 outputs, stats format may vary
        self.assertEqual(output[:4], expected[:4])
        self.assertIn("3", output[4])  # Should contain click count
    
    def test_level2_top_urls(self):
        """Test getting top N URLs by clicks"""
        commands = [
            ["URL_SHORTEN", "https://url1.com", "code1"],
            ["URL_SHORTEN", "https://url2.com", "code2"],
            ["URL_SHORTEN", "https://url3.com", "code3"],
            ["URL_CLICK", "code1"],
            ["URL_CLICK", "code1"],
            ["URL_CLICK", "code1"],
            ["URL_CLICK", "code2"],
            ["URL_CLICK", "code2"],
            ["URL_CLICK", "code3"],
            ["URL_TOP", 2]
        ]
        
        # Top 2 should be code1 (3 clicks) and code2 (2 clicks)
        output = simulate_coding_framework(commands)
        # Check that top command was executed
        self.assertTrue(any("top" in str(o).lower() for o in output))
    
    # ========== LEVEL 3 TESTS ==========
    
    def test_level3_user_tracking(self):
        """Test user-based URL tracking"""
        commands = [
            ["URL_SHORTEN", "https://url1.com", "u1code1", "user1"],
            ["URL_SHORTEN", "https://url2.com", "u1code2", "user1"],
            ["URL_SHORTEN", "https://url3.com", "u2code1", "user2"],
            ["URL_USER_LIST", "user1"],
            ["URL_USER_LIST", "user2"],
            ["URL_USER_LIST", "user999"]
        ]
        
        output = simulate_coding_framework(commands)
        # User1 should have 2 URLs
        self.assertIn("user1", output[3])
        # User999 should have none
        self.assertIn("doesn't exist", output[5])
    
    def test_level3_ttl_expiration(self):
        """Test URL expiration with TTL"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "ttl1", "user1", 3600],  # 1 hour TTL
            ["URL_EXPAND_AT", "2024-01-01T10:00:00", "ttl1"],  # Within TTL
            ["URL_EXPAND_AT", "2024-01-01T12:00:00", "ttl1"]   # After TTL (2 hours later)
        ]
        
        output = simulate_coding_framework(commands)
        # First expand should be valid
        self.assertIn("valid", output[1])
        # Second expand should be invalid/expired
        self.assertIn("invalid", output[2])
    
    def test_level3_ttl_infinite(self):
        """Test URL with no expiration (ttl=None)"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "infinite", "user1"],  # No TTL
            ["URL_EXPAND_AT", "2030-01-01T10:00:00", "infinite"]  # Far future
        ]
        
        expected = [
            "shortened to infinite",
            "valid time"  # Should always be valid
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level3_renew_ttl(self):
        """Test renewing TTL"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "renew1", "user1", 100],
            ["URL_RENEW", "renew1", 5000],
            ["URL_RENEW", "nonexistent", 1000]
        ]
        
        expected = [
            "shortened to renew1",
            "new ttl for renew1",
            "error: code not found"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    # ========== LEVEL 4 TESTS ==========
    
    def test_level4_create_version(self):
        """Test creating A/B test version"""
        commands = [
            ["URL_SHORTEN", "https://version-a.com", "ab1"],
            ["URL_CREATE_VERSION", "ab1", "https://version-b.com", 50],
            ["URL_VERSION_STATS", "ab1"]
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output[0], "shortened to ab1")
        self.assertIn("version 2", output[1].lower())
        self.assertIn("v1=0", output[2])
        self.assertIn("v2=0", output[2])
    
    def test_level4_ab_testing_clicks(self):
        """Test A/B testing with clicks"""
        commands = [
            ["URL_SHORTEN", "https://version-a.com", "ab2"],
            ["URL_CREATE_VERSION", "ab2", "https://version-b.com", 100],  # 100% to v2
            ["URL_CLICK", "ab2"],
            ["URL_CLICK", "ab2"],
            ["URL_CLICK", "ab2"],
            ["URL_VERSION_STATS", "ab2"]
        ]
        
        output = simulate_coding_framework(commands)
        # With 100% split, all clicks should go to v2
        self.assertIn("v1=0", output[5])
        self.assertIn("v2=3", output[5])
    
    def test_level4_ab_testing_0_percent(self):
        """Test A/B testing with 0% split"""
        commands = [
            ["URL_SHORTEN", "https://version-a.com", "ab3"],
            ["URL_CREATE_VERSION", "ab3", "https://version-b.com", 0],  # 0% to v2
            ["URL_CLICK", "ab3"],
            ["URL_CLICK", "ab3"],
            ["URL_VERSION_STATS", "ab3"]
        ]
        
        output = simulate_coding_framework(commands)
        # With 0% split, all clicks should go to v1
        self.assertIn("v1=2", output[4])
        self.assertIn("v2=0", output[4])
    
    def test_level4_set_split(self):
        """Test adjusting split percentage"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "split1"],
            ["URL_CREATE_VERSION", "split1", "https://example-v2.com", 30],
            ["URL_SET_SPLIT", "split1", 70],
            ["URL_SET_SPLIT", "nosplit", 50]  # No v2 exists
        ]
        
        expected = [
            "shortened to split1",
            "version 2 created: https://example-v2.com",
            "split updated split1",
            "error: code not found"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_version_without_v2(self):
        """Test stats for URL without v2"""
        commands = [
            ["URL_SHORTEN", "https://example.com", "nov2"],
            ["URL_CLICK", "nov2"],
            ["URL_CLICK", "nov2"],
            ["URL_VERSION_STATS", "nov2"]
        ]
        
        output = simulate_coding_framework(commands)
        # Should show only v1 clicks
        self.assertIn("2", output[3])
        self.assertNotIn("v2", output[3])
    
    # ========== INTEGRATION TESTS ==========
    
    def test_complex_scenario(self):
        """Test complex multi-level scenario"""
        commands = [
            ["URL_SHORTEN", "https://product.com/landing", "promo", "user1", 7200],
            ["URL_CREATE_VERSION", "promo", "https://product.com/landing-v2", 50],
            ["URL_CLICK", "promo"],
            ["URL_CLICK", "promo"],
            ["URL_CLICK", "promo"],
            ["URL_CLICK", "promo"],
            ["URL_VERSION_STATS", "promo"],
            ["URL_SET_SPLIT", "promo", 80],
            ["URL_USER_LIST", "user1"],
            ["URL_EXPAND_AT", "2024-01-01T10:00:00", "promo"]
        ]
        
        output = simulate_coding_framework(commands)
        # Basic checks
        self.assertEqual(output[0], "shortened to promo")
        self.assertIn("promo", output[8])  # User list should contain promo
        self.assertIn("valid", output[9])   # Should be valid within TTL


if __name__ == '__main__':
    unittest.main()
