# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 09:28:18 2021

@author: trist
"""

import itertools as it

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

def compute_matrix():
    """Compute the probability matrix for the Sbox"""
    
    sbox_in = ["".join(seq) for seq in it.product("01", repeat=4)]
    
    pass