from flask import Flask, render_template, request, session
from flask import Blueprint, redirect, url_for
from toursapp.models import myjinjafilter, database
from flask_login import login_required

movie_blueprint = Blueprint(
    'movie',
    __name__,
    template_folder='./templates'
)

db = database.DataBase()


# 首页
@movie_blueprint.route('/')
def index():
    data, key = db.get_index_data()
    # # print(info6s_from_db[0])
    # if "user_id" in dict(session).keys():
    #     userid = session['user_id']
    #     likes = db.get_likes_from_id(userid)
    #     #print(userid)
    # else:
    #     likes = []
    return render_template('index.html', data=data, key_index=key)


# 单个电影信息

@movie_blueprint.route('/subject/<this_id>')
def item(this_id):
    if "user_id" in dict(session).keys():
        userid = session['user_id']
        likes = db.get_likes_from_id(userid)
        # print(userid)
    else:
        likes = []
    item_info = db.get_iterm_data(this_id)
    return render_template('item.html', item=item_info,  likemovies=likes)


# 搜索
@movie_blueprint.route('/search/<key>', methods={'GET'})
def search():
    info_all = db.search_from_key_name(key)
    return render_template('search.html', key=key, search_data=info_all)


# 分类/分页
@movie_blueprint.route('/tag/<this_tag>', methods={'GET'})
def classify(this_tag):

    if "user_id" in dict(session).keys():
        userid = session['user_id']
        likes = db.get_likes_from_id(userid)
        # print(userid)
    else:
        likes = []
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    if int(skip) < 0:
        skip = 0
    data = db.classify_data_from_tag(this_tag, skip, 10)
    # print(data)
    pre_skip = int(skip)-10
    next_skip = int(skip)+10
    return render_template('classify.html', classify_data=data, the_tag=this_tag, the_skip=skip, the_limit=10,
                           Previous=pre_skip, next=next_skip, likemovies=likes)


@movie_blueprint.route('/self', methods={'GET'})
@login_required
def self():
    id = session['user_id']
    db.from_user_like_to_recommend(int(id))
    self_movies = db.get_self_movies(int(id))
    selfmovies_random = db.get_random_movies()
    selfmovies_hot_ids = db.get_likes_from_id(id)
    selfmovies_hot = []
    for i in selfmovies_hot_ids:
        itm = db.get_iterm_data(i)
        selfmovies_hot.append(itm)

    #if len(selfmovies_hot)>6:
     #   selfmovies_hot = selfmovies_hot[:6]
    likes = db.get_likes_from_id(int(id))

    return render_template('self.html', selfmovies=self_movies, selfmovies_random=selfmovies_random, selfmovies_hot=selfmovies_hot, likemovies=likes)


@movie_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404





