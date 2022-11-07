from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/new-post", methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')

        if not title:
            flash('Both fields are compulsory', category='error')
        elif not text:
            flash('Both fields are compulsory', category='error')
        else:
            post = Post(text=text, title=title, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('new_post.html', user=current_user)


@views.route("/edit-post/<id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        
        post.title = title
        post.text = text
        db.session.commit()
        flash('Post updated.', category='success')
        return redirect(url_for('views.home', id=id))

    return render_template('edit_post.html', user=current_user, post=post)
    

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))
        

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)