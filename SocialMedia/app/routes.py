# app/routes.py
from flask import render_template, redirect, url_for, flash, request  # Flask utilities for routing and rendering templates
from app import app, db  # Importing the app instance and the database
from flask_login import login_user, logout_user, login_required, current_user  # Flask-Login utilities for user sessions
from app.models import User, Post, Comment, Like  # Importing the User, Post, Comment, and Like models
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm  # Importing the forms for login, registration, posts, and comments
from werkzeug.security import generate_password_hash, check_password_hash  # Functions for password hashing and checking

# Home route to display all posts
@app.route('/', endpoint='home')
@app.route('/home', endpoint='home')
def home():
    posts = Post.query.all()  # Fetch all posts from the database
    return render_template('home.html', posts=posts)  # Render the home template, passing the posts to it

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # If the user is already logged in, redirect to the home page
        return redirect(url_for('home'))
    form = RegistrationForm()  # Instantiate the registration form
    if form.validate_on_submit():  # If the form is submitted and valid
        hashed_password = generate_password_hash(form.password.data)  # Hash the user's password
        # Create a new user object with the form data
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)  # Add the new user to the database
        db.session.commit()  # Commit the changes to the database
        flash('Your account has been created! You can now log in.', 'success')  # Display a success message
        return redirect(url_for('login'))  # Redirect the user to the login page
    return render_template('register.html', title='Register', form=form)  # Render the registration form

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If the user is already logged in, redirect to the home page
        return redirect(url_for('home'))
    form = LoginForm()  # Instantiate the login form
    if form.validate_on_submit():  # If the form is submitted and valid
        user = User.query.filter_by(username=form.username.data).first()  # Find the user by their username
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  # Log the user in (sets the session)
            flash('Login successful!', 'success')  # Display a success message
            return redirect(url_for('home'))  # Redirect to the home page
        else:
            flash('Login failed. Check your username and password.', 'danger')  # Display an error message if login fails
    return render_template('login.html', title='Login', form=form)  # Render the login form

# User logout route
@app.route('/logout')
def logout():
    logout_user()  # Log the user out (clear the session)
    return redirect(url_for('home'))  # Redirect to the home page

# Route for creating a new post (requires login)
@app.route('/post/new', methods=['GET', 'POST'])
@login_required  # This decorator ensures that the user must be logged in to access this route
def new_post():
    form = PostForm()  # Instantiate the post form
    if form.validate_on_submit():  # If the form is submitted and valid
        # Create a new post object with the form data
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)  # Add the new post to the database
        db.session.commit()  # Commit the changes to the database
        flash('Your post has been created!', 'success')  # Display a success message
        return redirect(url_for('home'))  # Redirect the user to the home page
    return render_template('create_post.html', title='New Post', form=form)  # Render the new post form

# Route for editing an existing post (requires login)
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required  # The user must be logged in to access this route
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID, or return a 404 error if not found
    if post.user != current_user:  # Ensure that the current user is the author of the post
        flash('You do not have permission to edit this post.', 'danger')  # Display an error message
        return redirect(url_for('home'))  # Redirect to the home page
    form = PostForm()  # Instantiate the post form
    if form.validate_on_submit():  # If the form is submitted and valid
        post.title = form.title.data  # Update the post's title
        post.content = form.content.data  # Update the post's content
        db.session.commit()  # Commit the changes to the database
        flash('Your post has been updated!', 'success')  # Display a success message
        return redirect(url_for('home'))  # Redirect to the home page
    elif request.method == 'GET':
        # Pre-populate the form with the current post data if the page is being loaded for the first time
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')  # Render the edit post form

# Route for deleting an existing post (requires login)
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required  # The user must be logged in to access this route
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID, or return a 404 error if not found
    if post.user != current_user:  # Ensure that the current user is the author of the post
        flash('You do not have permission to delete this post.', 'danger')  # Display an error message
        return redirect(url_for('home'))  # Redirect to the home page
    db.session.delete(post)  # Delete the post from the database
    db.session.commit()  # Commit the changes to the database
    flash('Your post has been deleted!', 'success')  # Display a success message
    return redirect(url_for('home'))  # Redirect to the home page

# Route to view the user's profile and their posts (requires login)
@app.route('/profile')
@login_required  # The user must be logged in to access this route
def profile():
    user_posts = current_user.posts  # Retrieve all the posts created by the current user
    return render_template('profile.html', user=current_user, posts=user_posts)  # Render the profile template, passing the user and their posts

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)  # Find the post by ID, or return a 404 if not found
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post_id=post_id, user_id=current_user.id)
        db.session.add(comment)  # Add the new comment to the database
        db.session.commit()  # Commit the changes
        flash('Your reply has been posted!', 'success')
    return redirect(url_for('home'))  # Redirect back to the home page or post details page

@app.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()  # Check if the user already liked the post
    if like:
        db.session.delete(like)  # If the user already liked, remove the like (toggle unlike)
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)  # Add a new like
    db.session.commit()  # Commit changes
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)  # Fetch the post by ID, or return 404 if not found
    return render_template('post.html', post=post, form=CommentForm())  # Render post.html and pass the post and comment form