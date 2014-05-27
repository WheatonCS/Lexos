# -*- coding: utf-8 -*-
from collections import Counter, defaultdict, OrderedDict
import csv

def generateCounts(string):
    return dict(Counter(string.split()))