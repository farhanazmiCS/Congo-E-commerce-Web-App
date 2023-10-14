from flask import *
app = Flask(__name__, template_folder='template')


@app.route('/',methods=['GET','POST'])
def homepage():
    return render_template('index.html')

@app.route('/subcategory', methods=["GET","POST"])
def subcategory():
    return render_template('subcategory.html',categoryName="beauty-placeholder")

@app.route('/category', methods=["GET","POST"])
def category():
    return render_template('category.html', categoryName="category-placeholder")

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

@app.route('/search-result', methods=["GET","POST"])
def searchResult():
    return render_template('search-result.html',searchTerm="ligma fork")

@app.route('/login', methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route('/cart', methods=["GET","POST"])
def cart():
    return render_template('cart.html')

@app.route('/orders', methods=["GET","POST"])
def orders():
    return render_template('orders.html')

@app.route('/order', methods=["GET","POST"])
def order():
    return render_template('order.html',orderNumber="10006969",orderTotal="29.98",orderDate="14/10/2023",orderStatus="Shipped", orderArrivalDate="29/10/2023")

@app.route('/signup', methods=["GET","POST"])
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
