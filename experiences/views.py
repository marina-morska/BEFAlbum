from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from albums.models import Album, CollectedExperience
from experiences.forms import PersonalExperienceForm
from experiences.models import Experience


def experiences(request):
    album_id = request.session.get('album_id')
    experiences = Experience.objects.exclude(
        category = Experience.CategoryChoices.PERSONAL
    )
    if album_id:
        personal_experiences = Experience.objects.filter(
            category = Experience.CategoryChoices.PERSONAL,
            created_by_id = album_id
        )

        experiences = experiences | personal_experiences

        collected_ids = CollectedExperience.objects.filter(
            album_id = album_id
        ).values_list('experience_id', flat=True)
    else:
        collected_ids = []

    return render(request, 'experiences.html',
                  {'experiences': experiences, 'collected_ids': collected_ids},)


class CreatePersonalExperienceView(CreateView):
    model = Experience
    form_class = PersonalExperienceForm
    template_name = 'experiences/create_personal_experience.html'
    success_url = reverse_lazy('experiences:experiences')

    def form_valid(self, form):
        album_id = self.request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        album = Album.objects.filter(pk=album_id).first()

        if not album:
            return redirect('create_album')

        form.instance.category = Experience.CategoryChoices.PERSONAL
        form.instance.created_by = album

        return super().form_valid(form)

class CollectExperienceView(View):
    def post(self, request, pk):
        album_id = request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        album = get_object_or_404(Album, pk=album_id)
        experience = get_object_or_404(Experience, pk=pk)

        if experience.is_personal:
            if experience.created_by_id != album.pk:
                return redirect('experiences:experiences')

            return redirect('experiences:experiences')

        CollectedExperience.objects.get_or_create(
            album = album,
            experience = experience,
        )

        return redirect('experiences:experiences')