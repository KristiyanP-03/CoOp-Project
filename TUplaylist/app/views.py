from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate, get_user_model

from .forms import *
from .models import *



# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------

# #Main view
#=======================================================================================================================
def home(request):
    songs = SongModel.objects.all()


    genre = request.GET.get('genre', None)
    if genre:
        songs = songs.filter(genre=genre)


    year = request.GET.get('year', None)
    if year:
        songs = songs.filter(release_year=year)


    artist_type = request.GET.get('artist_type', None)
    if artist_type:
        songs = songs.filter(artist_type=artist_type)


    uploader = request.GET.get('uploader', None)
    if uploader:
        songs = songs.filter(uploader__username=uploader)


    genres = SongModel.GENRE_CHOICES
    artist_types = SongModel.ARTIST_TYPE_CHOICES

    return render(request, 'home-page.html', {
        'songs': songs,
        'genres': genres,
        'artist_types': artist_types,
    })

#Profile Register / Log In / Log Out Views
#=======================================================================================================================

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'profile-register.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)

        return response



class LoginView(LoginView):
    template_name = 'profile-log-in.html'
    redirect_authenticated_user = True




class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')




class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile-details.html'
    context_object_name = 'profile'
    model = ProfileModel

    def get_object(self, queryset=None):
        return self.request.user





class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'profile-edit.html'
    success_url = reverse_lazy('profile details')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile details')





class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = ProfileModel
    template_name = 'profile-delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home')



@login_required
def user_songs(request):
    user = request.user
    songs = SongModel.objects.filter(uploader=user)
    return render(request, 'user-songs.html', {'songs': songs})


def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('user songs')
    else:
        form = SongForm()

    return render(request, 'song-create.html', {'form': form})


def song_details(request, pk):
    song = get_object_or_404(SongModel, pk=pk)

    if request.method == 'POST':
            return redirect('song details', pk=pk)

    context = {
        'song': song,
    }
    return render(request, 'song-details.html', context)


@login_required
def song_edit(request, pk):
    song = get_object_or_404(SongModel, pk=pk)

    if song.uploader != request.user:
        return redirect("home")

    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('user songs')
    else:
        form = SongForm(instance=song)

    context = {'form': form, 'is_edit': True}
    return render(request, 'song-edit.html', context)


def song_delete(request, pk):
    song = SongModel.objects.get(pk=pk)

    if request.method == 'POST':
        song.delete()
        return redirect('user songs')

    context = {'song': song}
    return render(request, 'song-delete.html', context)
