from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from albums.models import Album, CollectedExperience
from experiences.forms import PersonalExperienceForm
from experiences.models import Experience

from badges.services import award_badges


def experiences(request):
    album_id = request.session.get('album_id')
    album = None
    experiences = Experience.objects.exclude(
        category=Experience.CategoryChoices.PERSONAL
    )

    if album_id:
        album = Album.objects.filter(pk=album_id).first()
        personal_experiences = Experience.objects.filter(
            category=Experience.CategoryChoices.PERSONAL,
            created_by_id=album_id
        )

        experiences = (experiences | personal_experiences)

        collected_ids = CollectedExperience.objects.filter(
            album_id=album_id
        ).values_list('experience_id', flat=True)
    else:
        collected_ids = []

    memories = {}
    if album:
        for memory in album.memories.all():
            memories[memory.experience_id] = memory

    category_order = [
        'Sights',
        'Eurovision',
        'Nearby',
        'Culinary',
        'Personal',
    ]

    experiences = sorted(
        experiences,
        key=lambda exp: (category_order.index(exp.category), exp.title)
    )

    return render(request, 'experiences.html',{
        'experiences': experiences,
        'collected_ids': collected_ids,
        'album': album,
        'memories': memories
    },)


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

        personal_experiences_count = Experience.objects.filter(
            created_by=album,
            category=Experience.CategoryChoices.PERSONAL,
        ).count()

        if personal_experiences_count >= Experience.MAX_PERSONAL_EXPERIENCES:
            form.add_error(
                None,
                f"You can create a maximum of {Experience.MAX_PERSONAL_EXPERIENCES} personal experiences."
            )
            return self.form_invalid(form)

        form.instance.category = Experience.CategoryChoices.PERSONAL
        form.instance.created_by = album

        response = super().form_valid(form)

        CollectedExperience.objects.create(
            album=album,
            experience=self.object,
        )

        award_badges(album)

        return response

class CollectExperienceView(View):
    def post(self, request, pk):
        album_id = request.session.get('album_id')

        if not album_id:
            return redirect('create_album')

        album = get_object_or_404(Album, pk=album_id)
        experience = get_object_or_404(Experience, pk=pk)

        if experience.is_personal:
            return redirect('experiences:experiences')

        CollectedExperience.objects.get_or_create(
            album=album,
            experience=experience,
        )

        award_badges(album)

        return redirect('experiences:experiences')