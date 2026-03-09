from abc import ABC, abstractmethod
from datetime import datetime

class InsufficientFundsError(Exception):
    """Custom exception for overdrawing."""
    pass

class Account(ABC):
    def __init__(self, account_number: str, owner: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        # Encapsulation: Prefixing with __ makes it private
        self.__balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        self._log_transaction("Deposit", amount)
        print(f"Deposited ${amount}. New balance: ${self.__balance}")

    @abstractmethod
    def withdraw(self, amount: float):
        """Must be implemented by subclasses."""
        pass

    def get_balance(self):
        return self.__balance

    def _set_balance(self, amount: float):
        self.__balance = amount

    def _log_transaction(self, task, amount):
        self.transaction_history.append({
            "timestamp": datetime.now(),
            "type": task,
            "amount": amount,
            "balance_after": self.__balance
        })

class SavingsAccount(Account):
    def __init__(self, account_number, owner, balance, interest_rate=0.02):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount: float):
        # Savings might have stricter rules, but here we check basic funds
        if amount > self.get_balance():
            raise InsufficientFundsError(f"Short by ${amount - self.get_balance()}")
        
        new_balance = self.get_balance() - amount
        self._set_balance(new_balance)
        self._log_transaction("Withdrawal", amount)

    def apply_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        print(f"Interest applied: ${interest}")

class CheckingAccount(Account):
    def __init__(self, account_number, owner, balance, overdraft_limit=100.0):
        super().__init__(account_number, owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        # Polymorphism: This withdraw allows going into negative up to a limit
        available_funds = self.get_balance() + self.overdraft_limit
        if amount > available_funds:
            raise InsufficientFundsError("Transaction exceeds overdraft limit.")
        
        new_balance = self.get_balance() - amount
        self._set_balance(new_balance)
        self._log_transaction("Withdrawal", amount)
