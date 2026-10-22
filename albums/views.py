from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from albums.models import Album
from albums.forms import CreateAlbumForm

def home(request):
    album_id = request.session.get('album_id')
    album = None

    if album_id:
        album = Album.objects.filter(pk=album_id).first()

    return render(request, 'home.html', {'album': album})


# def create_album(request):
#     if request.method == 'POST':
#         form = CreateAlbumForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = CreateAlbumForm()
#
#     return render(request, 'albums/create_album.html', {'form': form})


class CreateAlbumView(CreateView):
    model = Album
    form_class = CreateAlbumForm
    success_url = reverse_lazy('experiences:experiences')
    template_name = 'albums/create_album.html'

    def form_valid(self, form):
        self.object = form.save() #response = super().form_valid(form)
        self.request.session['album_id'] = self.object.pk  #form.instance.pk
        self.request.session.modified = True
        return redirect(self.get_success_url()) #response


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detailes.html'
    context_object_name = 'album'


