# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:17:47 2021

@author: trist

Substitution Permutation Network Cypher

Followed tutorial from http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf

"""

import numpy as np
import secrets
import os

np.random.seed(42)

HEX_TABLE = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
HEX_DICT = {str(i): HEX_TABLE[i] for i in range(16)}
REV_HEX_DICT = {HEX_DICT[str(i)]:str(i) for i in range(16)}
BLOCK_SIZE = 16

### STEP 1: substitution
subs_table = np.random.permutation(BLOCK_SIZE)
subs_dict = {HEX_DICT[str(i)]:HEX_DICT[str(subs_table[i])] for i in range(16)}
rev_subs_dict = {v:k for k,v in subs_dict.items()}

### STEP 2: permutation
perm_table = np.random.permutation(BLOCK_SIZE)
perm_table = {i:perm_table[i] for i in range(BLOCK_SIZE)}
rev_perm_table = {v:k for k,v in perm_table.items()}

### STEP 3: key mix
# We need 5 key block of size 16 each
def generate_keys(path=None):
    if path is not None:
        with open(path, 'rb') as fkey:
            keys = fkey.read()
    else:
        keys = secrets.token_bytes(BLOCK_SIZE*5)
        with open('keys.txt', 'w') as fkey:
            fkey.write(str(keys))
    return keys



def hex_pad(hex_in):
    
    if len(hex_in)<4:
        hex_in = "0" * (4-len(hex_in)) + hex_in
    return hex_in

def byte_xor(ba1, ba2):
    xor = bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    return xor

def subs(hex_input, subs_dict=subs_dict):
    
    hex_out = ''
    for char in hex_input:
        hex_out += subs_dict[char]
    return hex_out

def perm(hex_input, perm_table=perm_table):
    
    b_in = bin(int(hex_input, 16))[2:]
    
    if len(b_in)<16:
        b_in = '0'*(16-len(b_in)) + b_in

    b_out = ''
    
    for i in range(16):
        b_out += b_in[perm_table[i]]
        
    hex_out = hex(int(b_out,2))[2:]
    return hex_out

def SPN(text, subkeys):
    """Simple Substitution Permutation Network"""
    
    cypher = bytearray.fromhex(text[2:])

    
    k1 = bytes.fromhex(subkeys[:BLOCK_SIZE].hex())
    k2 = bytes.fromhex(subkeys[BLOCK_SIZE:2*BLOCK_SIZE].hex())
    k3 = bytes.fromhex(subkeys[2*BLOCK_SIZE:3*BLOCK_SIZE].hex())
    k4 = bytes.fromhex(subkeys[3*BLOCK_SIZE:4*BLOCK_SIZE].hex())
    k5 = bytes.fromhex(subkeys[4*BLOCK_SIZE:].hex())


    subk = [k1, k2, k3, k4, k5]

    for i in range(3):
        
        ## KEY MIX: XOR
        cypher = byte_xor(cypher, subk[i]).hex()
        ## SUBSTITUTION
        cypher = subs(cypher)
        ## PERMUTATION
        cypher = hex_pad(perm(cypher))
        
        cypher = bytes.fromhex(cypher)
    # 4TH KEY MIX
    cypher = byte_xor(cypher, subk[3]).hex()
    
    # LAST SUBSTITUTION
    cypher = subs(cypher)
    
    # LAST KEY MIX
    cypher = bytes.fromhex(cypher)
    cypher = byte_xor(cypher, subk[4]).hex()
    
    return cypher
        
        
def decrypt(cypher, subkeys):
    
    k1 = bytes.fromhex(subkeys[:BLOCK_SIZE].hex())
    k2 = bytes.fromhex(subkeys[BLOCK_SIZE:2*BLOCK_SIZE].hex())
    k3 = bytes.fromhex(subkeys[2*BLOCK_SIZE:3*BLOCK_SIZE].hex())
    k4 = bytes.fromhex(subkeys[3*BLOCK_SIZE:4*BLOCK_SIZE].hex())
    k5 = bytes.fromhex(subkeys[4*BLOCK_SIZE:].hex())


    subk = [k1, k2, k3, k4, k5]
    
    cypher = bytes.fromhex(cypher)
    cypher = byte_xor(cypher, subk[4]).hex()
    # LAST SUBSTITUTION
    cypher = subs(cypher, subs_dict=rev_subs_dict)
    cypher = bytes.fromhex(cypher)
    
    for i in range(3,0,-1):
    
        cypher = byte_xor(cypher, subk[i]).hex()
        cypher = hex_pad(perm(cypher, perm_table=rev_perm_table))
        cypher = subs(cypher, subs_dict=rev_subs_dict)
        cypher = bytes.fromhex(cypher)
    
    cypher = byte_xor(cypher, subk[0]).hex()
    
    return cypher

if __name__  == '__main__':
    
    text = 0b1010011010110111
    hex_text = hex(text)
    print(hex_text)
    
    if os.path.exists('keys.txt'):
        keys = generate_keys(path='keys.txt')
    else:
        keys = generate_keys(path=None)
    cypher = SPN(hex_text, keys)
    print(cypher)
    dec_text = decrypt(cypher, keys)
    print(dec_text)
        