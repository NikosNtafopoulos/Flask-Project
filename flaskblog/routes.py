from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user,logout_user, login_required

# static blog test
posts = [
    {
        'author':'Nik Ntaf',
        'title':'Devops',
        'content':'devops sucks',
        'date_posted':'November 20 2019'
    },
    {
        'author':'Ziu Ntaf',
        'title': 'Devops',
        'content': 'devops da best',
        'date_posted': 'November 21 2019'
}
]

# home route page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# about route page
@app.route("/about")
def about():
    return render_template('about.html', title='About', test='bla bla bla bla')

# registration form page
@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    # instance of the form class
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

# login form page
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    # instance of the form class
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        # example query we want to trim  ex: login?next=%2Faccount
        next_page = request.args.get('next')
        #redirect to next if exists and if not redirect to blog page
        return redirect(next_page) if next_page else redirect(url_for('blog'))
    else:
        flash('Login Unsuccessful.Please check email and password','info')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    #set the image file we want to pass to the template
    image_file = url_for('static',filename='profile_imgs/' + current_user.image_file)
    #instance of the UpdateAccountForm that exist in forms.py and parsing through render_template as a variable
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #fetching username and email from db
        current_user.username = form.username.data
        current_user.email = form.email.data
        #commit to database
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',image_file=image_file,form=form)

@app.route("/blog")
def blog():
    return render_template('blog.html', title='myBlog',posts=posts)