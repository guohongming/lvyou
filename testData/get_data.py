# coding:utf-8
from testData.spider import Spider
import json
import pymongo

client = pymongo.MongoClient(host="47.94.223.220", port=20188)
db = client['lvyou']


# 爬数据 to mongo
def main():
    # url
    url = ""
    spider = Spider()
    data = spider.get_data_from(url)
    data_json = json.loads(data)
    # data_dict = eval(data)
    products = data_json["data"]["list"]
    for product in products:
        insert_to_mongo(filter_data(product))

    print(products)


def insert_to_mongo(data):
    db.product_info.insert_one(data)


def filter_data(data):
    out_data = {}
    out_data['productId'] = data['productId']
    out_data['name'] = data['name']
    out_data['picUrl'] = data['picUrl']
    out_data['classBrandName'] = data['classBrandName']
    out_data['classBrandChildName'] = data['classBrandChildName']
    out_data['satisfaction'] = data['satisfaction']
    out_data['remarkCount'] = data['remarkCount']
    out_data['travelNum'] = data['travelNum']
    out_data['departCity'] = data['departCity']
    out_data['groupCityName'] = data['groupCityName']
    out_data['productFeature'] = data['productFeature']
    out_data['productLevel'] = data['productLevel']
    tag = []
    if data['conditionTagCombination']:
        for i in data['conditionTagCombination']:
            tag += i['tagList']
    out_data['conditionTagCombination'] = tag
    out_data['vendorName'] = data['vendorName']
    return out_data


if __name__ == '__main__':
    main()
