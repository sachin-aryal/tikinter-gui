import unittest

from bankaccount import BankAccount


class TestBankAcount(unittest.TestCase):
    def setUp(self):
        # Create a test BankAccount object
        self.account = BankAccount()

        # Provide it with some property values        
        self.account.balance = 1000.0

    def test_legal_deposit_works(self):
        # Your code here to test that depsositing money using the account's
        # 'deposit_funds' function adds the amount to the balance.
        previous_balance = self.account.balance
        self.account.deposit_funds(2000)
        self.assertGreater(self.account.balance, previous_balance)

    def test_illegal_deposit_raises_exception(self):
        # Your code here to test that depositing an illegal value (like 'bananas'
        # or such - something which is NOT a float) results in an exception being
        # raised.
        try:
            self.account.deposit_funds("bananas")
        except ValueError:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised:'+str(e))

    def test_legal_withdrawal(self):
        # Your code here to test that withdrawing a legal amount subtracts the
        # funds from the balance.
        previous_balance = self.account.balance
        self.account.withdraw_funds(100)
        self.assertLess(self.account.balance, previous_balance)

    def test_illegal_withdrawal(self):
        # Your code here to test that withdrawing an illegal amount (like 'bananas'
        # or such - something which is NOT a float) raises a suitable exception.
        try:
            self.account.withdraw_funds("apple")
        except ValueError:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised:'+str(e))

    def test_insufficient_funds_withdrawal(self):
        # Your code here to test that you can only withdraw funds which are available.
        # For example, if you have a balance of 500.00 dollars then that is the maximum
        # that can be withdrawn. If you tried to withdraw 600.00 then a suitable exception
        # should be raised and the withdrawal should NOT be applied to the account balance
        # or the account's transaction list.
        try:
            self.account.withdraw_funds(5000000)
        except Exception as e:
            pass


# Run the unit tests in the above test case
if __name__ == '__main__':
    unittest.main()
