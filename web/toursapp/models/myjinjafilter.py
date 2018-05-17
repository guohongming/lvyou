__author__ = 'Guo'


# 自定义 jinja 过滤器 // 名字=》单个名字，原名字是以空格隔开的,并且只取前八个字符
def make_name_to_one(string):
    name = string.split(' ')[0]
    if len(name) > 8:
        name = name[:8]
    return name

