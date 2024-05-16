from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap5

import requests


app = Flask(__name__)

USER_API_BASE_URL = "http://localhost:5000/"
PRODUCT_CATEGORY_API_BASE_URL = "http://localhost:5001/"


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


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
bootstrap = Bootstrap5(app)



@app.route('/')
def get_all_posts():
    return render_template("index.html")

@app.route('/product')
def product():
    return render_template("product.html")

@app.route('/dress')
def dress():
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
                # This response message must get passed to the front end registration form
                return jsonify({'success': True, 'message': 'User successfully login'})
            elif login_received_login_info_response.status_code == 200:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Sorry, a user with this email address does not exist'})            
            else:
                # This response message must get passed to the front end registration form
                return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
        except:
            return jsonify({'success': False, 'message': 'Whoops something went wrong while processing this request. Try again later'})
        
    return render_template("login.html")
        

    # if request.method == 'GET':
        # return render_template("login.html")
    
    # login_form = LoginForm(request.form)  # Initialize form with request data
    # if login_form.validate_on_submit():  # Check if form is submitted and data is valid
    #     email = login_form.email.data
    #     password = login_form.password.data
    #     remember = login_form.remember.data

    #     # Prepare data for login API request
    #     login_user_post_data = {
    #         "email": email,
    #         "password": password
    #     }

    #     LOGIN_USER_URL = USER_API_BASE_URL + "user"

    #     headers = {
    #         'Content-type': 'application/json', 
    #         'Accept': 'application/json'
    #     }

    #     # Make request to login API endpoint
    #     login_user_response = requests.post(
    #         url=LOGIN_USER_URL,
    #         headers=headers, 
    #         json=login_user_post_data
    #     )

    #     # Check if login API request was successful
    #     # If the api staus returns 201, success message of login being successful
    #     # Else If the api status returns 200, success is false, message reads "Invalid username or password"
    #     # Else success is false, "Something went wrong, try again later"

    #     if login_user_response.status_code == 200:
    #         # Authenticate user
    #         user = User.query.filter_by(email=email).first()
    #         if user is not None:
    #             login_user(user, remember=remember)
    #             return jsonify({'success': True, 'message': 'User successfully logged in'})
    #         else:
    #             return jsonify({'success': False, 'message': 'Please check your login details and try again'}), 404
    #     else:
    #         return jsonify({'success': False, 'message': 'user not foundnvalid data submitted'}), 400
          
    # return render_template("login.html")


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

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = SignupForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         # Process signup data here, for example, you can access form data like:
#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         password = form.password.data
#         age = form.age.data
#         gender = form.gender.data
#         # Perform signup logic (e.g., store user data in database)
#         return "Signup successful!"
#     return render_template('register.html', form=form)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     login_form = LoginForm()
#     if login_form.validate_on_submit():
#         if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
#             return render_template("success.html")
#         else:
#             return render_template("denied.html")
#     return render_template("login.html", form=login_form)



if __name__ == "__main__":
    app.run(port=5002, debug=True)