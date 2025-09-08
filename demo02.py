class BankBalance:
    def __init__(self, holder, balance):
        self.holder = holder
        self.__balance = balance

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print('Error')

    def getBalance(self):
        return self.__balance


account = BankBalance('Ace', 2000)
account.withdraw(400)
print(account.getBalance())
# print(account.__balance)
account.withdraw(600)
print(account.getBalance())