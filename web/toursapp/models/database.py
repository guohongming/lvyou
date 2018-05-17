__author__ = 'Guo'

import pymongo
import random

class DataBase(object):

    def __init__(self):

        self.client = pymongo.MongoClient('47.94.223.220', 20188)
        self.movie_db = self.client.movie

    # 获取首页所需要的数据： 分类下的6个电影信息

    def write_movie_relation(self, data):
        self.movie_db.movierelation.insert_one(data)

    def get_index_data(self):

        info6s_from_db_love = self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(0).limit(6)
        info6s_from_db_comedy = self.movie_db.movieinfo.find({'types': {'$regex': '喜剧'}}).skip(0).limit(6)
        info6s_from_db_plot = self.movie_db.movieinfo.find({'types': {'$regex': '剧情'}}).skip(6).limit(6)
        info6s_from_db_animation = self.movie_db.movieinfo.find({'types': {'$regex': '动画'}}).skip(12).limit(6)
        info6s_from_db_science = self.movie_db.movieinfo.find({'types': {'$regex': '科幻'}}).skip(18).limit(6)
        info6s_from_db_action = self.movie_db.movieinfo.find({'types': {'$regex': '动作'}}).skip(24).limit(6)
        info6s_from_db_classic = self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(30).limit(6)
        info6s_from_db_suspence = self.movie_db.movieinfo.find({'types': {'$regex': '悬疑'}}).skip(36).limit(6)
        info6s_from_db_youth= self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(42).limit(6)
        info6s_from_db_thriller = self.movie_db.movieinfo.find({'types': {'$regex': '惊悚'}}).skip(48).limit(6)
        info6s_from_db_moving = self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(0).limit(6)

        data = {}

        data['爱情'] = info6s_from_db_love
        data['喜剧'] = info6s_from_db_comedy
        data['剧情'] = info6s_from_db_plot
        data['动画'] = info6s_from_db_animation
        data['科幻'] = info6s_from_db_science
        data['动作'] = info6s_from_db_action
        data['经典'] = info6s_from_db_classic
        data['悬疑'] = info6s_from_db_suspence
        data['青春'] = info6s_from_db_youth
        data['惊悚'] = info6s_from_db_thriller
        data['感人'] = info6s_from_db_moving
        key = ['爱情', '喜剧', '剧情', '动画', '科幻', '动作', '经典', '悬疑', '青春', '惊悚', '感人']

        return data, key

    #  根据id 查询信息,返回一条记录的数据 和 主演的前8
    def get_iterm_data(self, this_id):

        item_from_db = self.movie_db.movieinfo.find_one({'id': this_id})

        return item_from_db

    # 根据分类/skip/limit 查询
    def classify_data_from_tag(self, tag, skip, limit=10):

        skip = int(skip)
        limit = int(limit)
        info = self.movie_db.movieinfo.find({'types': {'$regex': tag}}).skip(skip).limit(limit)
        return info

    # 根据搜索的key 查询数据
    def search_from_key_name(self, key):

        info = self.movie_db.movieinfo.find({'name': {'$regex': key}}).skip(0).limit(20)
        info_stairs = self.movie_db.movieinfo.find({'stars': {'$regex': key}}).skip(0).limit(20)
        info_all = []
        for it in info:
            info_all.append(it)
        for it in info_stairs:
            info_all.append(it)
        return info_all

    def find_user_name(self, name):
        a_user = self.movie_db.userinfo.find_one({'name': name})

        if a_user:
            return True

        return False

    def check_pass(self, name, password):
        a_password = self.movie_db.userinfo.find_one({'name': name})
        if a_password == password:
            return True
        else:
            return False

    def get_self_movies(self,id):
        user_info = self.movie_db.userinfo.find_one({'id':int(id)})
        # print(user_info)
        ids = user_info['recommend_movies']
        # print(ids)
        movies = []
        for id_a in ids:
            movie_a = self.movie_db.movieinfo.find_one({'id':id_a})
            movies.append(movie_a)
        return movies

    def get_random_movies(self):
        num = random.choice(range(0, 1990))
        info = self.movie_db.movieinfo.find().skip(num).limit(6)
        return info


    def get_userid(self):
        users = self.movie_db.userinfo.find()
        ids=[]
        for user in users:
            ids.append(user['id'])
        return ids

    def add_likemovie_to_userid(self,user_id,movie_id):
        user = self.movie_db.userinfo.find_one({'id': int(user_id)})
        likemovies = list(user['like_movies'])
        likemovies.insert(0,movie_id)
        self.movie_db.userinfo.update({"id": int(user_id)},{"$set":{"like_movies":likemovies}})
        return 1


    def remove_likemovie_from_userid(self,user_id,movie_id):
        user = self.movie_db.userinfo.find_one({'id': int(user_id)})
        likemovies = list(user['like_movies'])
        likemovies.remove(movie_id)
        self.movie_db.userinfo.update({"id":int(user_id)},{"$set":{"like_movies":likemovies}})
        return 1

    def get_likes_from_id(self,id):
        user = self.movie_db.userinfo.find_one({'id': int(id)})
        likes = user['like_movies']
        return likes

    def from_user_like_to_recommend(self,id):
        user = self.movie_db.userinfo.find_one({'id': int(id)})
        likemovies = user['like_movies']
        if len(likemovies)==0:
            movie_recom = []
        if len(likemovies)==1:
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[0]})
            movie_recom0 = movie0['relation'][1:13]
            movie_recom = movie_recom0
        if len(likemovies)==2:
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[0]})
            movie_recom0 = movie0['relation'][1:7]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[1]})
            movie_recom1 = movie0['relation'][1:7]
            movie_recom = movie_recom0+movie_recom1
        if len(likemovies)==3:
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[0]})
            movie_recom0 = movie0['relation'][1:5]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[1]})
            movie_recom1 = movie0['relation'][1:5]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[2]})
            movie_recom2 = movie0['relation'][1:5]
            movie_recom = movie_recom0+movie_recom1+movie_recom2

        if len(likemovies)>3:
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[0]})
            movie_recom0 = movie0['relation'][1:4]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[1]})
            movie_recom1 = movie0['relation'][1:4]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[2]})
            movie_recom2 = movie0['relation'][1:4]
            movie0 = self.movie_db.movierelation.find_one({'id':likemovies[3]})
            movie_recom3 = movie0['relation'][1:4]
            movie_recom = movie_recom0+movie_recom1+movie_recom2+movie_recom3
        self.movie_db.userinfo.update({"id":id},{"$set":{"recommend_movies":movie_recom}})

        return 1

    def test(self):

        info = self.movie_db.movieinfo.find({'types': {'$regex': '爱情'}}).skip(0).limit(6)
        for i in info:
            print(i.key)

if __name__ == '__main__':
    db = DataBase()
    # db.test()
    # print(db.find_user_name('guo'))
    print(db.from_user_like_to_recommend(1))


