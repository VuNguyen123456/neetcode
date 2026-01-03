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

# def TASK_CREATE(task_id, description):
#     if task_id in dic:
#         results.append("error: task already exists")
#         return
#     dic[task_id] = description
#     results.append(f"created {task_id}")

def TASK_GET(task_id):
    if task_id not in dic:
        results.append("task not found")
        return
    results.append(f"got {task_id} ({dic[task_id][1]})")
    return dic[task_id]

def TASK_UPDATE(task_id, description):
    if task_id not in dic:
        results.append("error: task not found")
        return
    dic[task_id][0] = description
    results.append(f"updated {task_id}")

def TASK_DELETE(task_id):
    if task_id not in dic:
        results.append("error: task not found")
        return
    del dic[task_id]
    results.append(f"deleted {task_id}")
#dic => [tid: (des, status)]
# def TASK_CREATE(task_id, description, status="TODO"):
#     if task_id in dic:
#         results.append("error: task already exists")
#         return
#     dic[task_id] = [description, status]
#     results.append(f"created {task_id}")

def TASK_SET_STATUS(task_id, status):
    if task_id not in dic:
        results.append("error: task not found")
        return
    dic[task_id][1] = status
    results.append(f"status updated {task_id}")

def TASK_FILTER(status):
    lst = []
    for task in dic:
        if dic[task][1] == status:
            lst.append(task)

    sorted_tasks = sorted(lst)  # This sorts strings alphabetically/numerically
    # Format output
    task_string = ", ".join(sorted_tasks)
    results.append(f"found [{task_string}]")

#dic => [tid: (des, status,prio)]
def TASK_CREATE(task_id, description, status = "TODO", priority = 5):
    if task_id in dic:
        results.append("error: task already exists")
        return
    dic[task_id] = [description, status, priority]
    results.append(f"created {task_id}")

def TASK_TOP(n):
    task_list = []
    for task_id in dic:
        priority = int(dic[task_id][2])  # Convert to int for proper comparison
        task_list.append((task_id, priority))
    
    # Sort by priority (ascending, 1=highest), then by task_id
    sorted_tasks = sorted(task_list, key=lambda x: (x[1], x[0]))
    # sorted_tasks = sorted(task_list, key=lambda x: (-x[1], -x[0])) # For descending order if needed
    
    # Take top n and extract just the task_ids
    top_n = [task_id for task_id, priority in sorted_tasks[:n]]
    
    # Format output
    result = ", ".join(top_n)
    results.append(f"top {n} [{result}]")
    return top_n

def TASK_SEARCH(keyword):
    taskList = []
    for task in dic:
        if keyword in dic[task][0]:
            taskList.append(task)
    
    foundedTasks = ", ".join(taskList)
    results.append(f"found [{foundedTasks}]")


def TASK_SET_PRIORITY(task_id, priority):
    if task_id not in dic:
        results.append("error: task not found")
        return
    dic[task_id][2] = int(priority)
    results.append(f"priority updated {task_id}")

ts = {}
# dic = {tid : desc, status, prio, list of [dictionary]}
def TASK_CREATE_AT(timestamp, task_id, description, status, priority):
    if task_id in dic:
        results.append("error: task already exists")
        return
    dic[task_id] = [description, status, priority, []]
    temp = {}
    temp["time"] = timestamp
    temp["action"] = "created"
    temp["status"] = status
    temp["priority"] = priority
    dic[task_id][3].append(temp)
    results.append(f"created {task_id} at {timestamp}")

def TASK_SET_STATUS_AT(timestamp, task_id, status):
    if task_id not in dic:
        results.append("error: task not found")
        return
    dic[task_id][1] = status
    temp = {}
    temp["time"] = timestamp
    temp["action"] = "status"
    temp["value"] = status
    dic[task_id][3].append(temp)
    results.append(f"status updated {task_id} at {timestamp}")  # Add "at {timestamp}"

def TASK_SET_PRIORITY_AT(timestamp, task_id, priority):
    if task_id not in dic:
        results.append("error: task not found")
        return
    dic[task_id][2] = int(priority)
    temp = {}
    temp["time"] = timestamp
    temp["action"] = "priority"
    temp["value"] = priority
    dic[task_id][3].append(temp)
    results.append(f"priority updated {task_id} at {timestamp}")  # Add "at {timestamp}"

def TASK_SNAPSHOT(timestamp):
    # All the intermediate overwrites happened, 
    # but **only the last one before ts matters**!

    target = datetime.fromisoformat(timestamp)
    snapshot = {}
    for task in dic:
        # Create a state for the current timestamp, each task is their own key in dic
        state = None
        for his in dic[task][3]: #for each timestamp in the task history
            event_time = datetime.fromisoformat(his["time"])
            if event_time > target:
                break  # Don't apply future events
            if his["action"] == "created":
                state = {"status": his["status"], "priority": his["priority"]}
            elif his["action"] == "status":
                state["status"] = his["value"]
            elif his["action"] == "priority":
                state["priority"] = his["value"]
        if state:
            snapshot[task] = state
    lstTask = []
    for task in sorted(snapshot.keys()):
        lstTask.append(f"{task} ({snapshot[task]['status']})")
    res = ", ".join(lstTask)
    results.append(f"snapshot at {timestamp}: [{res}]")

def TASK_HISTORY(task_id):
    if task_id not in dic:  # ADD THIS CHECK
        results.append("error: task not found")
        return
    lst = []
    for his in dic[task_id][3]:
        if his["action"] == "created":
            lst.append(f'{his["time"]} created')
        elif his["action"] == "status":
            lst.append(f'{his["time"]} status->{his["value"]}')
        elif his["action"] == "priority":
            lst.append(f'{his["time"]} priority->{his["value"]}')

    res = ", ".join(lst)
    results.append(f"history {task_id}: [{res}]")

def simulate_coding_framework(list_of_lists):
    global dic, results
    dic = {}
    results = []
    
    for command in list_of_lists:
        operation = command[0]
        
        if operation == "TASK_CREATE":
            if len(command) == 5:
                TASK_CREATE(command[1], command[2], command[3], int(command[4]))
            elif len(command) == 4:
                TASK_CREATE(command[1], command[2], command[3])
            else:
                TASK_CREATE(command[1], command[2])
        elif operation == "TASK_GET":
            TASK_GET(command[1])
        elif operation == "TASK_UPDATE":
            TASK_UPDATE(command[1], command[2])
        elif operation == "TASK_DELETE":
            TASK_DELETE(command[1])
        elif operation == "TASK_SET_STATUS":
            TASK_SET_STATUS(command[1], command[2])
        elif operation == "TASK_FILTER":
            TASK_FILTER(command[1])
        elif operation == "TASK_SET_PRIORITY":
            TASK_SET_PRIORITY(command[1], command[2])
        elif operation == "TASK_TOP":
            TASK_TOP(int(command[1]))  # Convert n to int
        elif operation == "TASK_SEARCH":
            TASK_SEARCH(command[1])
        elif operation == "TASK_CREATE_AT":
            TASK_CREATE_AT(command[1], command[2], command[3], command[4], int(command[5]))
        elif operation == "TASK_SET_STATUS_AT":
            TASK_SET_STATUS_AT(command[1], command[2], command[3])
        elif operation == "TASK_SET_PRIORITY_AT":
            TASK_SET_PRIORITY_AT(command[1], command[2], command[3])
        elif operation == "TASK_SNAPSHOT":
            TASK_SNAPSHOT(command[1])
        elif operation == "TASK_HISTORY":
            TASK_HISTORY(command[1])
    
    return results



# # import unittest
# # from sim import simulate_coding_framework

# # # class TestTaskManagement(unittest.TestCase):
    
# # #     def setUp(self):
# # #         """Reset state before each test"""
# # #         global dic
# # #         dic = {}
    
# # #     # ========== LEVEL 1 TESTS ==========
# # #     def test_level1_basic_operations(self):
# # #         """Test basic CRUD operations"""
# # #         commands = [
# # #             ["TASK_CREATE", "T1", "Implement login feature"],
# # #             ["TASK_GET", "T1"],
# # #             ["TASK_UPDATE", "T1", "Implement login with OAuth"],
# # #             ["TASK_GET", "T1"],
# # #             ["TASK_DELETE", "T1"],
# # #             ["TASK_GET", "T1"]
# # #         ]
        
# # #         expected = [
# # #             "created T1",
# # #             "got T1",
# # #             "updated T1",
# # #             "got T1",
# # #             "deleted T1",
# # #             "task not found"
# # #         ]
        
# # #         output = simulate_coding_framework(commands)
# # #         self.assertEqual(output, expected)
    
# # #     def test_level1_duplicate_create(self):
# # #         """Test creating duplicate task"""
# # #         commands = [
# # #             ["TASK_CREATE", "T1", "First task"],
# # #             ["TASK_CREATE", "T1", "Duplicate task"]
# # #         ]
        
# # #         expected = [
# # #             "created T1",
# # #             "error: task already exists"
# # #         ]
        
# # #         output = simulate_coding_framework(commands)
# # #         self.assertEqual(output, expected)
    
# # #     def test_level1_update_nonexistent(self):
# # #         """Test updating non-existent task"""
# # #         commands = [
# # #             ["TASK_UPDATE", "T99", "This doesn't exist"]
# # #         ]
        
# # #         expected = [
# # #             "error: task not found"
# # #         ]
        
# # #         output = simulate_coding_framework(commands)
# # #         self.assertEqual(output, expected)
    
# # #     def test_level1_multiple_tasks(self):
# # #         """Test managing multiple tasks"""
# # #         commands = [
# # #             ["TASK_CREATE", "T1", "Task One"],
# # #             ["TASK_CREATE", "T2", "Task Two"],
# # #             ["TASK_CREATE", "T3", "Task Three"],
# # #             ["TASK_GET", "T2"],
# # #             ["TASK_DELETE", "T1"],
# # #             ["TASK_GET", "T1"],
# # #             ["TASK_GET", "T3"]
# # #         ]
        
# # #         expected = [
# # #             "created T1",
# # #             "created T2",
# # #             "created T3",
# # #             "got T2",
# # #             "deleted T1",
# # #             "task not found",
# # #             "got T3"
# # #         ]
        
# # #         output = simulate_coding_framework(commands)
# # #         self.assertEqual(output, expected)

# # class TestTaskManagementLevel2(unittest.TestCase):
    
# #     # ========== LEVEL 2 TESTS ==========
# #     def test_level2_create_with_status(self):
# #         """Test creating tasks with status"""
# #         commands = [
# #             ["TASK_CREATE", "T1", "Implement login", "TODO"],
# #             ["TASK_CREATE", "T2", "Write tests", "IN_PROGRESS"],
# #             ["TASK_CREATE", "T3", "Deploy", "DONE"],
# #             ["TASK_GET", "T1"],
# #             ["TASK_GET", "T2"]
# #         ]
        
# #         expected = [
# #             "created T1",
# #             "created T2",
# #             "created T3",
# #             "got T1 (TODO)",
# #             "got T2 (IN_PROGRESS)"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_default_status(self):
# #         """Test default status is TODO"""
# #         commands = [
# #             ["TASK_CREATE", "T1", "Default status task"],
# #             ["TASK_GET", "T1"]
# #         ]
        
# #         expected = [
# #             "created T1",
# #             "got T1 (TODO)"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_set_status(self):
# #         """Test changing task status"""
# #         commands = [
# #             ["TASK_CREATE", "T1", "Backend API", "TODO"],
# #             ["TASK_SET_STATUS", "T1", "IN_PROGRESS"],
# #             ["TASK_GET", "T1"],
# #             ["TASK_SET_STATUS", "T1", "DONE"],
# #             ["TASK_GET", "T1"]
# #         ]
        
# #         expected = [
# #             "created T1",
# #             "status updated T1",
# #             "got T1 (IN_PROGRESS)",
# #             "status updated T1",
# #             "got T1 (DONE)"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_set_status_nonexistent(self):
# #         """Test setting status on non-existent task"""
# #         commands = [
# #             ["TASK_SET_STATUS", "T99", "DONE"]
# #         ]
        
# #         expected = [
# #             "error: task not found"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_filter_by_status(self):
# #         """Test filtering tasks by status"""
# #         commands = [
# #             ["TASK_CREATE", "T3", "Task Three", "TODO"],
# #             ["TASK_CREATE", "T1", "Task One", "IN_PROGRESS"],
# #             ["TASK_CREATE", "T5", "Task Five", "TODO"],
# #             ["TASK_CREATE", "T2", "Task Two", "DONE"],
# #             ["TASK_CREATE", "T4", "Task Four", "IN_PROGRESS"],
# #             ["TASK_FILTER", "TODO"],
# #             ["TASK_FILTER", "IN_PROGRESS"],
# #             ["TASK_FILTER", "DONE"]
# #         ]
        
# #         expected = [
# #             "created T3",
# #             "created T1",
# #             "created T5",
# #             "created T2",
# #             "created T4",
# #             "found [T3, T5]",           # TODO tasks sorted by task_id
# #             "found [T1, T4]",            # IN_PROGRESS tasks sorted by task_id
# #             "found [T2]"                 # DONE tasks
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_filter_empty(self):
# #         """Test filtering when no tasks match"""
# #         commands = [
# #             ["TASK_CREATE", "T1", "Only TODO", "TODO"],
# #             ["TASK_FILTER", "DONE"]
# #         ]
        
# #         expected = [
# #             "created T1",
# #             "found []"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)
    
# #     def test_level2_backward_compatibility(self):
# #         """Test that Level 1 operations still work"""
# #         commands = [
# #             ["TASK_CREATE", "T1", "Task", "TODO"],
# #             ["TASK_UPDATE", "T1", "Updated Task"],
# #             ["TASK_GET", "T1"],
# #             ["TASK_DELETE", "T1"],
# #             ["TASK_GET", "T1"]
# #         ]
        
# #         expected = [
# #             "created T1",
# #             "updated T1",
# #             "got T1 (TODO)",
# #             "deleted T1",
# #             "task not found"
# #         ]
        
# #         output = simulate_coding_framework(commands)
# #         self.assertEqual(output, expected)


# # if __name__ == '__main__':
# #     unittest.main()


# """
# LEVEL 3 - Priority & Advanced Search

# Test Cases for Priority System and Keyword Search
# """

# import unittest
# from sim import simulate_coding_framework

# class TestTaskManagementLevel3(unittest.TestCase):
    
#     # ========== LEVEL 3 TESTS ==========
    
#     def test_level3_create_with_priority(self):
#         """Test creating tasks with priority"""
#         commands = [
#             ["TASK_CREATE", "T1", "High priority task", "TODO", 1],
#             ["TASK_CREATE", "T2", "Medium priority", "IN_PROGRESS", 3],
#             ["TASK_CREATE", "T3", "Low priority", "TODO", 5],
#             ["TASK_GET", "T1"],
#             ["TASK_GET", "T2"]
#         ]
        
#         expected = [
#             "created T1",
#             "created T2",
#             "created T3",
#             "got T1 (TODO)",
#             "got T2 (IN_PROGRESS)"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_default_priority(self):
#         """Test default priority is 5"""
#         commands = [
#             ["TASK_CREATE", "T1", "Default priority", "TODO"],
#             ["TASK_TOP", 1]
#         ]
        
#         expected = [
#             "created T1",
#             "top 1 [T1]"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_set_priority(self):
#         """Test changing task priority"""
#         commands = [
#             ["TASK_CREATE", "T1", "Task", "TODO", 5],
#             ["TASK_SET_PRIORITY", "T1", 1],
#             ["TASK_TOP", 1]
#         ]
        
#         expected = [
#             "created T1",
#             "priority updated T1",
#             "top 1 [T1]"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_set_priority_nonexistent(self):
#         """Test setting priority on non-existent task"""
#         commands = [
#             ["TASK_SET_PRIORITY", "T99", 1]
#         ]
        
#         expected = [
#             "error: task not found"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_top_sorted_by_priority(self):
#         """Test TOP returns tasks sorted by priority, then task_id"""
#         commands = [
#             ["TASK_CREATE", "T5", "Priority 3", "TODO", 3],
#             ["TASK_CREATE", "T2", "Priority 1", "TODO", 1],
#             ["TASK_CREATE", "T4", "Priority 2", "TODO", 2],
#             ["TASK_CREATE", "T1", "Priority 1", "TODO", 1],
#             ["TASK_CREATE", "T3", "Priority 2", "TODO", 2],
#             ["TASK_TOP", 5]
#         ]
        
#         expected = [
#             "created T5",
#             "created T2",
#             "created T4",
#             "created T1",
#             "created T3",
#             "top 5 [T1, T2, T3, T4, T5]"  # Priority 1 first (T1, T2), then priority 2 (T3, T4), then priority 3 (T5)
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_top_n_less_than_total(self):
#         """Test TOP with n less than total tasks"""
#         commands = [
#             ["TASK_CREATE", "T1", "P1", "TODO", 1],
#             ["TASK_CREATE", "T2", "P2", "TODO", 2],
#             ["TASK_CREATE", "T3", "P3", "TODO", 3],
#             ["TASK_CREATE", "T4", "P1", "TODO", 1],
#             ["TASK_TOP", 3]
#         ]
        
#         expected = [
#             "created T1",
#             "created T2",
#             "created T3",
#             "created T4",
#             "top 3 [T1, T4, T2]"  # Top 3: two priority 1 tasks, one priority 2
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_search_by_keyword(self):
#         """Test searching tasks by keyword"""
#         commands = [
#             ["TASK_CREATE", "T1", "Implement login feature", "TODO", 1],
#             ["TASK_CREATE", "T2", "Write login tests", "TODO", 2],
#             ["TASK_CREATE", "T3", "Design dashboard", "TODO", 3],
#             ["TASK_CREATE", "T4", "Implement dashboard API", "TODO", 1],
#             ["TASK_SEARCH", "login"],
#             ["TASK_SEARCH", "dashboard"],
#             ["TASK_SEARCH", "Implement"]
#         ]
        
#         expected = [
#             "created T1",
#             "created T2",
#             "created T3",
#             "created T4",
#             "found [T1, T2]",           # Contains "login"
#             "found [T3, T4]",           # Contains "dashboard"
#             "found [T1, T4]"            # Contains "Implement" (case-sensitive)
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_search_no_results(self):
#         """Test search with no matching results"""
#         commands = [
#             ["TASK_CREATE", "T1", "Task one", "TODO", 1],
#             ["TASK_SEARCH", "nonexistent"]
#         ]
        
#         expected = [
#             "created T1",
#             "found []"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_search_case_sensitive(self):
#         """Test that search is case-sensitive"""
#         commands = [
#             ["TASK_CREATE", "T1", "Login Feature", "TODO", 1],
#             ["TASK_CREATE", "T2", "login tests", "TODO", 2],
#             ["TASK_SEARCH", "login"],
#             ["TASK_SEARCH", "Login"]
#         ]
        
#         expected = [
#             "created T1",
#             "created T2",
#             "found [T2]",      # Only lowercase "login"
#             "found [T1]"       # Only capitalized "Login"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_complex_scenario(self):
#         """Test complex scenario with all Level 3 features"""
#         commands = [
#             ["TASK_CREATE", "T1", "Implement authentication", "TODO", 1],
#             ["TASK_CREATE", "T2", "Write auth tests", "IN_PROGRESS", 2],
#             ["TASK_CREATE", "T3", "Deploy authentication", "TODO", 3],
#             ["TASK_SET_PRIORITY", "T3", 1],
#             ["TASK_TOP", 2],
#             ["TASK_SEARCH", "auth"],
#             ["TASK_SET_STATUS", "T1", "DONE"],
#             ["TASK_FILTER", "TODO"],
#             ["TASK_TOP", 5]
#         ]
        
#         expected = [
#             "created T1",
#             "created T2",
#             "created T3",
#             "priority updated T3",
#             "top 2 [T1, T3]",                    # Both priority 1, sorted by task_id
#             "found [T1, T2, T3]",                # All contain "auth" substring
#             "status updated T1",
#             "found [T3]",                        # Only T3 is TODO now
#             "top 5 [T1, T3, T2]"                 # All tasks by priority
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)
    
#     def test_level3_backward_compatibility(self):
#         """Test that Level 1 and 2 operations still work"""
#         commands = [
#             ["TASK_CREATE", "T1", "Task"],       # Default status=TODO, priority=5
#             ["TASK_GET", "T1"],
#             ["TASK_SET_STATUS", "T1", "DONE"],
#             ["TASK_UPDATE", "T1", "Updated Task"],
#             ["TASK_FILTER", "DONE"],
#             ["TASK_DELETE", "T1"]
#         ]
        
#         expected = [
#             "created T1",
#             "got T1 (TODO)",
#             "status updated T1",
#             "updated T1",
#             "found [T1]",
#             "deleted T1"
#         ]
        
#         output = simulate_coding_framework(commands)
#         self.assertEqual(output, expected)


# if __name__ == '__main__':
#     unittest.main()


"""
LEVEL 4 - Time Travel & History

Test Cases for Timestamp-based Operations and History Tracking
"""

import unittest
from sim import simulate_coding_framework

class TestTaskManagementLevel4(unittest.TestCase):
    
    # ========== LEVEL 4 TESTS ==========
    
    def test_level4_create_at(self):
        """Test creating tasks with timestamps"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "First task", "TODO", 1],
            ["TASK_CREATE_AT", "2024-01-01T11:00:00", "T2", "Second task", "IN_PROGRESS", 2],
            ["TASK_GET", "T1"],
            ["TASK_GET", "T2"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "created T2 at 2024-01-01T11:00:00",
            "got T1 (TODO)",
            "got T2 (IN_PROGRESS)"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_set_status_at(self):
        """Test changing status with timestamps"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "Task", "TODO", 1],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SET_STATUS_AT", "2024-01-01T12:00:00", "T1", "DONE"],
            ["TASK_GET", "T1"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "status updated T1 at 2024-01-01T12:00:00",
            "got T1 (DONE)"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_snapshot_single_task(self):
        """Test snapshot with single task"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "Task", "TODO", 1],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SNAPSHOT", "2024-01-01T10:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T11:30:00"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "snapshot at 2024-01-01T10:30:00: [T1 (TODO)]",      # Before status change
            "snapshot at 2024-01-01T11:30:00: [T1 (IN_PROGRESS)]" # After status change
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_snapshot_multiple_tasks(self):
        """Test snapshot with multiple tasks at different times"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T09:00:00", "T1", "First", "TODO", 1],
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T2", "Second", "TODO", 2],
            ["TASK_CREATE_AT", "2024-01-01T11:00:00", "T3", "Third", "TODO", 3],
            ["TASK_SNAPSHOT", "2024-01-01T08:00:00"],
            ["TASK_SNAPSHOT", "2024-01-01T09:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T10:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T12:00:00"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T09:00:00",
            "created T2 at 2024-01-01T10:00:00",
            "created T3 at 2024-01-01T11:00:00",
            "snapshot at 2024-01-01T08:00:00: []",                           # Before any tasks
            "snapshot at 2024-01-01T09:30:00: [T1 (TODO)]",                  # Only T1 exists
            "snapshot at 2024-01-01T10:30:00: [T1 (TODO), T2 (TODO)]",       # T1 and T2 exist
            "snapshot at 2024-01-01T12:00:00: [T1 (TODO), T2 (TODO), T3 (TODO)]" # All exist
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_snapshot_with_updates(self):
        """Test snapshot showing state changes over time"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "Task", "TODO", 1],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SET_STATUS_AT", "2024-01-01T12:00:00", "T1", "DONE"],
            ["TASK_SNAPSHOT", "2024-01-01T10:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T11:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T12:30:00"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "status updated T1 at 2024-01-01T12:00:00",
            "snapshot at 2024-01-01T10:30:00: [T1 (TODO)]",
            "snapshot at 2024-01-01T11:30:00: [T1 (IN_PROGRESS)]",
            "snapshot at 2024-01-01T12:30:00: [T1 (DONE)]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_history_single_task(self):
        """Test history tracking for a single task"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "Implement feature", "TODO", 1],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SET_STATUS_AT", "2024-01-01T12:00:00", "T1", "DONE"],
            ["TASK_HISTORY", "T1"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "status updated T1 at 2024-01-01T12:00:00",
            "history T1: [2024-01-01T10:00:00 created, 2024-01-01T11:00:00 status->IN_PROGRESS, 2024-01-01T12:00:00 status->DONE]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_history_nonexistent(self):
        """Test history for non-existent task"""
        commands = [
            ["TASK_HISTORY", "T99"]
        ]
        
        expected = [
            "error: task not found"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_history_multiple_changes(self):
        """Test history with multiple types of changes"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T1", "Task", "TODO", 1],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SET_PRIORITY_AT", "2024-01-01T12:00:00", "T1", 2],
            ["TASK_SET_STATUS_AT", "2024-01-01T13:00:00", "T1", "DONE"],
            ["TASK_HISTORY", "T1"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "priority updated T1 at 2024-01-01T12:00:00",
            "status updated T1 at 2024-01-01T13:00:00",
            "history T1: [2024-01-01T10:00:00 created, 2024-01-01T11:00:00 status->IN_PROGRESS, 2024-01-01T12:00:00 priority->2, 2024-01-01T13:00:00 status->DONE]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_complex_scenario(self):
        """Test complex scenario with multiple tasks and time travel"""
        commands = [
            ["TASK_CREATE_AT", "2024-01-01T09:00:00", "T1", "First", "TODO", 1],
            ["TASK_CREATE_AT", "2024-01-01T10:00:00", "T2", "Second", "TODO", 2],
            ["TASK_SET_STATUS_AT", "2024-01-01T11:00:00", "T1", "IN_PROGRESS"],
            ["TASK_SET_STATUS_AT", "2024-01-01T12:00:00", "T2", "IN_PROGRESS"],
            ["TASK_SNAPSHOT", "2024-01-01T09:30:00"],
            ["TASK_SNAPSHOT", "2024-01-01T11:30:00"],
            ["TASK_HISTORY", "T1"],
            ["TASK_HISTORY", "T2"]
        ]
        
        expected = [
            "created T1 at 2024-01-01T09:00:00",
            "created T2 at 2024-01-01T10:00:00",
            "status updated T1 at 2024-01-01T11:00:00",
            "status updated T2 at 2024-01-01T12:00:00",
            "snapshot at 2024-01-01T09:30:00: [T1 (TODO)]",
            "snapshot at 2024-01-01T11:30:00: [T1 (IN_PROGRESS), T2 (TODO)]",
            "history T1: [2024-01-01T09:00:00 created, 2024-01-01T11:00:00 status->IN_PROGRESS]",
            "history T2: [2024-01-01T10:00:00 created, 2024-01-01T12:00:00 status->IN_PROGRESS]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)
    
    def test_level4_backward_compatibility(self):
        """Test that non-timestamped operations still work"""
        commands = [
            ["TASK_CREATE", "T1", "Task", "TODO", 1],
            ["TASK_GET", "T1"],
            ["TASK_SET_STATUS", "T1", "DONE"],
            ["TASK_FILTER", "DONE"],
            ["TASK_TOP", 1]
        ]
        
        expected = [
            "created T1",
            "got T1 (TODO)",
            "status updated T1",
            "found [T1]",
            "top 1 [T1]"
        ]
        
        output = simulate_coding_framework(commands)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
