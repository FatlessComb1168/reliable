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

try:
    from tkinter import *;
    from tkinter import ttk;
    from tkinter.filedialog import *; # Call open file window
    import sys;
    from os import path;
    from subprocess import call;
    from hashlib import sha256;
    from random import randint, seed;
    import ctypes;
    from webbrowser import open_new;
    try:
        from pyperclip import copy; # Copy text (HEX, DEC)
    except:
        path.insert(0, path.dirname(sys.executable) + "\\pyperclip");
        from pyperclip import copy;
    try:
        from PIL import ImageTk, Image;
    except:
        path.insert(0, path.dirname(sys.executable) + "\\PIL");
        from PIL import ImageTk, Image;

    call('taskkill /f /im reliable.exe', shell = True);

    myappid = 'fedoregorov.reliable.1.13' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid);

    def open_site(url):
        open_new(url);

    def geometry(window_width, window_height):
        global window;
        screen_width = window.winfo_screenwidth();
        screen_height = window.winfo_screenheight();

        x_cordinate = int((screen_width / 2) - (window_width / 2));
        y_cordinate = int((screen_height / 2) - (window_height / 2));

        window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate));
        window.resizable(width=False, height=False);

    def on_close():
        sys.exit();
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
            password.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
            password.mark_set(INSERT, "1.0");
            password.see(INSERT);

    def apc(hash):
        global text_output1, done;
        hash = sha256(bytes(hash, encoding = 'utf-8')).hexdigest();
        apb = [];
        apb2 = [];
        while len(hash) < (250 * 50):
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
                
            done += (str(count) + '. ' + p + '\n').replace('\\', '').replace('<', '').replace('>', '');
            count += 1;
        
        text_output1.configure(state = 'normal');
        text_output1.delete('1.0', END);
        text_output1.insert("1.0", done[0:-1]);
        text_output1.configure(state = 'disabled');

    def toggle_password(): # Author: acw1668, Stack Overflow.
        global text_output, show_hide_button;
        if password.cget('show') == '':
            password.config(show='*');
            show_hide_button.config(text = 'Show');
        else:
            password.config(show='');
            show_hide_button.config(text='Hide');

    Tk().withdraw();

    window = Toplevel();
    geometry(715, 420);
    window.title('Reliable');
    try:
        window.iconbitmap(path.dirname(sys.executable) + '\\resources\\logo.ico');
    except:
        window.iconbitmap('resources/logo.ico');

    nb = ttk.Notebook(window);
    f1 = Frame(window);
    f2 = Frame(window);
    nb.add(f1, text='Main');
    nb.add(f2, text = 'About');
    nb.pack(fill='both', expand='yes');

    show_hide_button = ttk.Button(f1, text = 'Show', command = toggle_password);
    show_hide_button.grid(row = 1, column = 1, padx = (25, 0), pady = (15, 0));

    text_label = Label(f1, text = 'Enter a master-password:');
    text_label.grid(row = 1, column = 2, padx = (10, 0), pady = (15, 0));

    password = ttk.Entry(f1, width = 30, show = '*', font = 'NotoSans-Regular.ttf');
    password.grid(row = 1, column = 3, padx = (10, 0), pady = (15, 0));

    password.bind_all("<Control-Key-a>", lambda event: password.get('1.0', 'end-1c'));
    password.bind_all("<Key>", _onKeyRelease, "+");

    get_values_button = ttk.Button(f1, text = 'Generate passwords', command = lambda: apc(password.get()));
    get_values_button.grid(row = 1, column = 4, padx = (10, 0), pady = (15, 0));

    frame = Frame(f1);
    text_output1 = Text(frame, width = 75, height = 13, font = 'NotoSans-Regular.ttf');

    vscroll = Scrollbar(frame, orient = VERTICAL, command = text_output1.yview);
    text_output1['yscroll'] = vscroll.set;
    vscroll.pack(side = "right", fill = "y");

    password.bind_all("<Return>", lambda event: apc(password.get()));
    text_output1.configure(state = 'disabled');
    text_output1.pack();
    frame.place(x = 10, y = 50);

    tip = Label(f1, text = 'TIP: you can mark passwords in documents and on paper this way. For example:', fg='#008000');
    tip.place(x = 10, y = 300);

    tip = Label(f1, text = 'Password #90: MySocialNetwork1; Password #101: MySocialNetwork2:', fg='#008000');
    tip.place(x = 10, y = 320);

    warning = Label(f1, text = 'ATTENTION: REMEMBER YOUR MASTER PASSWORD FOR LIFE AND NEVER ENTRUST IT TO OTHER PEOPLE,', fg='#f00');
    warning.place(x = 10, y = 340);

    warning = Label(f1, text = 'UNLESS THEY ARE YOUR CONFIDANTS OR RELATIVES! CREATE A NEW PASSWORD THAT YOU HAVE NEVER USED BEFORE', fg='#f00');
    warning.place(x = 10, y = 360);


    # ABOUT THE PROGRAM

    iy = 5;
    ix = 110;

    try:
        img = Image.open(path.dirname(sys.executable) + 'resources\\logo.png');
    except:
        img = Image.open('resources\\logo.png');
    (w, h) = img.size;
    img = img.resize((w // 5, h // 5), Image.ANTIALIAS);

    img = ImageTk.PhotoImage(img);
    panel = Label(f2, image = img);
    panel.place(x = 25 + ix, y = 80 - iy + 60);

    program_name = Label(f2, text = 'Reliable', font = 'Arial 15');
    program_name.place(x = 140 + ix, y = 80 - iy);

    version = Label(f2, text = 'Version 1.13', font = 'Arial 10');
    version.place(x = 140 + ix, y = 110 - iy);

    author = Label(f2, text = 'Author: Fedor Egorov (FatlessComb1168)', font = 'Arial 10');
    author.place(x = 140 + ix, y = 130 - iy);

    author_github = Label(f2, text = '(GitHub)', font = 'Arial 10', fg = "blue", cursor = "hand2");
    author_github.place(x = 383 + ix, y = 130 - iy);
    author_github.configure(underline = True);
    author_github.bind("<Button-1>", lambda e: open_site("https://github.com/FatlessComb1168"));

    licensed = Label(f2, text = 'The program is distributed under the GNU Public License,', font = 'Arial 10');
    licensed.place(x = 140 + ix, y = 160 - iy);

    licensed = Label(f2, text = 'version 3. You can read more about the license here:', font = 'Arial 10');
    licensed.place(x = 140 + ix, y = 180 - iy);

    licensed3 = Label(f2, text = 'https://www.gnu.org/licenses/gpl-3.0.en.html', fg = "blue", cursor = "hand2", font = 'Arial 10');
    licensed3.place(x = 140 + ix, y = 200 - iy);   
    licensed3.configure(underline = True); 
    licensed3.bind("<Button-1>", lambda e: open_site("https://www.gnu.org/licenses/gpl-3.0.en.html"));

    github = Label(f2, text = 'See project on GitHub: ', font = 'Arial 10');
    github.place(x = 140 + ix, y = 230 - iy);

    licensed3 = Label(f2, text = 'https://github.com/FatlessComb1168/reliable', fg = "blue", cursor = "hand2", font = 'Arial 10');
    licensed3.place(x = 140 + ix, y = 250 - iy);   
    licensed3.configure(underline = True); 
    licensed3.bind("<Button-1>", lambda e: open_site("https://github.com/FatlessComb1168/reliable"));

    window.protocol('WM_DELETE_WINDOW', on_close);

    window.mainloop();
except Exception as e:
    input(e);