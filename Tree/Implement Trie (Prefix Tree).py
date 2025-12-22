class TrieNode:
    def __init__(self):
        self.children = {}
        self.endOfWord = False

class PrefixTree:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        cur = self.root
        for i in word:
            if i in cur.children:
                cur = cur.children[i]
            else:
                cur.children[i] = TrieNode()
                cur = cur.children[i]
        cur.endOfWord = True

            # if i not in cur.children:
            #     cur.children[i] = TrieNode()
            # cur = cur.children[c]

    def search(self, word: str) -> bool:
        cur = self.root
        for i in word:
            if i in cur.children:
                cur = cur.children[i]
            else:
                return False
        return cur.endOfWord

    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for i in prefix:
            if i in cur.children:
                cur = cur.children[i]
            else:
                return False
        return True
        
        
