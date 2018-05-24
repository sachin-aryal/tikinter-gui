class BankAccount():
    def __init__(self):
        """Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list."""
        self.account_number = 0
        self.pin_number = ""
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []

    def deposit_funds(self, amount):
        """Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float."""
        try:
            self.balance = self.balance + float(amount)
        except ValueError:
            raise ValueError("entered amount is not a number.")

    def withdraw_funds(self, amount):
        """Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account."""
        try:
            temp_amount = float(amount)
            if temp_amount <= float(self.balance):
                self.balance -= temp_amount
            else:
                raise Exception("withdraw amount requested is higher than your account balance")
        except ValueError:
            raise ValueError("entered amount is not a number.")
        except Exception as ex:
            raise Exception(str(ex))

    def get_transaction_string(self):
        """Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line."""
        transaction_string = ''
        for each_transaction in self.transaction_list:
            transaction_string = transaction_string + each_transaction[0]+":"+str(each_transaction[1])+"\n"
        return transaction_string

    def save_to_file(self):
        """Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function."""
        with open(str(self.account_number)+".txt", "w") as file_account:
            file_account.write(str(self.account_number)+"\n")
            file_account.write(self.pin_number+"\n")
            file_account.write(str(self.balance)+"\n")
            file_account.write(str(self.interest_rate)+"\n")
            for each_transaction in self.transaction_list:
                file_account.write(each_transaction[0]+"\n")
                file_account.write(str(each_transaction[1])+"\n")

    def reset(self):
        """
        Reset all attributes to their initial state
        :return: 
        """
        self.account_number = 0
        self.pin_number = ""
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []
