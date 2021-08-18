# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 09:28:18 2021

@author: trist
"""

def str_xor(bit1, bit2):
    
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