#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:40:52 2021

@author: motionpay
"""


def on_vocareum():
    import os
    return os.path.exists('.voc')

def download(file, local_dir="", url_base=None, checksum=None):
    import os, requests, hashlib, io
    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)            
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(file))
    
if on_vocareum():
    DATA_PATH = "./resource/asnlib/publicdata/"
else:
    DATA_PATH = ""
datasets = {'groceries.csv': '0a3d21c692be5c8ce55c93e59543dcbe'}

for filename, checksum in datasets.items():
    download(filename, local_dir=DATA_PATH, checksum=checksum)

with open('{}{}'.format(DATA_PATH, 'groceries.csv')) as fp:
    groceries_file = fp.read()
print (groceries_file[0:250] + "...\n... (etc.) ...") # Prints the first 250 characters only
print("\n(All data appears to be ready.)")

from collections import defaultdict
from itertools import combinations
#print(groceries_file)

groceries_file=groceries_file.strip()
norm=groceries_file.split("\n")
lis=[]

for i in norm:
    se=i.split(",")
    lis.append(set(se))


itemset=lis
# Confidence threshold
THRESHOLD = 0.5

# Only consider rules for items appearing at least `MIN_COUNT` times.
MIN_COUNT = 10



def update_pair_counts (pair_counts, itemset):
    """
    Updates a dictionary of pair counts for
    all pairs of items in a given itemset.
    """
    assert type (pair_counts) is defaultdict
    for a,b in combinations(itemset,2):
        pair_counts[(a,b)]+=1
        pair_counts[(b,a)]+=1
        
def update_item_counts(item_counts, itemset):
    ###
    ### YOUR CODE HERE
    ###
    for i in itemset:
       item_counts[i]+=1
def filter_rules_by_conf (pair_counts, item_counts, min_count, threshold):
    rules = {} # (item_a, item_b) -> conf (item_a => item_b)
    ###
    ### YOUR CODE HERE
    ###
    for a,b in pair_counts.keys():
        assert a in item_counts
        if item_counts[a] >=min_count and pair_counts[(a,b)]/item_counts[a]>=threshold:
            rules[(a,b)]=pair_counts[(a,b)]/item_counts[a]
    return rules



def find_assoc_rules(receipts, min_count, threshold):
    ###
    ### YOUR CODE HERE
    ###
    dic=defaultdict(int)
    dicn=defaultdict(int)
    for i in receipts:
        for a,b in combinations(i,2):
            dic[(a,b)]+=1
            dic[(b,a)]+=1
        for n in i:
            dicn[n]+=1
    return filter_rules_by_conf(dic,dicn, min_count, threshold)
            

res=find_assoc_rules(itemset,MIN_COUNT, THRESHOLD)

print(res)







