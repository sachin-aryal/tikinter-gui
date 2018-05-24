class BankAccount():
    def __init__(self):
        """Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list."""
        self.account_number = 0
        self.pin_number = ""
        self.balance = 0.0
        self.interest_rate = 8.0
        self.transaction_list = list()

    def deposit_funds(self, amount):
        """Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float."""
        try:
            amount = float(amount)
            self.balance += amount
        except ValueError:
            raise ValueError("Amount should be number")
        except Exception as ex:
            raise Exception(str(ex))

    def withdraw_funds(self, amount):
        """Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account."""
        try:
            amount = float(amount)
            if amount <= float(self.balance):
                self.balance -= amount
            else:
                raise Exception("Withdraw amount is higher than account balance.")
        except ValueError:
            raise ValueError("Amount should be number")
        except Exception as ex:
            raise Exception(str(ex))

    def get_transaction_string(self):
        """Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line."""
        transaction_string = ""
        for transaction in self.transaction_list:
            transaction_string += transaction[0]+":"+str(transaction[1])+"\n"
        return transaction_string

    def save_to_file(self):
        """Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function."""
        with open(self.account_number+".txt", "w") as account_file:
            account_file.write(self.account_number+"\n")
            account_file.write(self.pin_number+"\n")
            account_file.write(str(self.balance)+"\n")
            account_file.write(str(self.interest_rate)+"\n")
            for transaction in self.transaction_list:
                account_file.write(transaction[0]+"\n")
                account_file.write(str(transaction[1])+"\n")

    def reset(self):
        """
        Reset all attributes to their initial state
        :return: 
        """
        self.account_number = 0
        self.pin_number = ""
        self.balance = 0.0
        self.interest_rate = 8.0
        self.transaction_list = list()
