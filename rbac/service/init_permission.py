from django.conf import settings


def init_permission(user, request):
    """
    用于做用户登录成功之后，权限信息的初始化。
    :param user:登录的用户对象
    :param request:请求相关的对象
    :return:
    """
    """
    [
        {'permissions__title': '用户列表', 'permissions__url': '/users/', 'permissions__code': 'list', 'permissions__group_id': 1}
        {'permissions__title': '添加用户', 'permissions__url': '/users/add/', 'permissions__code': 'add', 'permissions__group_id': 1}
        {'permissions__title': '删除用户', 'permissions__url': '/users/del/(\d+)/', 'permissions__code': 'del', 'permissions__group_id': 1}
        {'permissions__title': '修改用户', 'permissions__url': '/users/edit/(\d+)/', 'permissions__code': 'edit', 'permissions__group_id': 1}
        {'permissions__title': '主机列表', 'permissions__url': '/hosts/', 'permissions__code': 'list', 'permissions__group_id': 2}
        {'permissions__title': '添加主机', 'permissions__url': '/hosts/add/', 'permissions__code': 'add', 'permissions__group_id': 2}
        {'permissions__title': '删除主机', 'permissions__url': '/hosts/del/(\d+)/', 'permissions__code': 'del', 'permissions__group_id': 2}
        {'permissions__title': '修改主机', 'permissions__url': '/hosts/edit/(\d+)/', 'permissions__code': 'edit', 'permissions__group_id': 2}
    ]

    {
        1(权限组ID): {
            urls: [/users/,/users/add/ ,/users/del/(\d+)/],
            codes: [list,add,del]
        },
        2: {
            urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
            codes: [list,add,del]
        }
    }
    """
    permission_list = user.roles.filter(permissions__id__isnull=False).values(
        'permissions__id',  # 权限  'permissions__id': 1
        'permissions__title',  # 权限名称
        'permissions__url',  # 权限URL
        'permissions__code',  # 权限CODE
        'permissions__group_menu_id',  # 组内菜单ID(null表示自己是菜单，1)
        'permissions__group_id',  # 权限组ID
        'permissions__group__menu__id',  # 一级菜单ID
        'permissions__group__menu__name',  # 一级菜单名称
    ).distinct()  # 去重
    # print(permission_list)
    # < QuerySet
    #     [
    #         {'permissions__id': 1, 'permissions__title': '用户列表', 'permissions__url': '/users/','permissions__code': 'list', 'permissions__group_menu_id': None, 'permissions__group_id': 1,'permissions__group__menu__id': 1, 'permissions__group__menu__name': '菜单1'},
    #         {'permissions__id': 2,'permissions__title': '添加列表','permissions__url': '/users/add/', 'permissions__code': 'add','permissions__group_menu_id': 1,'permissions__group_id': 1, 'permissions__group__menu__id': 1,'permissions__group__menu__name': '菜单1'},
    #         { 'permissions__id': 3, 'permissions__title': '删除列表', 'permissions__url': '/users/del/(\\d+)/', 'permissions__code': 'del', 'permissions__group_menu_id': 1, 'permissions__group_id': 1,'permissions__group__menu__id': 1, 'permissions__group__menu__name': '菜单1'},
    #         {'permissions__id': 4,'permissions__title': '修改列表', 'permissions__url': '/users/edit/(\\d+)/', 'permissions__code': 'edit','permissions__group_menu_id': 1, 'permissions__group_id': 1,'permissions__group__menu__id': 1,'permissions__group__menu__name': '菜单1'},
    #         {'permissions__id': 5, 'permissions__title': '主机列表', 'permissions__url': '/hosts/','permissions__code': 'list', 'permissions__group_menu_id': None, 'permissions__group_id': 2,'permissions__group__menu__id': 2, 'permissions__group__menu__name': '菜单2'},
    #         {'permissions__id': 6, 'permissions__title': '添加主机','permissions__url': '/hosts/add/','permissions__code': 'add', 'permissions__group_menu_id': 5, 'permissions__group_id': 2,'permissions__group__menu__id': 2,'permissions__group__menu__name': '菜单2'},
    #         {'permissions__id': 7, 'permissions__title': '删除主机', 'permissions__url': '/hosts/del/(\\d+)/','permissions__code': 'del', 'permissions__group_menu_id': 5, 'permissions__group_id': 2,'permissions__group__menu__id': 2, 'permissions__group__menu__name': '菜单2'},
    #         {'permissions__id': 8,'permissions__title': '修改主机', 'permissions__url': '/hosts/edit/(\\d+)/', 'permissions__code': 'edit','permissions__group_menu_id': 5,'permissions__group_id': 2,'permissions__group__menu__id': 2,'permissions__group__menu__name': '菜单2'}
    #     ]
    # >
    # 获取权限信息+组+菜单，放入session，用于以后在页面上自动生成动态菜单。
    permission_memu_list = []
    for item in permission_list:
        val = {
            'id': item['permissions__id'],   # 'id': 1,
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__group_menu_id'],
            'menu_id': item['permissions__group__menu__id'],
            'menu__name': item['permissions__group__menu__name'],
        }
        permission_memu_list.append(val)
        # print(permission_memu_list)
        # [
        #     {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
        #     {'id': 2, 'title': '添加列表', 'url': '/users/add/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
        #     {'id': 3, 'title': '删除列表', 'url': '/users/del/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
        #     {'id': 4, 'title': '修改列表', 'url': '/users/edit/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
        #     {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'},
        #     {'id': 6, 'title': '添加主机', 'url': '/hosts/add/', 'pid': 5, 'menu_id': 2, 'menu__name': '菜单2'},
        #     {'id': 7, 'title': '删除主机', 'url': '/hosts/del/(\\d+)/', 'pid': 5, 'menu_id': 2, 'menu__name': '菜单2'},
        #     {'id': 8, 'title': '修改主机', 'url': '/hosts/edit/(\\d+)/', 'pid': 5, 'menu_id': 2, 'menu__name': '菜单2'}
        # ]
    request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_memu_list



    # 获取权限信息，放入session，用于以后在中间件中权限进行匹配
    permission_dict = {}
    """
   {
       1: {
           urls: ['/users/', ],
           codes: ['list',]
       }
   }

   """
    for permission in permission_list:
        group_id = permission['permissions__group_id']  # 字典，获取权限表（权限组）ID
        url = permission['permissions__url']  # 获取权限表url
        code = permission['permissions__code']  # 获取权限表code
        if group_id in permission_dict:  # 起始permission_dict为空，先执行else
            permission_dict[group_id]['urls'].append(url)
            permission_dict[group_id]['codes'].append(code)
        else:
            permission_dict[group_id] = {'urls': [url, ], 'codes': [code, ]}
    # print(permission_dict)
    '''
    当叶良辰登录时，动态抓取角色的初始化权限信息
    {
        1: {'urls': ['/users/', '/users/add/', '/users/del/(\\d+)/', '/users/edit/(\\d+)/'],
         'codes': ['list', 'add', 'del', 'edit']
         },
        2: {'urls': ['/hosts/', '/hosts/add/', '/hosts/del/(\\d+)/', '/hosts/edit/(\\d+)/'],
         'codes': ['list', 'add', 'del', 'edit']
         }
    }
    '''
    request.session[settings.PERMISSION_DICT_SESSION_KEY] = permission_dict



