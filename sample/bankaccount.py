class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''


    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
