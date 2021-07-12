"""
Python file for FIT2004 assignment 1
Author : Neo Shao Hong
Student ID : 31276520
"""

#%%
"""
Sort a list on the col-th column in non-decreasing order

Arguments : 
    lst -> a list of non-negative integers
    base -> chosen base to sort with
    col -> chosen column to sort on
    weight -> function to determine value of element to sort on

Time : O(n + b) where 
        n is the number of elements in lst
        b is the base

Aux. space : O(n + b) where 
        n is the number of elements in lst
        b is the base
"""
def counting_sort(lst, base, col, weight):
    # build count array
    count_array = [[] for _ in range(base)]

    # count frequency of elements
    for item in lst:
        count_array[weight(item)//(base**col)%base].append(item)
    
    # update lst into sorted lst
    index = 0
    for bucket in count_array:
        for item in bucket:
            lst[index] = item
            index+=1
    
    return lst

"""
Sorts elements in lst in non-decreasing order

Arguments:
    lst -> a list of non-negative integers

Time : O(kn) where 
        n is the number of elements in lst,
        k is the greatest number of digits in any element in lst

Aux. space : O(n) where n is the number of elements in lst
"""
def radix_sort(lst):
    max_item = lst[0]
    for item in lst:
        if item>max_item:
            max_item = item
                
    base = 2
    col = 0
    while max_item//(base**col)>0:
        lst = counting_sort(lst, base, col, lambda x: x)
        col+=1
    
    return lst

"""
Group duplicate elements in a sorted list into a tuple of (element, frequency)

Arguments:
    lst -> a sorted list of non-negative integers

Time : O(kn) where 
        n is the number of number of elements in lst
        k is the greatest number of digits in any element in transaction

Aux. space : O(n) where n is the number of number of elements in lst
"""
def group(lst):
    j=0
    freq = 1
    for i in range(1,len(lst)):
        if lst[j]!=lst[i]:
            lst[j] = lst[j],freq
            j+=1
            lst[j] = lst[i]
            freq=1
        else:
            freq+=1
    lst[j] = lst[j],freq
    return lst[:j+1]

"""
Given a number t, finds the interval of length t contains the most transactions

Arguments:
    transaction -> a list of non-negative integers
    t -> non-negative integer

Time : O(kn) where 
        n is the number of elements in transaction
        k is the greatest number of digits in any element in transaction

Aux. space : O(n) where n is the number of elements in transaction
"""
def best_interval(transaction, t):
    if len(transaction) == 0:
        return (0,0)

    # sort transaction
    transaction = radix_sort(transaction)

    # group elements
    transaction = group(transaction)
        
    # find best interval
    best_count = 0
    best_t = 0
    j = 0
    i = 0
    cur_count = 0
    while i < len(transaction):
        interval = transaction[i][0] - transaction[j][0]
        # shrink area if current interval > t
        if interval > t:
            cur_count -= transaction[j][1]
            j+=1
        else:
            cur_count+=transaction[i][1]
            if cur_count > best_count:
                best_count = cur_count
                best_t = max(transaction[i][0]-t,0)
            i+=1
    return (best_t, best_count)
    
# %%
"""
Sort a list of string tuples based on the selected column of the first element of 
the tuple.

Arguments:
    lst -> a list of string tuples
    col -> selected column to sort on

Time : O(n) where n is the number of elements in lst at the current column

Aux. space : O(n) where n is the number of elements in lst at the current column 
"""
def alpha_counting_sort(lst, col):
    # build count array
    count_array = [[] for _ in range(26)]

    # sort bottom-up, stop if no more elements in column
    for i in range(len(lst)-1,-1,-1):
        item = lst[i]
        if col<len(item[0]):
            count_array[ord(item[0][col])-97].append(item)
        else:
            i+=1
            break

    # update lst 
    index = i
    for bucket in count_array:
        for j in range(len(bucket),0,-1):
            lst[index] = bucket[j-1]
            index+=1

    return lst

"""
Sort a list of string tuples based on the first element of the tuple.

Arguments: lst -> a list of string tuples

Time : O(k) where k is the total number of characters of the first element strings

Aux. space : O(n) where n is the total number of elements in lst
"""
def alpha_radix_sort(lst):
    # find longest word
    if len(lst)==0:
        return []

    longest = lst[0]
    for word in lst:
        if len(word[0])>len(longest[0]):
            longest = word

    # sort by length of word
    base = 2
    col = 0
    while len(longest[0])//(base**col):
        lst = counting_sort(lst, base, col, lambda x: len(x[0]))
        col+=1

    # sort 
    col = len(longest[0])-1
    while col>=0:
        lst = alpha_counting_sort(lst, col)
        col-=1

    return lst

"""
Return a sorted copy of word

Arguments: word -> a string

Time : O(n) where n is the length of the word

Aux. space : O(n) where n is the length of the word
"""
def sort_word(word):
    count_array = [[] for _ in range(26)]
    for i in range(len(word)):
        count_array[ord(word[i])-97].append(word[i])
    
    output = ""
    for bucket in count_array:
        for item in bucket:
            output += item
    return output

"""
Find all words in the first list which have an anagram in the second list.

Arguments: list1, list2 -> list of strings

Time : O(L1M1 + L2M2) where
        L1 is the number of elements in list1
        L2 is the number of elements in list2
        M1 is the number of characters in the longest string in list1
        M2 is the number of characters in the longest string in list2

Aux. space : O(L1 + L2) where
        L1 is the number of elements in list1
        L2 is the number of elements in list2
"""
def words_with_anagrams(list1, list2):
    # convert all words into (sorted , original)
    for i in range(len(list1)):
        list1[i] = sort_word(list1[i]) , list1[i]
    for j in range(len(list2)):
        list2[j] = sort_word(list2[j]) , list2[j]
    
    list1 = alpha_radix_sort(list1)
    list2 = alpha_radix_sort(list2)
    
    # since the lists are sorted, if list2[0...j] is < list1[i],
    # we know that no anagram of list1[i] can exists in list2[0...j],
    # similarly, since list1[i+1] is > list1[i], we know that no anagram
    # of list1[i+1] can exist in list2[0...j]
    output = []
    i = 0
    j = 0
    while i<len(list1) and j<len(list2):
        if list1[i][0]<list2[j][0]:
            i+=1
        elif list1[i][0] == list2[j][0]:
            output.append(list1[i][1]) 
            i+=1
        else:
            j+=1
    return output

# %%
