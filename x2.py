import re
permission_menu_list = [
    {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 2, 'title': '添加用户', 'url': '/users/add/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 3, 'title': '删除用户', 'url': '/users/del/(\d+)/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 4, 'title': '修改用户', 'url': '/users/edit/(\d+)/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 6, 'title': '添加主机', 'url': '/hosts/add/', 'pid': 5, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 7, 'title': '删除主机', 'url': '/hosts/del/(\d+)/', 'pid': 5, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 8, 'title': '修改主机', 'url': '/hosts/edit/(\d+)/', 'pid': 5, 'menu_id': 1, 'menu__name': '菜单1'}
]
# current_url = "/users/"
current_url = "/users/del/1/"

"""
leetcode
current_url和url通过正则匹配，如果匹配成功： 
        if pid == None:
            自己添加active=True
        else:
            获取当前循环行的pid，根据 pid,找到指定数据：active=True

    获取其中是菜单的权限（'pid': None）
"""

per_dict = {}
for item in permission_menu_list:
    if not item['pid']:
        per_dict[item['id']] = item
# print(per_dict)
"""
{
    1:  {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    5:  {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
}
"""

for item in permission_menu_list:
    if not re.match(item['url'], current_url):
        continue        # 没有匹配成功继续
    # 匹配成功
    if item['pid']:     # 如果pid不为空，为真
        per_dict[item['pid']]['active'] = True  # pid的大字典里面加入'active': True
    else:
        item['active'] = True

print(per_dict)
# {
#     1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True},
#     5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'}
# }
