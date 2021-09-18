'''
Reliable.
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

from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import *; # Call open file window
from pyperclip import copy; # Copy text (HEX, DEC)
from sys import exit;
from subprocess import call;
from hashlib import sha256;
from random import randint, seed;
import ctypes;

call('taskkill /f /im reliable.exe', shell = True);

myappid = 'fedoregorov.reliable.1.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def geometry(window_width, window_height):
    global window;
    screen_width = window.winfo_screenwidth();
    screen_height = window.winfo_screenheight();

    x_cordinate = int((screen_width / 2) - (window_width / 2));
    y_cordinate = int((screen_height / 2) - (window_height / 2));

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate));
    window.resizable(width=False, height=False);

def on_close():
    exit();
    # subprocess.call('taskkill /f /im hexdec.exe & taskkill /f /im python.exe & taskkill /f /im pythonw.exe', shell=True);

def _onKeyRelease(event): # Author: sergey.s1, Stack Overflow.
    ctrl  = (event.state & 0x4) != 0;
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>");

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>");
    
    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>");

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        text_output.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
        text_output.mark_set(INSERT, "1.0");
        text_output.see(INSERT);

def select_all():
    text_output.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
    text_output.mark_set(INSERT, "1.0");
    text_output.see(INSERT);
    return 'break';

def apc(hash):
    global text_output1, done;
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
    
    text_output1.configure(state = 'normal');
    text_output1.delete('1.0', END);
    text_output1.insert("1.0", done[0:-1]);
    text_output1.configure(state = 'disabled');

def toggle_password(): # Author: acw1668, Stack Overflow.
    global text_output, show_hide_button;
    if text_output.cget('show') == '':
        text_output.config(show='*');
        show_hide_button.config(text = 'Show');
    else:
        text_output.config(show='');
        show_hide_button.config(text='Hide');

Tk().withdraw();

window = Tk();
geometry(715, 300);
window.title('Reliable');
window.iconbitmap('resources/logo.ico');

show_hide_button = ttk.Button(window, text = 'Show', command = toggle_password);
show_hide_button.grid(row = 1, column = 1, padx = (25, 0), pady = (15, 0));

text_label = Label(window, text = 'Enter a master-password:');
text_label.grid(row = 1, column = 2, padx = (10, 0), pady = (15, 0));

text_output = ttk.Entry(window, width = 30, show = '*', font = 'NotoSans-Regular.ttf');
text_output.grid(row = 1, column = 3, padx = (10, 0), pady = (15, 0));

text_output.bind_all("<Control-Key-a>", lambda event: text_output.get('1.0', 'end-1c'));
text_output.bind_all("<Key>", _onKeyRelease, "+");

get_values_button = ttk.Button(window, text = 'Generate passwords', command = lambda: apc(text_output.get()));
get_values_button.grid(row = 1, column = 4, padx = (10, 0), pady = (15, 0));

frame = Frame(window);
text_output1 = Text(frame, width = 75, height = 13, font = 'NotoSans-Regular.ttf');

vscroll = Scrollbar(frame, orient = VERTICAL, command = text_output1.yview);
text_output1['yscroll'] = vscroll.set;
vscroll.pack(side = "right", fill = "y");

text_output.bind_all("<Return>", lambda event: apc(text_output.get()));
text_output1.configure(state = 'disabled');
text_output1.pack();
frame.place(x = 10, y = 50);

window.protocol('WM_DELETE_WINDOW', on_close);

window.mainloop();