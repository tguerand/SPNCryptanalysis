# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 09:28:18 2021

@author: trist
"""

import itertools as it
import basic_SPN
import numpy as np

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
        
    # get the subs_dict from the SPN in bits    
    sbox = {fill(bin(int(k,16))[2:]):fill(bin(int(v,16))[2:]) for k,v in basic_SPN.subs_dict.items()}
    
    # initialize probability matrix
    matrix = np.zeros((len(sbox),len(sbox)))
    
    for i in range(len(sbox)):
    
        X1,X2,X3,X4 = [int(bit) for bit in fill(bin(i)[2:])]
        Y1,Y2,Y3,Y4 = [int(bit) for bit in sbox[fill(bin(i)[2:])]]
        
        equ_in = [0, X4, X3, X3^X4, X2, X2^X4, X2^X3, X2^X3^X4, X1, X1^X4,
                  X1^X3, X1^X3^X4, X1^X2, X1^X2^X4, X1^X2^X3, X1^X2^X3^X4]
        equ_out = [0, Y4, Y3, Y3^Y4, Y2, Y2^Y4, Y2^Y3, Y2^Y3^Y4, Y1, Y1^Y4,
                   Y1^Y3, Y1^Y3^Y4, Y1^Y2, Y1^Y2^Y4, Y1^Y2^Y3, Y1^Y2^Y3^Y4]
        
        # will optimize that later
        for x in range(len(equ_in)):
            for y in range(len(equ_out)):
                matrix[x,y] += (equ_in[x] == equ_out[y])
                
    
    return matrix, sbox