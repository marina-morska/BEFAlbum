
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from albums.models import Album, Memory, CollectedExperience
from albums.forms import CreateAlbumForm, MemoryForm, EditAlbumForm
from experiences.models import Experience


def home(request):
    album_id = request.session.get('album_id')
    album = None

    if album_id:
        album = Album.objects.filter(pk=album_id).first()

    all_albums = Album.objects.all() ##just for testing - demo helpers

    return render(request, 'home.html', {
        'album': album,
        'all_albums': all_albums
    })

#just for testing - demo helpers
def logout_album(request):
    request.session.pop('album_id', None)
    return redirect('home')


def select_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    request.session['album_id'] = album.pk
    return redirect('home')

#just for testing - demo helpers ^

class CreateAlbumView(CreateView):
    model = Album
    form_class = CreateAlbumForm
    success_url = reverse_lazy('experiences:experiences')
    template_name = 'albums/create_album.html'

    def form_valid(self, form):
        self.object = form.save()
        self.request.session['album_id'] = self.object.pk
        self.request.session.modified = True
        return redirect(self.get_success_url())


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_details.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_groups = []

        for category_value, category_label in Experience.CategoryChoices.choices:
            collected_experiences = (
                self.object.experiences
                .filter(category=category_value)
                .order_by('title')
            )
            category_groups.append({
                'label': category_label,
                'experiences': collected_experiences,
            })

        context['category_groups'] = category_groups
        context['earned_badges'] = self.object.earned_badges.select_related('badge').all()

        return context


class AlbumEditView(UpdateView):
    model = Album
    form_class = EditAlbumForm
    template_name = 'albums/album_edit.html'
    context_object_name = 'album'

    def dispatch(self, request, *args, **kwargs):
        album_id = request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        self.album = get_object_or_404(Album, pk=album_id)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.album

    def get_success_url(self):
        return reverse_lazy('album_details', kwargs={'pk': self.album.pk})


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'albums/album_delete.html'

    def dispatch(self, request, *args, **kwargs):
        album_id = request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        self.album = get_object_or_404(Album, pk=album_id)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.album

    def get_success_url(self):
        self.request.session.pop('album_id', None)

        return reverse_lazy('create_album')


class CreateMemoryView(CreateView):
    model = Memory
    form_class = MemoryForm
    success_url = reverse_lazy('experiences:experiences')
    template_name = 'memories/create_memory.html'

    def dispatch(self, request, *args, **kwargs):
        album_id = request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        self.experience = get_object_or_404(Experience, pk=kwargs['experience_pk'])
        self.album = get_object_or_404(Album, pk=album_id)

        collected = CollectedExperience.objects.filter(
            album=self.album,
            experience=self.experience
        ).exists()

        if not collected:
            return redirect('experiences:experiences')

        existing_memory = Memory.objects.filter(
            album=self.album,
            experience=self.experience
        ).first()

        if existing_memory:
            return redirect('memory_edit', pk=existing_memory.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        form.instance.experience = self.experience
        return super().form_valid(form)


class MemoryDetailsView(DetailView):
    model = Memory
    template_name = 'memories/memory_details.html'
    context_object_name = 'memory'

class MemoryEditView(UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'memories/memory_edit.html'
    context_object_name = 'memory'

    def get_success_url(self):
        return reverse_lazy('memory_details', kwargs={'pk': self.object.pk})


class MemoryDeleteView(DeleteView):
    model = Memory
    template_name = 'memories/memory_delete.html'
    context_object_name = 'memory'

    def get_success_url(self):
        return reverse_lazy('album_details', kwargs={'pk': self.object.album.pk})