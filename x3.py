# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:daly

# 1. 字典根据key查找，速度非常快（索引）
# val = {
#     'k1':'v1',
#     'k2':'v2'
# }
# print(val['k1'])


# 2. 列表和字典和可变类型（引用类型）
# v1 = [11,22]
# v2 = v1
# v2.append(33)
# print(v1)
# print(v2)


# li = [
#     {'id':1,'name':'alex'},
#     {'id':2,'name':'eric'},
# ]
# v1 = li[0]
# print(li[0])
# print(v1)
# v1['active'] = True
# print(li)
# print(v1)


# li = [
#     {'id':1,'name':'alex'},
#     {'id':2,'name':'eric'},
# ]
#
# li2 = [
#     li[0],
#     li[1],
# ]
# for item in li:
#     li2.append(item)
#
# li2[0]['active'] = True
#
# print(li)
# [{'id': 1, 'name': 'alex', 'active': True}, {'id': 2, 'name': 'eric'}]