###----------------------- BruteFoce Solution ----------------
class WordFilter:
    def __init__(self, words: List[str]):
        self.words = words
    def f(self, pref: str, suff: str) -> int:
        for i in range(len(self.words)-1, -1, -1):
            if self.words[i].startswith(pref) and self.words[i].endswith(suff):
                return i
        return -1
### --------------------- Trie Solution ------------------------

class TrieNode:
  def __init__(self):
      self.children = {}  # Maps character -> TrieNode (children nodes)
      self.index = -1     # Stores the largest word index that passes through this node

class WordFilter:
  def __init__(self, words: List[str]):
      self.root = TrieNode()  # Create the root of our Trie

      # Process each word with its index
      for index, word in enumerate(words):
          # Generate all possible suffixes of the word
          # For "apple": generates "", "e", "le", "ple", "pple", "apple"
          for i in range(len(word) + 1):
              suffix = word[i:]  # Get suffix starting from position i to end

              # Create the key: suffix + separator + full word
              # Example: for "apple" with suffix "le" -> "le#apple"
              key = suffix + '#' + word

              # Insert this key into the Trie
              cur = self.root  # Start at root node

              # Traverse/create path for each character in the key
              for c in key:
                  # If this character path doesn't exist, create a new node
                  if c not in cur.children:
                      cur.children[c] = TrieNode()

                  # Move to the child node for this character
                  cur = cur.children[c]

                  # Update the index at this node
                  # If multiple words share this path, keep the largest index
                  cur.index = index

  def f(self, pref: str, suff: str) -> int:
      # Search for: suffix + '#' + prefix
      # This will find words that END with suff and START with pref
      search_key = suff + '#' + pref

      cur = self.root  # Start at root

      # Traverse the Trie following the search key
      for c in search_key:
          # If path doesn't exist, no matching word found
          if c not in cur.children:
              return -1
          # Move to next node
          cur = cur.children[c]

      # Return the index stored at the final node
      # This is the largest index of words matching our criteria
      return cur.index
