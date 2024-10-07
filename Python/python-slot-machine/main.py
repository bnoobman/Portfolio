import json
import random

with open('settings.json', 'r') as f:
    config = json.load(f)

MAX_LINES = config['MAX_LINES']
MAX_BET = config['MAX_BET']
MIN_BET = config['MIN_BET']
ROWS = config['ROWS']
COLS = config['COLS']
symbol_count = config['symbol_count']
symbol_value = config['symbol_value']


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbols_count in symbols.items():
        for _ in range(symbols_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_spin(columns):
    # transpose the rows to columns
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print("")


def deposit():
    while True:
        amount = input("How much do you want to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please enter a positive number")
        else:
            print("Please enter a number")

    return amount


def get_number_lines():
    while True:
        lines = input("Enter number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Amount must be between 1 and " + str(MAX_LINES))
        else:
            print("Please enter a number")

    return lines


def get_bet():
    while True:
        amount = input("How much would you like to bet? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}")
        else:
            print("Please enter a number")

    return amount


def spin(balance):
    lines = get_number_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Your balance is only ${balance}. Not enough funds for bet.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")
    slots = get_slot_spin(ROWS, COLS, symbol_count)
    print_slot_spin(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines, sep="")
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"You have ${balance} available.")
        answer = input("Press ENTER to spin the wheel (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"Thanks for playing! You left with ${balance}")


if __name__ == '__main__':
    main()
