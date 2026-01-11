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
from dateutil.relativedelta import relativedelta

roomDic = {}
bookDic = {}
results = []
booking_counter = 1  # Global variable
series_counter = 1


def ROOM_CREATE(room_id, capacity):
    if room_id in roomDic:
        results.append(f"room already existed")
        return None
    roomDic[room_id] = {'capacity': capacity}
    results.append(f"created room {room_id}")  # Not "{room_id} created"


def BOOK(room_id, start_time, end_time, meeting_name, user_id=None):
    global booking_counter
    if room_id not in roomDic:  # Room doesn't exist
        results.append("error: room not found")
        return
    
    overlapped = False
    for book in bookDic:
        if bookDic[book]['room_id'] == room_id:
            # Overlap logic => Draw out to see the thing
            s1 = datetime.fromisoformat(bookDic[book]['start_time'])
            e1 = datetime.fromisoformat(bookDic[book]['end_time'])
            s2 = datetime.fromisoformat(start_time)
            e2 = datetime.fromisoformat(end_time)
            if s1 < e2 and s2 < e1:
                overlapped = True
                break
    if overlapped:
        results.append("Cannot double book")
        return None
    booking_counter += 1
    booking_id = f"B{booking_counter:03d}"

    bookDic[booking_id] = {
        'room_id' : room_id,
        'start_time' : start_time,
        'end_time' : end_time,
        'meeting_name' : meeting_name,
        'user_id': user_id
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
    # Step 1: Add ALL rooms meeting capacity
    avai_room = set()
    for room in roomDic:
        if roomDic[room]['capacity'] >= min_capacity:
            avai_room.add(room)

    # Step 2: REMOVE rooms with conflicts
    s2 = datetime.fromisoformat(start_time)
    e2 = datetime.fromisoformat(end_time)
    for book in bookDic:
        # Overlap logic => Draw out to see the thing
        s1 = datetime.fromisoformat(bookDic[book]['start_time'])
        e1 = datetime.fromisoformat(bookDic[book]['end_time'])
        if (s1 < e2 and s2 < e1):
            # avai_room.remove(bookDic[book]['room_id'])
            avai_room.discard(bookDic[book]['room_id']) # (silent, no error)

    
    sorted_rooms = sorted(avai_room)
    result = ", ".join(sorted_rooms)
    results.append(f"available [{result}]")
    return sorted_rooms

def ROOM_SCHEDULE(room_id, date):
    if room_id not in roomDic:
        results.append(f"no room")
        return None
    all_bookings = []
    for book in bookDic:
        if bookDic[book]['room_id'] == room_id:
            sd = datetime.fromisoformat(bookDic[book]['start_time']).date()
            ed = datetime.fromisoformat(bookDic[book]['end_time']).date()
            if date == sd or date == ed:
                all_bookings.append(book)
    
    if not all_bookings:
        results.append(f"no room schedule")
    else:
        results.append(f"room schedule: [{all_bookings}]")

def MY_BOOKINGS(user_id): # Where does this user_id came from???
    all_bookings = []
    for book in bookDic:
        if bookDic[book].get('user_id') == user_id:
            all_bookings.append(book)
    if not all_bookings:
        results.append(f"no user schedule")
    else:
        results.append(f"user schedule: [{all_bookings}]")

def BOOK_RECURRING(room_id, start_time, end_time, meeting_name, pattern, until, user_id=None):
    global booking_counter
    global series_counter
    if room_id not in roomDic:  # Room doesn't exist
        results.append("error: room not found")
        return
    
    overlapped = False

    if pattern == "DAILY":
        delta = relativedelta(days=1)
    elif pattern == "WEEKLY":
        delta = relativedelta(weeks=1)  # Can use weeks!
    elif pattern == "MONTHLY":
        delta = relativedelta(months=1)  # Proper month handling!
    else:
        results.append("error: invalid pattern")
        return

    st = datetime.fromisoformat(start_time)
    et = datetime.fromisoformat(end_time)
    while et < datetime.fromisoformat(until):    
        for book in bookDic:
            if bookDic[book]['room_id'] == room_id:
                # Overlap logic => Draw out to see the thing
                s1 = datetime.fromisoformat(bookDic[book]['start_time'])
                e1 = datetime.fromisoformat(bookDic[book]['end_time'])
                s2 = st
                e2 = et
                if s1 < e2 and s2 < e1:
                    overlapped = True
                    break
        if overlapped:
            results.append("Cannot double book. So noo bkooking at all")
            return None
        st += delta
        et += delta

    series_counter += 1
    series_id = f"S{series_counter:03d}"
    st = datetime.fromisoformat(start_time)
    et = datetime.fromisoformat(end_time)
    while et < datetime.fromisoformat(until):
        booking_counter += 1
        booking_id = f"B{booking_counter:03d}"
        bookDic[booking_id] = {
            'room_id' : room_id,
            'start_time' : st.isoformat(),
            'end_time' : et.isoformat(),
            'meeting_name' : meeting_name,
            'user_id': user_id,
            'series_id': series_id,
            'pattern': pattern
        }
        st += delta
        et += delta
    results.append(f"booked recurring")

def isNewOverlappSchedule(booking_id, new_start_time, new_end_time):
    overlapped = False
    # Check every booking overlap with new time
    for book in bookDic:
        if book == booking_id:
            continue
        # Overlap logic => Draw out to see the thing
        s1 = datetime.fromisoformat(bookDic[book]['start_time'])
        e1 = datetime.fromisoformat(bookDic[book]['end_time'])
        s2 = datetime.fromisoformat(new_start_time)
        e2 = datetime.fromisoformat(new_end_time)
        if s1 < e2 and s2 < e1:
            overlapped = True
            break
    return overlapped

def isNewOverlappScheduleAll(new_start_time, new_end_time):
    overlapped = False
    # Check every booking overlap with new time
    for book in bookDic:
        # Overlap logic => Draw out to see the thing
        s1 = datetime.fromisoformat(bookDic[book]['start_time'])
        e1 = datetime.fromisoformat(bookDic[book]['end_time'])
        s2 = datetime.fromisoformat(new_start_time)
        e2 = datetime.fromisoformat(new_end_time)
        if s1 < e2 and s2 < e1:
            overlapped = True
            break
    return overlapped

def UPDATE_RECURRING(series_id, option, booking_id=None, new_start_time=None, new_end_time=None, new_name=None):    
    if option == "THIS":
        if booking_id not in bookDic:
            results.append("error: booking not found")
            return
        if 'series_id' not in bookDic[booking_id] or bookDic[booking_id]['series_id'] != series_id:
            results.append("error: booking not part of series")
            return
        if isNewOverlappSchedule(booking_id, new_start_time, new_end_time):
            results.append("Cannot double book")
            return
        else:
            bookDic[booking_id]['start_time'] = new_start_time
            bookDic[booking_id]['end_time'] = new_end_time
            if new_name is not None:
                bookDic[booking_id]['meeting_name'] = new_name
            results.append("updated this booking")
            return
    elif option == "FUTURE": # booking_id is the only booking that stay
        # Implement future booking update logic
        if booking_id not in bookDic:
            results.append("error: booking not found")
            return
        if 'series_id' not in bookDic[booking_id] or bookDic[booking_id]['series_id'] != series_id:
            results.append("error: booking not part of series")
            return
        target_start_time = datetime.fromisoformat(bookDic[booking_id]['start_time'])
        for book in bookDic:
            if 'series_id' in bookDic[book] and booking_id != book and bookDic[book]['series_id'] == series_id:
                if datetime.fromisoformat(bookDic[book]['start_time']) >= target_start_time:
                    if isNewOverlappSchedule(book, new_start_time, new_end_time):
                        results.append("Cannot double book")
                        return
        # If no overlap, proceed to update
        for book in bookDic:
            if 'series_id' in bookDic[book] and booking_id != book and bookDic[book]['series_id'] == series_id:
                if datetime.fromisoformat(bookDic[book]['start_time']) >= target_start_time:
                    bookDic[book]['start_time'] = new_start_time
                    bookDic[book]['end_time'] = new_end_time
                    if new_name is not None:
                        bookDic[book]['meeting_name'] = new_name
    elif option == "ALL":
        # Update all bookings in the series
        for book in bookDic:
            if 'series_id' in bookDic[book] and bookDic[book]['series_id'] == series_id:
                if isNewOverlappScheduleAll(book, new_start_time, new_end_time):
                    results.append("Cannot double book")
                    return
        
        for book in bookDic:
            if 'series_id' in bookDic[book] and bookDic[book]['series_id'] == series_id:
                bookDic[book]['start_time'] = new_start_time
                bookDic[book]['end_time'] = new_end_time
                if new_name is not None:
                    bookDic[book]['meeting_name'] = new_name
    else:
        results.append("error: invalid pattern")
        return

def CANCEL_RECURRING(series_id, option, booking_id=None):
    if option == "THIS":
        # Cancel only the specific booking
        for book in bookDic:
            if 'series_id' in bookDic[book] and bookDic[book]['series_id'] == series_id and book == booking_id:
                del bookDic[book]
                break
    elif option == "FUTURE":
        # Cancel all future bookings in the series
        # Cancel FUTURE
        target_start_time = datetime.fromisoformat(bookDic[booking_id]['start_time'])
        for book in list(bookDic.keys()):
            if 'series_id' in bookDic[book] and bookDic[book]['series_id'] == series_id:
                if datetime.fromisoformat(bookDic[book]['start_time']) >= target_start_time:
                    del bookDic[book]

    
    elif option == "ALL":
        # Cancel all bookings in the series
        for book in list(bookDic.keys()):
            if 'series_id' in bookDic[book] and bookDic[book]['series_id'] == series_id:
                del bookDic[book]
    else:
        results.append("error: invalid pattern")
        return

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
            if len(command) == 6:
                BOOK(command[1], command[2], command[3], command[4], command[5])
            else:
                BOOK(command[1], command[2], command[3], command[4], None)
        elif operation == "CANCEL":
            CANCEL(command[1])
        elif operation == "GET_BOOKING":
            GET_BOOKING(command[1])
        elif operation == "ROOM_AVAILABLE":
            if len(command) == 4:
                ROOM_AVAILABLE(command[1], command[2], command[3])
            else:
                ROOM_AVAILABLE(command[1], command[2], 0)
        elif operation == "ROOM_SCHEDULE":
            ROOM_SCHEDULE(command[1], command[2])
        elif operation == "MY_BOOKINGS":
            MY_BOOKINGS(command[1])
        elif operation == "BOOK_RECURRING":
            if len(command) == 7:
                BOOK_RECURRING(command[1], command[2], command[3], command[4], command[5], command[6], None)
            else:
                BOOK_RECURRING(command[1], command[2], command[3], command[4], command[5], command[6], command[7])
        elif operation == "UPDATE_RECURRING":
            if len(command) == 6:
                UPDATE_RECURRING(command[1], command[2], command[3], command[4], command[5])
            else:
                UPDATE_RECURRING(command[1], command[2])
        elif operation == "CANCEL_RECURRING":
            if len(command) == 3:
                CANCEL_RECURRING(command[1], command[2])
            else:
                CANCEL_RECURRING(command[1], command[2], command[3])
        
    return results
