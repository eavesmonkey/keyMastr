#! /usr/bin/env python3
# Master key for passwords GUI
import tkinter as tk
from tkinter import ttk
import classes.vault

win = tk.Tk()
win.title('keyMastr')

# vars
accountName = tk.StringVar()
masterPassword = tk.StringVar()

#initiate vault
vault = classes.vault.Vault()

#functions
def populate():
    accounts = vault.getAllAccounts()
    for account in accounts:
        treeview.insert("" , "end", text=account, values=(accounts[account]['length'],accounts[account]['symbols']))

def addAccount():
    vault.addAccount(accountName.get())
    treeview.insert("" , "end", text=accountName.get(), values=("10",True))

def getPassword(masterPass, account):
    vault.getAccounPassword(masterPass,account)

def popup(event):
    item = treeview.identify('item',event.x,event.y)
    print(treeview.item(item,"text"))
    popup = tk.Toplevel()
    popup.wm_title("Window")
    ttk.Label(popup, text="Master password").grid(column=0, row=0)
    ttk.Entry(popup, width=20, textvariable=masterPassword).grid(column=0, row=1)
    ttk.Button(popup, text="Okay", command=lambda:getPassword( masterPassword.get(),treeview.item(item,"text"))).grid(column=0, row=2)

#add label
ttk.Label(win, text="Account name").grid(column=0, row=0)
ttk.Entry(win, width=12, textvariable=accountName).grid(column=0, row=1)

# add button
# Use lambda to pass vars: https://stackoverflow.com/questions/5767228/why-is-button-parameter-command-executed-when-declared
ttk.Button(win, text="Add account", command=addAccount).grid(column=1, row=1)
ttk.Button(win, text="Get password", command=getPassword).grid(column=2, row=1)

#account list
treeview = ttk.Treeview(win)
treeview.grid(column=0, row=2, columnspan=3)
treeview["columns"]=("length","symbols")
treeview.column("length", width=100)
treeview.column("symbols", width=100)
treeview.heading("length", text="Length")
treeview.heading("symbols", text="Symbols")
treeview.bind("<Double-1>", popup)

populate()

win.mainloop()
