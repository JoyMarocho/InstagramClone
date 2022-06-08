from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm,CommentForm,UploadImageForm,ProfileEditForm,UpdateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView  
from .models import Image, Comment, Profile, Follow
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import RedirectView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.edit import CreateView,FormView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.
@login_required(login_url='/login')
def index(request):
    images = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    params = {
        'images': images,
        'form': form,
        'users': users,

    }
    return render(request, 'index.html', params)

class RegisterPage(FormView):
    template_name='registration/registration_form.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('login')


    def form_valid(self, form ) :
        user=form.save()
        # if user is not None:{
        #     login(self.request,user)
        # }
        return super(RegisterPage,self).form_valid(form)

        # an authenticated user should not access the register page

    def get(self,*args,**kwargs):
            if self.request.user.is_authenticated:
                return redirect('index')
            return super(RegisterPage,self).get(*args,**kwargs)  



class CustomLoginView(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    
# ONCE LOGGED IN THE USER WILL BE AUTOMATICALLY BE DIRECTED TO THE HOMEPAGE
    def get_success_url(self):
        # return render (request, 'index')
        return reverse_lazy('image_list')



@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'images': images,
    }
    return render(request, 'index.html', params)

@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'user_profile.html', params)

def logout_user(request):
    logout(request)
    messages.info(request, f'You have successfully logged out.')
    return redirect('index')

@login_required(login_url='login')
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


# class CommentCreateView(LoginRequiredMixin,CreateView):
#     model = Comment
#     fields = ['comment']
#     template_name = 'joyimages/index.html'

@login_required(login_url='login')
def post_comment(request, id):
    image = get_object_or_404(Post, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'single_post.html', params)

def like_post(request):
    # image = get_object_or_404(Post, id=request.POST.get('image_id'))
    image = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = False

    params = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', params, request=request)
        return JsonResponse({'form': html})

@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'results.html', {'message': message})


def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)


def follow(request, to_follow):
    if request.method == 'GET':
        user_profile3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_profile3)
        follow_s.save()
        return redirect('user_profile', user_profile3.user.username)


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


def form_valid(self, form):
    form.instance.username = self.request.user
    return super().form_valid(form)


###### index ########

    # comments = image.comments.filter(active=True)
    # new_comment = None
    # if request.method == 'POST':
    #         # comment_form = CommentForm(data=request.POST)
    # if comment_form.is_valid():

    # #Create Comment object but fail to save to the database yet
    #         new_comment = comment_form.save(commit=False)

    # #Assign current post to comment
    #         new_comment.image = image

#     #Save comment to database
#             new_comment.save()
#     else:
#             comment_form = CommentForm
    # return render(request, 'index.html', {"images":images})

###### end index ########


###### login ########

# @login_required(login_url='login')
# def my_login_required(function):
#     def wrapper(request, *args, **kw):
#         user=request.user  
#         if not (user.id and request.session.get('code_success')):
#             return HttpResponseRedirect('/splash/')
#         else:
#             return function(request, *args, **kw)
#     return wrapper


# def login_user(request):
#     form = AuthenticationForm(request, data=request.POST is None) 
#     if request.method == 'POST' and form.is_valid():
        
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username,password=password)
#             return render(request, 'registration/login.html', {"login_form": form})

#     form = AuthenticationForm()
#     if user is not None:
#         login(request.method != 'POST', user)
#         messages.info(request, f"You are now logged in as {username}.")
#         return redirect('index')
#     else :
#         messages.error(request, f'Invalid Username or password')
#         return render(request, 'registration/login.html', {"login_form": form})

###### end login process ########


###### Registration ########
# def register_new_user(request):
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')
#         else:
#             form = NewUserForm()
#         return render(request, 'registration/registration_form.html', {'form': form})


        # if request.method == "POST" and form.is_valid():
        #     user = form.save()
        # login(request, user)
        # messages.success(request, 'Registration Successful.')
        # return redirect('index')
        # messages.error(request, 'Unsuccessful registration. Invalid information.')
        # form = NewUserForm()
        # return render(request, 'registration/registration_form.html', {"registration_form": form} )

###### End Registration ########
