from rbac.service.init_permission import init_permission
from django.shortcuts import render, HttpResponse
from app01.form import LoginFrom
from rbac import models
from django.conf import settings #此处的setting包含了自定义+内置
# from day12 import settings      #此处的setting仅包含用户自定义
# from utils.md5 import md5


""" 两个验证，第一个是form验证，第二个是帐号或者密码不存在错误 """
def login(request):
    if request.method == "GET":
        form = LoginFrom()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginFrom(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)  通过form验证可以拿到前端的用户名，密码 {'username': '叶良辰', 'password': '123'}
            # form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            #另外两种
            # models.UserInfo.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            # models.UserInfo.objects.filter(**{'username':'daly','password':123456})
            if user:
                # 将用户信息放置到session中,user是个对象，python只能序列化字典，元组
                request.session[settings.USER_SESSION_KEY] = {'id':user.id,'username':user.username}
                # print(user.id,user.username)   # 1 叶良辰
                # 获取当前用户的所有角色
                # role_liat = user.roles.all()
                # print(role_liat)   打印出来的为对象，使用__str__回调函数可以显示中文
                init_permission(user, request)  # 跟init_permission函数关联，作用权限初始化
                return HttpResponse('登陆成功')
            else:
                form.add_error('password', '用户名或密码错误')
        return render(request, 'login.html', {'form': form})


def users(request):
    # print(request.permission_codes)
    # ['list', 'add', 'del', 'edit']
    user_list = models.UserInfo.objects.all()
    return render(request,'users.html',{'user_list':user_list})


def user_add(request):
    return HttpResponse('添加页面！')


def hosts(request):
    return render(request,'hosts.html')




# from app01 import models
# @cache_page(2)#超时时间2秒
# def test(request):
    # models.Info.objects.create(name='jack')
    # print('你好!')
    # return HttpResponse("...")
    # ctime = str(time.time())
    # return HttpResponse(ctime)
    # ctime = str(time.time())
    # return render(request,'test.html',{'ctime':ctime})