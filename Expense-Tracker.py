import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------
# Basic configuration
# ------------------------------

DATA_FILE = "expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Amount"]


def load_expenses():
    """Load existing expenses from CSV, or create an empty table."""
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
    return df


def save_expenses(df):
    """Save current expenses back to CSV."""
    df.to_csv(DATA_FILE, index=False)


def add_expense(df):
    """Collect expense details from user and append to DataFrame."""
    print("\n--- Add New Expense ---")
    date_str = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")

    category = input("Category (Food, Travel, Bills, etc.): ").strip()
    description = input("Short description: ").strip()

    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError:
            print("Please enter a valid number for amount.")

    new_row = {
        "Date": date_str,
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_expenses(df)
    print("Expense added successfully!\n")
    return df


def view_expenses(df, n=10):
    """Show the last n expenses."""
    if df.empty:
        print("\nNo expenses recorded yet.\n")
        return

    print(f"\n--- Last {n} expenses ---")
    print(df.tail(n).to_string(index=False))
    print()


def monthly_summary(df):
    """Show total spent per month and overall statistics."""
    if df.empty:
        print("\nNo data available for summary.\n")
        return

    df["Date"] = pd.to_datetime(df["Date"])
    df["YearMonth"] = df["Date"].dt.to_period("M")
    monthly_totals = df.groupby("YearMonth")["Amount"].sum()

    print("\n--- Monthly Spending ---")
    print(monthly_totals)

    amounts = df["Amount"].values
    print("\n--- Overall Stats ---")
    print(f"Total spent : {amounts.sum():.2f}")
    print(f"Average spend: {np.mean(amounts):.2f}")
    print(f"Max spend    : {np.max(amounts):.2f}")
    print(f"Min spend    : {np.min(amounts):.2f}\n")


def plot_by_category(df):
    """Visualize total expense per category using matplotlib."""
    if df.empty:
        print("\nNo data to plot.\n")
        return

    category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 4))
    category_totals.plot(kind="bar", color="skyblue")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()


def plot_daily_trend(df):
    """Visualize daily spending trend."""
    if df.empty:
        print("\nNo data to plot.\n")
        return

    df["Date"] = pd.to_datetime(df["Date"])
    daily_totals = df.groupby("Date")["Amount"].sum()

    plt.figure(figsize=(8, 4))
    daily_totals.plot(kind="line", marker="o")
    plt.title("Daily Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    df = load_expenses()

    while True:
        print("==== Expense Tracker ====")
        print("1. Add expense")
        print("2. View recent expenses")
        print("3. Show monthly summary")
        print("4. Plot expenses by category")
        print("5. Plot daily trend")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            df = add_expense(df)
        elif choice == "2":
            view_expenses(df)
        elif choice == "3":
            monthly_summary(df)
        elif choice == "4":
            plot_by_category(df)
        elif choice == "5":
            plot_daily_trend(df)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main() 

