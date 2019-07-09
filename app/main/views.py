from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db, photos
from flask_login import login_required, current_user
from ..models import User, Post, Comment
from .forms import UpdateProfile, PostForm, CommentForm
import markdown2
from ..email import mail_message
from ..requests import get_quote

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to Quote'
    quote= get_quote()
    return render_template('index.html', title = title, quote=quote)
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = 'Welcome to Quote'
    return render_template("profile/profile.html", user = user, title=title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/post/<int:id>')
def post(id):

    '''
    View post page function that returns the post details page and its data
    '''
    posts = Post.query.filter_by(id=id)
    comments = Comment.query.filter_by(post_id=id).all()

    return render_template('post.html',posts = posts,comments = comments)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_p = current_user
        users = User.query.all()
        new_post = Post(user_p=current_user._get_current_object().id, title=title, description = description)

        for user in users:
            mail_message("New post from Quote","email/newpost",user.email,user=user)

        new_post.save_post()
        posts = Post.query.order_by(Post.posted_p.desc()).all()
        return render_template('index.html', posts=posts)
    return render_template('newpost.html', form=form)

@main.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.order_by(Post.posted_p.desc()).all()
    return render_template('posts.html', posts=posts)

@main.route('/comment/new/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)

    if form.validate_on_submit():
        comment = form.comment.data
        
        new_comment = Comment(comment=comment, user_c=current_user._get_current_object().id,post_id=post_id)

        new_comment.save_comment()
        return redirect(url_for('.new_comment',post_id = post_id ))

    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('comments.html', form=form, comments=all_comments, post=post)


@main.route('/post/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index.html"))
