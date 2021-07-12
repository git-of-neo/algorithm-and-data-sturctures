"""
Python file for FIT2004 assignment 2
Author : Neo Shao Hong
Student ID : 31276520
"""

#%%
"""
Calculates the maximum amount of money you can earn by combining 
your job as a personal trainer with participating in competitions. 
Returns an integer, which is the maximum amount of money that can be earned.

Arguments:
    weekly_income -> a list of non-negative integers, where weekly_income[i] 
    is the amount of money you will earn working as a personal trainer in week i.

    competition -> a list of tuples, each representing a sporting competition. 
    Each tuple contains 3 non-negative integers, (start_time, end_time, winnings).

Time : O(n + m log m) where
            n is the total number of elements in weekly_income
            m is the total number of elements in competitions

Aux. space : O(n) where n is the total number of elements in weekly_income
"""
def best_schedule(weekly_income, competitions):
    competitions.sort(key = (lambda x: x[0]))
    memo = [0]*(len(weekly_income)+1)
    j = 0
    for i in range(len(weekly_income)):
        while j<len(competitions) and competitions[j][0]==i:
            memo[competitions[j][1]+1] = max(competitions[j][2] + memo[i], memo[competitions[j][1]+1])
            j+=1
        memo[i+1] = max(memo[i]+weekly_income[i], memo[i+1])
    return memo[-1]
    
#%%
"""
Curry function to check if index is a valid index for lst. Returns true if 
is valid, false otherwise.

Arguments:
    lst -> a list
    index -> an integer

Time : O(1)
Aux. space : O(1)
"""
def valid(lst):
    def g(index):
        return index >=0 and index<len(lst)
    return g

"""
Calculates the maximum amount of money that can be earned by the salesperson.
Returns an integer, which is the maximum amount of money that can be
earned by the salesperson.

Arguments:
    profit -> a list of lists. All interior lists are length n. Each interior 
    list represents a different day. profit[d][c] is the profit that the 
    salesperson will make by working in city c on day d.

    quarantine_time -> a list of non-negative integers. quarantime_time[i] 
    is the number of days city i requires visitors to quarantine before 
    they can work there.

    home -> is an integer which represents the city that the salesperson
    starts in. 

Time : O(nd) where n is the number of cities, and d is the number of days 
Aux. space : O(nd) where n is the number of cities, and d is the number of days 
"""

def best_itinerary(profit, quarantine_time,home):
    if len(profit) <= 0:
        return 0
    if len(profit[0])<=0:
        return 0

    days = len(profit)
    cities = len(quarantine_time)

    valid_c = valid(quarantine_time)
    valid_d = valid(profit)

    # (profit not under quarantine, profit under quarantine)
    memo = [ [(0,0)] *cities for _ in range(days)]
    memo[0][home] = (profit[0][home],0)
    
    for d in range(1,days):
        lo = home-d if home-d>0 else 0
        hi = home+d+1 if home+d+1<cities else cities
        for c in range(lo,hi):
            # collect data from neighbour city
            l = memo[d-1][c-1] if valid_c(c-1) else (0,0)
            r = memo[d-1][c+1] if valid_c(c+1) else (0,0)

            # see if I can make more money after going through a quarantine
            if valid_c(c-1) and valid_d(d-quarantine_time[c]-1):
                l_quarantine = max(memo[d-quarantine_time[c]-1][c-1])
            else:
                l_quarantine = 0
            
            if valid_c(c+1) and valid_d(d-quarantine_time[c]-1):
                r_quarantine = max(memo[d-quarantine_time[c]-1][c+1])
            else:
                r_quarantine = 0
            
            # initial traveling
            if c==home or d>=quarantine_time[c] + abs(home-c):
                stay = memo[d-1][c][0] + profit[d][c]
            else:
                stay = 0

            memo[d][c] = (max(stay,l_quarantine,r_quarantine) , max(max(l),max(r)))
    
    return max(max(memo[-1]))
