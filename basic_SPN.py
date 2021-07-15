# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:17:47 2021

@author: trist

Substitution Permutation Network Cypher

Followed tutorial from http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf

"""

import numpy as np
import random

HEX_TABLE = "0123456789ABCDEF"
HEX_DICT = {i: hex(i) for i in range(16)}
REV_HEX_DICT = {HEX_DICT[i]:i for i in range(16)}
BLOCK_SIZE = 16

### STEP 1: substitution
subs_table = np.random.permutation(BLOCK_SIZE)
subs_dict = {i:HEX_DICT[subs_table[i]] for i in range(BLOCK_SIZE)}
rev_subs_dict = {subs_dict[i]:i for i in range(BLOCK_SIZE)}

### STEP 2: permutation
perm_table = np.random.permutation(BLOCK_SIZE)
perm_table = {i:perm_table[i] for i in range(BLOCK_SIZE)}

### STEP 3: key mix
# We need 5 key block of size 16 each
keys = random.getrandbits(BLOCK_SIZE*5)

def SPN(text, subkeys):
    """Simple Substitution Permutation Network"""
    
    cypher = text
    
    k1 = hex(subkeys[:BLOCK_SIZE])
    k2 = hex(subkeys[BLOCK_SIZE:2*BLOCK_SIZE])
    k3 = hex(subkeys[2*BLOCK_SIZE:3*BLOCK_SIZE])
    k4 = hex(subkeys[3*BLOCK_SIZE:4*BLOCK_SIZE])
    k5 = hex(subkeys[4*BLOCK_SIZE:])

    subk = [k1, k2, k3, k4, k5]

    for i in range(3):
        
        ## KEY MIX: XOR
        cypher = cypher ^ subk[i]
        
        
        