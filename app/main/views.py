from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db,photos
from flask_login import login_required, current_user
from ..models import User, Blog, Comment, Upvote, Downvote
from .forms import UpdateProfile, BlogForm, CommentForm
import markdown2

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to my Blog'
    return render_template('index.html', title = title)
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = 'Welcome to my Blog'
    return render_template("profile/profile.html", user = user)

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

@main.route('/<cat>', methods=['GET', 'POST'])
def category(cat):
    cat = cat
    blog = Blog.query.filter_by(category=cat).order_by(Blog.posted.desc()).all()

    title = 'Welcome to my Blog'
    return render_template('category.html', blog=blog)

@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():

    form = BlogForm()
    my_upvotes = Upvote.query.filter_by(blog_id=Blog.id)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_p = current_user
        category = form.category.data

        new_blog = Blog(user_p=current_user._get_current_object().id, title=title, category=category, description = description)

        new_blog.save_blog()
        blog = Blog.query.filter_by(category=category).order_by(Blog.posted.desc()).all()
        return render_template('category.html', blog=blog)
    return render_template('blog.html', form=form)

@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)

    if form.validate_on_submit():
        comment = form.comment.data
         
        # Updated comment instance
        new_comment = Comment(comment=comment,user_c=current_user._get_current_object().id, blog_id=blog_id)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.new_comment',blog_id = blog_id ))

    all_comments = Comment.query.filter_by(blog_id=blog_id).all()
    return render_template('comments.html', form=form, comments=all_comments, blog=blog)

@main.route('/blog/upvote/<int:blog_id>/upvote', methods=['GET','POST'])
@login_required
def upvote(blog_id):
    blog = Blog.query.get(blog_id)
    user = current_user
    blog_upvotes = Upvote.query.filter_by(blog_id=blog_id)
    blog = Blog.query.filter_by(category=blog.category).order_by(Blog.posted.desc()).all()

    if Upvote.query.filter(Upvote.user_id == user.id, Upvote.blog_id == blog_id).first():
        return render_template('category.html', blog=blog)

    new_upvote = Upvote(blog_id=blog_id, user=current_user)
    new_upvote.save_upvotes()
    
    return render_template('category.html', blog=blog)

@main.route('/blog/downvote/<int:blog_id>/downvote', methods=['GET', 'POST'])
@login_required
def downvote(blog_id):
    blog = Blog.query.get(blog_id)
    user = current_user
    blog_downvotes = Downvote.query.filter_by(blog_id=blog_id)
    blog = Blog.query.filter_by(category=blog.category).order_by(Blog.posted.desc()).all()

    if Downvote.query.filter(Downvote.user_id == user.id, Downvote.blog_id == blog_id).first():
        return render_template('category.html', blog=blog)

    new_downvote = Downvote(blog_id=blog_id, user=current_user)
    new_downvote.save_downvotes()
    return render_template('category.html', blog=blog)

@main.route('/myblog', methods=['GET', 'POST'])
@login_required
def my_blog():
    user = current_user._get_current_object().id
    blog = Blog.query.filter_by(user_p=user)
    return render_template('category.html', blog=blog)
