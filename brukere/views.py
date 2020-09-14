from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import UserRegisterForm, UserUpdateForm, ProfilUpdateForm
from .models import Profil
from blogg.models import Post


@login_required
def show_user(request, username=None):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage: 
        posts = paginator.page(paginator.num_pages)

    context = {'user': user, 'posts': posts, 'page': page}

    return render(request, 'brukere/show_user.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto opprettet for {username}!')
            return redirect('blogg-home')
    else:
        form = UserRegisterForm()
    return render(request, 'brukere/register.html', {'form': form})

@login_required
def profil(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilUpdateForm(request.POST, request.FILES, instance=request.user.profil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Endringer lagret")
            return redirect('profil')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilUpdateForm(instance=request.user.profil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'brukere/profil.html', context)

#First arguments of render is the request, than the template to return,
#lastly a dictionary with values for the template.
