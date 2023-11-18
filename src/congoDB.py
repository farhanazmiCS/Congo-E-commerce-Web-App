from flask import *
from controller.PostGresController import initialise_crud
from controller.mongodbController import MongoDBController

app = Flask(__name__, template_folder='template')
app.secret_key = 'inf2003'  # Replace 'your_secret_key_here' with your actual secret key

create, read, update, delete = initialise_crud()
mgdb = MongoDBController()

# Import app_pages logic
import app_pages.home
import app_pages.signup
import app_pages.login
import app_pages.update_profile
import app_pages.category
import app_pages.subcategory
import app_pages.search_result
import app_pages.product
import app_pages.subcategories
import app_pages.categories
import app_pages.cart
import app_pages.order
import app_pages.admin
import app_pages.orders
import app_pages.single_order
import app_pages.user_dashboard
import app_pages.admin_orders
import app_pages.admin_category

# @app.route('/cart', methods=["GET","POST"])
# def cart():
#     return render_template('cart.html')

#@app.route('/orders', methods=["GET","POST"])
#def orders():
#    return render_template('orders.html')

# @app.route('/order', methods=["GET","POST"])
# def order():
#     return render_template('order.html',orderNumber="10006969",orderTotal="29.98",orderDate="14/10/2023",orderStatus="Shipped", orderArrivalDate="29/10/2023")

@app.route('/logout')
def logout():
    # Clear the user's session data to log them out
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_type', None)
    session.pop('cart', None)

    # Redirect the user to the homepage or any other appropriate page
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)