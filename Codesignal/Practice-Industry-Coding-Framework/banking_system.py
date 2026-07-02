import math
from datetime import datetime, timedelta

def to_dt(timestamp):
    return datetime.fromisoformat(timestamp)

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.payments = {}
        self.accountsBalanceHistory = {} #=> {acc: {time: balance}}
        self.payment_time = 0

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = {"created_at": timestamp, "balance": 0, "total_outgoing_amount": 0}
        self.accountsBalanceHistory[account_id] = {timestamp: 0} 
        return True
    
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        self.cashback(timestamp, account_id)
        self.accounts[account_id]["balance"] += amount
        self.accountsBalanceHistory[account_id][timestamp] = self.accounts[account_id]["balance"]
        return self.accounts[account_id]["balance"]
    
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        if source_account_id not in self.accounts or target_account_id not in self.accounts or target_account_id == source_account_id or self.accounts[source_account_id]["balance"] < amount:
            return None
        self.cashback(timestamp, source_account_id)
        self.accounts[source_account_id]["balance"] -= amount
        self.accounts[target_account_id]["balance"] += amount
        self.accounts[source_account_id]["total_outgoing_amount"] += amount

        self.accountsBalanceHistory[source_account_id][timestamp] = self.accounts[source_account_id]["balance"]
        self.accountsBalanceHistory[target_account_id][timestamp] = self.accounts[target_account_id]["balance"]

        return self.accounts[source_account_id]["balance"]
    
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        all_acc = [acc for acc in self.accounts]
        all_acc.sort(key=lambda x: (-self.accounts[x]["total_outgoing_amount"], x))
        topN = all_acc[:n]
        res = []
        for acc in topN:
            total = self.accounts[acc]["total_outgoing_amount"]
            res.append(f"{acc}({total})")
        return res

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        if account_id not in self.accounts or self.accounts[account_id]["balance"] < amount:
            return None
        self.cashback(timestamp, account_id)
        self.accounts[account_id]["balance"] -= amount
        self.accounts[account_id]["total_outgoing_amount"] += amount
        self.accountsBalanceHistory[account_id][timestamp] = self.accounts[account_id]["balance"]

        res = self.get_payment_str()
        self.payments[res] = {"status": "IN_PROGRESS", "at": timestamp, "by": account_id, "cb": math.floor(amount * 0.02)}
        return res

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        if account_id not in self.accounts or payment not in self.payments or self.payments[payment]["by"] != account_id:
            return None
        self.cashback(timestamp, account_id)
        return self.payments[payment]["status"]

    def cashback(self, timestamp: int, account_id: str):
        for pay in self.payments:
            if self.payments[pay]["by"] == account_id and self.payments[pay]["status"] != "CASHBACK_RECEIVED":
                if timestamp >= self.payments[pay]["at"] + 86400000:
                    self.accounts[account_id]["balance"] += self.payments[pay]["cb"]
                    self.payments[pay]["status"] = "CASHBACK_RECEIVED"
        self.accountsBalanceHistory[account_id][timestamp] = self.accounts[account_id]["balance"]


    def get_payment_str(self):
        self.payment_time += 1
        return f"payment{self.payment_time}"

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        if account_id_1 == account_id_2 or account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False
        # Payment status transfer
        for pay in self.payments:
            if self.payments[pay]["by"] == account_id_2:
                self.payments[pay]["by"] = account_id_1
        # Money transfer
        self.accounts[account_id_1]["balance"] += self.accounts[account_id_2]["balance"]
        self.accountsBalanceHistory[account_id_1][timestamp] = self.accounts[account_id_1]["balance"] # Need to inheritate balance history somehow
        self.accountsBalanceHistory[account_id_1].update(self.accountsBalanceHistory[account_id_2])
        # Total transaction amount too
        self.accounts[account_id_1]["total_outgoing_amount"] += self.accounts[account_id_2]["total_outgoing_amount"]
        self.accounts.pop(account_id_2)
        self.accountsBalanceHistory.pop(account_id_2)

        self.cashback(timestamp, account_id_1)
        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        if account_id not in self.accountsBalanceHistory:
            return None
        # find latest history entry at or before time_at
        history = self.accountsBalanceHistory[account_id]
        valid_times = [t for t in history if t <= time_at]
        if not valid_times:
            return None
        return history[max(valid_times)]
