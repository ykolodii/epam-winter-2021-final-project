from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from .. import db
from ..models import Employee
from ..forms import RegisterForm, LoginForm

from . import user


@user.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegisterForm()
    if form.validate_on_submit():
        employee_to_create = Employee(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data
        )

        # add employee to the database
        db.session.add(employee_to_create)
        db.session.commit()
        login_user(employee_to_create)
        flash(f'Account created successfully! You are now logged in as {employee_to_create.username}',
              category='success')

        # redirect to the home page (WILL UPDATE)
        return redirect(url_for('user.home_page'))

    # if there are no errors from the validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    # load registration template
    return render_template('register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Handle requests to the /login route
    Add an employee to the database through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        attempted_employee = Employee.query.filter_by(email=form.email.data).first()
        if attempted_employee and attempted_employee.check_password_correction(
                attempted_password=form.password.data
        ):
            # log employee in
            login_user(attempted_employee)
            flash(f'Success! You are logged in as: {attempted_employee.email}', category='success')

            # redirect to the home page after login (WILL UPDATE)
            return redirect(url_for('user.home_page'))

        # when login details are incorrect
        else:
            flash('Email and password are not match! Please try again!', category='danger')

    # load login template
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout_page():
    """
    Handle requests to the /logout route
    Allow employee to logout moving to home page.
    """
    logout_user()
    flash('You have been logged out!', category='info')

    # redirect to the home page
    return redirect(url_for('user.home_page'))
