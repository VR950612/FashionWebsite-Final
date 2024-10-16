from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

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

    
def login_merchant(merchant):
    session['logged_in_merchant'] = {
        'email': merchant.email,
        'password': merchant.password
    }        

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

 
@app.route('/logout')
def logout():
    session.pop("logged_in_user", None)
    session.pop("name", None)  
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route('/merchant_logout')
def merchant_logout():
    session.pop("logged_in_merchant", None)
    session.pop("name", None)  
    flash("You have been logged out.", "info")
    return redirect(url_for('merchant_login'))

@app.route("/searchdata", methods=["POST", "GET"])
def searchdata():
    RANDOM_PRODUCTS_URL = PRODUCT_CATEGORY_API_BASE_URL + "random-product-set"
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    if request.method == 'POST':
        try:
            search_word = request.form.get('search_word')
            print(f"Search word: {search_word}")  

            # Make API requests
            random_products_response_one = requests.get(RANDOM_PRODUCTS_URL, headers=headers)
            random_products_response_two = requests.get(RANDOM_PRODUCTS_URL, headers=headers)

            # Check if API requests were successful
            if random_products_response_one.status_code == 200 and random_products_response_two.status_code == 200:
                random_products_response_one_data = json.loads(random_products_response_one.text)
                random_products_response_two_data = json.loads(random_products_response_two.text)

                return render_template("results.html",
                                       random_products_one=random_products_response_one_data,
                                       random_products_two=random_products_response_two_data)
            else:
                print("API request failed with status codes", random_products_response_one.status_code, random_products_response_two.status_code)
                return render_template("results.html", error="API request failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template("results.html", error="No products found!")
    
    return render_template("results.html")


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


@app.route('/merchant_addproduct')
def merchant_addproduct():
    return render_template("merchant_addproduct.html")


@app.route('/admin_all_categories')
def merchant_showcategories():
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
    except:
        print("Whoops something went wrong here!")
    '''
    try:
        categories = PRODUCT_CATEGORY_API_BASE_URL() 
        if categories is None or len(categories) == 0:
            return render_template('merchant_showcategories.html', categories=[], error="No categories found.")
        return render_template('merchant_showcategories.html', categories=categories)
    except Exception as e:
        return render_template('merchant_showcategories.html', categories=[], error=str(e))
    '''


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


@app.route('/merchant_viewproducts')
def merchant_viewproducts():
    return render_template('merchant_viewproducts.html')

@app.route('/merchant_category')
def merchant_category():
    return render_template("merchant_category.html")

@app.route('/merchant_addnewcategory', methods=['GET', 'POST'])
def merchant_addnewcategory():
    if request.method == 'POST':
        category_name = request.form.get('PRODUCT_CATEGORY_API_BASE_URL')
        category_code = request.form.get('PRODUCT_CATEGORY_API_BASE_URL')

        if category_name and category_code:
            # Here, you would typically save to your database
            product.append({'name': category_name, 'code': category_code})
            flash('Category added successfully!', 'success')
            return redirect(url_for('merchant_showcategories'))
        else:
            flash('Please provide both category name and code.', 'danger')

    return render_template('merchant_addnewcategory.html')  # Render your form template

@app.route('/merchant/show_categories')
def merchant_show_categories():
    return render_template('merchant_showcategories.html', product=product)


@app.route('/shopping_cart')
def shopping_cart():
    return render_template("shopping_cart.html")

@app.route('/merchant_nav')
def merchant_nav():
    return render_template("merchant_nav.html")

@app.route('/search', methods=['GET'])
def search():
    RANDOM_PRODUCTS_URL = PRODUCT_CATEGORY_API_BASE_URL + "random-product-set"
    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
    }
    if request.method == 'POST':
        try:
            search_word = request.form.get('search_word')
            print(f"Search word: {search_word}")  

            # Make API requests
            random_products_response_one = requests.get(RANDOM_PRODUCTS_URL, headers=headers)
            random_products_response_two = requests.get(RANDOM_PRODUCTS_URL, headers=headers)

            # Check if API requests were successful
            if random_products_response_one.status_code == 200 and random_products_response_two.status_code == 200:
                random_products_response_one_data = json.loads(random_products_response_one.text)
                random_products_response_two_data = json.loads(random_products_response_two.text)

                return render_template("search_results.html",
                                       random_products_one=random_products_response_one_data,
                                       random_products_two=random_products_response_two_data)
            else:
                print("API request failed with status codes", random_products_response_one.status_code, random_products_response_two.status_code)
                return render_template("search_results.html", error="API request failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template("search_results.html", error="No products found!")
    
    return render_template("search_results.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)