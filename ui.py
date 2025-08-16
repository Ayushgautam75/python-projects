import tkinter as tk
from tkinter import messagebox
import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("no such file exist")
    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        num = ''.join(random.choices(string.digits, k=8))
        return num

    def create_account(self, name, age, email, pin):
        info = {
            "name": name,
            "age": int(age),
            "email": email,
            "pin": int(pin),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            return None
        else:
            Bank.data.append(info)
            Bank.__update()
            return info

    def deposit(self, accnumber, pin, amount):
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == int(pin)]
        if not userdata:
            return None
        else:
            if int(amount) > 10000 or int(amount) <= 0:
                return False
            userdata[0]['balance'] += int(amount)
            Bank.__update()
            return userdata[0]['balance']

    def withdraw(self, accnumber, pin, amount):
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == int(pin)]
        if not userdata:
            return None
        else:
            if userdata[0]['balance'] < int(amount):
                return False
            userdata[0]['balance'] -= int(amount)
            Bank.__update()
            return userdata[0]['balance']

    def details(self, accnumber, pin):
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == int(pin)]
        if not userdata:
            return None
        return userdata[0]


# -------- GUI -------- #
bank = Bank()

root = tk.Tk()
root.title("Bank Management System")
root.geometry("500x500")


def create_account():
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    pin = entry_pin.get()

    info = bank.create_account(name, age, email, pin)
    if info:
        messagebox.showinfo("Success", f"Account Created!\nYour Account No: {info['accountNo.']}")
    else:
        messagebox.showerror("Error", "Account creation failed. Age must be >=18 & Pin must be 4 digits")


def deposit_money():
    acc = entry_acc.get()
    pin = entry_acc_pin.get()
    amount = entry_amount.get()
    result = bank.deposit(acc, pin, amount)
    if result is None:
        messagebox.showerror("Error", "Account not found")
    elif result is False:
        messagebox.showerror("Error", "Deposit must be between 1-10000")
    else:
        messagebox.showinfo("Success", f"Deposited! New Balance: {result}")


def withdraw_money():
    acc = entry_acc.get()
    pin = entry_acc_pin.get()
    amount = entry_amount.get()
    result = bank.withdraw(acc, pin, amount)
    if result is None:
        messagebox.showerror("Error", "Account not found")
    elif result is False:
        messagebox.showerror("Error", "Insufficient balance")
    else:
        messagebox.showinfo("Success", f"Withdrawn! New Balance: {result}")


def show_details():
    acc = entry_acc.get()
    pin = entry_acc_pin.get()
    result = bank.details(acc, pin)
    if result is None:
        messagebox.showerror("Error", "Account not found")
    else:
        details = "\n".join([f"{k}: {v}" for k, v in result.items()])
        messagebox.showinfo("Account Details", details)


# -------- Widgets -------- #
tk.Label(root, text="Create Account", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Age").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Pin (4 digit)").pack()
entry_pin = tk.Entry(root, show="*")
entry_pin.pack()

tk.Button(root, text="Create Account", command=create_account, bg="green", fg="white").pack(pady=10)

tk.Label(root, text="Account No").pack()
entry_acc = tk.Entry(root)
entry_acc.pack()

tk.Label(root, text="Pin").pack()
entry_acc_pin = tk.Entry(root, show="*")
entry_acc_pin.pack()

tk.Label(root, text="Amount").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Deposit", command=deposit_money, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Withdraw", command=withdraw_money, bg="red", fg="white").pack(pady=5)
tk.Button(root, text="Show Details", command=show_details, bg="purple", fg="white").pack(pady=5)

root.mainloop()
