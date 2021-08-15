# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 16:12:30 2021

@author: trist
"""

import random
import os
from tqdm import tqdm

from basic_SPN import SPN, generate_keys

def generate_cyphers(n, key_path, save_path='./cyphers'):
    """Generate n cypher text with the key saved at key_path"""
    
    number = 0b0000000000000000
    
    keys = generate_keys(path=key_path)
    
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    for i in tqdm(range(n)):
        
        number =random.randint(0,65535)
        with open(os.path.join(save_path, str(number)+'.txt'), 'w') as f:
            f.write(SPN(hex(number), keys))

if __name__ == '__main__':
    
    key_path = 'keys.txt'
    
    generate_cyphers(10, key_path)