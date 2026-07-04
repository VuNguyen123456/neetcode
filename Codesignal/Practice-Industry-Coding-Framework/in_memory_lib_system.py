import math
from datetime import datetime, timedelta
import copy

class InMemoryLibrarySystem:
    def __init__(self):
        self.lib = {}
        self.users = {}
        self.history = {}
    
    def ADD_BOOK(self, book_id, title, copies):
        if book_id in self.lib:
            return "false"
        self.lib[book_id] = {"title": title, "copies": int(copies), "total_borrow_count": 0}
        return "true"

    def BORROW_BOOK(self, book_id):
        if book_id not in self.lib or self.lib[book_id]["copies"] <= 0:
            return "false"
        self.lib[book_id]["copies"] -= 1
        self.lib[book_id]["total_borrow_count"] += 1
        return "true"

    def RETURN_BOOK(self, book_id):
        if book_id not in self.lib:
            return "false"
        self.lib[book_id]["copies"] += 1
        return "true"
    
    def GET_COPIES(self, book_id):
        if book_id not in self.lib:
            return ""
        return str(self.lib[book_id]["copies"])
    
    def ADD_USER(self, user_id, borrow_limit):
        if user_id in self.users:
            return "false"
        self.users[user_id] = {"borrow_limit": int(borrow_limit), "current_borrow_num": 0, "current_borrow_book":{}, "all_time_borrow": 0}
        return "true"
    
    def BORROW_BOOK_BY(self, user_id, book_id):
        if book_id not in self.lib or user_id not in self.users or self.lib[book_id]["copies"] <= 0 or self.users[user_id]["borrow_limit"] == self.users[user_id]["current_borrow_num"]:
            return ""
        
        self.lib[book_id]["total_borrow_count"] += 1

        self.lib[book_id]["copies"] -= 1
        self.users[user_id]["current_borrow_num"] += 1
        self.users[user_id]["all_time_borrow"] += 1
        self.users[user_id]["current_borrow_book"][book_id] = {"borrowed_at": None, "return_at": None}

        return str(self.users[user_id]["borrow_limit"] - self.users[user_id]["current_borrow_num"])

    def GET_TOP_BORROWED(self, n):
        all_books = [b for b in self.lib]
        all_books.sort(key=lambda x : (-self.lib[x]["total_borrow_count"],x))
        topN = all_books[:int(n)]

        res = []
        for book in topN:
            res.append(f"{book}({self.lib[book]['total_borrow_count']})")

        return ", ".join(res)
#------------------------------------------------------------------------------------------------------------------------ USEEEEE DICCCCC NOT LIST
    def BORROW_BOOK_AT(self, timestamp, user_id, book_id, duration):
        self.process_expire(timestamp)
        if book_id not in self.lib or user_id not in self.users or self.lib[book_id]["copies"] <= 0 or self.users[user_id]["borrow_limit"] == self.users[user_id]["current_borrow_num"]:
            return ""
        self.lib[book_id]["total_borrow_count"] += 1

        self.lib[book_id]["copies"] -= 1
        self.users[user_id]["current_borrow_num"] += 1
        self.users[user_id]["all_time_borrow"] += 1
        self.users[user_id]["current_borrow_book"][book_id] = {"borrowed_at": int(timestamp), "return_at": int(timestamp) + int(duration)}

        return str(self.users[user_id]["borrow_limit"] - self.users[user_id]["current_borrow_num"])

    def RETURN_BOOK_AT(self, timestamp, user_id, book_id):
        if book_id not in self.users[user_id]["current_borrow_book"]:
            return "false"
        if self.is_expired(timestamp, user_id, book_id):
            return "already_returned"
        self.process_expire(timestamp)
        
        self.lib[book_id]["copies"] += 1
        self.users[user_id]["current_borrow_num"] -= 1
        self.users[user_id]["current_borrow_book"].pop(book_id)

        return "true"

    def is_expired(self, timestamp, user_id, book_id):
        if self.users[user_id]["current_borrow_book"][book_id]["return_at"] is None:
            return False
        if timestamp >= self.users[user_id]["current_borrow_book"][book_id]["return_at"]:
            return True
        return False
    
    def GET_COPIES_AT(self, timestamp, book_id):
        self.process_expire(timestamp)
        if book_id not in self.lib:
            return ""
        # the one that's still in 
        res = self.lib[book_id]["copies"]
        return str(res)
    
    def process_expire(self, timestamp):
        book_to_return = []
        for user_id in self.users:
            for book_id in self.users[user_id]["current_borrow_book"]:
                if self.is_expired(timestamp, user_id, book_id):
                    book_to_return.append((book_id, user_id))

        for book_id, user_id in book_to_return:
            self.lib[book_id]["copies"] += 1
            self.users[user_id]["current_borrow_num"] -= 1
            self.users[user_id]["current_borrow_book"].pop(book_id)

#--------------------------------------------------------
    def BACKUP(self, timestamp):
        self.process_expire(timestamp)
        self.history[timestamp] = {"lib":copy.deepcopy(self.lib), "users":copy.deepcopy(self.users)}
        res = 0
        for user_id in self.users:
            res += self.users[user_id]["current_borrow_num"]

        return str(res)
    
    def RESTORE(self, timestamp, restore_to_timestamp):
        all_ts_before = [int(ts) for ts in self.history if int(ts) <= restore_to_timestamp]
        restore_ts = max(all_ts_before)
        self.lib = copy.deepcopy(self.history[restore_ts]["lib"])
        self.users = copy.deepcopy(self.history[restore_ts]["users"])
        for user_id in self.users:
            for book_id in self.users[user_id]["current_borrow_book"]:
                if self.users[user_id]["current_borrow_book"][book_id]["return_at"] != None: # Recalc
                    old_return = int(self.users[user_id]["current_borrow_book"][book_id]["return_at"])
                    new_return =  int(timestamp) + (old_return - int(restore_ts))
                    self.users[user_id]["current_borrow_book"][book_id]["return_at"] = new_return
        return ""

    def GET_USER_STATS(self, user_id):   
        if user_id not in self.users:
            return ""
        return f"total_borrowed({self.users[user_id]['all_time_borrow']}), active({self.users[user_id]['current_borrow_num']})"
