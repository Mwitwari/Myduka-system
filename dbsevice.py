import psycopg2

connection=psycopg2.connect(
        dbname="myduka",
        user="postgres",
        password="STANLEYMK227",
        host="localhost",
        port=5432
    )
cursor=connection.cursor()
def get_data(tablename):
        query = f"select * from {tablename}"
        cursor.execute(query)
        data= cursor.fetchall()
        return data

def insert_sales(values):
    query="insert into sales(productid, quantity, createdat) values (%s, %s, now())"
    cursor.execute(query, values)
    connection.commit()

def insert_products(values):
      query= "insert into products(productname, buyingprice, sellingprice, stockquantity ) values( %s, %s, %s, %s)"
      cursor.execute(query, values)
      connection.commit()

def register_user(values):
      query="insert into users(fullname, email, password) values(%s, %s, %s)"
      cursor.execute(query, values)
      connection.commit()

def email_exists(email):
      query="select * from users where email=%s"
      cursor.execute(query, (email,))
      exist=cursor.fetchone()
      if exist:
            return exist
      

def edit_product(values):
      query="update products set productname=%s, buyingprice=%s, sellingprice=%s, stockquantity=%s where productid=%s"
      cursor.execute(query, (productname, buyingprice, sellingprice, stockquantity))
      connection.commit()



# def get_all_sales():
#         query2= "SELECT * FROM sales"
#         cursor.execute(query2)
#         get_all_sales=sales
#         sales = cursor.fetchall()
#         return sales

# define the cursor to perfom database operations

# cursor=connection.cursor()
# cursor.execute("select * from users")
# users=cursor.fetchall()
# print(users)
# cursor.execute("select productname from products")
# product_name=cursor.fetchall()
# print(product_name)

# cursor.execute("select * from sales")
# sales=cursor.fetchall()
# print(sales)






# sales per product
def sales_product():
    query="select productname, sum(sellingprice*quantity) as sales from products join sales on products.productid=sales.productid group by productname"
    cursor.execute(query)
    data=cursor.fetchall()
    return data
sperproduct=sales_product()
# print(sperproduct)



def profit_product():
      query="select productname, sum((sellingprice-buyingprice)*quantity) as profit from products join sales on products.productid=sales.productid group by productname"
      cursor.execute(query)
      result=cursor.fetchall()
      return result
profitperproduct=profit_product()
# print(profitperproduct)