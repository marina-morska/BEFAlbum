from badges.models import Badge, AlbumBadge
from experiences.models import Experience


def create_badges():
    badges = [
        {
            'name': 'Burgas Treasures',
            'description': 'Collected all 5 Sights experiences.',
        },
        {
            'name': 'Eurovision Fever',
            'description': 'Collected all 5 Eurovision experiences.',
        },
        {
            'name': 'Beyond Burgas',
            'description': 'Collected all 5 Nearby experiences.',
        },
        {
            'name': 'Taste Bulgaria',
            'description': 'Collected all 5 Culinary experiences.',
        },
        {
            'name': 'Eurovision Explorer',
            'description': 'Collected all 20 predefined experiences.',
        },
        {
            'name': 'Ultimate Explorer',
            'description': 'Collected all 20 predefined experiences and all 5 personal experiences.',
        },
        {
            'name': 'Star Collector I',
            'description': 'Earned at least 15 stars.',
            'stars_required': 15,
        },
        {
            'name': 'Star Collector II',
            'description': 'Earned at least 30 stars.',
            'stars_required': 30,
        },
        {
            'name': 'Star Collector III',
            'description': 'Earned at least 50 stars.',
            'stars_required': 50,
        },
    ]

    for badge_data in badges:
        Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults={
                'description': badge_data['description'],
                'stars_required': badge_data.get('stars_required', 0),
                'image': 'badges/default.png',
            },
        )

def award_badge(album, badge_name):
    badge = Badge.objects.get(name=badge_name)

    AlbumBadge.objects.get_or_create(
        album=album,
        badge=badge,
    )

def award_badges(album):
    category_badges = {
        Experience.CategoryChoices.SIGHTS: 'Burgas Treasures',
        Experience.CategoryChoices.EUROVISION: 'Eurovision Fever',
        Experience.CategoryChoices.NEARBY: 'Beyond Burgas',
        Experience.CategoryChoices.CULINARY: 'Taste Bulgaria',
    }

    for category, badge_name in category_badges.items():
        collected_count = album.collected.filter(
            experience__category=category,
        ).count()

        if collected_count >= Experience.PREDEFINED_EXPERIENCES_PER_CATEGORY:
            award_badge(album, badge_name)

    predefined_count = album.collected.exclude(
            experience__category=Experience.CategoryChoices.PERSONAL
        ).count()

    personal_count = album.collected.filter(
            experience__category=Experience.CategoryChoices.PERSONAL
        ).count()

    if predefined_count >= 20:
            award_badge(album, 'Eurovision Explorer')

    if predefined_count >= 20 and personal_count >= 5:
            award_badge(album, 'Ultimate Explorer')

    star_badges = Badge.objects.filter(stars_required__gt=0)

    for badge in star_badges:
        if album.collected_stars >= badge.stars_required:
            award_badge(album, badge.name)