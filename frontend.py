from ast import main
from curses import window
from tkinter import *
from tkinter import ttk
import json
from backend import sele

class app():
    def __init__(self):

        se = sele()


        with open('settings.json') as f:
            self.sett = json.load(f)

        with open('link.json') as f:
            self.link = json.load(f)

        window = Tk()              #open the window
        window.title('Selenium Gui')

        n = ttk.Notebook(window) #creat the notebook and adding the tabs 
        n['padding'] = 15
        n.pack(expand = 1, fill ="both")

        self.main_tab = ttk.Frame(n) #home tab
        self.main_tab['padding'] = 20
        n.add(self.main_tab, text='Home')

        #get a link with an entry and open it
        self.link_var = StringVar()
        def submit_link():
            print(self.link_var.get())
            self.link['link'] = self.link_var.get()
            self.dump('li')

        def run():
            print(self.link['link'])
            se.get(self.link['link'])

        self.link_entry = ttk.Entry(self.main_tab, textvariable=self.link_var).grid()
        ttk.Button(self.main_tab, text="Submit", command=submit_link).grid()
        ttk.Button(self.main_tab, text="Run", command=run).grid()

        self.set_tab = ttk.Frame(n) #Settings tab
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
        elif loc == 'li':
            with open('link.json', 'w') as f:
                json.dump(self.link, f, indent=2)

ap = app()