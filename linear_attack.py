# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 09:28:18 2021

@author: trist
"""

import itertools as it
import basic_SPN

def str_xor(bit1, bit2):
    """Args:
        bit1: '0' or '1'
        bit2: '0' or '1'
        
       Returns:
           '0' or '1'
    """
    return bin(bool(int(bit1)) ^ bool(int(bit2)))[2:]

def linear_equation(X, Y):
    """Compute the linear XOR sum of all the bits of X and Y
    
    Args: 
        X, hex str
        Y, hex str"""
        
    bin_X = bin(int(X, 16))[2:]
    bin_Y = bin(int(Y, 16))[2:]
    
    bin_XY = bin_X + bin_Y
    
    last = bin_XY[0]
    
    for i in range(1,len(bin_XY)):
        
        last = str_xor(last, bin_XY[i])
        
    return last

def fill(str_in, n=4):
    """fill the beginning of the str until it is n character long"""
    while len(str_in)<4:
        str_in = '0'+str_in
    return str_in

def compute_matrix():
    """Compute the probability matrix for the Sbox"""
    matrix = {}
    
    sbox_in = ["".join(seq) for seq in it.product("01", repeat=4)]
    sbox_out = [basic_SPN.subs_dict[hex(int(s,2))[2:]] for s in sbox_in]
    sbox_out = [fill(bin(int(s,16))[2:]) for s in sbox_out]
    return matrix, sbox_in, sbox_out