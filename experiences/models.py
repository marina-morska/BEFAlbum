from django.core.validators import validate_image_file_extension
from django.db import models

from experiences.validators import FileSizeValidator


class Experience(models.Model):
    class CategoryChoices(models.TextChoices):
        SIGHTS = 'Sights', 'Burgas Treasures'
        EUROVISION = 'Eurovision', 'Eurovision Fever'
        NEARBY = 'Nearby', 'Beyond Burgas'
        CULINARY = 'Culinary', 'Taste Bulgaria'
        PERSONAL = 'Personal', 'My Own Adventure'

    CATEGORY_STARS = {
        'Sights': 2,
        'Eurovision': 5,
        'Nearby': 3,
        'Culinary': 1,
        'Personal': 4,
    }

    PREDEFINED_EXPERIENCES_PER_CATEGORY = 5
    MAX_PERSONAL_EXPERIENCES = 5

    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(
        upload_to='experiences',
        blank=True,
        null=True,
        validators=[
            FileSizeValidator(5),
            validate_image_file_extension
        ]
    )
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    created_by = models.ForeignKey(
        'albums.Album',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='personal_experiences'
    )

    @property
    def stars(self):
        return self.CATEGORY_STARS.get(self.category, 0)

    @property
    def star_display(self):
        return '⭐' * self.stars

    @property
    def is_personal(self):
        return self.category == self.CategoryChoices.PERSONAL

    def __str__(self):
        return self.title

