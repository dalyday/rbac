# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:daly

data_list = {
    5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True},
    10: {'id': 10, 'title': 'xx列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'}
}
result = {}
for item in data_list.values():
    # print(item)
    # {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'}
    # {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True}
    # {'id': 10, 'title': 'xx列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'}
    menu_id = item['menu_id']
    if menu_id in result:
        temp = {'id':item['id'],'title':item['title'],'url':item['url'],'active':item.get('active',False)}
        result[menu_id]['chilren'].append(temp)
        if item.get('active',False):
            result[menu_id]['active'] = item.get('active',False)
    else:
        result[menu_id] = {
            'menu__name':item['menu__name'],
            'active':item.get('active',False),
            'chilren':[
                {'id':item['id'],'title':item['title'],'url':item['url'],'active':item.get('active',False)}
            ]
        }
print(result)

# {
#     1: {
#         'menu__name': '菜单1',
#         'active': False,
#         'children': [
#             {'id': 1, 'title': '用户列表', 'url': '/users/', 'active': True}
#         ]
#     },
#     2: {
#         'menu__name': '菜单1',
#         'children': [
#             {'id': 10, 'title': 'xx列表', 'url': '/hosts/'}
#         ]
#
#     }
# }