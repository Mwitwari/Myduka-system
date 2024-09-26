from flask import Flask, flash, render_template, request, redirect, url_for, session

from flask_bcrypt import Bcrypt

from dbsevice import get_data, insert_sales, insert_products, sales_product, profit_product, register_user, email_exists

from functools import wraps


# create flask instance
# configure your application
# define routes


# run application
app=Flask(__name__)
app.config['SECRET_KEY'] = 'admin'
bcrypt=Bcrypt(app)

# url=
# routes
@app.route("/")
def index():
    return render_template("index.html")


def protected():
    if 'email' not in session:
        return redirect(url_for('login'))    
    
@app.route("/dashboard")

def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    s_prods=sales_product()
    # print(s_prods)
    names=[]
    sales=[]
    for i in s_prods:
        names.append(i[0])
        sales.append(float(i[1]))

    p_product=profit_product()
    # print(p_product)
    product=[]
    profit=[]
    for i in p_product:
        product.append(i[0])
        profit.append(float(i[1]))
    return render_template("dashboard.html", names=names, sales=sales, product=product, profit=profit)


    

@app.route("/sales")
def sales():
    if 'email' not in session:
        return redirect(url_for('login'))
    salesdata=get_data("sales")
    print(salesdata)
    products=get_data("products")
    return render_template("sales.html", salesdata=salesdata, products=products)
    
@app.route("/products")
def products():
    if 'email' not in session:
        return redirect(url_for('login'))
    prods=get_data("products")
    return render_template("products.html", prods=prods)


@app.route("/stock")
def stock():
    if 'email' not in session:
        return redirect(url_for('login'))
    stock=get_data("stock")
    print(stock)
    products=get_data("products")
    return render_template("stock.html", stock=stock, products=products)



@app.route("/make_sales", methods=["POST", "GET"])
def make_sale():
    # CHECK METHOD
    if request.method == "POST":
        # REQUEST DATA
        pid=request.form['pid']
        quantity=request.form['quantity']
        # insert sale
        new_sale=(pid, quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))


@app.route("/add_stock", methods=['post', 'get'])
def add_stock():
    if request.method=="post":
        productid=request.form['pid']
        quantity=request.form['quantity']
        new_stock=(productid, quantity)
        add_stock(new_stock)
        return redirect(url_for('stock'))
    
@app.route("/add_product", methods=["POST"])
def add_product():
    if request.method == "POST":
       productname=request.form["productname"]
       buyingprice=request.form["buyingprice"]
       sellingprice=request.form["sellingprice"]
       stockquantity=request.form["stockquantity"]
       new_product=(productname, buyingprice, sellingprice, stockquantity)
       insert_products(new_product)
       return redirect(url_for("products"))


@app.route('/edit_product', methods=['post', 'get'])
def edit_product():
    productname=request.form["pname"]
    buyingprice=request.form["buyingprice"]
    sellingprice=request.form["sellingprice"]
    stockquantity=request.form["stockquantity"]
    edited_product=(productname, buyingprice, sellingprice, stockquantity)
    edit_product(edited_product)
    return redirect(url_for("products"))
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=="POST":
       fname= request.form['full_name']
       email=request.form['email']
       password=request.form['password']
       hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
       
       x= email_exists(email)
       if x==None:
          new_user=(fname, email, hashed_password)
          
          register_user(new_user)
          return redirect(url_for('login'))
       else:
          flash("Email already exists, please login")
          return redirect(url_for('login'))
    return render_template('register.html')
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method=="POST":
        email= request.form['email']
        password= request.form['password']
        user= email_exists(email)
        # print(user)
        

        if user==None:
            flash("Email does not exist")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1], password):
                flash('login successful')
                session['email'] = request.form['email']
                return redirect(url_for('dashboard'))
            else:
                flash("password is incorrect")
    return render_template("login.html")

@app.route("/logout", methods=['post', 'get'])
def logout():
    session.clear()
    flash("You have successfully logged out")
    return redirect(url_for("login"))

    

app.run(debug=True)


