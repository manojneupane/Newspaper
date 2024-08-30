from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render

from newspaper.forms import CommentForm, ContactForm, NewsletterForm
from newspaper.models import Category, Post, Tag, UserProfile
from django.contrib import messages


from django.views.generic import ListView, DetailView, View, TemplateView
from datetime import timedelta

from django.utils import timezone


class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False, status="active")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-view_count")
            .first()
        )
        context["featured_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at", "-view_count")[1:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-view_count")[:7]

        context["recent_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:7]

        # context["categories"] = Category.objects.all()[:5]
        # context["tags"] = Tag.objects.all()[:10]

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.view_count += 1
        obj.save()

        context["previous_post"] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__lt=obj.id
            )
            .order_by("-id")
            .first()
        )

        context["next_post"] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__gt=obj.id
            )
            .order_by("id")
            .first()
        )

        return context


class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)

        post = Post.objects.get(pk=post_id)
        return render(
            request,
            "aznews/detail/detail.html",
            {"post": post, "form": form},
        )


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Successfully submitted your queries. We will contact you soon.",
            )
            return redirect("contact")
        else:
            messages.error(
                request,
                "Cannot submit your query. Please make sure all the fields are properly filled.",
            )
            return render(
                request,
                self.template_name,
                {"form": form},
            )

class PostByCategoryView(ListView):
    model=Post
    template_name="aznews/list/list.html"
    context_object_name="posts"
    paginate_by =1

    def get_queryset(self):
        query=super().get_queryset()
        query=query.filter(
            published_at__isnull=False,
            status="active",
            category_id=self.kwargs["category_id"],
        ).order_by("published_at")
        return query
    
class PostByTagView(ListView):
    model=Post
    template_name="aznews/list/list.html"
    context_object_name="posts"
    paginate_by =1

    def get_queryset(self):
        query=super().get_queryset()
        query=query.filter(
            published_at__isnull=False,
            status="active",
            category_id=self.kwargs["tag_id"],
        ).order_by("published_at")
        return query
    
class NewsletterView(View):
    def post(self, request):
        is_ajax = request.header.get("x-requested-with")
        if is_ajax=="XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message":"Successfully subscribed to the newsletter.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {"success": False,
                     "message": "Cannot subscribe to the newsletter."
                     },
                     status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpReqquest",
                },
                status=400,
            )
    
    