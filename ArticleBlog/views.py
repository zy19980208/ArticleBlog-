from django.http import HttpResponse,JsonResponse
from django.template import Template,Context
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator

# import json
# json.dump() # 序列化
# json.loads() # 反序列化


def test(request):
    return HttpResponse('hello')
#登录装饰器
def loginVaild(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('name')
        if username:
            return fun(request,*args,**kwargs)
        else:
            # url = request.META.get('REFERE')
            return HttpResponseRedirect('/login/')
    return inner


@loginVaild
def about(request):
    username = request.COOKIES.get('name')
    user = User.objects.filter(id=id).first()
    return render(request, 'about.html',locals())




def index(request):
    """
    查询6条数据
    查询推荐的七条数据
    查询点击率排行榜的12条数据
    """
    article = Article.objects.order_by('-date')[:6]
    recommend_article = Article.objects.all()[:7]
    click_article = Article.objects.order_by('-click')[:12]
    return render(request, 'index.html',locals())

def listpic(request):
    return render(request, 'listpic.html')

def base(request):
    return render(request, 'base.html')
def articledetails(request,id):
    # id为字符串
    id = int(id)
    article = Article.objects.get(id=id)
    return render(request,'articledetails.html', locals())

def addarticle(request):
    goods_type = Type.objects.all()
    if request.method == 'POST':
        error_msg = ''
        titlename = request.POST.get('title')
        if titlename:
            title = Article.objects.filter(title=titlename).first()
            if not title:
                article = Article()
                article.title = titlename
                article.date = request.POST.get('date')
                article.content = request.POST.get('content')
                article.description = request.POST.get('description')
                article.picture = request.FILES.get('picture')
                article.author_id = request.COOKIES.get('user_id')
                article.save()
                type = request.POST.get('goods_type')
                article.type.add(type)
                article.save()
            else:
                error_msg = '文章已存在'
        else:
            error_msg = '文章名不能为空'
    return render(request,'addarticle.html',locals())

def fytest(request):
    # 使用Django自带分页Paginator的时候，元数据要增排序属性
    article = Article.objects.all().order_by('-date')
    # print(article)
    # 每次显示5条数据
    paginator = Paginator(article,5) # 设置每一页显示多少条，返回一个Paginator
    # print(paginator.count) # 返回内容总条数
    # print(paginator.page_range) # 可迭代的页数
    # print(paginator.num_pages) # 最大页数

    page_obj = paginator.page(2)
    print(page_obj) # 可以有的页数的数据  表示当前对象 <Page 2 of 21>
    for one in page_obj:
        print(one.content)

    print(page_obj.number) # 当前页数
    print(page_obj.has_next()) # 有没有下一页，返回值  是True或者False
    print(page_obj.has_previous()) # 判断是否有上一页 是True 或者False
    print(page_obj.has_other_pages()) # 判断是否有其他页  是True 或者False
    print(page_obj.next_page_number()) # 返回下一页的代码 如果没有下一页 抛出异常
    print(page_obj.previous_page_number()) # 返回上一页的页码


    return HttpResponse('分页功能测试')


def reqtest(request):
    # 获取get请求传递的参数
    # data = request.GET
    # data = request.POST
    # print(data)
    # print(data.get('name'))
    # print(data.get('age'))


    # return HttpResponse('姓名：%s，年龄：%s'%(data.get('name'),data.get('age')))
    # request包含请求信息的，请求对象
    # print(request)
    # print(dir(request))
    # print(request.COOKIES)
    # print(request.FILES)
    # print(request.GET)
    # print(request.POST)
    # print(request.scheme)
    # print(request.method)
    # print(request.path)
    print(request.body)
    # meta = request.META
    # print(meta)
    # for key in meta:
    #     print(key)
    # print('-----')
    # print(request.META.get('OS'))
    # print(request.META.get('HTTP_USER_AGENT'))
    # print(request.META.get('HTTP_HOST'))
    # print(request.META.get('HTTP_REFERER'))


    return HttpResponse('请求测试')

def formtest(request):
    # get 请求
    data = request.GET
    serach = data.get('serach')
    print(serach)
    # 通过form提交的数据，判断数据库中是否存在某个文章
    # 通过模型进行查询
    if serach:
        article = Article.objects.filter(title__contains=serach).all()
        print(article)


    # print(request.method)
    # data = request.POST
    # print(data.get('username'))
    # print(data.get('password'))
    #
    return render(request,'formtest.html',locals())
    # return render_to_reponse('formtest.html',locals())


import hashlib
def setPassword(password):
    # 实现一个密码加密
    md5 = hashlib.md5() # 创建一个md5实例对象
    md5.update(password.encode()) # 进行加密
    result = md5.hexdigest()
    return result



def ajax_get(request):
    return render(request,'ajax_get.html')

def ajax_get_data(request):
    result = {"code":10000,"content":""}
    data = request.GET
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        result['code'] = 10001
        result['content'] = '请求参数为空'
    else:
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            result['code'] = 10000
            result['content'] = '用户可登陆'
        else:
            result['code'] = 10002
            result['content'] = '用户不存在或者密码错误'
    # result['content'] = "成功拿到数据"

    # 返回一个json对象
    return JsonResponse(result)
    # return HttpResponse('这是ajax提交数据')


def ajax_post(request):
    # 调用页面
    return render(request,'ajax_post.html')
def ajax_post_data(request):
    # 注册
    result = {"code":10000,"content":""}
    # print(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User()
    # 注册
    if username == '' or password == '':
        result['code'] = 10001
        result['content'] = '请求参数为空'
    else:
        # 添加用户
        user = User()
        user.name = username
        user.password=setPassword(password)
        try:
            user.save()
            result["code"] = 10000
            result['content'] = '添加数据成功'
        except:
            result['code'] = 10002
            result['content'] = '添加数据失败'
        # user = User.objects.filter(name=username,password=setPassword(password)).first()
        # if user:
        #     result['code'] = 10000
        #     result['content'] = '用户可登陆'
        # else:
        #     result['code'] = 10002
        #     result['content'] = '用户不存在或者密码错误'
    # print(username)
    # print(password)
    return JsonResponse(result)



def checkusername(request):
    result = {'code':10001,'content':''}
    #get 请求
    username = request.GET.get("name")
    print(username)
    # 判断用户是否存在
    user = User.objects.filter(name=username).first()
    if user:
        # 存在
        result = {'code': 10001, 'content': '用户名已存在'}
    else:
        result = {'code': 10000, 'content': '用户名可以使用'}

    return JsonResponse(result)

# 重定向  300问题
from django.http import HttpResponseRedirect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        # print(password)
        # 校验
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            # 用户存在并且密码正确
            if user.password == setPassword(password):
                # 密码正确
                # 跳转首页  状态码  300 重定向
                # return HttpResponseRedirect('/index/')
                response = HttpResponseRedirect('/index/')
                response.set_cookie('name','hello')
                response.set_cookie('user_id',user.id)
                request.session['username']=username
                return response

    return render(request,'login.html')

def logout(request):
    response = HttpResponseRedirect('/index/')
    response.delete_cookie('name')
    # 删除session  目的是用户再次使用相同的sessionid 进行访问，那倒的session的值是不一样的
    del request.session['username'] # 删除指定session  删除的是保存在服务器上面的session的值
    # request.session.flush() # 删除所有的session
    return response

def register(request):

    if request.method == 'POST':
        error_msg = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username:
            user = User.objects.filter(name=username).first()
            if not user:
                user = User()
                user.name = username
                user.password = setPassword(password)
                user.save()
            else:
                error_msg = '用户名已存在'
        else:
            error_msg = '用户名不能为空'

    return render(request,'register.html',locals())