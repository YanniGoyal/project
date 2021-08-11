import sqlite3
from random import sample, randint


class Card:
    """Bank card data model"""
    id = 0        # INTEGER
    number = ''   # TEXT
    pin = ''      # TEXT
    balance = 0   # INTEGER DEFAULT 0


class Account(Card):
    """Customer account. Since, by condition, a client can have only one bank card, then client id = card id."""
    def __init__(self):
        self.id = randint(100000000, 999999999) * 10                        # casual generator of account identifier
        self.number = self.luhn(str(4000000000000000 + self.id))            # generator of 16 digits number of the card
        self.pin = ''.join(map(str, sample(range(1, 9), 4)))                # generator of random 4 digits pin code

    @staticmethod
    def luhn(num):
        """Adds a checksum to the bank card number using the Luhn algorithm.
        It takes the card number as a string value and returns the card number
        where the last digit replaced by the checksum."""
        num = num[:-1]  # drop the last digit
        list_num = []
        for c, n in enumerate(num, 1):
            n = int(n)
            if c % 2:  # multiply odd digits by 2
                n *= 2
            list_num.append(n-9 if n > 9 else n)  # subtract 9 to number over 9
        n = sum(list_num) % 10
        return num + str(10 - n if n else n)


class Menu:
    """Menu of the program"""
    def __init__(self):
        self.__choice = '0'

    def __repr__(self):
        return self.__choice

    def __eq__(self, other):
        return True if self.__choice == other else False

    @staticmethod
    def __show_main_menu():
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

    @staticmethod
    def __show_account_menu():
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

    def show_and_get_choice(self):
        if self.__choice.startswith('2'):
            self.__show_account_menu()
            self.__choice = f'{self.__choice[0]}.{input()}'
        else:
            self.__show_main_menu()
            self.__choice = input()

    def back_to_main(self):
        self.__choice = '0'


class DataBase:
    def __init__(self):
        # init ours database
        self.conn = sqlite3.connect("card.s3db")
        self.cursor = self.conn.cursor()
        # create the table
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS card 
            (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
        except sqlite3.OperationalError:
            pass

    def __del__(self):
        """Frivolous, complacent and unfounded confidence in a successful outcome. =)"""
        self.conn.close()

    def add(self, account):
        """Gets an instance of an account and add it to the database."""
        self.cursor.execute(f'INSERT INTO card VALUES ({account.id}, {account.number}, {account.pin}, "0")')
        self.conn.commit()

    def get(self, number):
        """Returns an instance of an account by card number. Otherwise returns None."""
        acc = self.cursor.execute(f'SELECT * FROM card WHERE number={number}').fetchone()
        if acc:
            account = Account()
            account.id, account.number, account.pin, account.balance = acc
            return account
        return None

    def get_all(self):
        """For tests"""
        return self.cursor.execute(f'SELECT * FROM card')

    def set_balance(self, number, balance):
        """Accepts the card number and sets the transferred balance for it."""
        self.cursor.execute(f'UPDATE card SET balance = {balance} WHERE number = {number}')
        self.conn.commit()

    def delete(self, number):
        """Deletes a card entry corresponding to the transmitted number."""
        self.cursor.execute(f'DELETE FROM card WHERE number = {number}')
        self.conn.commit()


class Banking:
    """Banking system"""
    def __init__(self):
        self.menu = Menu()
        self.db = DataBase()
        self.current_account = None

    def create_account(self):
        """Creates a customer account"""
        account = Account()
        self.db.add(account)  # add account to database
        # show the result according to the condition of the task
        print('\nYour card has been created')
        print('Your card number:')
        print(f'{account.number}')
        print('Your card PIN:')
        print(f'{account.pin}\n')

    def login(self):
        """Implements user login to the account.
        It asks the client for the card number and pin,
        then reconciles the received data with existing accounts.
        If the entered data is found, displays a menu for the account."""
        print('\nEnter your card number:')
        number = input()
        print('Enter your PIN:')
        pin = input()
        # check the correctness of the entered data
        account = self.db.get(number)
        if account:
            if account.pin == pin:
                print('\nYou have successfully logged in!\n')
                self.current_account = account
                return
        print('\nWrong card number or PIN!\n')
        self.menu.back_to_main()

    def show_balance(self):
        """Shows client balance"""
        print(f'\nBalance: {self.current_account.balance}\n')

    def add_income(self):
        """Adds the entered income to the balance of the current account."""
        print('\nEnter income:')
        income = int(input())
        self.current_account.balance += income
        self.db.set_balance(self.current_account.number, self.current_account.balance)
        print('Income was added!\n')

    def transfer(self):
        """It transfers money from the current account to another account.
        It asks the user for the account number to which he wants to transfer money.
        Checks the checksum of the entered account number according to the Luhn algorithm."""
        print('\nTransfer\nEnter card number:')
        number = input()
        if number == Account.luhn(number):
            account = self.db.get(number)
            if account:
                print('Enter how much money you want to transfer:')
                transfer = int(input())
                if self.current_account.balance >= transfer:
                    self.db.set_balance(number, account.balance + transfer)
                    print(f'>>> num: {self.current_account.number} bal: {self.current_account.balance}')
                    self.current_account.balance -= transfer
                    self.db.set_balance(self.current_account.number, self.current_account.balance)
                    print(f'>>> num: {self.current_account.number} bal: {self.current_account.balance}')
                    print('Success!\n')
                else:
                    print('Not enough money!\n')
            else:
                print('Such a card does not exist.\n')
        else:
            print('Probably you made mistake in the card number. Please try again!\n')

    def close_account(self):
        """Deletes the current account."""
        self.db.delete(self.current_account.number)
        print('\nThe account has been closed!\n')

    def log_out(self):
        """Shows the main menu, allowing the client to log in with another account."""
        print('\nYou have successfully logged out!\n')
        self.menu.back_to_main()

    def run(self):
        """Main logic of the program"""
        while True:
            self.menu.show_and_get_choice()
            # fulfill the wishes of the client
            if self.menu == '1':
                self.create_account()
            elif self.menu == '2':
                self.login()
            elif self.menu == '2.1':
                self.show_balance()
            elif self.menu == '2.2':
                self.add_income()
            elif self.menu == '2.3':
                self.transfer()
            elif self.menu == '2.4':
                self.close_account()
            elif self.menu == '2.5':
                self.log_out()
            else:
                print('\nBye!')
                break


if __name__ == '__main__':
    banking = Banking()
    banking.run()
