import os
import sys

a = [4, 2, 6, 9, 45, 21, 4, 5, 6, 3, 2, 3, 4, 4, 9, 11, 34, 555, 0]
#print(a)
#print(len(a))

def sort_bubble():
    i = len(a) - 1
    while i > 0:
        j = 0
        while j < i:
            if a[j] > a[j + 1]:
                temp = a[j+1]
                a[j+1] = a[j]
                a[j] = temp
            j = j + 1
        i = i - 1
    return a

def sort_choice():
    print(a)
    i = 0
    while i < len(a):
        min = i
        j = i + 1
        while j < len(a):
            if a[j] < a[min]:
                min = j
            j = j + 1
        temp = a[i]
        a[i] = a[min]
        a[min] = temp
        i = i + 1
    print(a)

def sort_insert():
    print(a)
    i = 1
    while i < len(a):
        j = i
        while j > 0:
            if a[j] < a[j-1]:
                temp = a[j-1]
                a[j-1] = a[j]
                a[j] = temp
            j = j - 1
        i = i + 1
    print(a)

def sort_xier():
    h = int(len(a) / 2)
    while h >= 1:
        i = h
        while i < len(a):
            j = i
            while j >= h:
                if a[j] < a[j-h]:
                    temp = a[j]
                    a[j] = a[j-h]
                    a[j-h] = temp
                j = j - h
            i = i + 1
        h = int(h/2)
    print(a)

def sort_heap(lo, hi):
    while hi <= lo:
        return
    mid = lo + int((hi - lo)/2)
    sort_heap(lo, mid)
    sort_heap(mid + 1, hi)
    heap_merge(lo, mid, hi)

def heap_merge(lo, mid, hi):
    i = lo
    j = mid + 1
    k = lo
    m = lo
    while k <= hi:
        b[k] = a[k]
        k = k + 1
    while m <= hi:
        if i > mid:
            a[m] = b[j]
            j = j + 1
        elif j > hi:
            a[m] = b[i]
            i = i + 1
        elif b[j] < b[i]:
            a[m] = b[j]
            j = j + 1
        else:
            a[m] = b[i]
            i = i + 1
        m = m + 1

def sort_quick(lo, hi):
    if hi <= lo:
        return
    j = quick_partination(lo, hi)
    sort_quick(lo, j - 1)
    sort_quick(j + 1, hi)

def quick_partination(lo, hi):
    i = lo
    j = hi + 1
    v = a[lo]
    while True:
        i = i + 1
        while a[i] < v:
            if i == hi:
                break
            i = i + 1
        j = j - 1
        while a[j] > v:
            #print(a[j], v)
            #print(j, lo)
            if j == lo:
                break
            j = j - 1
            #print(j, lo)
        if i >= j:
            break
        temp = a[i]
        a[i] = a[j]
        a[j] = temp
    tmp = a[j]
    a[j] = a[lo]
    a[lo] = tmp
    return j

def search_binary(b, key):
    lo = 0
    hi = len(b) - 1
    while lo <= hi:
        mid = lo + int((hi - lo)/2)
        if key < b[mid]:
            hi = mid - 1
        elif key > b[mid]:
            lo = mid + 1
        else:
            return mid

import operator
def IsPopOrder(pushV1, popV):
    if len(pushV1) == 0 and len(popV) == 0:
        return False
    if pushV1 is None and popV is not None:
        return False
    if pushV1 is not None and popV is None:
        return False
    if len(pushV1) != len(popV):
        return False
    lens = len(pushV1)
    aa = []
    while lens > 0:
        aa.append(pushV1[lens - 1])
        lens = lens - 1
    while aa:
        if aa.pop() != popV.pop():
            return False
    return True

def MoreThanHalfNum(numbers):
    if len(numbers) == 0:
        return None
    x = len(numbers) / 2
    flag = numbers[0]
    times = 1
    for i in numbers[1:]:
        if times == 0:
            flag = i
            times = 1
        elif i == flag:
            times += 1
        else:
            times -= 1
    times = 0
    for i in numbers:
        if i == flag:
            times += 1
    if times > x:
        return flag
import collections
def FindApperOnce(array):
    dicts = collections.Counter(array)
    a = []
    for item,num in dicts.items():
        if num == 1:
            a.append(item)
    if a is None:
        return None
    else:
        return a

if __name__ == "__main__":
    a = [1,3,3,4,4,6,5,5,8]
    print(FindApperOnce(a))
    #print(MoreThanHalfNum(a))
    '''
    a = []
    b = []
    res = IsPopOrder(a, b)
    print(res)

    
    sort_choice()
    b = [None] * len(a)
    sort_heap(0, len(a)-1)
    print(a)
    sort_quick(0, len(a)-1)
    print(a)

    b = sort_bubble()
    print(b)
    keys = search_binary(b, 6)
    print(keys)
    '''