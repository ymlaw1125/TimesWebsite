from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import HttpRequest
from django.shortcuts import render, reverse, redirect
from django.views.generic import RedirectView
from django.contrib.auth import get_user_model
from .models import Magazine
from magazines import forms
from datetime import datetime
from django.db.models import Q
# email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
User = get_user_model()
def send_email(sender, addr, port, receiver, secret, header, body):
    # 1. 连接邮箱服务器
    con = smtplib.SMTP_SSL(addr, port)
    # 2. 登录邮箱
    con.login(sender, secret)
    # 2. 准备数据
    # 创建邮件对象
    msg = MIMEMultipart()
    # 设置邮件主题
    subject = Header(header, 'utf-8').encode()
    msg['Subject'] = subject
    # 设置邮件发送者
    msg['From'] = sender + "<" + sender + ">"
    # 设置邮件接受者
    msg['To'] = receiver
    # 添加⽂文字内容
    text = MIMEText(body, 'plain', 'utf-8')
    msg.attach(text)
    # 3.发送邮件
    con.sendmail(sender, receiver, msg.as_string())
    print("Success")
    con.quit()

def home(request):
    assert isinstance(request, HttpRequest)
    magazines = Magazine.objects.order_by('-upload_date')[:3]
    all_mags = Magazine.objects.all()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'addMagazine':
            form = forms.MagazineForm(request.POST, request.FILES)
            if form.is_valid():
                print("magazine add success")
                form.save()
                for user in User.objects.filter(subscribe=True):
                    email = user.email
                    # TODO - change email header and content
                    send_email('ymlaw1125@163.com', 'smtp.163.com', 465, email, 'ECIJLSHSVZDEBGYF', 'test header', 'test body')
            else:
                print(form)
                print(request.POST)
                print(request.FILES)
        elif request.POST.get("form_type") == 'removeMagazine':
            magazine_id = request.POST['Magazine']
            Magazine.objects.filter(id=magazine_id).delete()
    return render(request, 'index.html', {"title": "Home", "recent_issues": magazines, 'magazines': all_mags})


def magazine(request, magazine_id):
    assert isinstance(request, HttpRequest)
    mag = Magazine.objects.filter(id=magazine_id)[0]
    recents = Magazine.objects.filter(~Q(id=magazine_id)).order_by('-upload_date')[:5]
    return render(
        request,
        'magazine.html',
        {
            "title": "Magazine",
            "magazine": mag,
            "recent_issues": recents
        }
    )


def library(request):
    assert isinstance(request, HttpRequest)
    magazines = Magazine.objects.all()
    searched = ''
    if request.method == 'GET':
        if request.GET.get("form_type") == 'search':
            query = request.GET['query']
            if len(query) != 0:
                searched = query
                query_in_list = query.split()
                to_ignore = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with']
                filtered_query = [e for e in query_in_list if e not in to_ignore]
                results = []
                for item in filtered_query:
                    mags = Magazine.objects.filter(
                        Q(title__icontains=item)
                    )
                    for mag in mags:
                        if mag not in results:
                            results.append(mag)
                magazines = results
    return render(
        request,
        'library.html',
        {
            "title": "Library",
            "magazines": magazines,
            "searched": searched
        }
    )


class MagazineFavoriteView(RedirectView):
    pattern_name = "magazine_detail"

    def get_redirect_url(self, *args, **kwargs):
        url = self.request.POST.get("next", None)
        if url:
            return url
        else:
            return super().get_redirect_url(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _id = self.kwargs.get("magazine_id", None)
        print(_id)
        if request.user.has_favorited(_id):
            request.user.remove_favorite(_id)
        else:
            request.user.add_favorite(_id)
        return super().post(request, *args, **kwargs)
