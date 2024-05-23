from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length


import requests, json


app = Flask(__name__)

USER_API_BASE_URL = "http://localhost:5000/"
PRODUCT_CATEGORY_API_BASE_URL = "http://localhost:5001/"
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/product')
def product():
    # Call API to return 6 products at random
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
    print(dress_category_products_response)
    print(dress_category_products_response.status_code)

    try:
        if dress_category_products_response.status_code == 200:
            # This response message must get passed to the front end registration form
            dress_category_products_response_data = json.loads(dress_category_products_response.text)
            # Get the information of the logged in user here
            print(dress_category_products_response_data)
            print(type(dress_category_products_response_data))

            print("CHECK 1")

            print("CHECK2")      
            return render_template("dress.html", dress_category_products=dress_category_products_response_data)
        else:
            return render_template("dress.html")
    except:
        print("Whoops something went wrong here!")
        return render_template("dress.html")


@app.route('/top')
def top():
    return render_template("top.html")

@app.route('/skirt')
def skirt():
    return render_template("skirt.html")

@app.route('/jumpsuit')
def jumpsuit():
    return render_template("jumpsuit.html")


@app.route("/login", methods=["GET", "POST"])
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
                session["name"] = logged_in_user_response_data["id"]
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

@app.route('/logout')
def logout():
    #Destroy the session variable
    session.pop("name")
    session.pop("logged_in_user")
    return redirect(url_for('index'))
    return render_template("/")

@app.route('/sale_dresses')
def sale_dresses():
    return render_template("sale_dresses.html")

@app.route('/sale_tops')
def sale_tops():
    return render_template("sale_tops.html")

@app.route('/sale_skirts')
def sale_skirts():
    return render_template("sale_skirts.html")

@app.route('/sale_jumpsuits')
def sale_jumpsuits():
    return render_template("sale_jumpsuits.html")

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

if __name__ == "__main__":
    app.run(port=5002, debug=True)