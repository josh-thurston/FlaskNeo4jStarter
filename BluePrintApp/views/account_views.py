from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from data.db_session import db_auth
from services.accounts_service import create_user, login_user, get_profile


blueprint = Blueprint('accounts', __name__, template_folder='templates')

graph = db_auth()


@blueprint.route('/accounts/register', methods=['GET'])
@response(template_file='accounts/register.html')
def register_get():
    return{}


@blueprint.route('/accounts/register', methods=['POST'])
@response(template_file='accounts/register.html')
def register_post():
    # Get the form data from register.html
    name = request.form.get('name')
    email = request.form.get('email').lower().strip()
    company = request.form.get('company').strip()
    password = request.form.get('password').strip()
    confirm = request.form.get('confirm').strip()

    # Check for blank fields in the registration form
    if not name or not email or not company or not password or not confirm:
        return{
            'name': name,
            'email': email,
            'company': company,
            'password': password,
            'confirm': confirm,
            'error':"Please populate all the registration fields."
        }
    # Check if password and confirm match
    if password != confirm:
        return {
            'name': name,
            'email': email,
            'company': company,
            'error': "Passwords do not match."
        }

    # Create the user
    user = create_user(name, email, company, password)
    # Verify another user with the same email does not exist
    if not user:
        return {
            'name': name,
            'email': email,
            'company': company,
            'error': "A user with that email already exists."
        }

    # TODO: Login browser as a session
    usr = request.form["email"]
    session["usr"] = usr
    # After creating the user, redirect to the login page
    return redirect(url_for('accounts.login_get'))


@blueprint.route('/accounts/login', methods=['GET'])
@response(template_file='accounts/login.html')
def login_get():
    # Check if the user is already logged in.  if yes, redirect to profile page.
    if "usr" in session:
        return redirect(url_for("accounts.profile_get"))
    else:
        return {}


@blueprint.route('/accounts/login', methods=['POST'])
@response(template_file='accounts/login.html')
def login_post():
    # Get the form data from login.html
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        return {
            'email': email,
            'password': password
        }
    # call the login function to verify the password and email address.  If failed, flash error message
    # TODO: Validate the user
    user = login_user(email, password)
    if not user:
        return {
            'email': email,
            'password': password,
            'error': "No account for that email address or the password is incorrect."
        }
    # TODO: Log in browser as session
    usr = request.form["email"]
    session["usr"] = usr
    return redirect(url_for("accounts.profile_get"))


@blueprint.route('/accounts/profile', methods=['GET'])
@response(template_file='accounts/index.html')
def profile_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        user_profile = get_profile(usr)
        return {"user_profile": user_profile}
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/accounts/profile', methods=['POST'])
@response(template_file='accounts/index.html')
def profile_post():
    if "usr" in session:
        usr = session["usr"]
        # user_profile = get_profile(usr)
        return {}
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/accounts/logout')
# @response(template_file='accounts/logout.html')
def logout():
    session.pop("usr", None)
    flash("You have successfully been logged out.", "info")
    return redirect(url_for("accounts.login_get"))
