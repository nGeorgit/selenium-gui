from ast import main
from cgitb import text
from curses import window
from tkinter import *
from tkinter import ttk
import json
from backend import sele

class fram():
    def __init__(self) -> None:
        pass
    def clean(self, frame):
        for i in frame.grid_slaves():
            i.destroy()

class rout_cr():
    def __init__(self, parent, name=''):
        self.parent = parent

        self.id = 0
        self.actions = []

        with open('link.json') as f:
            self.link = json.load(f)        

        self.rout_name = StringVar()
        self.rout_name.set(name)
        ttk.Entry(self.parent, textvariable=self.rout_name).grid()
        ttk.Button(self.parent ,text='Add action', command=self.add_action).grid() #button that adds an action frame
        self.act_frame = ttk.Frame(self.parent).grid()

        ttk.Button(self.parent, text='submit', command=self.submit).grid()

    def dump(self, loc):
        with open('link.json', 'w') as f:
            json.dump(self.link, f, indent=2)

    def add_action(self, act_1='', act_2=''):
        self.actions.append(actionOb(self.parent, self.id, act_1=act_1, act_2=act_2))
        self.id = self.id + 1

    def submit(self):
        rout = []
        for i in self.actions:
            rout.append(i.ret_str())
            print(i.ret_str())
        self.link[self.rout_name.get()] = rout
        self.dump('li')

class routin(fram): #routin ob
    def __init__(self, name, rout, parent, id, edit_fr):
        self.edit_fr = edit_fr
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
        self.clean(self.edit_fr)

        ed = rout_cr(self.edit_fr, name=self.name)
        id = 0
        for i in self.rout:
            act = i.split('|')
            print(act)
            ed.add_action(act_1=act[0], act_2=act[1])
            id += 1

class actionOb(): #action ob
    def __init__(self, parent, id, act_1='', act_2=''):
        self.act_ar = []

        self.parent = parent

        self.id = StringVar()
        self.id.set(str(id))
        print(self.id.get())
        self.act_lable = ttk.Label(self.parent, textvariable=self.id)
        self.act_lable.grid()
        act_1_op = ['go to', 'click', 'wait', 'quit']

        self.act_1 = StringVar()
        self.comb_1 = ttk.Combobox(self.parent, textvariable=self.act_1) #the first level entry combox
        self.comb_1.set(act_1)
        self.comb_1['values'] = act_1_op
        self.comb_1.grid()
        self.add_act(self.creat_act_el(self.act_1, 0))

        self.act_2 = StringVar()
        self.act_2.set(act_2)
        self.entry_2 = ttk.Entry(self.parent, textvariable=self.act_2)
        self.entry_2.grid()
        self.add_act(self.creat_act_el(self.act_2, 1))

        self.del_bt = ttk.Button(self.parent, text='Delete', command=self.clean)
        self.del_bt.grid()

    def clean(self): #func to clean a frame NotInUseYet!
        self.act_lable.destroy()
        self.comb_1.destroy()
        self.entry_2.destroy()
        self.del_bt.destroy()

        for i in self.parent.grid_slaves():
            i.id_dec()

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

    def id_dec(self):
        self.id.set(str(int(self.id.get()) - 1))

class app():
    def __init__(self):


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

        rout_crdf = rout_cr(self.main_tab)

        #routins tab
        self.rout_tab = ttk.Frame(n)
        self.rout_tab['padding'] = 20
        n.add(self.rout_tab, text='Routins')
        self.edit_fr = ttk.Frame(self.rout_tab)

        self.routings = []
        rout_id = 0

        for name in self.link:
            print(name)
            self.routings.append(routin(name, self.link[name], self.rout_tab, rout_id, self.edit_fr))
            rout_id += 2

        
        self.edit_fr.grid(columnspan=2)
        
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

    def dump(self, loc):
        if loc == 'set':
            with open('settings.json', 'w') as f:
                json.dump(self.sett, f, indent=2)


ap = app()