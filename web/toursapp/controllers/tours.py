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
    if "user_id" in dict(session).keys():
        userid = session['user_id']
        orders = []
        orders_list = db.get_orders_from_id(userid)
        for i in orders_list:
            orders.append(int(i["product_id"]))

    else:
        orders = []
    print(orders)
    return render_template('index.html', data=data, key_index=key,orders = orders)


# 单个产品信息
@movie_blueprint.route('/subject/<this_id>')
def item(this_id):
    if "user_id" in dict(session).keys():
        userid = session['user_id']
        orders = []
        orders_list = db.get_orders_from_id(userid)
        for i in orders_list:
            orders.append(int(i["product_id"]))
    else:
        orders = []
    item_info = db.get_iterm_data(this_id)
    # print(item_info)
    return render_template('item.html', product=item_info,  orders=orders)


# 搜索
@movie_blueprint.route('/search', methods={'POST'})
def search():
    if "user_id" in dict(session).keys():
        user_id = session['user_id']
        orders = []
        orders_list = db.get_orders_from_id(user_id)
        for i in orders_list:
            orders.append(int(i["product_id"]))
        # print(user_id)
    else:
        orders = []
    key = request.form['data']
    info_all = db.search_from_key_name(key)
    return render_template('search.html', key=key, search_data=info_all,orders = orders)


# 分类/分页
@movie_blueprint.route('/tag/<this_tag>', methods={'GET'})
def classify(this_tag):

    if "user_id" in dict(session).keys():
        user_id = session['user_id']
        orders = []
        orders_list = db.get_orders_from_id(user_id)
        for i in orders_list:
            orders.append(int(i["product_id"]))
        # print(user_id)
    else:
        orders = []
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    if int(skip) < 0:
        skip = 0
    data = db.classify_data_from_tag(this_tag, skip, 10)
    print(data)
    pre_skip = int(skip)-10
    next_skip = int(skip)+10
    return render_template('classify.html', classify_data=data, the_tag=this_tag, the_skip=skip, the_limit=10,
                           Previous=pre_skip, next=next_skip, orders=orders)


@movie_blueprint.route('/self', methods={'GET'})
@login_required
def self():
    id = session['user_id']
    orders = db.get_orders_from_id(id)
    result = []
    for item in orders:
        if item["product_id"] not in result:
            result.append(item["product_id"])
    self_products= db.get_recommend(result)

    self_random = db.get_random_movies()

    return render_template('self.html', self_products=self_products, self_random=self_random)


@movie_blueprint.route('/order', methods={'GET'})
@login_required
def order():
    id = session['user_id']
    orders = db.get_orders_from_id(id)
    result = []
    for item in orders:
        item["product_id"]
        item["time"]
        result.append({"time": item["time"], "product": db.get_iterm_data(item["product_id"])})
    return render_template('order.html', order_list=result)


@movie_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404





