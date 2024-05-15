from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    if request.method == 'POST':
        firstname = request.form['firstName']

        return jsonify({'success': False, 'message': 'User successfully registered.'})
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