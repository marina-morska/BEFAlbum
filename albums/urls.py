from django.urls import path
from albums import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_album/', views.CreateAlbumView.as_view(), name='create_album'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album_details'),
]