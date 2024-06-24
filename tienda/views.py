from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, UpdateView, DeleteView
from .forms import PostCreateForm
from .models import Post
from django.urls import reverse_lazy

# Create your views here.


class TiendaView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            "posts": posts,
        }
        return render(request, "tienda_list.html", context)


class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostCreateForm()
        context = {"form": form}
        return render(request, "blog_create.html", context)

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST, request.FILES)  # Incluye request.FILES
        if form.is_valid():
            form.save()
            return redirect("tienda:home")
        context = {"form": form}
        return render(request, "blog_create.html", context)


class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {"post": post}
        return render(request, "blog_detail.html", context)


class BlogUpdateView(UpdateView):
    model = Post
    fields = ["title", "content", "marca", "sub_title", "img", "price", "amount"]
    template_name = "blog_update.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("tienda:detail", kwargs={"pk": pk})


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "blog_delete.html"
    success_url = reverse_lazy("tienda:home")
