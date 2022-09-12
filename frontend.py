from ast import main
from cgitb import text
from curses import window
from tkinter import *
from tkinter import ttk
import json
from backend import sele

class routin(): #routin ob
    def __init__(self, name, rout, parent, id):
        self.o = []
        self.parent = parent
        self.rout = rout    #the routin string from link.json
        self.name = name    #the routin's name
        ttk.Label(parent, text=name).grid(column=0, columnspan=2, row=id)
        ttk.Button(parent, text='Run', command=self.run).grid(column=0, row=id+1) #button to run the routin
        ttk.Button(parent, text='Edit', command=self.edit).grid(column=1, row=id+1)

    def run(self): #functions that runs the routin
        self.se = sele() #opening browser with slen
        self.se.get(self.rout) #sending the routin to backend

    def edit(self):
        #print(self.rout)
        id = 0
        for i in self.rout:
            act = i.split('|')
            print(act)
            self.o.append(actionOb(self.parent, id, act_1=act[0], act_2=act[1]))
            id += 1

class actionOb(): #action ob
    def __init__(self, parent, id, act_1='', act_2=''):
        self.act_ar = []

        self.act_1 = StringVar()
        act_lable = ttk.Label(parent, text='Action: '+ str(id)).grid()
        act_1_op = ['go to', 'click', 'wait', 'quit']

        self.comb_1 = ttk.Combobox(parent, textvariable=self.act_1) #the first level entry combox
        self.comb_1.set(act_1)
        self.comb_1['values'] = act_1_op
        self.comb_1.grid()
        self.add_act(self.creat_act_el(self.act_1, 0))

        self.act_2 = StringVar()
        self.act_2.set(act_2)
        self.entry_2 = ttk.Entry(parent, textvariable=self.act_2).grid()
        self.add_act(self.creat_act_el(self.act_2, 1))

    def clean(self, frame): #func to clean a frame NotInUseYet!
        for widget in frame.winfo_children():
            widget.destroy()

    def creat_act_el(self, act, level):
        return {
            'str' : act, #the actual string of the act
            'level' : level #and the level of it(first is 'go to', 'click'... and second is the links and selectors...)
        }

    def add_act(self, act):
        try:
            self.act_ar[act['level']] = act
        except:
            self.act_ar.append(act)
    
    def ret_str(self):
        stri = ''
        for i in self.act_ar:
            print(i['str'].get())
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
        n.add(self.main_tab, text='New routin')

        self.rout_name = StringVar()
        ttk.Entry(self.main_tab, textvariable=self.rout_name).grid()
        ttk.Button(self.main_tab ,text='Add action', command=self.add_action).grid() #button that adds an action frame
        self.act_frame = ttk.Frame(self.main_tab).grid()

        ttk.Button(self.main_tab, text='submit', command=self.submit).grid()

        #routins tab
        self.rout_tab = ttk.Frame(n)
        self.rout_tab['padding'] = 20
        n.add(self.rout_tab, text='Routins')

        self.routings = []
        rout_id = 0
        for name in self.link:
            print(name)
            self.routings.append(routin(name, self.link[name], self.rout_tab, rout_id))
            rout_id += 2

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
        self.actions.append(actionOb(self.main_tab, self.id))
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
        self.link[self.rout_name.get()] = rout
        self.dump('li')


ap = app()