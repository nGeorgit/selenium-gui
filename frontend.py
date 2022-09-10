from ast import main
from curses import window
from tkinter import *
from tkinter import ttk
import json
from backend import sele

class routin():
    def __init__(self, name, rout, parent):
        self.se = sele()
        self.rout = rout
        self.name = name
        fr = ttk.Frame(parent).grid()
        ttk.Button(fr, text='Run routin', command=self.run).grid()

    def run(self):
        self.se.get(self.rout)

class actionOb():
    def __init__(self, parent, id):
        self.frame = ttk.Frame(parent).grid()
        self.act_ar = []

        self.act_1 = StringVar()

        self.comb_1 = ttk.Combobox(self.frame, textvariable=self.act_1)
        self.comb_1['values'] = ['go to', 'click']
        self.comb_1.grid()
        self.add_act(self.creat_act_el(self.act_1, 0))

        self.frame_2 = ttk.Frame(self.frame).grid()

        self.act_2 = StringVar()
        self.entry_2 = ttk.Entry(self.frame_2, textvariable=self.act_2).grid()
        self.add_act(self.creat_act_el(self.act_2, 1))

    def clean(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def creat_act_el(self, act, level):
        return {
            'str' : act,
            'level' : level
        }

    def add_act(self, act):
        try:
            self.act_ar[act['level']] = act
        except:
            self.act_ar.append(act)
    
    def ret_str(self):
        stri = ''
        for i in self.act_ar:
            stri += i['str'].get() + "|"
        return stri

class app():
    def __init__(self):


        self.id = 0
        self.actions = []
        with open('settings.json') as f:
            self.sett = json.load(f)

        with open('link.json') as f:
            self.link = json.load(f)

        window = Tk()              #open the window
        window.title('Selenium Gui')

        n = ttk.Notebook(window) #creat the notebook and adding the tabs 
        n['padding'] = 15
        n.grid() #pack(expand = 1, fill ="both")

        #home tab
        self.main_tab = ttk.Frame(n)
        self.main_tab['padding'] = 20
        n.add(self.main_tab, text='Home')

        ttk.Button(self.main_tab ,text='Add action', command=self.add_action).grid() #button that adds an action frame
        self.act_frame = ttk.Frame(self.main_tab).grid()

        ttk.Button(self.main_tab, text='submit', command=self.submit).grid()

        #routins tab
        self.rout_tab = ttk.Frame(n)
        self.rout_tab['padding'] = 20
        n.add(self.rout_tab, text='Routins')

        self.routings = []
        for name in self.link:
            print(name)
            self.routings.append(routin(name, self.link[name], self.rout_tab))

        #Settings tab
        self.set_tab = ttk.Frame(n)
        self.set_tab['padding'] = 20
        n.add(self.set_tab, text='Settings')

        #Settings select browser
        Label(self.set_tab, text="Select browser").grid()
        self.browser = StringVar()
        def changeBrowser(e):
            self.sett['browser'] = self.browser.get()
            self.dump('set')


        print(self.sett['browser'])
        
        self.com_browser = ttk.Combobox(self.set_tab, textvariable=self.browser)
        self.com_browser['values'] = ['Chrome', 'Firefox', 'Opera']
        self.com_browser.bind('<<ComboboxSelected>>', changeBrowser)
        self.com_browser.grid()

        window.mainloop()

    def add_action(self):
        self.actions.append(actionOb(self.act_frame, self.id))
        self.id = self.id + 1

    def dump(self, loc):
        if loc == 'set':
            with open('settings.json', 'w') as f:
                json.dump(self.sett, f, indent=2)
        elif loc == 'li':
            with open('link.json', 'w') as f:
                json.dump(self.link, f, indent=2)

    def submit(self):
        rout = []
        for i in self.actions:
            rout.append(i.ret_str())
            print(i.ret_str())
        self.link['routin1'] = rout
        self.dump('li')


ap = app()