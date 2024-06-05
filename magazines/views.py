from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import HttpRequest
from django.shortcuts import render, reverse, redirect
from django.views.generic import RedirectView
from .models import Magazine
from magazines import forms
from datetime import datetime
from django.db.models import Q


def home(request):
    assert isinstance(request, HttpRequest)
    magazines = Magazine.objects.order_by('-upload_time')[:3]

    if request.method == 'POST':
        if request.POST.get("form_type") == 'addMagazine':
            form = forms.MagazineForm(request.POST, request.FILES)
            if form.is_valid():
                print("success")
                form.save()
            else:
                print(form)
                print(request.POST)
                print(request.FILES)
    return render(request, 'index.html', {"title": "Home", "recent_issues": magazines, })


def magazine(request, magazine_id):
    assert isinstance(request, HttpRequest)
    mag = Magazine.objects.filter(id=magazine_id)[0]
    recents = Magazine.objects.filter(~Q(id=magazine_id)).order_by('-upload_time')[:5]
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
    return render(
        request,
        'library.html',
        {
            "title": "Library",
            "magazines": magazines,
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
