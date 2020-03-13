"""User Dashboard."""

from model import connect_to_db, db, User, ToDoList, ToDoItem, SharedUsersLists
from stocks import get_stocks_by_symbols
from news import get_news_info

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from pytz import timezone

import os
import datetime
import requests
import json


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


########## API KEYS
STOCK_API_KEY = os.environ.get("AV_API_KEY", "")

CAL_CLIENT_ID = os.environ.get("CAL_CLIENT_ID", "")
CAL_CLIENT_SECRET = os.environ.get("CAL_CLIENT_SECRET", "")
CAL_API_KEY = os.environ.get("CAL_API_KEY", "")

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")


########## LANDING PAGE
@app.route("/")
def index():
    """Homepage."""

    return render_template("landingpage.html")


########## NEW USER REGISTRATION
@app.route("/register", methods=["GET"])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Process registration."""

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


######### EXISTING USER LOGIN
@app.route("/login", methods=["GET"])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    if not user.user_id:
        raise Exception("No user logged in.")

    return redirect("/dashboard")


########## USER LOGOUT
@app.route("/logout", methods=["GET"])
def logout():
    """Log out."""

    del session["user_id"]
    return redirect("/")


########## SHOW USER DASHBOARD
@app.route("/dashboard")
def show_dashboard():
    """Show user's dashboard."""

    if "user_id" not in session:
        return redirect("/login")
    else:
        user_id = session["user_id"]
        user = User.query.options(db.joinedload("to_do_lists")\
                                    .joinedload("to_do_items"),
                                  db.joinedload("shared_lists")\
                                    .joinedload("to_do_items")
                                  ).get(user_id)
        article_list = get_news_info(NEWS_API_KEY)

        return render_template("dashboard.html",
                               user=user,
                               article_list=article_list,
                               client_id=CAL_CLIENT_ID,
                               api_key=CAL_API_KEY)


########## ADD A NEW TO-DO LIST
@app.route("/addlist/<int:user_id>", methods=["POST"])
def add_list(user_id):
    """Allow the user to add a new list."""

    list_title = request.form["list_title"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.filter_by(list_title=list_title).first()

    if to_do_list:
        flash("List name already exists. Please select a new name.")
        return redirect("/dashboard")

    new_list = ToDoList(list_title=list_title, user_id=user_id)
    
    db.session.add(new_list)
    db.session.commit()
    
    return redirect("/dashboard")


########## REMOVE AN EXISTING TO-DO LIST
@app.route("/removelist/<list_title>", methods=["POST"])
def remove_list(list_title):
    """Allow the user to remove an existing list."""

    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.filter_by(list_title=list_title).first()

    db.session.delete(to_do_list)
    db.session.commit()
    
    return "OK"


########## ALL ITEMS IN THE TO-DO LIST
@app.route("/lists/<int:list_id>", methods=["GET"])
def access_list(list_id):
    """View all items in a user's list."""

    to_do_list = ToDoList.query.get(list_id)

    shared_lists = SharedUsersLists.query.filter(SharedUsersLists.shared_list_id==to_do_list.list_id)
    num_users = len({shared_list.shared_user_id for shared_list in shared_lists})

    return render_template("items.html", 
                            to_do_list=to_do_list,
                            num_users=num_users)


########## SHARE TO-DO LISTS WITH OTHER USERS
@app.route("/lists/<int:list_id>", methods=["POST"])
def share_lists(list_id):
    """Share lists with other existing users."""

    email = request.form["email"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.get(list_id)
    shared_user = User.query.filter_by(email=email).first()

    if not shared_user:
        flash("No user found. Please enter a valid email.")
        return redirect(f"/lists/{list_id}")

    shared_user.shared_lists.append(to_do_list)
    flash(f"{shared_user.name} has now been added to the list!")
    db.session.add(shared_user)
    db.session.commit()

    return redirect(f"/lists/{list_id}")


########## ITEM STATUS
@app.route("/item/<int:item_id>/update-completed", methods=["POST"])
def item_status(item_id):
    """Update completed status of item in a list."""

    item_completed = request.form.get("item_completed", "off")
    list_id = request.form["list_id"]

    item_completed = item_completed == "on"

    to_do_item = ToDoItem.query.get(item_id)
    to_do_item.completed = item_completed
    db.session.commit()

    return redirect(f"/lists/{list_id}")


########## ADD A NEW ITEM
@app.route("/additem/<int:list_id>", methods=["POST"])
def add_items(list_id):
    """Add a new item to a user's list."""

    item_title = request.form["item_title"]
    item_description = request.form["item_description"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.get(list_id)

    new_item = ToDoItem(item_title=item_title,
                        item_description=item_description)
    to_do_list.to_do_items.append(new_item)
    db.session.add(new_item)
    db.session.commit()

    return redirect(f"/lists/{list_id}")


########## REMOVE AN EXISTING ITEM
@app.route("/removeitem/<item_title>", methods=["POST"])
def remove_items(item_title):
    """Remove an existing item from a user's list."""

    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_item = ToDoItem.query.filter_by(item_title=item_title).first()

    db.session.delete(to_do_item)
    db.session.commit()

    return "OK"


########## ALL ITEMS IN THE SHARED TO-DO LIST
@app.route("/shared-lists/<int:shared_list_id>", methods=["GET"])
def access_sharedlist(shared_list_id):
    """View all items in a user's shared list."""

    list_items = ToDoList.query.get(shared_list_id)
    shared_lists = SharedUsersLists.query.filter(SharedUsersLists.shared_list_id==list_items.list_id)
    num_users = len({shared_list.shared_user_id for shared_list in shared_lists})

    return render_template("shareditems.html", 
                            list_items=list_items, 
                            num_users=num_users)


########## SHARE SHARED TO-DO LISTS WITH OTHER USERS
@app.route("/shared-lists/<int:shared_list_id>", methods=["POST"])
def share_sharedlist(shared_list_id):
    """Share a list with an existing user of the dashboard."""

    email = request.form["email"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.get(list_id)
    shared_user = User.query.filter_by(email=email).first()

    if not shared_user:
        flash("No user found. Please enter a valid email.")
        return redirect(f"/shared-lists/{shared_list_id}")

    shared_user.shared_lists.append(to_do_list)
    flash(f"This list has been shared with {shared_user.name}!")
    db.session.add(shared_user)
    db.session.commit()

    return redirect(f"/shared-lists/{shared_list_id}")


########## ADD NEW SHARED ITEM
@app.route("/addshareditem/<int:shared_list_id>", methods=["POST"])
def add_shared_items(shared_list_id):
    """Add a new item to an existing shared list"""

    item_title = request.form["item_title"]
    item_description = request.form["item_description"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_list = ToDoList.query.get(shared_list_id)
    new_item = ToDoItem(item_title=item_title,
                        item_description=item_description)
    to_do_list.to_do_items.append(new_item)

    db.session.add(new_item)
    db.session.commit()

    return redirect(f"/lists/{shared_list_id}")


######### REMOVE EXISTING SHARED ITEM
@app.route("/removeshareditem/<item_title>", methods=["POST"])
def remove_shared_item(shared_list_id):
    """Remove an item from an existing shared list."""

    item_title = request.form["item_title"]
    user_id = session.get("user_id")

    if not user_id:
        raise Exception("No user logged in.")

    to_do_item = ToDoItem.query.filter_by(item_title=item_title).first()

    db.session.delete(to_do_item)
    db.session.commit()

    return redirect(f"/lists/{shared_list_id}")


@app.route("/api/stocks", methods=["GET"])
def get_user_stock_info():
    """Get latest stock price for user input in modal window."""

    api_key = os.environ.get("AV_API_KEY", "")

    if "symbol" in request.args:
        symbol = request.args.getlist("symbol")
    elif "symbol[]" in request.args:
        symbol = request.args.getlist("symbol[]")
    else:
        symbol = ["AMZN"]

    closing_price_list = get_stocks_by_symbols(symbol, api_key)

    return jsonify(closing_price_list)


@app.route("/api/stock_details/<stock_id>", methods=["GET"])
def display_chart_stuff(stock_id):
    """Display chart graph for the day with half-hourly stock prices."""

    api_key = os.environ.get("AV_API_KEY", "")

    chart_x = ["10", "10:30", "11", "11:30", "12", "12:30", "13", "13:30",
                "14", "14:30", "15", "15:30", "16"]

    data = []
    daily_graph = []
    
    tz = timezone("EST")
    today = datetime.datetime.now(tz)

    if today.weekday() == 5:
        day = today - datetime.timedelta(days=1)
    elif today.weekday() == 6:
        day = today - datetime.timedelta(days=2)
    else:
        day = today

    day = day.strftime("%Y-%m-%d")

    payload={"function": "TIME_SERIES_INTRADAY",
            "symbol": stock_id,
            "interval": "30min",
            "apikey": api_key}

    url = requests.get("https://www.alphavantage.co/query", params=payload)
    open_page = url.json()
    time_series = open_page.get("Time Series (30min)")
    chart_y = []

    if time_series:
        for item in time_series.keys():
            if day in item:
                new_dict = time_series[item]
                data_points = new_dict["4. close"]
                chart_y.append(data_points)

    chart_y.reverse()

    symbol_d = {"symbol": stock_id, "data": []}

    for x, y in zip(chart_x, chart_y):
        symbol_d["data"].append({"x": x, "y": y})

    daily_graph.append(symbol_d)

    return jsonify(daily_graph)


@app.route("/chartjs", methods=["GET"])
def show_chartjs():

    return render_template("dashboard.html")


if __name__ == "__main__":

    app.debug = False

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
