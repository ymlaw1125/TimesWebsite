from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import RedirectView

from forum import forms
from user.models import CustomUser
from .models import Posts, Vote, Comments
from django.db.models import F, ExpressionWrapper, FloatField, Count

from django.contrib.auth.decorators import login_required


# Create your views here.
def forum(request):
    assert isinstance(request, HttpRequest)
    posts = Posts.objects.all()
    '''
    votes = []
    for post in posts:
        votes.append(Vote.objects.filter(user=request.user, post=post).first())
    votes = Vote.objects.filter(user=request.user, post_id=1).first()
    '''
    return render(
        request,
        'forum_main.html',
        {
            "title": "Home",
            "posts": posts,
            # "votes": votes
        }
    )


def popular(request):
    assert isinstance(request, HttpRequest)
    posts = Posts.objects.annotate(
        comment_count=Count('comments'),
        age_in_days=ExpressionWrapper(
            (datetime.now() - F('upload_date')) / timedelta(days=1),  # Age of post in days
            output_field=FloatField()
        ),
        popularity_score=ExpressionWrapper(
            (F('upvotes') - F('downvotes')) * 0.5 + F('comment_count') * 0.2 + F('views') * 0.3 - F('age_in_days') * 0.1,  # Adjust weights here
            output_field=FloatField()
        )
    ).order_by('-popularity_score')
    '''
    posts = Posts.objects.annotate(
        popularity_score=ExpressionWrapper(
            (F('upvotes') - F('downvotes')) * 0.5 + F('views') * 0.2,  # Adjust the weights
            output_field=FloatField()
        )
    ).order_by('-popularity_score')
    '''
    print(posts)
    return render(
        request,
        'forum_popular.html',
        {
            "title": "Popular",
            "posts": posts
        }
    )


def submit(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'addPosts':
            form = forms.PostsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                print("post add success")
            else:
                print(form)
                print(request.POST)
                print(request.FILES)
            return redirect("forum")
    return render(
        request,
        'forum_newpost.html',
        {
            "title": "Create a Post",
            "communities": {
                'News',
                "Lifestyle",
                "Literature",
                "Science & Technology",
                "Games",
            },
        }
    )


def community(request, community_name):
    assert isinstance(request, HttpRequest)
    posts = Posts.objects.filter(community=community_name)
    return render(
        request,
        'forum_community.html',
        {
            "title": community_name,
            "posts": posts,
        }
    )


def post(request, community_name, post_id):
    assert isinstance(request, HttpRequest)
    post = Posts.objects.filter(id=post_id)[0]
    post.views += 1
    post.save()
    if request.user.is_authenticated:
        vote = Vote.objects.filter(post_id=post_id, user=request.user).first()
        if request.method == 'POST':
            if request.POST.get("form_type") == "commentForm":
                form = forms.CommentsForm(request.POST)
                if form.is_valid():
                    form.save()
                    print("comment add success")
                else:
                    print(form)
                    print(request.POST)
                    print(request.FILES)
            elif request.POST.get("form_type") == "replyForm":
                form = forms.CommentsForm(request.POST)
                if form.is_valid():
                    form.save()
                    print("reply add success")
                else:
                    print(form)
                    print(request.POST)

        return render(
            request,
            'forum_post.html',
            {
                "title": post.title,
                "post": post,
                "vote": vote
            }
        )
    else:
        return render(
            request,
            'forum_post.html',
            {
                "title": post.title,
                "post": post,
            }
        )


class PostLikeView(RedirectView):
    pattern_name = "post_detail"

    def get_redirect_url(self, *args, **kwargs):
        url = self.request.POST.get("next", None)
        if url:
            return url
        else:
            return super().get_redirect_url(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _id = self.kwargs.get("post_id", None)
        print(_id)
        if request.user.has_post_liked(_id):
            request.user.remove_post_like(_id)
        else:
            request.user.add_post_like(_id)
        return super().post(request, *args, **kwargs)


def vote_post(request, post_id, vote_type):
    post = Posts.objects.filter(id=post_id)[0]
    if request.method == "POST":
        form = forms.VoteForm(request.POST)
        user_vote = None
        if form.is_valid():
            if request.user.is_authenticated:
                user_vote = Vote.objects.filter(user=request.user, post_id=post_id).first()
                print(user_vote)
                if user_vote:
                    if vote_type == 1:
                        if user_vote.vote_type == 1:
                            post.upvotes -= 1
                            user_vote.delete()
                            change = False
                        else:
                            post.downvotes -= 1
                            post.upvotes += 1
                            user_vote.vote_type = 1
                            user_vote.save()
                            change = True
                    elif vote_type == 0:
                        if user_vote.vote_type == 0:
                            post.downvotes -= 1
                            user_vote.delete()
                            change = False
                        else:
                            post.upvotes -= 1
                            post.downvotes += 1
                            user_vote.vote_type = 0
                            user_vote.save()
                            change = True
                    post.save()

                    return JsonResponse({"upvotes": post.upvotes, "downvotes": post.downvotes, "changed": change})
            form.save()
            if vote_type == 1:
                post.upvotes += 1
            elif vote_type == 0:
                post.downvotes += 1
            post.save()
            print("vote success")
        else:
            print(form)
            print(request.POST)

    return JsonResponse({"upvotes": post.upvotes, "downvotes": post.downvotes, "changed": True})

def vote_comment(request, comment_id, vote_type):
    comment = Comments.objects.filter(id=comment_id)[0]
    if request.method == "POST":
        form = forms.VoteForm(request.POST)
        user_vote = None
        if form.is_valid():
            if request.user.is_authenticated:
                user_vote = Vote.objects.filter(user=request.user, comment_id=comment_id).first()
                print(user_vote)
                if user_vote:
                    if vote_type == 1:
                        if user_vote.vote_type == 1:
                            comment.upvotes -= 1
                            user_vote.delete()
                            change = False
                        else:
                            comment.downvotes -= 1
                            comment.upvotes += 1
                            user_vote.vote_type = 1
                            user_vote.save()
                            change = True
                    elif vote_type == 0:
                        if user_vote.vote_type == 0:
                            comment.downvotes -= 1
                            user_vote.delete()
                            change = False
                        else:
                            comment.upvotes -= 1
                            comment.downvotes += 1
                            user_vote.vote_type = 0
                            user_vote.save()
                            change = True
                    comment.save()

                    return JsonResponse({"upvotes": comment.upvotes, "downvotes": comment.downvotes, "changed": change})
            form.save()
            if vote_type == 1:
                comment.upvotes += 1
            elif vote_type == 0:
                comment.downvotes += 1
            comment.save()
            print("vote success")
        else:
            print(form)
            print(request.POST)

    return JsonResponse({"upvotes": comment.upvotes, "downvotes": comment.downvotes, "changed": True})



