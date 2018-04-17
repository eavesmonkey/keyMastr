#! /usr/bin/env python3
# Master key for passwords GUI
import tkinter as tk
from tkinter import ttk
import classes.vault

win = tk.Tk()

# OSX theme overrules styling. We need to set our own style.
style = ttk.Style()
style.theme_use('classic')
style.configure('green/black.TButton', foreground='green', background='black') # TButton only styles all btns.

win.title('keyMastr')
win.configure(background='#eee')

# vars
accountName = tk.StringVar()
masterPassword = tk.StringVar()
passwordSize = tk.IntVar()
passwordSize.set(10)
hasSymbols = tk.BooleanVar()
hasSymbols.set(True)
globSelectedItem = ''

# Initiate vault
vault = classes.vault.Vault()

# Functions
def populate():
    accounts = vault.getAllAccounts()
    for account in accounts:
        treeview.insert("" , "end", text=account, values=(accounts[account]['length'],accounts[account]['symbols']))

def addAccount():
    vault.addAccount(accountName.get(), passwordSize.get(), hasSymbols.get())
    treeview.insert("" , "end", text=accountName.get(), values=(passwordSize.get(),hasSymbols.get()))

def getPassword(masterPass, account):
    vault.getAccounPassword(masterPass,account)

def deleteAccount():
    vault.deleteAccount(globSelectedItem)
    treeview.delete(treeview.selection()[0])

def selectItem(event):
    global globSelectedItem
    item = treeview.identify('item',event.x,event.y)
    globSelectedItem = treeview.item(item,"text")
    print('select item' + globSelectedItem)

def popup(event):
    item = treeview.identify('item',event.x,event.y)
    print(str(event))
    popup = tk.Toplevel()
    popup.wm_title("Window")
    ttk.Label(popup, text="Master password").grid(column=0, row=0)
    ttk.Entry(popup, width=20, textvariable=masterPassword).grid(column=0, row=1)
    ttk.Button(popup, text="Okay", command=lambda:getPassword( masterPassword.get(),treeview.item(item,"text"))).grid(column=0, row=2)

#add label
ttk.Label(win, background="#eee", text="Account name").grid(column=0, row=0, sticky="w")
ttk.Entry(win, width=12, textvariable=accountName).grid(column=0, row=1)
ttk.Label(win, background="#eee", text="Password size").grid(column=1, row=0, sticky="w")
ttk.Entry(win, width=12, textvariable=passwordSize).grid(column=1, row=1)
ttk.Label(win, background="#eee", text="Allow symbols?").grid(column=2, row=0, columnspan=2, sticky="w")
ttk.Radiobutton(win, text="Yes", variable=hasSymbols, value="True").grid(column=2, row=1)
ttk.Radiobutton(win, text="No", variable=hasSymbols, value="False").grid(column=3, row=1)

# Add account button
# Use lambda to pass vars: https://stackoverflow.com/questions/5767228/why-is-button-parameter-command-executed-when-declared
ttk.Button(win, text="Add account", command=addAccount).grid(column=4, row=1)

# Account list
treeview = ttk.Treeview(win)
treeview.grid(column=0, row=3, columnspan=5)
treeview["columns"]=("length","symbols")
treeview.column("length", width=100, stretch = True)
treeview.column("symbols", width=100, stretch = True)
treeview.heading("length", text="Length")
treeview.heading("symbols", text="Symbols")
treeview.bind("<Double-1>", popup)
treeview.bind("<Button-1>", selectItem)

# Password button
ttk.Button(win, text="Get password", command=getPassword).grid(column=4, row=5)

# Delete button
ttk.Button(win, text="Delete rule", command=deleteAccount, style='green/black.TButton').grid(column=3, row=5)

populate()

win.mainloop()
