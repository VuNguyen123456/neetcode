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
from datetime import datetime, timedelta

def to_dt(timestamp):
    return datetime.fromisoformat(timestamp)

rooms = {} # dic of dic
time_mark = {} # Dis of rooms state
guests = {}

def ADD_ROOM(room_id, capacity):
    if room_id in rooms:
        raise RuntimeError()
    rooms[room_id] = {"capacity": capacity, "booked": False, "guest": None, "booked_at": [], "durations": []}

def GET_ROOM(room_id):
    if not rooms.get(room_id):
        return None
    return rooms[room_id]["capacity"]

def BOOK_ROOM(room_id, guest_name):
    if not rooms.get(room_id) or rooms[room_id]["booked"] == True:
        raise RuntimeError()
    rooms[room_id]["booked"] = True
    rooms[room_id]["guest"] = guest_name
    if not guests.get(guest_name):
        guests[guest_name] = [room_id]
    else:
        guests[guest_name].append(room_id)

def CHECKOUT(room_id):
    if not rooms.get(room_id) or rooms[room_id]["booked"] == False:
        raise RuntimeError()
    rooms[room_id]["booked"] = False

def FIND_AVAILABLE(capacity):
    # for x in y => x is the key not the object since it's a dictionary
    good_room = [room for room in rooms if rooms[room]["capacity"] >= capacity and rooms[room]["booked"] == False]

    good_room.sort(key=lambda x:(rooms[x]["capacity"], x))

    top5 = good_room[:5]
    res = ", ".join(top5)
    return f"available [{res}]"

def GUEST_HISTORY(guest_name):
    history = guests[guest_name][::-1] if guests.get(guest_name) else []
    res = ", ".join(history)
    return f"history [{res}]"
# -------------------------------------------------------------------------------------------------------
def BOOK_ROOM_AT(timestamp, room_id, guest_name, duration):
    if not rooms.get(room_id):
        raise RuntimeError()
    # check overlap logic
    for i in range(len(rooms[room_id]["booked_at"])): # each start time
        
        start1 = to_dt(rooms[room_id]["booked_at"][i])
        end1 = start1 + timedelta(seconds=rooms[room_id]["durations"][i])
        start2 = to_dt(timestamp)
        end2 = start2 + timedelta(seconds=duration)

        # (start1 > start2 and end1 > end2) => 
        if end1 > start2 and end2 > start1:
            raise RuntimeError()
    # rooms[room_id]["booked"] = True
    rooms[room_id]["guest"] = guest_name
    rooms[room_id]["durations"].append(duration)
    rooms[room_id]["booked_at"].append(timestamp)
    if not guests.get(guest_name):
        guests[guest_name] = [room_id]
    else:
        guests[guest_name].append(room_id)
    time_mark[timestamp] = copy.deepcopy(rooms)

def CHECKOUT_AT(timestamp, room_id):
    if not rooms.get(room_id):
        raise RuntimeError()
    booking_exist = False
    checkedout = 0
    # Check if the room is booked at that time
    for i in range(len(rooms[room_id]["booked_at"])):
        start = to_dt(rooms[room_id]["booked_at"][i])
        end = start + timedelta(seconds=rooms[room_id]["durations"][i])
        if start < to_dt(timestamp) < end: # they should be booked
            booking_exist = True
            checkedout = i
    if booking_exist == False:
        raise RuntimeError()
    rooms[room_id]["booked_at"].pop(checkedout)
    rooms[room_id]["durations"].pop(checkedout)
    time_mark[timestamp] = copy.deepcopy(rooms)

def FIND_AVAILABLE_AT(timestamp, capacity):
    # Check to see if overlap? and add all fit room in
    good_rooms = []
    for room_id in rooms:
        is_available = True
        if rooms[room_id]["capacity"] < capacity:
            continue
        # Go through time
        for i in range(len(rooms[room_id]["booked_at"])):
            start = to_dt(rooms[room_id]["booked_at"][i])
            end = start + timedelta(seconds=rooms[room_id]["durations"][i])
            if start < to_dt(timestamp) < end: # overlapped and cannot
                is_available = False # Not available room
                break
        if is_available:
            good_rooms.append(room_id)
    
    good_rooms.sort(key=lambda x: (rooms[x]["capacity"], x))
    top5 = good_rooms[:5]
    res = ", ".join(top5)
    return f"available [{res}]"
                
def ROLLBACK(timestamp):
    global rooms
    rooms = copy.deepcopy(time_mark[timestamp])

def GET_REVENUE(start_timestamp, end_timestamp):
    rev = 0
    for room_id in rooms:
        for i in range(len(rooms[room_id]["booked_at"])):
            room_start = to_dt(rooms[room_id]["booked_at"][i])
            if to_dt(start_timestamp) <= room_start <= to_dt(end_timestamp):
                rev += rooms[room_id]["capacity"] * rooms[room_id]["durations"][i]
    return f"revenue [{rev}]"


# https://github.com/EricZheng0404/LibreSignal/blob/main/Questions/bank_system/level1.md




