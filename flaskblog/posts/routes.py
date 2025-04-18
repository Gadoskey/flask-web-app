from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask_login import login_user, current_user, logout_user, login_required


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()  # Initialize the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)  # Add the new post to the database
        db.session.commit()  # Commit the changes to the database
        flash("Post Created!", 'success')  # Flash a success message
        return redirect(url_for('main.homepage'))  # Redirect to the homepage

    return render_template('newPost.html', title='New Post', form=form, legend='New Post')  # Render the template with form


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated!", 'success')  # Flash a success message
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', title='Update post', form=form, legend='Update Post')

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()  # Commit the changes to the database
    flash("Post Deleted!", 'success')  # Flash a success message
    return redirect(url_for('main.homepage'))