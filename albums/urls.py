from django.urls import path
from albums import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_album/', views.CreateAlbumView.as_view(), name='create_album'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album_details'),
    path('edit/', views.AlbumEditView.as_view(), name='album_edit'),
    path('delete/', views.AlbumDeleteView.as_view(), name='album_delete'),
    path('experience/<int:experience_pk>/memory/create/',
         views.CreateMemoryView.as_view(), name='create_memory'),
    path('memory/<int:pk>/', views.MemoryDetailsView.as_view(), name='memory_details'),
    path('memory/edit/<int:pk>/', views.MemoryEditView.as_view(), name='memory_edit'),
    path('memory/delete/<int:pk>/', views.MemoryDeleteView.as_view(), name='memory_delete'),
    # just for testing
    path('logout/', views.logout_album, name='logout_album'),
    path('select/<int:pk>/', views.select_album, name='select_album'),
]