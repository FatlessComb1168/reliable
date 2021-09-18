'''
Reliable Console.
Copyright (C) 2021 by Fedor Egorov <fedoregorov1@yandex.ru>
This file is part of Reliable.

Reliable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Reliable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Reliable. If not, see <https://www.gnu.org/licenses/>.
'''

from hashlib import sha256;
from random import randint, seed;
from os import system;
import ctypes;

ctypes.windll.kernel32.SetConsoleTitleW('Reliable');
system('mode 120, 32');

def apc(hash):
    hash = sha256(bytes(hash, encoding = 'utf-8')).hexdigest();
    apb = [];
    apb2 = [];
    while len(hash) < (250 * 30):
        hash += sha256(bytes(hash, encoding = 'utf-8')).hexdigest();
    
    start = 0;
    finish = 250;

    while finish < len(hash):
        apb.append(hash[start:finish]);
        start += 250;
        finish += 250;
    
    done = 'Passwords:\n';
    count = 1;

    for i in apb:
        seed(i[1:10]);
        apb2 = [];
        p = '';
        length = randint(12, 24);
        start = 0;
        finish = 10;
        while finish < len(i):
            apb2.append(i[start:finish]);
            start += 10;
            finish += 10;
        
        for i in apb2:
            seed(i);
            p += chr(randint(33, 126));
            p = p[0:length];
            
        done += (str(count) + '. ' + p + '\n').replace('\\', '');
        count += 1;
    
    return done[0:-1];

while True:
    a = input('Welcome to Reliable!\n0 - Generate a set of passwords\n1 - Exit\n');
    if a == '0':
        a = (input('Enter a master-password: '));
        system('cls');
        input(apc(a) + '\n' + 'Enter to continue...');
    if a == '1':
        break;
    else:
        system('cls');