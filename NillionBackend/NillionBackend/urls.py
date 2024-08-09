from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from base.Router.profile import *
from base.Router.chat import *
from base.Router.Reject import *
from base.Router.Favorites import *
from django.shortcuts import redirect

def redirect_to_swagger(request):
    return redirect('/schema/swagger-ui/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_swagger),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

profiles = [
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/all/', get_all_profiles, name='get_all_profiles'),
    path('profile/address/<str:address>/', get_profile_by_address, name='get_profile_by_address'),
    path('profile/match/<str:address>/', get_matching_profiles, name='get_matching_profiles'),
    path('profile/favorites/details/<str:address>/', get_favorites_details, name='get_favorites_details'),
]

chat = [
    path('chat/<str:address>/<str:endpoint>/', chat_room, name='chat_room'),
]

RejectedProfile = [
    path('rejectd/', create_rejectd, name='create_rejectd'),
    path('rejectd/all/', get_all_rejectd, name='get_all_rejectd'),
    path('rejectd/<str:from_address>/', get_rejectd, name='get_rejectd'),
    path('rejectd/<str:from_address>/update/', update_rejectd, name='update_rejectd'),
    path('rejectd/<str:from_address>/delete/', delete_rejectd, name='delete_rejectd'),
]

FavoriteProfile = [
    path('favorites/', create_favorite, name='create_favorite'),
    path('favorites/all/', get_all_favorites, name='get_all_favorites'),
    path('favorites/<str:to_address>/', get_favorite, name='get_favorite'),
    path('favorites/<str:to_address>/update/', update_favorite, name='update_favorite'),
    path('favorites/<str:to_address>/delete/', delete_favorite, name='delete_favorite'),
]

urlpatterns += profiles
urlpatterns += chat
urlpatterns += RejectedProfile
urlpatterns += FavoriteProfile