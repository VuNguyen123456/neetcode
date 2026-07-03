import math
from datetime import datetime, timedelta
import copy

class Storage:
    def __init__(self):
        self.file_sys = {}
        self.users = {}
        self.history = {}
        
    def ADD_FILE(self, name, size):
        if name in self.file_sys:
            return "false"
        self.file_sys[name] = {"size": size, "userId": "admin"}
        return "true"

    def GET_FILE_SIZE(self, name):
        if name not in self.file_sys:
            return ""
        return self.file_sys[name]["size"]
    
    def DELETE_FILE(self, name):
        if name not in self.file_sys:
            return ""
        del_size = self.GET_FILE_SIZE(name)
        self.file_sys.pop(name)
        return del_size
    
    def GET_N_LARGEST(self, prefix, n):
        matches = [file for file in self.file_sys if file.startswith(prefix)]
        matches.sort(key=lambda x:(-int(self.file_sys[x]["size"]), x))
        topN = matches[:int(n)]
        res = []
        for f in topN:
            res.append(f"{f}({self.file_sys[f]['size']})")
        return ", ".join(res)
    
    def ADD_USER(self, userId, capacity):
        if userId in self.users:
            return "false"
        self.users[userId] = {"capacity": int(capacity), "current_size": 0, "files_num": 0}
        return "true"
    
    def ADD_FILE_BY(self, userId, name, size):
        size = int(size)
        if userId not in self.users or name in self.file_sys:
            return ""
        # If no more space
        if self.users[userId]["capacity"] < self.users[userId]["current_size"] + size:
            return ""
        self.users[userId]["current_size"] += size
        self.users[userId]["files_num"] += 1
        self.file_sys[name] = {"size": size, "userId": userId}
        remain = self.users[userId]["capacity"] - self.users[userId]["current_size"]
        return f"{remain}"
    
    def MERGE_USER(self, userId1, userId2):
        if userId1 == userId2 or userId1 not in self.users or userId2 not in self.users:
            return ""
        
        # Transfer all file of 2 to 1
        for file in self.file_sys:
            if self.file_sys[file]["userId"] == userId2:
                self.file_sys[file]["userId"] = userId1
        # Add capacity too
        self.users[userId1]["capacity"] += self.users[userId2]["capacity"]
        self.users[userId1]["current_size"] += self.users[userId2]["current_size"]
        self.users[userId1]["files_num"] += self.users[userId2]["files_num"]
        self.users.pop(userId2)
        remain = self.users[userId1]["capacity"] - self.users[userId1]["current_size"]
        return str(remain)

    def BACKUP_USER(self, userId):
        if userId not in self.users:
            return ""
        # Back up the files with user id
        user_files = {}
        for file, data in self.file_sys.items():
            if data["userId"] == userId:
                user_files[file] = data
        self.history[userId] = copy.deepcopy(user_files) # the files with user id that got saved
        return str(len(user_files))
    
    def RESTORE_USER(self, userId):
        if userId not in self.users:
            return ""
        # delete current files
        to_delete = [f for f in self.file_sys if self.file_sys[f]["userId"] == userId]
        for f in to_delete:
            self.file_sys.pop(f)
        # restore the back up files
        restored = 0
        backup = self.history.get(userId, {})
        new_size = 0
        for file, data in backup.items():
            if file not in self.file_sys:
                self.file_sys[file] = {"size": data["size"], "userId": userId}
                new_size += data["size"]
                restored += 1
        self.users[userId]["current_size"] = new_size
        return str(restored)
