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
    # comments = image.comments.filter(active=True)
    # new_comment = None
    # if request.method == 'POST':
    #   comment_form = CommentForm(data=request.POST)
    #   if comment_form.is_valid():

    #     #Create Comment object but fail to save to the database yet
    #     new_comment = comment_form.save(commit=False)

    #     #Assign current post to comment
    #     new_comment.image = image

    #     #Save comment to database
    #     new_comment.save()
    #   else:
    #     comment_form = CommentForm
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
