"""A simple ATM demonstration using Tkinter and ValueError."""
import tkinter as tk
from tkinter import ttk

PIN = "1234"
balance = 10000  # Whole rupees; resets when the program restarts.
logged_in = False


def show_message(text, error=False):
    message.config(text=text, fg="#b42318" if error else "#176447")


def login():
    global logged_in
    try:
        entered_pin = pin_entry.get().strip()
        if not entered_pin:
            raise ValueError("Please enter your PIN.")
        if entered_pin != PIN:
            raise ValueError("Invalid PIN. Please try again.")
        logged_in = True
        for widget in account_widgets:
            widget.config(state="normal")
        pin_entry.delete(0, tk.END)
        pin_entry.config(state="disabled")
        login_button.config(state="disabled")
        amount_entry.focus_set()
        show_message("Login successful. Choose an operation.")
    except ValueError as error:
        show_message(str(error), error=True)


def check_balance():
    if logged_in:
        show_message(f"Available balance: ₹{balance:,}")
    else:
        show_message("Please log in first.", error=True)


def transact(operation):
    global balance
    try:
        if not logged_in:
            raise ValueError("Please log in first.")
        text = amount_entry.get().strip()
        if not text:
            raise ValueError("Please enter an amount.")
        try:
            amount = int(text)
        except ValueError:
            raise ValueError("Enter a whole number of rupees.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if operation == "Withdraw":
            if amount > balance:
                raise ValueError("Insufficient balance.")
            balance -= amount
            result = "Withdrawal successful"
        else:
            balance += amount
            result = "Deposit successful"
        show_message(f"{result}: ₹{amount:,}\n"
                     f"Available balance: ₹{balance:,}")
        amount_entry.delete(0, tk.END)
    except ValueError as error:
        show_message(str(error), error=True)


def create_app():
    global pin_entry, amount_entry, login_button, message
    global account_widgets
    root = tk.Tk()
    root.title("ATM Withdrawal Program")
    root.geometry("510x530")
    root.resizable(False, False)
    root.configure(bg="#f3f6fa")
    root.option_add("*Font", ("Segoe UI", 11))
    frame = ttk.Frame(root, padding=26)
    frame.pack(fill="both", expand=True, padx=14, pady=14)
    ttk.Label(frame, text="ATM WITHDRAWAL PROGRAM",
              font=("Segoe UI", 17, "bold")).pack(pady=(0, 6))
    ttk.Label(frame, text="Python Programming | Mini-project").pack()
    ttk.Separator(frame).pack(fill="x", pady=18)
    ttk.Label(frame, text="Enter PIN").pack(anchor="w")
    pin_entry = ttk.Entry(frame, show="*", justify="center")
    pin_entry.pack(fill="x", pady=(5, 8))
    login_button = ttk.Button(frame, text="Login", command=login)
    login_button.pack(fill="x")
    ttk.Label(frame, text="Amount (whole rupees)").pack(
        anchor="w", pady=(16, 5))
    amount_entry = ttk.Entry(frame, state="disabled")
    amount_entry.pack(fill="x")
    actions = ttk.Frame(frame)
    actions.pack(fill="x", pady=12)
    account_widgets = [amount_entry]
    commands = [("Check Balance", check_balance),
                ("Withdraw", lambda: transact("Withdraw")),
                ("Deposit", lambda: transact("Deposit"))]
    for column, (label, command) in enumerate(commands):
        button = ttk.Button(actions, text=label, command=command,
                            state="disabled")
        button.grid(row=0, column=column, padx=3, sticky="ew")
        actions.columnconfigure(column, weight=1)
        account_widgets.append(button)
    message = tk.Label(frame, text="Welcome! Please log in.",
                       wraplength=400, height=3, bg="#e8eef5",
                       fg="#334155", font=("Segoe UI", 11))
    message.pack(fill="x", pady=(0, 12))
    ttk.Button(frame, text="Exit", command=root.destroy).pack(fill="x")
    ttk.Label(frame, text="Demonstration only | No real transactions",
              font=("Segoe UI", 9)).pack(pady=(12, 0))
    pin_entry.focus_set()
    return root


if __name__ == "__main__":
    create_app().mainloop()
