def show_commands():
    print("\nAvailable commands:")
    print("  - balance")
    print("  - sale")
    print("  - purchase")
    print("  - account")
    print("  - list")
    print("  - warehouse")
    print("  - review")
    print("  - end")


def main():
    account_balance = 0.0
    warehouse = {}  # product -> {'price': float, 'quantity': int}
    operations = []

    show_commands()

    while True:
        command = input("\nEnter command: ").strip().lower()
        if command == "balance":
            try:
                amount = float(input("Enter amount to add/subtract (use negative for subtraction): "))
                comment = input("Comment: ")
                account_balance += amount
                operations.append({'command': 'balance', 'amount': amount, 'comment': comment})
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

        elif command == "sale":
            try:
                product = input("Product name: ").strip()
                price = float(input("Sale price per item: "))
                quantity = int(input("Quantity sold: "))

                if product in warehouse and warehouse[product]['quantity'] >= quantity:
                    warehouse[product]['quantity'] -= quantity
                    account_balance += price * quantity
                    operations.append({'command': 'sale', 'product': product, 'price': price, 'quantity': quantity})
                else:
                    print("Not enough inventory to complete the sale.")
            except ValueError:
                print("Invalid input. Please enter numeric values for price and quantity.")

        elif command == "purchase":
            try:
                product = input("Product name: ").strip()
                price = float(input("Purchase price per item: "))
                quantity = int(input("Quantity to purchase: "))
                total_cost = price * quantity

                if total_cost > account_balance:
                    print("Insufficient funds for this purchase.")
                else:
                    if product in warehouse:
                        warehouse[product]['quantity'] += quantity
                        warehouse[product]['price'] = price
                    else:
                        warehouse[product] = {'price': price, 'quantity': quantity}
                    account_balance -= total_cost
                    operations.append({'command': 'purchase', 'product': product, 'price': price, 'quantity': quantity})
            except ValueError:
                print("Invalid input. Please enter numeric values for price and quantity.")

        elif command == "account":
            print(f"Current account balance: {account_balance:.2f}")

        elif command == "list":
            if warehouse:
                print("Warehouse Inventory:")
                for product, data in warehouse.items():
                    print(f"  - {product}: {data['quantity']} units at {data['price']:.2f} each")
            else:
                print("Warehouse is empty.")

        elif command == "warehouse":
            product = input("Enter product name to check: ").strip()
            if product in warehouse:
                print(f"{product}: {warehouse[product]['quantity']} units at {warehouse[product]['price']:.2f} each")
            else:
                print("Product not found in warehouse.")

        elif command == "review":
            from_input = input("From index (leave empty for start): ").strip()
            to_input = input("To index (leave empty for end): ").strip()
            try:
                from_idx = int(from_input) if from_input else 0
                to_idx = int(to_input) if to_input else len(operations)

                if from_idx < 0 or to_idx > len(operations) or from_idx > to_idx:
                    print("Invalid index range.")
                else:
                    print("Reviewing operations:")
                    for i, op in enumerate(operations[from_idx:to_idx], start=from_idx):
                        print(f"{i}: {op}")
            except ValueError:
                print("Invalid indices. Please enter integer values or leave blank.")

        elif command == "end":
            print("Program terminated.")
            break

        else:
            print("Unknown command. Please try again.")

        show_commands()


if __name__ == "__main__":
    main()
