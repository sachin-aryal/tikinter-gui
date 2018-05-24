# import tkinter as tk
# from tkinter import *
# from project1 import main
#
# win = tk.Tk()
# win.geometry("380x640")
# # Set window title here to 'FedUni Banking'
# win.title("FedUni Banking")
#
# fed_ui_banking = tk.Label(win, text="FedUni Banking", font=("Helvetica", 24))
# fed_ui_banking.grid(column=0, row=0, sticky=N + S + E + W)
#
# # ----- Row 1 -----
#
# # Account number label here
# main.account_number_label["text"] = "23423432432423423"
# main.account_number_label.grid(column=0, row=1, sticky="nsew")
# # Balance label here
# main.balance_label.grid(column=1, row=1, sticky="nsew")
# # Log out button here
# logout_button = tk.Button(text="Logout")
# logout_button.grid(column=2, row=1, sticky="nsew")
#
# # ----- Row 2 -----
#
# # Amount label here
# amount_label = tk.Label(text="Amount")
# amount_label.grid(column=0, row=2)
# # Amount entry here
# main.amount_entry.grid(column=1, row=2)
# # Deposit button here
# deposit_button = tk.Button(text="Deposit")
# deposit_button.grid(column=2, row=2)
# # Withdraw button here
# winthdraw_button = tk.Button(text="Withdraw")
# winthdraw_button.grid(column=3, row=2)
#
# for i in range(0, 5):
#     button = tk.Button(win, text=i)
#     button.grid(row=3, column=i)
#
# # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
# for column in range(0, 5):
#     win.columnconfigure(column, weight=1)
#
# for row in range(0, 1):
#     win.rowconfigure(row, weight=1)
#
# win.mainloop()