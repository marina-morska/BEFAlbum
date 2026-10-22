from django.db import models
from experiences.models import Experience


class Album(models.Model):
    nickname = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    collected_stars = models.PositiveIntegerField(default=0)
    experiences = models.ManyToManyField(
        Experience,
        through='CollectedExperience',
        blank=True,
        related_name='collected_in_album',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nickname', 'country'],
                name='unique_nickname_country',
            )
        ]

    def __str__(self):
        return f"{self.nickname} ({self.country}) - {self.collected_stars}⭐"


class CollectedExperience(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='collected')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'experience'],
                name='unique_album_experience',
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_stars()

    def delete(self, *args, **kwargs):
        album = self.album
        super().delete(*args, **kwargs)
        self._update_stars(album=album)

    def _update_stars(self, album=None):
        album = album or self.album
        album.collected_stars = sum(
            collection.experience.stars
            for collection in album.collected.select_related('experience')
        )
        album.save(update_fields=['collected_stars'])

    def __str__(self):
        return f"{self.album.nickname} collected {self.experience.title}"


class Memory(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='memories')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='memories')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'experience'],
                name='unique_album_experience_memory',
            ),
        ]
        verbose_name_plural = "Memories"
        ordering = ['-created_at']

    def __str__(self):
        return f"Memory of {self.experience.title}"