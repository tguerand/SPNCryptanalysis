# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:17:47 2021

@author: trist

Substitution Permutation Network Cypher

Followed tutorial from http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf

"""

import numpy as np
import secrets
import binascii

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
keys = secrets.token_bytes(BLOCK_SIZE*5)


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def SPN(text, subkeys=keys):
    """Simple Substitution Permutation Network"""
    
    cypher = text
    
    k1 = bytes.fromhex(subkeys[:BLOCK_SIZE].hex())
    k2 = bytes.fromhex(subkeys[BLOCK_SIZE:2*BLOCK_SIZE].hex())
    k3 = bytes.fromhex(subkeys[2*BLOCK_SIZE:3*BLOCK_SIZE].hex())
    k4 = bytes.fromhex(subkeys[3*BLOCK_SIZE:4*BLOCK_SIZE].hex())
    k5 = bytes.fromhex(subkeys[4*BLOCK_SIZE:].hex())


    subk = [k1, k2, k3, k4, k5]

    for i in range(3):
        print(cypher)
        ## KEY MIX: XOR
        cypher = byte_xor(cypher, subk[i]).hex()
        ## SUBSTITUTION
        cypher = [subs_dict[cypher[i]] for i in range(len(cypher))]
        ## PERMUTATION
        cypher = [cypher[perm_table[i]] for i in range(len(cypher))]
        cypher = bytes.fromhex(cypher)
    # 4TH KEY MIX
    cypher = byte_xor(cypher, subk[3])
    
    # LAST SUBSTITUTION
    cypher = [subs_dict[cypher[i]] for i in range(len(cypher))]
    
    # LAST KEY MIX
    cypher = byte_xor(cypher, subk[4])
    
    return cypher
        
        
def decrypt(cypher, subkeys):
    
    pass

if __name__  == '__main__':
    
    text = b'hello'
    hex_text = binascii.hexlify(text)
    print(hex_text)
    
    
    cypher = SPN(hex_text)
    print(cypher)
        