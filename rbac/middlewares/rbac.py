import re
from django.conf import settings
from django.shortcuts import HttpResponse

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request):
        # 当前访问的URL
        current_url = request.path_info
        for valid in settings.VALID_LIST:   #  VALID_LIST包含所有白名单的列表
            if re.match(valid, current_url):
                return None             # 如果与白名单匹配成功则通过；否则走下面权限路径

        # 当前用户的所有权限
        permission_dict = request.session.get(settings.PERMISSION_DICT_SESSION_KEY)
        # print(permission_dict)
        # （角色：叶良辰）
        # {
        #     '1': {
        #         'urls': ['/users/', '/users/add/', '/users/del/(\\d+)/', '/users/edit/(\\d+)/'],
        #         'codes': ['list', 'add', 'del', 'edit']
        #         },
        #     '2': {
        #         'urls': ['/hosts/', '/hosts/add/', '/hosts/del/(\\d+)/', '/hosts/edit/(\\d+)/'],
        #         'codes': ['list', 'add', 'del', 'edit']
        #     }
        # }
        if not permission_dict:
            return HttpResponse('当前用户无权限信息')

        # 用户权限和当前URL进行匹配
        flag = False
        for item in permission_dict.values():
            urls = item['urls']
            codes = item['codes']
            for rex in urls:
                reg = settings.REX_FORMAT %(rex,)# 调用settings相关权限配置
                if re.match(reg,current_url):   # reg固定起始符，终止符与当前url匹配
                    flag = True
                    request.permission_codes = codes
                    break
            if flag:
                break
        if not flag:
            return HttpResponse('无权限访问')