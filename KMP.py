#!/usr/bin/env python
# -*- coding: utf-8 -*-

'KMP string search algorithm'

__author__ = "XNY"

def GetNext(string):
    length = len(string)
    j = 0
    next = []
    next.insert(0, 0)
    next.insert(1, 0)

    for i in range(1, length):
        while j > 0 and string[i] != string[j]:
            j = next[j]
        if string[i] == string[j]:
            j += 1
        next.insert(i + 1, j)

    return next

def KMP_Search(original, find):
    original_length = len(original)
    find_length = len(find)
    next = GetNext(original)
    j = 0
    for i in range(original_length):
        while j > 0 and original[i] != find[j]:
            j = next[j]
        if original[i] == find[j]:
            j += 1
        if j == find_length:
            print "Find at position: ", i - j + 1
            print original[i - j + 1: i + 1]
            j = next[j]
