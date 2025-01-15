import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fintracker.db")


@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Register new users

    # Clear any existing session
    session.clear()

    if request.method == "POST":
        # Retrieve form inputs
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        email = request.form.get("email").strip().lower()
        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Server-side validations
        if not first_name:
            return apology("must provide first name", 400)

        if not last_name:
            return apology("must provide last name", 400)

        if not email:
            return apology("must provide email", 400)

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        # Ensure email is unique
        existing_email = db.execute("SELECT id FROM users WHERE email = ?", email)
        if existing_email:
            return apology("email already registered", 400)

        # Ensure username is unique
        existing_username = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing_username:
            return apology("username already taken", 400)

        # Insert the new user into the database
        try:
            db.execute("""
                INSERT INTO users (first_name, last_name, email, username, hash)
                VALUES (?, ?, ?, ?, ?)
            """, first_name, last_name, email, username, generate_password_hash(password))
        except Exception as e:
            return apology(f"unexpected error: {e}", 500)

        # Redirect user to sign-in page
        return redirect("/signin")

    else:
        return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/budget")

    else:
        return render_template("signin.html")


@app.route('/careers', methods=["GET", "POST"])
def careers():
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("name").strip()
        email = request.form.get("email").strip().lower()
        message = request.form.get("message").strip()

        # Server-side validation
        if not name:
            return apology("must provide your name", 400)
        if not email:
            return apology("must provide your email", 400)
        if not message:
            return apology("must provide a message", 400)

        # Insert inquiry into the database
        try:
            db.execute("""
                INSERT INTO career_inquiries (name, email, message)
                VALUES (?, ?, ?)
            """, name, email, message)
        except Exception as e:
            return apology(f"unexpected error: {e}", 500)

        # Flash success message and redirect
        flash("Thank you for your inquiry! We will get back to you soon.", "success")
        return redirect("/careers")

    # Render careers page for GET requests
    return render_template("careers.html")


@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    if request.method == "POST":
        # Get form data with default values if not filled
        paycheck1 = float(request.form.get("paycheck1", 0) or 0)
        paycheck2 = float(request.form.get("paycheck2", 0) or 0)
        charity = float(request.form.get("charity", 0) or 0)
        emerFund = float(request.form.get("emerFund", 0) or 0)
        rent = float(request.form.get("rent", 0) or 0)
        water = float(request.form.get("water", 0) or 0)
        natgas = float(request.form.get("natgas", 0) or 0)
        electric = float(request.form.get("electric", 0) or 0)
        cable = float(request.form.get("cable", 0) or 0)
        gasoline = float(request.form.get("gasoline", 0) or 0)
        grocery = float(request.form.get("grocery", 0) or 0)
        cloth = float(request.form.get("cloth", 0) or 0)
        entertain = float(request.form.get("entertain", 0) or 0)
        gym = float(request.form.get("gym", 0) or 0)
        insurance = float(request.form.get("insurance", 0) or 0)
        miscellaneous = float(request.form.get("miscellaneous", 0) or 0)

        # Calculate total expenses and remaining budget
        total_expenses = sum([charity, emerFund, rent, water, natgas, electric, cable,
                             gasoline, grocery, cloth, entertain, gym, insurance, miscellaneous])
        total_income = paycheck1 + paycheck2
        remaining_budget = total_income - total_expenses

        # Save to database (from GPT-4)
        db.execute("""
            INSERT INTO budgets (user_id, paycheck1, paycheck2, charity, emerFund, rent, water, natgas, electric, cable, gasoline, grocery, cloth, entertain, gym, insurance, miscellaneous, total_expenses, remaining_budget)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                paycheck1=excluded.paycheck1,
                paycheck2=excluded.paycheck2,
                charity=excluded.charity,
                emerFund=excluded.emerFund,
                rent=excluded.rent,
                water=excluded.water,
                natgas=excluded.natgas,
                electric=excluded.electric,
                cable=excluded.cable,
                gasoline=excluded.gasoline,
                grocery=excluded.grocery,
                cloth=excluded.cloth,
                entertain=excluded.entertain,
                gym=excluded.gym,
                insurance=excluded.insurance,
                miscellaneous=excluded.miscellaneous,
                total_expenses=excluded.total_expenses,
                remaining_budget=excluded.remaining_budget
        """, session["user_id"], paycheck1, paycheck2, charity, emerFund, rent, water, natgas, electric, cable, gasoline, grocery, cloth, entertain, gym, insurance, miscellaneous, total_expenses, remaining_budget)

        return redirect("/budget")

    else:
        # Fetch existing budget data if available
        rows = db.execute("SELECT * FROM budgets WHERE user_id = ?", session["user_id"])

        budget_data = rows[0] if rows else {
            "paycheck1": 0, "paycheck2": 0, "charity": 0, "emerFund": 0, "rent": 0,
            "water": 0, "natgas": 0, "electric": 0, "cable": 0, "gasoline": 0,
            "grocery": 0, "cloth": 0, "entertain": 0, "gym": 0, "insurance": 0,
            "miscellaneous": 0, "total_expenses": 0, "remaining_budget": 0
        }

        return render_template("budget.html", budget=budget_data)


@app.route("/savings_redirect", methods=["POST"])
@login_required
def savings_redirect():
    response = request.form.get("response")
    if response == "savings":
        return redirect("/savings")
    elif response == "stocks":
        return redirect("/stocks")
    elif response == "no":
        return redirect("/budget")
    else:
        return redirect("/budget")


@app.route("/savings", methods=["GET", "POST"])
@login_required
def savings():
    if request.method == "POST":
        budget = db.execute(
            "SELECT remaining_budget FROM budgets WHERE user_id = ?", session["user_id"])[0]
        remaining_budget = budget["remaining_budget"] if budget else 0

        amount = float(request.form.get("amount", 0))

        if amount > remaining_budget:
            return render_template("savings.html", error="Investment exceeds remaining budget!", budget=budget)

        db.execute("""
            INSERT INTO savings (user_id, amount, annual_rate)
            VALUES (?, ?, ?)
        """, session["user_id"], amount, 4.5)

        new_remaining_budget = remaining_budget - amount
        db.execute("UPDATE budgets SET remaining_budget = ? WHERE user_id = ?",
                   new_remaining_budget, session["user_id"])

        return render_template("savings.html", success="Investment made successfully!", budget={"remaining_budget": new_remaining_budget})

    else:
        budget = db.execute(
            "SELECT remaining_budget FROM budgets WHERE user_id = ?", session["user_id"])[0]
        rows = db.execute("""
            SELECT amount, annual_rate, created_at
            FROM savings
            WHERE user_id = ?
        """, session["user_id"])

        # Calculate updated savings data as before (from GPT-4)
        savings_data = []
        for row in rows:
            elapsed_years = (datetime.now() -
                             datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")).days / 365.0
            updated_amount = round(
                row["amount"] * (1 + row["annual_rate"] / 100) ** elapsed_years, 2)
            savings_data.append({"original": row["amount"], "updated": updated_amount,
                                "rate": row["annual_rate"], "created_at": row["created_at"]})

        return render_template("savings.html", budget=budget, savings_data=savings_data)


@app.route("/insights")
@login_required
def insights():
    return render_template("insights.html")


# Below function from GPT-4
@app.context_processor
def inject_year():
    return {'year': datetime.now().year}


@app.route("/signout")
def signout():
    # Sign user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/stocks", methods=["GET", "POST"])
@login_required
def stocks():
    if request.method == "POST":
        # Get user input
        # Convert to uppercase and remove any unnecessary whitespace
        symbol = request.form.get("symbol").strip().upper()
        shares = request.form.get("shares")

        # Validate stock symbol and number of shares
        if not symbol:
            return apology("Missing stock symbol")
        if not shares or not shares.isdigit() or int(shares) < 1:
            return apology("Invalid number of shares")
        shares = int(shares)

        # Lookup stock data
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid stock symbol")
        stockPrice = stock["price"]

        # Get user's remaining budget
        userBudget = db.execute(
            "SELECT remaining_budget FROM budgets WHERE user_id = ?", session["user_id"])
        if not userBudget:
            return apology("No budget found")
        remaining_budget = userBudget[0]["remaining_budget"]

        # Check if user can afford the stock
        totalCost = stockPrice * shares
        if totalCost > remaining_budget:
            return apology("Not enough remaining budget")

        # Update portfolio
        existing_stock = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?",
            session["user_id"], symbol
        )
        if existing_stock:
            # If stock exists, update shares
            new_shares = existing_stock[0]["shares"] + shares
            db.execute(
                "UPDATE portfolio SET shares = ? WHERE user_id = ? AND symbol = ?",
                new_shares, session["user_id"], symbol
            )
        else:
            # If stock doesn't exist, insert a new row
            db.execute(
                "INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)",
                session["user_id"], symbol, shares
            )

        # Update user's budget
        db.execute(
            "UPDATE budgets SET remaining_budget = remaining_budget - ? WHERE user_id = ?",
            totalCost, session["user_id"]
        )

        # Redirect to the stocks page
        return redirect("/stocks")

    else:
        # Fetch user portfolio and stock data
        stocks = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
        for stock in stocks:
            stockData = lookup(stock["symbol"])
            stock["price"] = stockData["price"]
            stock["total"] = stock["shares"] * stockData["price"]

        userBudget = db.execute(
            "SELECT remaining_budget FROM budgets WHERE user_id = ?", session["user_id"])
        remaining_budget = userBudget[0]["remaining_budget"] if userBudget else 0
        totalStocksValue = sum([stock["total"] for stock in stocks])

        return render_template("stocks.html", stocks=stocks, totalStocksValue=totalStocksValue,
                               budget={"remaining_budget": remaining_budget}
                               )


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Sell shares of stock
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)

        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) < 1:
            return apology("invalid number of shares", 400)
        shares = int(shares)

        stock = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if len(stock) != 1 or stock[0]["shares"] < shares:
            return apology("you don't own that many shares lil bro", 400)

        lookupDict = lookup(symbol)
        if not lookupDict:
            return apology("invalid symbol", 400)
        stockPrice = lookupDict["price"]
        saleValue = stockPrice * shares

        # Update user's remaining budget
        userCash = db.execute("SELECT remaining_budget FROM budgets WHERE user_id = ?",
                              session["user_id"])[0]["remaining_budget"]

        db.execute("UPDATE budgets SET remaining_budget = ? WHERE id = ?",
                   userCash + saleValue, session["user_id"])

        remainingShares = stock[0]["shares"] - shares
        if remainingShares > 0:
            db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND symbol = ?",
                       remainingShares, session["user_id"], symbol)
        else:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                       session["user_id"], symbol)

        return redirect("/stocks")

    else:
        symbol = request.args.get("symbol", "")
        datas = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", datas=datas, symbol=symbol)
