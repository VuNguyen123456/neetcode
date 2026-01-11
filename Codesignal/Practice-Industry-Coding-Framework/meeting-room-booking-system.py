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

roomDic = {}
bookDic = {}
results = []
booking_counter = 1  # Global variable


def ROOM_CREATE(room_id, capacity):
    if room_id in roomDic:
        results.append(f"room already existed")
        return None
    roomDic[room_id] = {'capacity': capacity}
    results.append(f"created room {room_id}")  # Not "{room_id} created"


def BOOK(room_id, start_time, end_time, meeting_name):
    global booking_counter
    if room_id not in roomDic:  # Room doesn't exist
        results.append("error: room not found")
        return
    
    overlapped = False
    for book in bookDic:
        if bookDic[book]['room_id'] == room_id:
            # Overlap logic => Draw out to see the thing
            s1 = datetime.fromisoformat(bookDic[book]['start_time'])
            e1 = datetime.fromisoformat(bookDic[book]['start_time'])
            s2 = datetime.fromisoformat(start_time)
            e2 = datetime.fromisoformat(end_time)
            if s1 < e2 and s2 < e1:
                overlapped = True
                break
    if overlapped:
        results.append("Cannot double book")
        return None
    booking_counter += 1
    booking_id = booking_counter
    bookDic[booking_id] = {
        'room_id' : room_id,
        'start_time' : start_time,
        'end_time' : end_time,
        'meeting_name' : meeting_name
    }
    results.append(f"booked {booking_id}")     # Not "Booked"
    return booking_id

def CANCEL(booking_id):
    if booking_id not in bookDic:
        results.append(f"no booking found")
        return None
    del bookDic[booking_id]
    results.append(f"del booking {booking_id}")

def GET_BOOKING(booking_id):
    if booking_id not in bookDic:
        results.append(f"no booking found")
        return None
    results.append(f"booking detail {bookDic[booking_id]}")

# def ROOM_AVAILABLE(start_time, end_time):
#     avai_room = set()
#     for book in bookDic:
#         # Overlap logic => Draw out to see the thing
#         s1 = datetime.fromisoformat(bookDic[book]['start_time'])
#         e1 = datetime.fromisoformat(bookDic[book]['start_time'])
#         s2 = datetime.fromisoformat(start_time)
#         e2 = datetime.fromisoformat(end_time)
#         if s1 < e2 and s2 < e1:
#             avai_room.append(bookDic[book]['room_id'])
#     for room in roomDic:
#         avai_room.append(room)
#     results.append(f"room available are: {avai_room}")

def ROOM_AVAILABLE(start_time, end_time, min_capacity = 0):
    avai_room = set()
    for book in bookDic:
        if roomDic[bookDic[book]['room_id']]['capacity'] >= min_capacity:
            # Overlap logic => Draw out to see the thing
            s1 = datetime.fromisoformat(bookDic[book]['start_time'])
            e1 = datetime.fromisoformat(bookDic[book]['start_time'])
            s2 = datetime.fromisoformat(start_time)
            e2 = datetime.fromisoformat(end_time)
            if s1 < e2 and s2 < e1:
                avai_room.append(bookDic[book]['room_id'])
    for room in roomDic:
        if roomDic[room]['capacity'] >= min_capacity:
            avai_room.append(room)
    results.append(f"room available are: {avai_room}")

def ROOM_SCHEDULE(room_id, date):
    if room_id not in roomDic:
        results.append(f"no room")
        return None
    all_bookings = []
    for book in bookDic:
        if bookDic[book]['room_id'] == room_id:
            sd = bookDic[book]['start_time'].date()
            ed = bookDic[book]['end_time'].date()
            if date == sd or date == ed:
                all_bookings.append(book)
    
    if not all_bookings:
        results.append(f"no room schedule")
    else:
        results.append(f"room schedule: [{all_bookings}]")

def MY_BOOKINGS(user_id): # Where does this user_id came from???
    all_bookings = []
    for book in bookDic:
        if bookDic[book]['user_id'] == user_id:
            all_bookings.append(book)
    if not all_bookings:
        results.append(f"no user schedule")
    else:
        results.append(f"user schedule: [{all_bookings}]")

def simulate_coding_framework(list_of_lists):
    global dic, results, tsdic
    dic = {}
    results = []
    tsdic = {}
    
    for command in list_of_lists:
        operation = command[0]
        if operation == "ROOM_CREATE":
            ROOM_CREATE(command[1], command[2])
        elif operation == "BOOK":
            BOOK(command[1], command[2], command[3], command[4])
        elif operation == "CANCEL":
            CANCEL(command[1])
        elif operation == "GET_BOOKING":
            GET_BOOKING(command[1])
        
    return results
