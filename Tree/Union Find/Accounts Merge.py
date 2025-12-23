class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.rank = [1] * n

    def find(self, x):
        if x != self.par[x]:
            self.par[x] = self.find(self.par[x])  # Path compression
        return self.par[x]

    def union(self, x1, x2):
        p1, p2 = self.find(x1), self.find(x2)
        if p1 == p2:
            return False
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
            self.rank[p1] += self.rank[p2]
        else:
            self.par[p1] = p2
            self.rank[p2] += self.rank[p1]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        emailToAcc = {} # Map each email to it corresponsding account index (include repeted one)
        for i, a in enumerate(accounts):
            for e in a[1:]: 
                # If this is a repeated email we will union these 2 index together 
                # (it basically mean these 2 index are the same and so email with this 2 index will belong to same owner and onl 1 parent will show up in merged set) 
                # so that they can belong to the same index after the solve this
                if e in emailToAcc:
                    uf.union(i, emailToAcc[e])
                else: # Just add in dic
                    emailToAcc[e] = i
        
        emailGroup = defaultdict(list) # index: all email (no repeated because only the index leader will count)
        for e, i in emailToAcc.items(): # For each email (key) and index (value) of this dictionary
            leader = uf.find(i) # Find the index leader (root parent if there are repeated email and decided to merge)
            #Able to determine who's the leader due to the union of index above
            emailGroup[leader].append(e) # Append all the email that belong to same highest parent into 1 leader index
        
        res = []
        for i, emails in emailGroup.items():
            name = accounts[i][0]
            res.append([name] + sorted(emails))
        return res
