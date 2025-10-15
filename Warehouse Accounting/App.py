from flask import Flask, render_template, request, redirect, url_for
import os
import ast

app = Flask(__name__)
DATA_FILE = "data.txt"

# Load data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 0.0, "warehouse": {}, "operations": []}
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {"balance": 0.0, "warehouse": {}, "operations": []}
            return ast.literal_eval(content)
    except Exception as e:
        print("Error reading data file:", e)
        return {"balance": 0.0, "warehouse": {}, "operations": []}

# Save data to file
def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            f.write(str(data))
    except Exception as e:
        print("Error writing to data file:", e)

# Main page route
@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    error = None

    if request.method == "POST":
        form_type = request.form.get("form_type")
        try:
            # PURCHASE FORM
            if form_type == "purchase":
                name = request.form["purchaseName"]
                price = float(request.form["purchasePrice"])
                quantity = int(request.form["purchaseQuantity"])
                total_cost = price * quantity
                if total_cost > data["balance"]:
                    raise ValueError("Insufficient funds")
                if name in data["warehouse"]:
                    data["warehouse"][name]["quantity"] += quantity
                    data["warehouse"][name]["price"] = price
                else:
                    data["warehouse"][name] = {"price": price, "quantity": quantity}
                data["balance"] -= total_cost
                data["operations"].append(f"Purchase,{name},{price},{quantity},{total_cost}")

            # SALE FORM
            elif form_type == "sale":
                name = request.form["saleName"]
                price = float(request.form["salePrice"])
                quantity = int(request.form["saleQuantity"])
                if name not in data["warehouse"] or data["warehouse"][name]["quantity"] < quantity:
                    raise ValueError("Not enough stock to sell")
                data["warehouse"][name]["quantity"] -= quantity
                data["balance"] += price * quantity
                data["operations"].append(f"Sale,{name},{price},{quantity},{price*quantity}")

            # BALANCE CHANGE FORM
            elif form_type == "balance":
                operation = request.form["operationType"]
                amount = float(request.form["balanceAmount"])
                if operation == "add":
                    data["balance"] += amount
                elif operation == "subtract":
                    data["balance"] -= amount
                else:
                    raise ValueError("Invalid operation")
                data["operations"].append(f"Balance,{operation},{amount}")

            save_data(data)
            return redirect(url_for("index"))

        except Exception as e:
            error = str(e)

    return render_template("index.html",
                           stock_level=sum(item["quantity"] for item in data["warehouse"].values()),
                           account_balance=data["balance"],
                           error_message=error)

# History page route
@app.route("/history/")
@app.route("/history/<int:line_from>/<int:line_to>/")
def history(line_from=None, line_to=None):
    data = load_data()
    operations = data["operations"]

    if line_from is not None and line_to is not None:
        operations = operations[line_from:line_to]

    return render_template("history.html", history=operations)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
