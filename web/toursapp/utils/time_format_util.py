__author__ = 'Guo'
import datetime


def time_to_chinese(source):
    return source.strftime('%Y{y}%m{m}%d{d}  %H:%M:%S').format(y='年', m='月', d='日')


if __name__ == '__main__':
    now = datetime.datetime.now()
    print(time_to_chinese(now))
