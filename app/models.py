from app.ext import db
from flask_login import UserMixin



# ---------------- USER ----------------

class User(db.Model, UserMixin):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(100),
        nullable=False
    )


    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(200),
        nullable=False
    )


    profile_image = db.Column(
        db.String(500),
        default="https://cdn-icons-png.flaticon.com/512/149/149071.png"
    )


    bio = db.Column(
        db.Text,
        default="No bio yet"
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    # User -> Posts

    posts = db.relationship(
        "Post",
        backref="user",
        cascade="all, delete"
    )



    # User -> Comments

    comments = db.relationship(
        "Comment",
        backref="user",
        cascade="all, delete"
    )



    # User -> Likes

    likes = db.relationship(
        "Like",
        backref="user",
        cascade="all, delete"
    )



    # User -> Created Fandoms

    fandoms = db.relationship(
        "Fandom",
        backref="creator",
        cascade="all, delete"
    )






# ---------------- FANDOM ----------------

class Fandom(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(100),
        nullable=False
    )


    category = db.Column(
        db.String(50)
    )


    description = db.Column(
        db.Text
    )


    image = db.Column(
        db.String(500)
    )



    # creator user

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )



    posts = db.relationship(
        "Post",
        backref="fandom",
        cascade="all, delete"
    )







# ---------------- POST ----------------

class Post(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    text = db.Column(
        db.Text,
        nullable=False
    )



    fandom_id = db.Column(
        db.Integer,
        db.ForeignKey("fandom.id")
    )



    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )



    comments = db.relationship(
        "Comment",
        backref="post",
        cascade="all, delete"
    )



    likes = db.relationship(
        "Like",
        backref="post",
        cascade="all, delete"
    )







# ---------------- COMMENT ----------------

class Comment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    text = db.Column(
        db.Text,
        nullable=False
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id")
    )








# ---------------- LIKE ----------------

class Like(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id")
    )