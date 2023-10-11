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

    return render_template('product.html', productName="ligma-fork",productRating=str(productRating),productDescription="Lorem ipsum dolor sit amnet.",productCategory="Lifestyle",productSubcategory="Lifestyle",productPrice = "14.99",productImageHTML=url_for('static', filename='fork.jpg'))

if __name__ == '__main__':
    app.run(debug=True)