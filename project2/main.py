import matplotlib

matplotlib.use("TkAgg")
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import tkinter as tk
from bankaccount import BankAccount
from tkinter import *
from tkinter import messagebox

win = tk.Tk()
# Set window size to 480x640
win.geometry("480x640")
# Set window title here to 'FedUni Banking'
win.title("FedUni Banking")
# The account number label
acpnlabel = tk.Label(win, text="Account Number/Pin Number", wraplength=70)
# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()
# Pin number label
acn_label = tk.Label(win, text="Account Number", wraplength=80)
# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, text='PIN Number', show="*", textvariable=pin_number_var)
# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, text="Balance: $0.00", wraplength=80)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry_var = tk.DoubleVar()
amount_entry = tk.Entry(win, textvariable=amount_entry_var)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=18)

# The bank account object we will work with
account = BankAccount()


# ---------- Button Handlers for Login Screen ----------


def clear_pin_entry(event):
    """Function to clear the PIN number entry when the Clear / Cancel button is clicked."""
    # Clear the pin number entry here
    pin_number_var.set("")


def handle_pin_button(event):
    """Function to add the number of the button clicked to the PIN number entry via its associated variable."""

    # Limit to 4 chars in length
    pin_number = pin_number_var.get()
    if len(pin_number) == 4:
        tk.messagebox.showerror(title="Error", message="pin number should be 4 digits")
        return
    # Set the new pin number on the pin_number_var
    pin_number = pin_number_var.get()
    button = event.widget
    pin_number = pin_number + str(button["text"])
    pin_number_var.set(pin_number)


def read_accoun_file(file_name):
    with open(file_name, 'r') as account_file:
        data = account_file.read().splitlines()
        return data


def initialize_transaction_list(data):
    transaction_list = []
    for i in range(4, len(data), 2):
        transaction_tuple = (data[i], data[i + 1])
        transaction_list.append(transaction_tuple)
    return transaction_list


def log_in(event):
    """Function to log in to the banking system using a known account number and PIN."""

    acn = account_number_var.get()
    if len(acn) == 0:
        # Reset account object
        account.reset()
        tk.messagebox.showerror(title="Error", message="Please insert account number.")
        return
    pin_number = pin_number_var.get()
    if len(pin_number) != 4:
        tk.messagebox.showerror(title="Error", message="pin number should be 4 digits")
        return
    file_name = acn + ".txt"
    if os.path.isfile(file_name):
        # Try to open the account file for reading
        # Open the account file for reading
        data = read_accoun_file(file_name)
        if (len(data)) >= 6:
            # First line is account number
            # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
            if pin_number != data[1]:
                # Reset account object
                account.reset()
                tk.messagebox.showerror(title="Error", message="Please enter valid pin number.")
                return

            # Read third and fourth lines (balance and interest rate)
            balance = data[2]
            interest_rate = data[3]

            # Attempt to read a line from the account file, break if we've hit the end of the file. If we read a
            # line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list
            transaction_list = initialize_transaction_list(data)
        else:
            balance = 0.0
            interest_rate = 12.0
            transaction_list = []
    else:
        # Create the filename from the entered account number with '.txt' on the end
        open(file_name, "w")
        balance = 0.0
        interest_rate = 12.0
        transaction_list = []

    account.account_number = acn
    account.pin_number = pin_number
    account.balance = float(balance)
    account.interest_rate = float(interest_rate)
    account.transaction_list = transaction_list
    balance_label["text"] = "Balance: $" + str(balance)
    pin_number_var.set("")
    remove_all_widgets()
    create_account_screen()


# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''

    # Save the account with any new transactions
    account.save_to_file()
    # Reset the bank acount object
    account.reset()
    # Reset the account number and pin to blank
    account_number_var.set("")
    pin_number_var.set("")
    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()


def perform_deposit():
    """Function to add a deposit for the amount in the amount entry to the
       account's transaction list."""

    # Get the cash amount to deposit. Note: We check legality inside account's deposit method
    try:
        deposit_amount = amount_entry_var.get()
        account.deposit_funds(deposit_amount)
    except Exception as ex:
        tk.messagebox.showerror(title="Error", message=str(ex))
        return
    transaction_tuple = ("Deposit", deposit_amount)
    account.transaction_list.append(transaction_tuple)
    account.save_to_file()

    # Deposit funds

    # Update the transaction widget with the new transaction by calling account.get_transaction_string()
    transaction_string = account.get_transaction_string()
    # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
    #       contents, and finally configure back to state='disabled' so it cannot be user edited.
    transaction_text_widget.config(state=NORMAL)
    transaction_text_widget.delete("1.0", END)
    transaction_text_widget.insert(END, transaction_string)
    transaction_text_widget.config(state=DISABLED)
    transaction_text_widget.see("end")
    # Change the balance label to reflect the new balance
    balance_label["text"] = "Balance: $" + str(account.balance)
    # Clear the amount entry
    amount_entry_var.set("")
    # Update the interest graph with our new balance
    plot_interest_graph()


def perform_withdrawal():
    """Function to withdraw the amount in the amount entry from the account balance and add an entry to the 
    transaction list. """

    # Try to increase the account balance and append the deposit to the account file
    try:
        withdraw_amount = amount_entry_var.get()
        account.withdraw_funds(withdraw_amount)  # Will increase the account balance for valida amount
    except Exception as ex:
        tk.messagebox.showerror(title="Error", message=str(ex))
        return

    # Withdraw funds
    row = ("Withdrawal", withdraw_amount)
    account.transaction_list.append(row)
    account.save_to_file()

    # Update the transaction widget with the new transaction by calling account.get_transaction_string()
    transaction_string = account.get_transaction_string()
    # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
    #       contents, and finally configure back to state='disabled' so it cannot be user edited.
    transaction_text_widget.config(state=NORMAL)
    transaction_text_widget.delete("1.0", END)
    transaction_text_widget.insert(END, transaction_string)
    transaction_text_widget.config(state=DISABLED)
    transaction_text_widget.see("end")

    # Change the balance label to reflect the new balance
    balance_label["text"] = "Balance: $" + str(account.balance)
    # Clear the amount entry
    amount_entry_var.set("")
    # Update the interest graph with our new balance
    plot_interest_graph()


# ---------- Utility functions ----------

def remove_all_widgets():
    """Function to remove all the widgets from the window."""
    for widget in win.winfo_children():
        widget.grid_remove()


def plot_interest_graph():
    """Function to plot the cumulative interest for the next 12 months here."""

    # YOUR CODE to generate the x and y lists here which will be plotted

    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    principle_amount = account.balance
    rate = account.interest_rate / 100.0
    n = 12.0
    t = 0.083  # (1/12)
    x = []
    y = []
    for i in range(1, 13):
        inner = 1 + (rate / n)
        pwr = 1  # nt = 12*1/12 = 1
        A = (principle_amount * math.pow(inner, pwr))
        principle_amount = A
        x.append(i)
        y.append(A)
    figure = Figure(figsize=(5, 2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()

    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    """Function to create the login screen."""

    # ----- Row 0 -----

    # 'FedUni Banking' label here. Font size is 32.

    fed_ui_banking = tk.Label(win, text="FedUni Banking", font=("Helvetica", 32))
    fed_ui_banking.grid(column=1, row=0, sticky=N + S + E + W)

    # ----- Row 1 -----

    # Acount Number / Pin label here
    acpnlabel.grid(column=0, row=1, sticky=N + S + E + W)

    # Account number entry here
    account_number_entry.grid(column=1, row=1)

    # Account pin entry here
    account_pin_entry.grid(column=2, row=1)

    # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    index = 0
    for i in range(1, 4):
        button = tk.Button(win, text=i)
        button.bind("<Button-1>", handle_pin_button)
        button.grid(column=index, row=2)
        index += 1

    index = 0
    # ----- Row 3 -----
    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    for i in range(4, 7):
        button = tk.Button(win, text=i)
        button.bind("<Button-1>", handle_pin_button)
        button.grid(column=index, row=3)
        index += 1

    index = 0
    # ----- Row 4 -----
    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    for i in range(7, 10):
        button = tk.Button(win, text=i)
        button.bind("<Button-1>", handle_pin_button)
        button.grid(column=index, row=4)
        index += 1

    # ----- Row 5 -----
    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    button = tk.Button(win, text="Clear", bg='red', activebackground="red")
    button.bind("<Button-1>", clear_pin_entry)
    button.grid(column=0, row=5)

    # Button 0 here
    button = tk.Button(win, text=0)
    button.bind("<Button-1>", handle_pin_button)
    button.grid(column=1, row=5)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    button = tk.Button(win, text="Login", bg="green", activebackground="green")
    button.bind("<Button-1>", log_in)
    button.grid(column=2, row=5)

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    for column in range(0, 4):
        win.columnconfigure(column, weight=1)

    for row in range(0, 6):
        win.rowconfigure(row, weight=1)


def create_account_screen():
    """Function to create the account screen."""

    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    fed_ui_banking = tk.Label(win, text="FedUni Banking", font=("Helvetica", 24))
    fed_ui_banking.grid(column=1, row=0, sticky="nsew")

    # ----- Row 1 -----

    # Account number label here
    acn_label["text"] = "Account Number: " + account_number_var.get()
    acn_label.grid(column=0, row=1, sticky="nsew")
    # Balance label here
    balance_label.grid(column=1, row=1, sticky="nsew")
    # Log out button here
    logout_button = tk.Button(win, text="Logout", command=save_and_log_out)
    logout_button.grid(column=2, row=1, sticky="nsew")

    # ----- Row 2 -----

    # Amount label here
    amount_label = tk.Label(win, text="Amount")
    amount_label.grid(column=0, row=2)
    # Amount entry here
    amount_entry.grid(column=1, row=2)
    # Deposit button here
    deposit_button = tk.Button(win, text="Deposit", command=perform_deposit)
    deposit_button.grid(column=2, row=2)
    # Withdraw button here
    winthdraw_button = tk.Button(win, text="Withdraw", command=perform_withdrawal)
    winthdraw_button.grid(column=3, row=2)

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.


    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = tk.Scrollbar(win, command=transaction_text_widget.yview)

    transaction_string = account.get_transaction_string()
    transaction_text_widget.insert(END, transaction_string)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited. Note: Set the
    # yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget Note: When updating
    # the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    transaction_text_widget.config(state=DISABLED)
    transaction_text_widget.grid(column=0, row=3)

    # Now add the scrollbar and set it to change with the yview of the text widget
    text_scrollbar.grid(column=1, row=3, sticky='nsew')
    transaction_text_widget['yscrollcommand'] = text_scrollbar.set
    transaction_text_widget.see("end")

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    for column in range(0, 4):
        win.columnconfigure(column, weight=1)

    for row in range(0, 5):
        win.rowconfigure(row, weight=1)


# ---------- Display Login Screen & Start Main loop ----------
create_login_screen()
while True:
    try:
        win.mainloop()
        break
    except UnicodeDecodeError:
        pass
