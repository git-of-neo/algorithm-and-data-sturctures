"""
Python file for FIT2004 assignment 3
Author : Neo Shao Hong
Student ID : 31276520
"""

#%% Node class
BASE =  64

class Node:
    """
    Constructor for Node class

    Arguments:
        payload -> data to be stored at the node
        size -> number of children of the node

    Time: O(size)
    Aux. space: O(size)
    """
    def __init__(self, payload = None, size = 5):
        self.payload = payload
        self.children = [None]*size

#%% Question 1 
class SequenceDatabase:
    """
    Zero parameter constructor for SequenceDatabase

    Time: O(1)
    Aux. space: O(1)
    """
    def __init__(self):
        self.root = Node()

    """
    Store s into the database. Returns nothing.

    Arguments: 
        s -> string to be inserted into the database

    Time: O(n) where n is the length of s
    Aux. space: O(n) where n is the length of s
    """
    def addSequence(self, s):
        self.insert_aux(s, 0, self.root)
    
    """
    Searches the database for a string with the following properties:
    • It must have q as a prefix
    • It should have a higher frequency in the database than any other string with q as a
    prefix
    • If two or more strings with prefix q are tied for most frequent, return the lexicographically
    least of them
    
    Returns the string that matches the properties or None if unmatched.

    Arguments:
        q -> prefix string to match

    Time: O(n) where n is the length of q
    Aux. space: O(1)
    """
    def query(self, q):
        current = self.root
        for char in q:
            current = current.children[ord(char)-BASE]
            if current == None:
                return None
        if current.payload == None:
            return None
        return current.payload[1]

    """
    Recursively update the database based on string. Returns ((frequency of string, most frequent string), 
    boolean value indicating if a change due to lexicographical order has been made on the current path).

    Arguments:
        string -> string to be inserted into the database
        index -> index of current character in string to be inserted 
        current -> current node

    Time: O(n) where n is the length of string
    Aux. space: O(n) where n is the length of string
    """
    def insert_aux(self, string, index, current):
        # leaves store (freq, string)
        if index>=len(string)+1:
            if current.payload is None:
                current.payload = (1,string)
            else:
                current.payload = (current.payload[0]+1, current.payload[1])
            return current.payload
        # just before leaves
        elif index==len(string):
            i = 0 
            if current.children[i] is None:
                current.children[i] = Node()
            data = self.insert_aux(string, index+1, current.children[i])
            
            # prefix of word always lexicographically smaller than the word
            if current.payload is None or not current.payload[0]>data[0]: 
                current.payload = data
            return (current.payload, False)

        else:
            i = ord(string[index])-BASE
            if current.children[i] is None:
                current.children[i] = Node()
            data, changed = self.insert_aux(string, index+1, current.children[i])
            
            if current.payload is None or data[0]>current.payload[0]:
                current.payload = data

            elif data[0]==current.payload[0] and index<len(current.payload[1]):
                lex_smaller = data[1][index] < current.payload[1][index]
                shorter = len(data[1]) < len(current.payload[1])
                same_char = data[1][index] == current.payload[1][index]
                
                if (same_char and shorter):
                    current.payload = data

                elif lex_smaller or (same_char and changed):
                    current.payload = data
                    return (current.payload, True)
            
            return (current.payload,False)

# %% Question 2 
class OrfFinder:
    """
    Constructor for OrfFinder.

    Arguments:
        string -> string that represents a genome

    Time: O(n^2) where n is the length of string
    Aux.space: O(n^2) where n is the length of string
    """
    def __init__(self, string):
        self.string = string
        self.front_root = Node()
        self.back_root = Node()
        self.build_suffix()
        self.build_prefix()

    """
    Finds all the substrings of genome which have start as a prefix and end as a suffix. 
    Returns the found substrings in a list.

    Time: O(S + E + U)
        where S is the length of start
            E is the length of end
            U is the number of characters in the output list
    
    Aux. space: O(U) where U is the number of characters in the output list
    """
    def find(self, start, end):
        start_id = self.get_payload(self.front_root, start)
        end_id = self.get_payload(self.back_root, end, True)
        output = []

        # no valid start or end point
        if len(start_id) == 0 or len(end_id) == 0:
            return output
        
        prev_stop = len(end_id)-1
        for i in range(len(start_id)):
            for j in range(0,prev_stop+1):
                if end_id[j]-start_id[i] +1 >= len(start) + len(end):
                    output.append(self.string[start_id[i]:end_id[j]+1])
                else:
                    j-=1
                    break
            if j<0:
                break
            prev_stop = j
        return output
        
    """
    Retrieves the data stored at the node in the trie with prefix string. Returns the data.

    Arguments:
        current -> starting node
        string -> prefix string to match
        reverse-> indicates to match string from the back

    Time: O(n) where n is the length of string
    Aux. space: O(1)
    """
    def get_payload(self, current, string, reverse = False):
        if reverse:
            for i in range(len(string)-1,-1,-1):
                char = string[i]
                current = current.children[ord(char)-BASE]
                if current is None:
                    return []
        else:
            for char in string:
                current = current.children[ord(char)-BASE]
                if current is None:
                    return []
        if current.payload == None:
            return []
        return current.payload

    """
    Builds a suffix trie for self.string. Returns nothing.

    Time: O(n^2) where n is the length of self.string
    Aux. space: O(n^2) where n is the length of self.string
    """
    def build_suffix(self):
        for i in range(len(self.string)):
            self.insert_aux(i, self.front_root, 1)

    """
    Builds a suffix trie for the reverse of self.string. Returns nothing.

    Time: O(n^2) where n is the length of self.string
    Aux. space: O(n^2) where n is the length of self.string
    """
    def build_prefix(self):
        for i in range(len(self.string)-1,-1,-1):
            self.insert_aux(i, self.back_root, -1)

    """
    Inserts the suffix string of suffix id index to the trie. Returns nothing.

    Arguments:
        index -> suffix id of trie to build
        current -> node to start inserting from
        increment -> integer used to step through self.string
    
    Time: O(n/s) 
        where n is the length of the suffix string
            s is the absolute value of increment

    Aux. space: O(n/s) 
        where n is the length of the suffix string
            s is the absolute value of increment
    """
    def insert_aux(self, index, current, increment):
        suffix_id = index

        while index>=0 and index<len(self.string):
            if current.payload is None:
                current.payload = [suffix_id]
            else:
                current.payload.append(suffix_id)

            i = ord(self.string[index])-BASE
            if current.children[i] is None:
                current.children[i] = Node()
            current = current.children[i]

            index+=increment

# %%

