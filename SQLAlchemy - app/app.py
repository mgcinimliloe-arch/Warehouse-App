from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# -------------------------
# Flask App Setup
# -------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# Database Models
# -------------------------
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # purchase, sale, balance
    product_name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)

# -------------------------
# Initialize Database
# -------------------------
with app.app_context():
    db.create_all()
    if Account.query.first() is None:
        db.session.add(Account(balance=0.0))
        db.session.commit()

# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    account = Account.query.first()
    products = Product.query.all()
    error = None

    if request.method == "POST":
        form_type = request.form.get("form_type")
        try:
            if form_type == "purchase":
                name = request.form["purchaseName"]
                price = float(request.form["purchasePrice"])
                quantity = int(request.form["purchaseQuantity"])
                total_cost = price * quantity
                if total_cost > account.balance:
                    raise ValueError("Insufficient funds for purchase.")

                product = Product.query.filter_by(name=name).first()
                if product:
                    product.quantity += quantity
                    product.price = price
                else:
                    product = Product(name=name, price=price, quantity=quantity)
                    db.session.add(product)

                account.balance -= total_cost
                db.session.add(Transaction(type='purchase', product_name=name, price=price, quantity=quantity, total=total_cost))

            elif form_type == "sale":
                name = request.form["saleName"]
                price = float(request.form["salePrice"])
                quantity = int(request.form["saleQuantity"])

                product = Product.query.filter_by(name=name).first()
                if not product or product.quantity < quantity:
                    raise ValueError("Not enough stock to sell.")

                product.quantity -= quantity
                account.balance += price * quantity
                db.session.add(Transaction(type='sale', product_name=name, price=price, quantity=quantity, total=price*quantity))

            elif form_type == "balance":
                operation = request.form["operationType"]
                amount = float(request.form["balanceAmount"])
                if operation == "add":
                    account.balance += amount
                    db.session.add(Transaction(type='balance', total=amount))
                elif operation == "subtract":
                    account.balance -= amount
                    db.session.add(Transaction(type='balance', total=-amount))
                else:
                    raise ValueError("Invalid balance operation.")

            db.session.commit()
            return redirect(url_for("index"))

        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            error = str(e)

    stock_level = sum(p.quantity for p in products)
    return render_template("index.html", stock_level=stock_level, account_balance=account.balance, error_message=error)

# -------------------------
# History page
# -------------------------
@app.route("/history/")
@app.route("/history/<int:line_from>/<int:line_to>/")
def history(line_from=None, line_to=None):
    transactions = Transaction.query.order_by(Transaction.id).all()
    if line_from is not None and line_to is not None:
        transactions = transactions[line_from:line_to]
    return render_template("history.html", history=transactions)

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
