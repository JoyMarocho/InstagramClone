from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import NewUserForm,CommentForm,UploadImageForm,ProfileEditForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Image
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required(login_url='/login')
def index(request):
    images = Image.objects.all()
    comments = image.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():

    #Create Comment object but fail to save to the database yet
            new_comment = comment_form.save(commit=False)

    #Assign current post to comment
            new_comment.image = image

    #Save comment to database
            new_comment.save()
    else:
            comment_form = CommentForm
    return render(request, 'index.html', {"images":images})

def register_new_user(request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
        login(request, user)
        messages.success(request, 'Registration Successful.')
        return redirect('index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
        form = NewUserForm()
        return render(request, 'registration/registration_form.html', {"registration_form": form} )


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

    form = AuthenticationForm()
    if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect('index')
    else :
        messages.error(request, f'Invalid Username or password')
        return render(request, 'registration/login.html', {"login_form": form})

def logout_user(request):
    logout(request)
    messages.info(request, f'You have successfully logged out.')
    return redirect('index')

@login_required(login_url='/login')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.username = current_user
        image.save()
        return redirect('index')
    else:
        form = UploadImageForm
        return render(request, 'new_image.html', {"image_form": form})


class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'joyimages/index.html'


def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ImageCreateView(LoginRequiredMixin,CreateView):
    form_class = UploadImageForm
    template_name = 'new_image.html'

def form_valid(self, form):
    form.instance.username = self.request.user
    return super().form_valid(form)


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image_detail.html'


class ImageListView(ListView):
    model = Image
    template_name = 'image_list.html'

class CommentCreateView(LoginRequiredMixin,CreateView):
    form_class = CommentForm
    template_name = 'new_comment.html'

def form_valid(self, form):
    form.instance.username = self.request.user
    return super().form_valid(form)


