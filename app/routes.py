from flask import Blueprint, render_template, request, redirect
from app.models import Fandom, Post, User, Comment, Like
from app.ext import db, login_manager
from app.forms import RegisterForm, LoginForm, FandomForm, PostForm

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


bp = Blueprint("main", __name__)
@bp.route("/test")
def test():
    return "Route works"

# ---------------- USER LOADER ----------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ---------------- HOME ----------------
@bp.route("/")
@login_required
def home():

    search = request.args.get("search")


    if search:

        fandoms = Fandom.query.filter(
            (Fandom.title.ilike(f"%{search}%")) |
            (Fandom.category.ilike(f"%{search}%"))
        ).all()

    else:

        fandoms = Fandom.query.all()


    return render_template(
        "home.html",
        fandoms=fandoms
    )



# ---------------- REGISTER ----------------

@bp.route("/register", methods=["GET","POST"])
def register():

    form = RegisterForm()


    if form.validate_on_submit():

        password = generate_password_hash(
            form.password.data
        )


        user = User(
            username=form.username.data,
            email=form.email.data,
            password=password
        )


        db.session.add(user)
        db.session.commit()


        return redirect("/login")



    return render_template(
        "register.html",
        form=form
    )



# ---------------- LOGIN ----------------

@bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()


        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            return redirect("/")


    return render_template(
        "login.html",
        form=form
    )

# ---------------- LOGOUT ----------------

@bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")



# ---------------- ADD FANDOM ----------------

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_fandom():

    form = FandomForm()

    if form.validate_on_submit():

        fandom = Fandom(

            title=form.title.data,

            category=form.category.data,

            description=form.description.data,

            image=form.image.data,

            user_id=current_user.id

        )


        db.session.add(fandom)
        db.session.commit()


        return redirect("/")


    return render_template(
        "add_fandom.html",
        form=form
    )

# ---------------- FANDOM DETAILS ----------------

@bp.route("/fandom/<int:fandom_id>")
@login_required
def fandom_detail(fandom_id):

    fandom = Fandom.query.get_or_404(fandom_id)


    return render_template(
        "fandom_detail.html",
        fandom=fandom
    )



# ---------------- ADD POST ----------------

@bp.route("/fandom/<int:id>/post", methods=["POST"])
@login_required
def add_post(id):

    post = Post(

        text=request.form["text"],

        fandom_id=id,

        user_id=current_user.id

    )


    db.session.add(post)

    db.session.commit()


    return redirect(f"/fandom/{id}")



# ---------------- EDIT POST ----------------

@bp.route("/post/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)


    # მხოლოდ ავტორს შეუძლია რედაქტირება
    if post.user_id != current_user.id:
        return redirect("/")


    if request.method == "POST":

        post.text = request.form["text"]

        db.session.commit()

        return redirect(
            f"/fandom/{post.fandom_id}"
        )


    return render_template(
        "edit_post.html",
        post=post
    )


# ---------------- DELETE POST ----------------

@bp.route("/post/delete/<int:id>")
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)


    # მხოლოდ ავტორს შეუძლია წაშლა
    if post.user_id != current_user.id:
        return redirect("/")


    fandom_id = post.fandom_id


    db.session.delete(post)

    db.session.commit()


    return redirect(f"/fandom/{fandom_id}")



# ---------------- PROFILE ----------------

@bp.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )



# ---------------- EDIT PROFILE ----------------

@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        current_user.username = request.form["username"]

        current_user.profile_image = request.form["image"]

        current_user.bio = request.form["bio"]


        db.session.commit()


        return redirect("/profile")


    return render_template(
        "edit_profile.html",
        user=current_user
    )
# ---------------- LIKE / UNLIKE POST ----------------

@bp.route("/post/<int:id>/like")
@login_required
def like_post(id):

    post = Post.query.get_or_404(id)


    existing_like = Like.query.filter_by(
        post_id=post.id,
        user_id=current_user.id
    ).first()


    # თუ უკვე დალაიქებულია -> წავშლით
    if existing_like:

        db.session.delete(existing_like)

    # თუ არ არის -> დავამატებთ
    else:

        like = Like(
            post_id=post.id,
            user_id=current_user.id
        )

        db.session.add(like)


    db.session.commit()


    return redirect(
        f"/fandom/{post.fandom_id}"
    )





# ---------------- ADD COMMENT ----------------

@bp.route("/post/<int:id>/comment", methods=["POST"])
@login_required
def add_comment(id):

    comment = Comment(

        text=request.form["text"],

        post_id=id,

        user_id=current_user.id

    )


    db.session.add(comment)

    db.session.commit()


    post = Post.query.get(id)


    return redirect(
        f"/fandom/{post.fandom_id}"
    )





# ---------------- DELETE COMMENT ----------------

@bp.route("/comment/delete/<int:id>")
@login_required
def delete_comment(id):

    comment = Comment.query.get_or_404(id)


    # მხოლოდ საკუთარი კომენტარის წაშლა შეუძლია
    if comment.user_id != current_user.id:

        return redirect("/")


    post = comment.post


    db.session.delete(comment)

    db.session.commit()

    return redirect(
        f"/fandom/{post.fandom_id}#post-{post.id}"
    )

# ---------------- DELETE FANDOM ----------------

@bp.route("/fandom/delete/<int:id>")
@login_required
def delete_fandom(id):

    fandom = Fandom.query.get(id)


    if fandom.user_id == current_user.id or current_user.is_admin:

        db.session.delete(fandom)

        db.session.commit()


    return redirect("/")