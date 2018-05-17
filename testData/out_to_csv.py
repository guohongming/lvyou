import csv
import pymongo

client = pymongo.MongoClient(host="47.94.223.220", port=20188)
db = client['lvyou']


def write_file(filename, data):
    with open(filename, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(data)


def to_list(data):
    list = []
    for i in data:
        list.append(data[i])
    return list[1:]


def main():
    list_data = db.product_info.find({})
    write_file("products.csv",
               ['productId', 'name', 'picUrl', 'classBrandName', 'classBrandChildName', 'satisfaction', 'remarkCount',
                'travelNum', 'departCity', 'groupCityName', 'productFeature', 'productLevel', 'conditionTagCombination',
                'vendorName'])
    for data in list_data:
        # print(data)
        write_file("products.csv", to_list(data))
        # to_list(data)


if __name__ == '__main__':
    main()
