from flask import *
from PostGresControllerV2.PostGresControllerV2 import initialise_crud
app = Flask(__name__, template_folder='template')
app.secret_key = 'inf2003'  # Replace 'your_secret_key_here' with your actual secret key

create, read, update, delete = initialise_crud()

# Import app_pages logic
import app_pages.signup
import app_pages.login
import app_pages.category
import app_pages.subcategory
import app_pages.search_result

@app.route('/',methods=['GET','POST'])
def homepage():
    return render_template('index.html')

@app.route('/categories', methods=["GET","POST"])
def categories():
    return render_template('categories.html')

@app.route('/subcategories', methods=["GET","POST"])
def subcategories():
    return render_template('subcategories.html')

@app.route('/product', methods=["GET","POST"])
def product():
    productRating=5.0
    return render_template('product.html', productName="ligma-fork",productRating=str(productRating),productDescription="Lorem ipsum dolor sit amnet.",productCategory="Lifestyle",productSubcategory="Lifestyle",productPrice = "14.99",productImageHTML=url_for('static', filename='fork.jpg'),productQuantity='2',productSupplier='SIT')

@app.route('/cart', methods=["GET","POST"])
def cart():
    return render_template('cart.html')

@app.route('/orders', methods=["GET","POST"])
def orders():
    return render_template('orders.html')

@app.route('/order', methods=["GET","POST"])
def order():
    return render_template('order.html',orderNumber="10006969",orderTotal="29.98",orderDate="14/10/2023",orderStatus="Shipped", orderArrivalDate="29/10/2023")

@app.route('/logout')
def logout():
    # Clear the user's session data to log them out
    session.pop('user_id', None)
    session.pop('user_name', None)

    # Redirect the user to the homepage or any other appropriate page
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)