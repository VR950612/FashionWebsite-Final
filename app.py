from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from werkzeug.utils import secure_filename
from datetime import datetime as dt
from flask import Flask, flash


import requests, json, os
import stripe
import logging

app = Flask(__name__)

if 'USER_API_BASE_URL' in os.environ:
    USER_API_BASE_URL=os.environ['USER_API_BASE_URL']
else:
    USER_API_BASE_URL = "http://localhost:5004/"

if 'PRODUCT_CATEGORY_API_BASE_URL' in os.environ:
    PRODUCT_CATEGORY_API_BASE_URL=os.environ['PRODUCT_CATEGORY_API_BASE_URL']
else:
    PRODUCT_CATEGORY_API_BASE_URL = "http://localhost:5001/"    

# USER_API_BASE_URL = "http://localhost:5004/"
# USER_API_BASE_URL="http://usersapi-prod.ap-southeast-2.elasticbeanstalk.com/"

#PRODUCT_CATEGORY_API_BASE_URL = "http://localhost:5001/"

# PRODUCT_CATEGORY_API_BASE_URL = "http://api-products-prod.ap-southeast-2.elasticbeanstalk.com/"
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

stripe_keys = {
    'secret_key': 'sk_test_51PQfmVCS1IJCxgBiWesnCRghxKtP5aizpwMjmBcJ4KGl9lhib7qrwiJ4t4JAhj61C3FgsBrg9BDfclfH6gsauBrv00Zbga0AzH',
    'publishable_key': 'pk_test_51PQfmVCS1IJCxgBiNh7RYzU64zQWQJgZrzv49LhXD66VxDm6JFa1Usjnh7rBHJ1L41cYCASwQ4p9HtQpNdxvGsel00nAoQrvQo'
}

stripe.api_key = stripe_keys['secret_key']

#Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
if 'RDS_DB_NAME' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
    )
else:
    # our database uri
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Adminadmin123@localhost/fashionfrontenddb'


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    age = IntegerField('Age', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class Merchant_SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    
class Merchant_LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/product')
def product():
    # Call API to return 6 products at random
    # Call that API twice
    RANDOM_PRODUCTS_URL = PRODUCT_CATEGORY_API_BASE_URL + "random-product-set"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    random_products_response_one = requests.get(
        url= RANDOM_PRODUCTS_URL,
        headers=headers
    )

    random_products_response_two = requests.get(
        url= RANDOM_PRODUCTS_URL,
        headers=headers
    )    
    print(random_products_response_one)
    print(random_products_response_one.status_code)
    print(random_products_response_two.status_code)

    try:
        if random_products_response_one.status_code == 200 and random_products_response_two.status_code == 200:
            # This response message must get passed to the front end template
            random_products_response_one_response_data = json.loads(random_products_response_one.text)
            print(random_products_response_one_response_data)
            print(type(random_products_response_one_response_data))

            # This response message must get passed to the front end template
            random_products_response_two_response_data = json.loads(random_products_response_two.text)
            print(random_products_response_two_response_data)
            print(type(random_products_response_two_response_data))            

    
            return render_template("product.html", random_products_one=random_products_response_one_response_data,random_products_two=random_products_response_two_response_data)
        else:
            return render_template("product.html")
    except:
        print("Whoops something went wrong here!")

    return render_template("product.html")

@app.route('/category-name/<category_name>')
def get_product_by_category(category_name):
    PRODUCT_BY_CATEGORY_NAME_URL = PRODUCT_CATEGORY_API_BASE_URL + "product_category_by_name/" + category_name
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    products_by_category_name_response = requests.get(
        url= PRODUCT_BY_CATEGORY_NAME_URL,
        headers=headers
    )
    print(products_by_category_name_response)
    print(products_by_category_name_response.status_code)

    try:
        if products_by_category_name_response.status_code == 200:
            # This response message must get passed to the front end 
            products_by_category_name_response_data = json.loads(products_by_category_name_response.text)

            print(products_by_category_name_response_data)
            print(type(products_by_category_name_response_data))
            print("CHECK 1")

            if(len(products_by_category_name_response_data) > 0):

                products_in_category = products_by_category_name_response_data['products']
                print(products_in_category)
                print(type(products_in_category))

                print("CHECK2")
                return render_template("products_by_category.html", category_products=products_in_category)
            else:
                return render_template("products_by_category.html", category_products=None)
        else:
            return render_template("products_by_category.html")
    except:
        print("Whoops something went wrong here!")

@app.route('/dress')
def dress():
    DRESS_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL + "product-by-category/2"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    dress_category_products_response = requests.get(
        url= DRESS_CATEGORY_URL,
        headers=headers
    )
    # print(dress_category_products_response)
    # print(dress_category_products_response.status_code)

    try:
        if dress_category_products_response.status_code == 200:
            # This response message must get passed to the front end 
            dress_category_products_response_data = json.loads(dress_category_products_response.text)

            print(dress_category_products_response_data)
            # print(type(dress_category_products_response_data))
     
            return render_template("dress.html", dress_category_products=dress_category_products_response_data)
        else:
            return render_template("dress.html")
    except:
        print("Whoops something went wrong here!")
     

@app.route('/top')
def top():
    TOP_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL + "product-by-category/4"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    top_category_products_response = requests.get(
        url= TOP_CATEGORY_URL,
        headers=headers
    )
    print(top_category_products_response)
    print(top_category_products_response.status_code)

    try:
        if top_category_products_response.status_code == 200:
            # This response message must get passed to the front end 
            top_category_products_response_data = json.loads(top_category_products_response.text)

            print(top_category_products_response_data)
            print(type(top_category_products_response_data))
  
            return render_template("top.html", top_category_products=top_category_products_response_data)
        else:
            return render_template("top.html")
    except:
        print("Whoops something went wrong here!")
        

@app.route('/skirt')
def skirt():
    SKIRT_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL + "product-by-category/12"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    skirt_category_products_response = requests.get(
        url= SKIRT_CATEGORY_URL,
        headers=headers
    )
    print(skirt_category_products_response)
    print(skirt_category_products_response.status_code)

    try:
        if skirt_category_products_response.status_code == 200:
            # This response message must get passed to the front end 
            skirt_category_products_response_data = json.loads(skirt_category_products_response.text)

            print(skirt_category_products_response_data)
            print(type(skirt_category_products_response_data))
     
            return render_template("skirt.html", skirt_category_products=skirt_category_products_response_data)
        else:
            return render_template("skirt.html")
    except:
        print("Whoops something went wrong here!")


@app.route('/jumpsuit')
def jumpsuit():
    JUMPSUIT_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL + "product-by-category/3"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    jumpsuit_category_products_response = requests.get(
        url= JUMPSUIT_CATEGORY_URL,
        headers=headers
    )
    print(jumpsuit_category_products_response)
    print(jumpsuit_category_products_response.status_code)

    try:
        if jumpsuit_category_products_response.status_code == 200:
            # This response message must get passed to the front end 
            jumpsuit_category_products_response_data = json.loads(jumpsuit_category_products_response.text)

            print(jumpsuit_category_products_response_data)
            print(type(jumpsuit_category_products_response_data))

            print("CHECK 1")

            print("CHECK2")      
            return render_template("jumpsuit.html", jumpsuit_category_products=jumpsuit_category_products_response_data)
        else:
            return render_template("jumpsuit.html")
    except:
        print("Whoops something went wrong here!")


#User Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #first grab all data from the form's variable i.e. the name property
        email = request.form['email']
        password = request.form['password']
    
    # Put this and store it in the post data variable
        received_login_info_post_data = {
            "email": email,
            "password":password
        }

        print(received_login_info_post_data)

        LOGIN_RECEIVED_LOGIN_INFO_URL = USER_API_BASE_URL + "login"

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
        }

        login_received_login_info_response = requests.post(
            url= LOGIN_RECEIVED_LOGIN_INFO_URL,
            headers=headers, 
            json=received_login_info_post_data
        )
        print(login_received_login_info_response)
        print(login_received_login_info_response.status_code)
        #print(login_received_login_info_response)

        try:
            if login_received_login_info_response.status_code == 201:
                logged_in_user_response_data = json.loads(login_received_login_info_response.text)
                # Get the information of the logged in user here
                print(logged_in_user_response_data)
                print(type(logged_in_user_response_data))

                print("CHECK 1")

                #Store the information of the logged in user as session variable
                session["logged_in_user"] = logged_in_user_response_data

                print("CHECK2")
                # Start the user session to login
                session["user"] = logged_in_user_response_data["id"]
                print("CHECK3")
                print(session)
                print("CHECK4")
                return jsonify({'success': True, 'message': 'User successfully logged in'})
            elif login_received_login_info_response.status_code == 200:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Sorry, a user with this email address does not exist'})            
            else:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
        except:
            print("DID it throw an exception??")
            return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
    if request.method == "GET":
        # If the user is already logged in i.e. a session is active, then redirect to the index page
        if session.get("name") is not None:
            return redirect(url_for('index'))
        # but if user is not logged in i.e. no active session, then go to login page
        else:
            return render_template("login.html")

def login_user(user):
    session['logged_in_user'] = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
        
#User SignUp 
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #first grab all data from the form's variable i.e. the name property
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        age = int(request.form['age'])
        gender = request.form['gender-select']

        print(type(age))

        # Put this and store it in the post data variable
        new_user_post_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password":password,
            "age": age,
            "gender":gender
        }

        print(new_user_post_data)

        REGISTER_NEW_USER_URL = USER_API_BASE_URL + "user"

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
        }

        register_new_user_response = requests.post(
            url=REGISTER_NEW_USER_URL,
            headers=headers, 
            json=new_user_post_data
        )
        print(register_new_user_response)
        print(register_new_user_response.status_code)
        #print(register_new_user_response)

        try:
            if register_new_user_response.status_code == 201:
                # This response message must get passed to the front end registration form
                return jsonify({'success': True, 'message': 'User successfully registered'})
            elif register_new_user_response.status_code == 200:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Sorry, a user with this email address already exists'})            
            else:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Whoops something went wrong while registering this user. Try again later'})
        except:
            return jsonify({'success': False, 'message': 'Whoops something went wrong while registering this user. Try again later'})
        
    return render_template("register.html")

#Merchant Admin Login 
@app.route('/merchant_login', methods=['GET', 'POST'])
def merchant_login():
    if request.method == 'POST':
        #first grab all data from the form's variable i.e. the name property
        merchant_email = request.form['email']
        merchant_password = request.form['password']
    
    # Put this and store it in the post data variable
        received_merchant_login_info_post_data = {
            "email": merchant_email,
            "password": merchant_password            
        }

        print(received_merchant_login_info_post_data)

        MERCHANT_LOGIN_RECEIVED_MERCHANT_LOGIN_INFO_URL = USER_API_BASE_URL + "merchant_login"

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
        }

        merchant_login_received_merchant_login_info_response = requests.post(
            url= MERCHANT_LOGIN_RECEIVED_MERCHANT_LOGIN_INFO_URL,
            headers=headers, 
            json=received_merchant_login_info_post_data
        )
        print(merchant_login_received_merchant_login_info_response)
        print(merchant_login_received_merchant_login_info_response.status_code)
        #print(merchant_login_received_merchant_login_info_response)

        try:
            if merchant_login_received_merchant_login_info_response.status_code == 201:
                logged_in_merchant_login_response_data = json.loads(merchant_login_received_merchant_login_info_response.text)
                # Get the information of the logged in admin here
                print(logged_in_merchant_login_response_data)
                print(type(logged_in_merchant_login_response_data))

                print("CHECK 1")

                #Store the information of the logged in admin as session variable
                session["logged_in_merchant"] = logged_in_merchant_login_response_data

                print("CHECK2")
                # Start the merchant session to login
                session["merchant"] = logged_in_merchant_login_response_data["id"]
                print("CHECK3")
                print(session)
                print("CHECK4")
                return redirect(url_for('merchant_addnewcategory'))
            elif merchant_login_received_merchant_login_info_response.status_code == 200:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Sorry, admin with this email address does not exist'})            
            else:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
        except:
            print("DID it throw an exception??")
            return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
    if request.method == "GET":
        # If the admin is already logged in i.e. a session is active, then redirect to the index page
        if session.get("name") is not None:
            return redirect(url_for('merchant_addnewcategory'))
        # but if admin is not logged in i.e. no active session, then go to login page
        else:
            return render_template("merchant_login.html")

#Merchant admin login
def login_merchant(merchant):
    session['logged_in_merchant'] = {
        'email': merchant.email,
        'password': merchant.password
    }        

#Merchant admin signup
@app.route('/merchant_signup', methods=['GET','POST'])
def merchant_signup():
    print("DOES IT EVEN COME HERE FIRST????")
    if request.method == 'POST':
        print("DOES IT EVEN COME HERE????")
        #first grab all data from the form's variable i.e. the name property
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        # Put this and store it in the post data variable
        new_merchant_post_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password":password
        }

        print(new_merchant_post_data)
     
        MERCHANT_SIGNUP_NEW_MERCHANT_URL = USER_API_BASE_URL + "merchant"

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
        }

        merchant_signup_new_merchant_response = requests.post(
            url= MERCHANT_SIGNUP_NEW_MERCHANT_URL,
            headers=headers, 
            json=new_merchant_post_data
        )
        print(merchant_signup_new_merchant_response)
        print(merchant_signup_new_merchant_response.status_code)
        #print(signup_new_merchant_response)

        try:
            if merchant_signup_new_merchant_response.status_code == 201:
                # This response message must get passed to the front end registration form
                return jsonify({'success': True, 'message': 'Admin successfully registered'})
            elif merchant_signup_new_merchant_response.status_code == 200:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Sorry, admin with this email address already exists'})            
            else:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Whoops something went wrong while registering this admin. Try again later'})
        except:
            return jsonify({'success': False, 'message': 'Whoops something went wrong while registering this admin. Try again later'})
        
    return render_template("merchant_signup.html")

#User logout
@app.route('/logout')
def logout():
    session.pop("logged_in_user", None)
    session.pop("name", None)  
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

#Merchant admin logout
@app.route('/merchant_logout')
def merchant_logout():
    session.pop("logged_in_merchant", None)
    session.pop("name", None)  
    flash("You have been logged out.", "info")
    return redirect(url_for('merchant_login'))

#Single product details
@app.route('/product/<int:product_id>')
def single_product(product_id):
    PRODUCT_DETAILS_URL = PRODUCT_CATEGORY_API_BASE_URL + "product/" + str(product_id)
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    product_details_response = requests.get(
        url= PRODUCT_DETAILS_URL,
        headers=headers
    )
    print(product_details_response)
    print(product_details_response.status_code)

    try:
        if product_details_response.status_code == 200:
            # This response message must get passed to the front end 
            product_details_response_data = json.loads(product_details_response.text)

            print(product_details_response_data)
            print(type(product_details_response_data))

            product_price = product_details_response_data['product_price']
            data_amount = float(product_price) * 100
            print(data_amount)
            print(type(data_amount))
     
            return render_template("product_details.html", data_amount = data_amount, product=product_details_response_data, key=stripe_keys['publishable_key'])
        else:
            return render_template("product_details.html", product={})
    except:
        print("Whoops something went wrong here!")    
    return render_template("product_details.html")

          

# @app.route('/sale_dresses')
# def sale_dresses():
#     return render_template("sale_dresses.html")

# @app.route('/sale_tops')
# def sale_tops():
#     return render_template("sale_tops.html")

# @app.route('/sale_skirts')
# def sale_skirts():
#     return render_template("sale_skirts.html")

# @app.route('/sale_jumpsuits')
# def sale_jumpsuits():
#     return render_template("sale_jumpsuits.html")

@app.route('/wishlist')
def wishlist():
    return render_template("wishlist.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/stripe-checkout/<int:product_id>', methods=['POST', 'GET'])
def stripe_checkout(product_id):
    PRODUCT_DETAILS_URL = PRODUCT_CATEGORY_API_BASE_URL + "product/" + str(product_id)
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    product_details_response = requests.get(
        url= PRODUCT_DETAILS_URL,
        headers=headers
    )
    try:
        if product_details_response.status_code == 200:
            # This response message must get passed to the front end 
            product_details_response_data = json.loads(product_details_response.text)

            print(product_details_response_data)
            print(type(product_details_response_data))
     
            return render_template("stripe_checkout.html", product=product_details_response_data)
        else:
            flash('Payment Successful! Thank you for shopping with us😊')
            return render_template("stripe_checkout.html", product={})
    except:
        print("Whoops something went wrong here!")
          
    return render_template("stripe_checkout.html")


#view all categories
@app.route('/admin_all_categories')
def merchant_show_categories():
    ALL_PRODUCT_CATEGORIES_URL = PRODUCT_CATEGORY_API_BASE_URL + "all_product_categories"
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    all_products_category_response = requests.get(
        url= ALL_PRODUCT_CATEGORIES_URL,
        headers=headers
    )
    print(all_products_category_response)
    print(all_products_category_response.status_code)

    try:
        if all_products_category_response.status_code == 200:
            # This response message must get passed to the front end 
            all_product_categories_response_data = json.loads(all_products_category_response.text)

            print(all_product_categories_response_data)
            print(type(all_product_categories_response_data))

            print("CHECK 1")

            print("CHECK2")      
            return render_template("merchant_showcategories.html", categories=all_product_categories_response_data)
        else:
            return render_template("merchant_showcategories.html")
    
    except Exception as e:
        print("Whoops, something went wrong:", e)
        return render_template("merchant_showcategories.html")
    '''
    try:
        categories = PRODUCT_CATEGORY_API_BASE_URL() 
        if categories is None or len(categories) == 0:
            return render_template('merchant_showcategories.html', categories=[], error="No categories found.")
        return render_template('merchant_showcategories.html', categories=categories)
    except Exception as e:
        return render_template('merchant_showcategories.html', categories=[], error=str(e))
    '''

#categories
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    name = session.get('name')
    password = session.get('password')

    if request.method == 'POST':
        category_name = request.form['category_name']
        category_code = request.form['category_code']

        PRODUCT_CATEGORY_CODE_URL = PRODUCT_CATEGORY_API_BASE_URL + "/product_category_by_code/" + category_code
        print(PRODUCT_CATEGORY_CODE_URL)

        # Check if category code already exists via API
        product_category_code_response = requests.get(PRODUCT_CATEGORY_CODE_URL)
        if response.status_code == 200:
            product_category_code_response_data = json.loads(product_category_code_response.text)

            print(product_category_code_response_data)
            print(type(product_category_code_response_data))

            if len(product_category_code_response_data) != 0:
                #return error message saying this category code already exists
                flash('Category code already exists. Please use a different code.', 'error')             
            else:
                #call api to perform the addition of category
                flash('Category added successfully', 'success')

        '''
        if response.status_code == 200 and response.json():
            flash('Category name already exists. Please use a different name.', 'error')
            return redirect(url_for('categories'))
        
        # Add new category via API
        new_product_category = {
            "category_name": category_name,
            "category_code": category_code
        }
        response = requests.post(f"{PRODUCT_CATEGORY_API_BASE_URL}/all_product_categories", json=new_product_category)

        if response.status_code == 201:
            flash('Category added successfully!', 'success')
        else:
            flash(f'An error occurred: {response.text}', 'error')
        '''
        return redirect(url_for('categories'))

    # Fetch all categories via API
    response = requests.get(f"{PRODUCT_CATEGORY_API_BASE_URL}/all_product_categories")
    categories = response.json() if response.status_code == 200 else []

    return render_template('categories.html', categories=categories, name=name, password=password)


#merchant admin add new category
@app.route('/merchant_addnewcategory', methods=['GET', 'POST'])
def merchant_addnewcategory():
    success = False
    output_message = ""
    if request.method == 'POST':
        category_name = request.form['category_name']
        category_code = request.form['category_code']

        PRODUCT_CATEGORY_CODE_URL = PRODUCT_CATEGORY_API_BASE_URL + "/product_category"
        print(PRODUCT_CATEGORY_CODE_URL)

        # Make the GET request to check if the category code exists
        # product_category_code_response = requests.post(PRODUCT_CATEGORY_CODE_URL)

        # Put this and store it in the post data variable
        received_product_category_post_data = {
            "category_name": category_name,
            "category_code":category_code,
            "products": []
        }        
        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
        }
        print(received_product_category_post_data)

        product_category_code_response = requests.post(
            url= PRODUCT_CATEGORY_CODE_URL,
            headers=headers, 
            json=received_product_category_post_data
        )        

        try:
            response_data = json.loads(product_category_code_response.text)
            # Check if the response is successful
            if product_category_code_response.status_code == 201:
                print("status code is 201")
                output_message = response_data['message']
                success = True
                # return jsonify({'output_msg': output_message, 'success': success})
            elif product_category_code_response.status_code == 200:
                print("Status code is 200")
                print(product_category_code_response.status_code)
                print(response_data)
                output_message = response_data['message']
                # return jsonify({'output_msg': output_message, 'success': success})                
            else:
                print("Status code is neither 200 nor 201")
                print(product_category_code_response.status_code)
                output_message = "Sorry something went wrong while adding this product category. Check if the category code already exists or try again later."
                # return jsonify({'output_msg': output_message, 'success': success})
        except Exception as e:
            print("Exception occured while adding product category")
            print(str(e))
            output_message="Whoops something unexpected happended while adding this product category. Please try again after a while."
        return jsonify({'message': output_message, 'success': success})

    else:
        # Render the template for the form
        return render_template('merchant_addnewcategory.html')

 #edit/update product
@app.route('/edit_product_category/<int:id>', methods=['GET', 'POST'])
def edit_product_category(id):
    product_category_id = id
    product_category={}
    print(request.method)
    if request.method == 'POST':
        # Handle form submission
        try:
            print("???????")
            # Use request.form.get to retrieve submitted data
            category_name = request.form.get('category_name')
            category_code = request.form.get('category_code')
            print("DOES IT EVEN COME HERE")
            print(category_name)
            print(category_code)

            # Call the update function with the category ID and new data
            if update_category(product_category_id, category_name, category_code):
                print("SUccess post??")
                flash('Category updated successfully!', 'success')
            else:
                print("failed post??")
                flash('Category update failed. Category not found.', 'error')

        except Exception as e:
            print("exception post??")
            print(e)
            flash(f'Error updating category: {str(e)}', 'error')
    else:
        print("SO IT GETS HERE AGAIN???")
        try:
            # Fetch the product category by ID
            category_url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product_category/{id}"
            response = requests.get(category_url)

            if response.status_code == 200:
                product_category = response.json()  # Assuming this gives you the category object
        except:
            print("exception get??")
            flash(f'Sorry category not found: {str(e)}', 'error')


    return render_template("edit_category.html", product_category=product_category)


def update_category(category_id, category_name, category_code):
    print("DOES IT EVEN GET HERE???")
    url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product_category/{category_id}"
    print(url)
    
    # Create the updated category data
    updated_data = {
        "category_name": category_name,
        "category_code": category_code
    }

    # Make a PUT request to update the category
    response = requests.put(url, json=updated_data)

    # Check if the update was successful
    if response.status_code == 200:
        return True
    else:
        print("Update failed:", response.status_code, response.text)  # Log error for debugging
        return False

#Update a Product_Category
@app.route('/product_category_old/<int:id>', methods=['POST'])
def update_category_old(id):
    # Fetch the current category details if needed (optional)
    product_category_code_response = f"{PRODUCT_CATEGORY_API_BASE_URL}/{id}"
    
    category_name = request.form.get('category_name')
    category_code = request.form.get('category_code')

    # Prepare the payload for updating the category
    payload = {
        'category_name': category_name,
        'category_code': category_code
    }

    # Send the PUT request to update the category
    response = requests.put(product_category_code_response, json=payload)

    if response.status_code == 200:
        flash('Category updated successfully!', 'success')
    else:
        flash('Failed to update category.', 'danger')

    return redirect(url_for('categories'))

#delete category
@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    product_category_id = category_id
    # External API URL for deleting products by category
    PRODUCT_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL +'/product_category/' + str(category_id)

    try:
        # Send the DELETE request to the external API
        response = requests.delete(PRODUCT_CATEGORY_URL)

        # Check if the response status code is 200 (successful)
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Category deleted successfully'
            })
        else:
            # If the status code is not 200, return an error message
            return jsonify({
                'success': False,
                'message': f'Failed to delete category. Status code: {response.status_code}'
            }), 400

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection problems, timeouts)
        return jsonify({
            'success': False,
            'message': f'Error occurred while trying to delete the category: {e}'
        }), 500

# #merchant admin view all products
@app.route('/merchant_viewproducts/<int:category_id>', methods=['GET'])
def merchant_viewproducts(category_id):
    product_category_id = category_id
    PRODUCT_CATEGORY_URL = PRODUCT_CATEGORY_API_BASE_URL + "product-by-category/" + str(product_category_id)
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    products_by_category_response = requests.get(
        url= PRODUCT_CATEGORY_URL,
        headers=headers
    )
    print(products_by_category_response)
    print(products_by_category_response.status_code)

    try:
        if products_by_category_response.status_code == 200:
            # This response message must get passed to the front end 
            products_by_category_response_data = json.loads(products_by_category_response.text)

            print(products_by_category_response_data)
            print(type(products_by_category_response_data))

            print("CHECK 1")

            print("CHECK2")      
            return render_template("merchant_viewproducts.html", products=products_by_category_response_data)
        else:
            return render_template("merchant_viewproducts.html", products=None)
    except:
        print("Whoops something went wrong here!")
        return render_template("merchant_viewproducts.html", products=None)

   
#merchant admin add new product
@app.route('/merchant_addproduct', methods=['GET', 'POST'])
def merchant_addproduct():
    success = False
    output_message = ""

    if request.method == 'POST':
        # Handle the POST request (product addition logic)
        product_name = request.form.get('product_name', '')
        product_category = request.form.get('product_category', '')
        product_display_title = request.form.get('product_display_title', '')
        product_description = request.form.get('product_description', '')
        product_price = float(request.form.get('product_price', 0))
        product_quantity = int(request.form.get('product_quantity', 0))
        discount_percentage = float(request.form.get('discount_percentage', 0))  # Default to 0 if not provided
        discounted_price = float(request.form.get('discounted_price', 0)) 
      
        received_product_post_data = {
            "product_name": product_name,
            "product_category": product_category,
            "product_display_title": product_display_title,
            "product_description": product_description,
            "product_price": product_price,
            "product_quantity": product_quantity,
            "discount_percentage" : discount_percentage,
            "discounted_price" : discounted_price,
            }

        headers = {
            'Content-type': 'application/json', 
            'Accept': 'application/json'
        }

        # If you need to make a request to check or create the product category:
        product_url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product"
        
        try:
            # Make the request to the product category API
            product_response = requests.post(product_url, headers=headers, json=received_product_post_data)
            
            # Parse the response
            response_data = product_response.json()

            # Check if the response is successful
            if product_response.status_code == 201:
                print("Product category created successfully.")
                output_message = "Product added successfully."
                success = True
            elif product_response.status_code == 200:
                print("Product category found.")
                output_message = "Product added successfully."
                success = True
            else:
                print("Error: ", product_response.status_code)
                output_message = "Something went wrong while adding this product. Please try again later."
                success = False

        except requests.exceptions.RequestException as e:
            print("Exception occurred while interacting with the product category API.")
            print(str(e))
            output_message = "Whoops! Something unexpected happened. Please try again later."
            success = False

        # If success, redirect to the 'merchant_viewproducts' route
        if success:
            return redirect(url_for('merchant_viewproducts'))  # Assuming this route exists

        # Return the output message as JSON (for debugging or handling errors)
        return jsonify({'message': output_message, 'success': success})

    # If it's a GET request, render the form
    return render_template('merchant_addproduct.html')

# Function to handle saving product images
def save_product_images(product_image, upload_folder):
    image_paths = {}

    if product_image:
        # Save the product image
        product_image_path = os.path.join(upload_folder, secure_filename(product_image.filename))
        product_image.save(product_image_path)
        image_paths['product_image'] = product_image_path

    return image_paths

# @app.route('/merchant_category')
# def merchant_category():
#     return render_template("merchant_category.html")

#edit/update product
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product_category_id = product_id  # Or fetch dynamically if needed
    url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product/{product_id}"
    
    response = requests.get(url)

    if response.status_code == 200:
        product = response.json()

        # Example of fetching the product category, assuming it has a similar endpoint
        category_response = requests.get(f"{PRODUCT_CATEGORY_API_BASE_URL}/category/{product_category_id}")
        if category_response.status_code == 200:
            product_category = category_response.json()  # Assuming this gives you the category object
        else:
            product_category = None  # Handle cases where the category is not found

        if request.method == 'POST':
            # Handle form submission
            try:
                product_name = request.form.get('product_name', '')
                product_category = request.form.get('product_category', '')
                product_display_title = request.form.get('product_display_title', '')
                product_description = request.form.get('product_description', '')
                product_price = float(request.form.get('product_price', 0))
                product_quantity = int(request.form.get('product_quantity', 0))

                if update_product(product_id, product_name, product_category, product_display_title, product_description, product_price, product_quantity):
                    flash('Product updated successfully!')
                else:
                    flash('Product update failed. Product not found.')

                return redirect(url_for("merchant_viewproducts", category_id=product_category))

            except Exception as e:
                flash(f'Error updating product: {str(e)}')
                return redirect(url_for("edit_product", category_id=1))

        return render_template("edit_product.html", product=product, product_category=product_category)

    else:
        flash('Product not found!')
        return redirect(url_for("merchant_viewproducts", category_id=1))

def update_product(product_id, product_name, product_category, product_display_title, product_description, product_price, product_quantity):
    url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product/{product_id}"
    
    # Create the updated product data
    updated_data = {
        "product_name": product_name,
        "product_category": product_category,
        "product_display_title": product_display_title,
        "product_description": product_description,
        "product_price": product_price,
        "product_quantity": product_quantity
    }

    # Make a PUT request to update the product
    response = requests.put(url, json=updated_data)

    # Check if the update was successful
    if response.status_code == 200:
        return True
    else:
        print("Update failed:", response.status_code, response.text)  # Log error for debugging
        return False


# Delete product
@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Construct the URL for deleting the product
    url = f"{PRODUCT_CATEGORY_API_BASE_URL}/product/{product_id}"

    try:
        # Send the DELETE request to the external API
        response = requests.delete(url)

        # Check if the response status code is 200 or 204 (successful deletion)
        if response.status_code in [200, 204]:
            return jsonify({
                'success': True,
                'message': 'Product deleted successfully'
            }), 200  # Return 200 OK on success
        else:
            # If the status code is not 200 or 204, return an error message
            return jsonify({
                'success': False,
                'message': f'Failed to delete product. Status code: {response.status_code}, Response: {response.text}'
            }), 400  # Return 400 Bad Request on failure

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection problems, timeouts)
        return jsonify({
            'success': False,
            'message': f'Error occurred while trying to delete the product: {e}'
        }), 500  # Return 500 Internal Server Error if there is an exception
    
    

@app.route('/shopping_cart')
def shopping_cart():
    return render_template("shopping_cart.html")

# @app.route('/merchant_nav')
# def merchant_nav():
#     return render_template("merchant_nav.html")

@app.route('/searchdata', methods=['GET'])
def searchdata():
    # Get the search term from the query string (the 'search_word' parameter)
    search_word = request.args.get('search_word', '')  # Default to empty string if not provided
    print(f"Search word: {search_word}")
    
    # Construct the API URL based on the search term
    RANDOM_PRODUCTS_URL = PRODUCT_CATEGORY_API_BASE_URL + "random-product-set"
    
    # Add the search_word parameter to the URL if it's provided
    if search_word:
        RANDOM_PRODUCTS_URL += f"?category_name={search_word}"

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Make the API requests with the updated URL
        random_products_response_one = requests.get(RANDOM_PRODUCTS_URL, headers=headers)
        random_products_response_two = requests.get(RANDOM_PRODUCTS_URL, headers=headers)

        # Check if API requests were successful
        if random_products_response_one.status_code == 200 and random_products_response_two.status_code == 200:
            # Parse the JSON response from the API
            random_products_response_one_data = random_products_response_one.json()
            random_products_response_two_data = random_products_response_two.json()

            # Check if both API responses have no products
            if not random_products_response_one_data and not random_products_response_two_data:
                return render_template("search_results.html", error="No products found matching your search criteria.")
            
            # Render the template with the fetched data
            return render_template("search_results.html",
                                   random_products_one=random_products_response_one_data,
                                   random_products_two=random_products_response_two_data)

        else:
            print("API request failed with status codes", random_products_response_one.status_code, random_products_response_two.status_code)
            return render_template("search_results.html", error="API request failed.")
    
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Request failed: {e}")
        return render_template("search_results.html", error="API request failed.")
    
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred: {e}")
        return render_template("search_results.html", error="Something went wrong.")



@app.route('/user_cart')
def user_cart():
    return render_template("user_cart.html")

@app.route('/user_home')
def user_home():
    return render_template("user_home.html")

@app.route('/user_nav')
def user_nav():
    return render_template("user_nav.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)