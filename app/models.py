from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    post = db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}' 

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Quote:
    '''
    Quote class to define Quote Objects
    '''

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    posted_p = db.Column(db.DateTime,default=datetime.utcnow)
    user_p = db.Column(db.Integer,db.ForeignKey("users.id"),  nullable=False)
    
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_post(cls,id):
        posts = Post.query.order_by(post_id=id).desc().all()
        return posts

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted_c = db.Column(db.DateTime,default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_c = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comments.query.filter_by(post_id=id).all()
        return comments

    @classmethod
    def delete_comment(cls,id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()
