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
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        res = n # Assume all node is 1 island and not connected
        # Will go through the island and union each edge if the edge not not already union mean that the 2 island became 1 island
        # Reduse the total amount of island
        for e in edges:
            if uf.union(e[0], e[1]): # If the 2 can be union means that they are not connected before and you can reduce total island present
                res -= 1
            # If they can't then because they already union
        return res
