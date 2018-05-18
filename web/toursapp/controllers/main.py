__author__ = 'Guo'

from flask import (render_template,
                   current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   flash,
                   jsonify,
                   session)

from toursapp.models.forms import LoginForm, RegisterForm
from toursapp.models.models import User, db_user
from flask_login import login_user, logout_user, current_user, login_required
from toursapp.models import database
import datetime

db = database.DataBase()
main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='./templates'
)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # print(form.username.data)
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()

        login_user(user, remember=form.remember.data)
        flash("you have been logged in !", category="success")
        # print('success')
        return redirect(url_for('movie.index'))
    # print(form.errors)

    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('movie.index'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)

        db_user.session.add(new_user)
        db_user.session.commit()
        flash("Your user has been created, please login.", category="success")

        user = User.query.filter_by(user_name=form.username.data).first()
        # print(user.id)
        like = []
        recom = []
        db.movie_db.userinfo.insert_one({
            'id': user.id, 'like_movies': like, 'recommend_movies': recom})
        return redirect(url_for('.login'))

    return render_template('register.html', form=form)


@main_blueprint.route('/test')
def test():
    return render_template('test.html')


@main_blueprint.route('/add')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(jsonify(result=a + b))

    return jsonify(result=a + b)


@main_blueprint.route('/like')
@login_required
def likemovie():
    userid = session.get('user_id')
    flag = request.args.get('flag', 0, type=int)
    product_id = request.args.get('product_id', 0, type=str)
    now =datetime.datetime.now()

    if flag == 1:
        db.add_like_product_to_userid(userid, product_id, now)

    else:
        db.remove_like_product_from_userid(userid, product_id)
    return jsonify(result=1)


@main_blueprint.route('/refresh')
@login_required
def refresh():
    movies = db.get_random_movies()
    random_movie = {}
    i = 0
    for itm in movies:
        it = {}
        it['id'] = itm['id']
        it['url'] = itm['img_url']
        it['name'] = itm['name'][:8]
        random_movie[str(i)] = it
        i += 1

    return jsonify(random_movie)
