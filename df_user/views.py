#coding=utf-8
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect #导入重定向
from models import *     #引入模型类
from hashlib import sha1 #引入sha1加密模块
from django.http import HttpResponse
#from . import user_decorator
#from df_goods.models import *
# Create your views here.
def register(requste):
    return render(requste,'df_user/register.html')

def register_handle(request):
    #接受用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码（虽然js端已经验证这里最好再次验证）
    if upwd!=upwd2:
        return redirect('/user/register')#false则重定向 返回自己的的页面
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()

    #创建对象（由于django通过模型类与数据库交互 所以这里要创建对象）
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功，转到登陆页面
    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()#返回判断直 要么0 要么1
    return jsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')#如果已经输入直接显示
    context={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户查询对象
    users=UserInfo.objects.filter(uname=uname)#filter get 要是用get要添加异常判断
    print uname
    #判断：如果未查询到则用户名错，如果查询到则判断密码是否正确，正确转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            #记住用户名
            if jizhu!=0:
                red.sed_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)#max_age 过期时间
            request.session['user_id']=users[0].id
            request.session['user_name']=uname#uname使用频率过高直接存在sessionna直接拿来用
            return red
        else:
            context = {'title': '用户登陆', 'error_name': 0, 'error_pwd': 1, 'uname': uname,'upwd':upwd}
            return render(request,'def_user/login.html',context)
    else:
        context = {'title': '用户登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname,'upwd':upwd}
        return render(request, 'def_user/login.html', context)#用户名错 密码对 继续渲染login模板

#@user_decorator.login
def info(request):
    user_email=UserInfo.object.get(id=request.session['user_id']).uemail#显示用户名和邮箱
    context={
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name']
    }
    return render(request,'df_user/user_center_info.html',context)

#@user_decorator.login
def order(request):
    context={"title":'用户中心'}
    return render(request,'df_user/user_center_order.html/',context)

#@user_decorator.login
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user}
    return render(request,'df_user/user_site.html',context)



