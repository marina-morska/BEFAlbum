from django.urls import path
from experiences import views

app_name = 'experiences'
urlpatterns = [
    path('', views.experiences, name='experiences'),
    path('create-personal/',
         views.CreatePersonalExperienceView.as_view(),
         name='create_personal_experience'),
    path('<int:pk>/collect_experience/',
         views.CollectExperienceView.as_view(),
         name='collect_experience'),
]