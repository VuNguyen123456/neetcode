class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur =  cur.children[c]
        cur.isEnd = True

    def search(self, word: str) -> bool:
        # Going to be recursive:
        def dfs(j, root):
            cur = root
            for i in range(j, len(word)):
                c = word[i]
                if c == ".": # Protentially match 26 diff char becase . can represent all of them
                # Use backtracking/recursion
                    for child in cur.children.values():
                        if dfs(i + 1, child): # j is index parameter, the other is the node we passed in
                            return True
                    return False
                else:
                    if c not in cur.children:
                        return False
                    cur =  cur.children[c]
            return cur.isEnd

        return dfs(0, self.root)
