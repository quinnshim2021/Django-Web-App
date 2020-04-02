from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Friend
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

@login_required
def not_found(request):
    messages.add_message(request, messages.ERROR, 'Not working')
    raise Http404()

@login_required
def not_found(request):
    messages.add_message(request, messages.ERROR, 'Not working')
    raise Http500()

# old
# @login_required
# def home(request):
#     friend = Friend.objects.get(current_user=request.user)
#     context = { # data that gets passed into template, posts is key to access data in template
#         'posts': Post.objects.all(),
#         'friends': friend.users.all()
#     }
#     return render(request, 'blog/home.html', context)

# loginrequiredmixin makes it required to be logged in
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    # can add pagination later, must add to context data below 

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        return context

class UserListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/view_users.html'
    context_object_name = 'all_data'
    ordering = ['username']

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-username')
        context['friends'] = Friend.objects.get(current_user=self.request.user).users.all()
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'all_data'
    paginate_by = 7

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        print(list(Friend.objects.get(current_user=self.request.user).users.all()))
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_body_name = 'all_data'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        print(list(Friend.objects.get(current_user=self.request.user).users.all()))
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    context_body_name = 'all_data'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        print(list(Friend.objects.get(current_user=self.request.user).users.all()))
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'
    context_object_name = 'all_data'

    # author of post is current author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        print(list(Friend.objects.get(current_user=self.request.user).users.all()))
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    content_body_name = 'all_data'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # author of post is current author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['friends'] = list(Friend.objects.get(current_user=self.request.user).users.all())
        print(list(Friend.objects.get(current_user=self.request.user).users.all()))
        return context

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def change_friend(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == "add":
        Friend.make_friend(request.user, new_friend)
    elif operation == "remove":
        Friend.lose_friend(request.user, new_friend)
    else:
        raise Http403()
    return redirect('blog-home')

# def handler404(request, exception, template_name="404.html"):
#     response = render(template_name)
#     response.status_code = 404
#     return response