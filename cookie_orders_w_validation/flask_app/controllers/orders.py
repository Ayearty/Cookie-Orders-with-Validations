from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.order import Order

@app.route("/")
def index():
    orders = Order.get_all()
    print(orders)
    return render_template("cookie_orders.html", orders = orders)

@app.route("/form")
def form():
    orders = Order.get_all()
    print(orders)
    return render_template("new_order.html", orders = orders)

@app.route('/create_order', methods=["POST"])
def create_user():
    if not Order.validate_order(request.form):
        return redirect('/form')
    data = {
        "customer_name":request.form["customer_name"],
        "cookie_type":request.form["cookie_type"],
        "number_of_boxes":request.form["number_of_boxes"],
    }
    Order.save(data)
    #print("Route routing!")
    return redirect('/')

@app.route('/edit/<int:id>')
def update(id):
    data = {
        'id' : id
        }
    order = Order.get_one(data)
    return render_template('change_order.html', order = order)

@app.route('/edit_order/<int:id>', methods=["POST"])
def edit(id):
    if not Order.validate_order(request.form):
        return redirect(f'/edit/{id}')
    data = {
        "id":id,
        "customer_name":request.form["customer_name"],
        "cookie_type":request.form["cookie_type"],
        "number_of_boxes":request.form["number_of_boxes"]
    }
    Order.edit(data)
    return redirect("/")