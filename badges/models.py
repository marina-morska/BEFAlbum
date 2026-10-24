from django.db import models

class Badge(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='badges')
    stars_required = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.stars_required}⭐ required)"


class AlbumBadge(models.Model):
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'badge'],
                name='unique_album_badge',
            ),
        ]

    def __str__(self):
        return f"{self.album.nickname} earned {self.badge.name}"
