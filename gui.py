#! /usr/bin/env python3
# Master key for passwords GUI
import tkinter as tk
from tkinter import ttk, Frame, messagebox
import classes.vault

win = tk.Tk()

# OSX theme overrules styling. We need to set our own style.
style = ttk.Style()
style.theme_use('clam')
style.configure('green/black.TButton',
    foreground='black',
    background='green',
    activebackground='green',
    activeforeground='black',
    borderwidth='0') # TButton only styles all btns.
style.configure('TLabel', foreground='white', background='black')
style.configure('TEntry', borderwidth='0', padx='5', pady='5')
style.configure('TRadiobutton', foreground='white', background='black', borderwidth='0')

win.title('keyMastr')
win.configure(background='black', padx="20", pady="20")

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
    if accountName.get() != '':
        vault.addAccount(accountName.get(), passwordSize.get(), hasSymbols.get())
        treeview.insert("" , "end", text=accountName.get(), values=(passwordSize.get(),hasSymbols.get()))
    else:
        messagebox.showinfo("Adding account failed", "Please provide an account name")

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
    selectedItem = treeview.item(item,"text")

    if selectedItem != '':
        popup = tk.Toplevel()
        popup.wm_title("Window")
        popup.configure(background='black', padx="20", pady="20")
        ttk.Label(popup, text="Master password").grid(column=0, row=0, sticky="w")
        ttk.Entry(popup, show="*", width=20, textvariable=masterPassword).grid(column=0, row=1)
        ttk.Button(popup, text="Okay", command=lambda:getPassword( masterPassword.get(),selectedItem), style='green/black.TButton').grid(column=0, row=2)

# Frames
top_frame = Frame(win, bg='black', width=450, height=80)
top_frame.grid(row=0, sticky="ew", columnspan=5, pady=10)
bottom_frame = Frame(win, bg='black', width=450, height=80)
bottom_frame.grid(row=4, sticky="ew", columnspan=5, pady=10)

# Add account rule
ttk.Label(top_frame, text="Account name").grid(column=0, row=0, sticky="w")
ttk.Entry(top_frame, width=12, textvariable=accountName).grid(column=0, row=1)
ttk.Label(top_frame, text="Password size").grid(column=1, row=0, sticky="w")
ttk.Entry(top_frame, width=12, textvariable=passwordSize).grid(column=1, row=1)
ttk.Label(top_frame, text="Allow symbols?").grid(column=2, row=0, columnspan=2, sticky="w")
ttk.Radiobutton(top_frame, text="Yes", variable=hasSymbols, value="True").grid(column=2, row=1)
ttk.Radiobutton(top_frame, text="No", variable=hasSymbols, value="False").grid(column=3, row=1)

# Add account button
# Use lambda to pass vars: https://stackoverflow.com/questions/5767228/why-is-button-parameter-command-executed-when-declared
ttk.Button(top_frame, text="Add account", command=addAccount, style='green/black.TButton').grid(column=4, row=1)

# Account list
treeview = ttk.Treeview(win)
treeview.grid(column=0, row=3, columnspan=5, sticky="ew")
treeview["columns"]=("length","symbols")
treeview.column("length", width=100, stretch = True)
treeview.column("symbols", width=100, stretch = True)
treeview.heading("length", text="Length")
treeview.heading("symbols", text="Symbols")
treeview.bind("<Double-1>", popup)
treeview.bind("<Button-1>", selectItem)

# Password button
ttk.Button(bottom_frame, text="Get password", command=getPassword, style='green/black.TButton').grid(column=4, row=5)

# Delete button
ttk.Button(bottom_frame, text="Delete rule", command=deleteAccount, style='green/black.TButton').grid(column=3, row=5)

populate()

win.mainloop()
