# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from pprint import pprint


KEY0 = re.compile(r'学科代码及名称：\d+(\w+)')
KEY1 = re.compile(r'\n([A-C][\+-]?)')
DATA = re.compile(r'([0-9]{5}) *([\u4e00-\u9fa5]+)[^0-9]')


def groups(content, regex):
    parts = regex.split(content)
    return OrderedDict(zip(parts[1::2], parts[2::2]))


def read_data(file_name):
    with open(file_name, 'r') as handle:
        return [
            (key0, key1, id, name)
            for key0, part0 in groups(handle.read(), KEY0).items()
            for key1, part1 in groups(part0, KEY1).items()
            for id, name in DATA.findall(part1)
        ]


def main():
    pprint(read_data(r"D:/Github/ToolsCollection/全国高校学科评估结果.txt"))


if __name__ == '__main__':
    main()