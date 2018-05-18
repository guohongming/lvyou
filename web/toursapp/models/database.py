__author__ = 'Guo'

import pymongo
import random


class DataBase(object):

    def __init__(self):

        self.client = pymongo.MongoClient('47.94.223.220', 20188)
        self.lvyou = self.client.lvyou
        self.product_info = self.lvyou.product_info
        self.order_list = self.lvyou.order_list
        self.similar = self.lvyou.similar

    # 获取首页所需要的数据： 分类下的6个电影信息

    def write_movie_relation(self, data):
        self.movie_db.movierelation.insert_one(data)

    def get_index_data(self):

        info_1 = self.product_info.find({'classBrandName': "跟团游"}).limit(6)
        info_2 = self.product_info.find({'classBrandName': "自助游"}).limit(6)
        info_3 = self.product_info.find({'classBrandName': "自驾游"}).limit(6)

        data = {}
        data['跟团游'] = info_1
        data['自助游'] = info_2
        data['自驾游'] = info_3

        key = ['跟团游', '自助游', '自驾游']

        return data, key

    #  根据id 查询信息,返回一条记录的数据
    def get_iterm_data(self, this_id):

        item_from_db = self.product_info.find_one({'product_id': this_id})

        return item_from_db

    # # 根据分类/skip/limit 查询
    def classify_data_from_tag(self, tag, skip, limit=10):

        skip = int(skip)
        limit = int(limit)
        info = self.product_info.find({'classBrandName': {'$regex': tag}}).skip(skip).limit(limit)
        return info

    # 根据搜索的key 查询数据
    def search_from_key_name(self, key):
        info = self.product_info.find({'name': {'$regex': key}}).limit(20)
        info_cat= self.product_info.find({'classBrandName': {'$regex': key}}).limit(20)
        info_all = []
        info_ids = []
        for it in info:
            if not it['product_id'] in info_ids:
                info_all.append(it)
        for it in info_cat:
            if not it['product_id'] in info_ids:
                info_all.append(it)
        return info_all

    # def find_user_name(self, name):
    #     a_user = self.movie_db.userinfo.find_one({'name': name})
    #
    #     if a_user:
    #         return True
    #
    #     return False
    #
    # def check_pass(self, name, password):
    #     a_password = self.movie_db.userinfo.find_one({'name': name})
    #     if a_password == password:
    #         return True
    #     else:
    #         return False
    #
    def get_self_orders(self, id):
        user_info = self.order_list.find_one({'id': int(id)})
        # print(user_info)
        ids = user_info['orders']
        # print(ids)
        orders = []
        for id_a in ids:
            order_a = self.order_list.find_one({'id': id_a})
            orders.append(order_a)
        return orders
    #
    # def get_random_movies(self):
    #     num = random.choice(range(0, 1990))
    #     info = self.movie_db.movieinfo.find().skip(num).limit(6)
    #     return info
    #
    # def get_userid(self):
    #     users = self.movie_db.userinfo.find()
    #     ids = []
    #     for user in users:
    #         ids.append(user['id'])
    #     return ids
    #

    def add_like_product_to_userid(self, user_id, product_id, now):
        user = self.order_list.find_one({'id': int(user_id)})
        if user:
            like_products = list(user['order_list'])
            like_products.insert(0, {"product_id":product_id, "time":now})
            self.order_list.update({"id": int(user_id)}, {"$set": {"order_list": like_products}})
        else:
            like_products = [{"product_id":product_id, "time":now}]
            data = {"id": int(user_id), "order_list": like_products}
            self.order_list.insert_one(data)
        return 1

    def remove_like_product_from_userid(self, user_id, product_id):
        user = self.order_list.find_one({'id': int(user_id)})
        like_products = list(user['order_list'])
        products = []
        for i in like_products:
            if i["product_id"] != product_id:
                products.append(i)
        self.order_list.update({"id": int(user_id)}, {"$set": {"order_list": products}})
        return 1

    def get_orders_from_id(self, id):
        user = self.order_list.find_one({'id': int(id)})
        if user:
            orders = user['order_list']
        else:
            orders = []
        return orders

    # def from_user_like_to_recommend(self, id):
    #     user = self.movie_db.userinfo.find_one({'id': int(id)})
    #     likemovies = user['like_movies']
    #     if len(likemovies) == 0:
    #         movie_recom = []
    #     if len(likemovies) == 1:
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[0]})
    #         movie_recom0 = movie0['relation'][1:13]
    #         movie_recom = movie_recom0
    #     if len(likemovies) == 2:
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[0]})
    #         movie_recom0 = movie0['relation'][1:7]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[1]})
    #         movie_recom1 = movie0['relation'][1:7]
    #         movie_recom = movie_recom0 + movie_recom1
    #     if len(likemovies) == 3:
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[0]})
    #         movie_recom0 = movie0['relation'][1:5]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[1]})
    #         movie_recom1 = movie0['relation'][1:5]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[2]})
    #         movie_recom2 = movie0['relation'][1:5]
    #         movie_recom = movie_recom0 + movie_recom1 + movie_recom2
    #
    #     if len(likemovies) > 3:
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[0]})
    #         movie_recom0 = movie0['relation'][1:4]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[1]})
    #         movie_recom1 = movie0['relation'][1:4]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[2]})
    #         movie_recom2 = movie0['relation'][1:4]
    #         movie0 = self.movie_db.movierelation.find_one({'id': likemovies[3]})
    #         movie_recom3 = movie0['relation'][1:4]
    #         movie_recom = movie_recom0 + movie_recom1 + movie_recom2 + movie_recom3
    #     self.movie_db.userinfo.update({"id": id}, {"$set": {"recommend_movies": movie_recom}})
    #
    #     return 1
    #
    # def test(self):
    #
    #     info = self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(0).limit(6)
    #     for i in info:
    #         print(i.key)


if __name__ == '__main__':
    db = DataBase()
    # db.test()
    # print(db.find_user_name('guo'))
    print(db.from_user_like_to_recommend(1))
