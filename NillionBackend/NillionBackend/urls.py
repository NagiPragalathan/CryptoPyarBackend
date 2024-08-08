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
    return redirect('/api/schema/swagger-ui/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_swagger),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

profiles = [
    path('create/', create_profile, name='create_profile'),
    path('all/', get_all_profiles, name='get_all_profiles'),
    path('address/<str:address>/', get_profile_by_address, name='get_profile_by_address'),
    path('match/<str:address>/', get_matching_profiles, name='get_matching_profiles'),
]

chat = [
    path('create_chat/', create_chat, name='create_chat'),
    path('send_message/', send_message, name='send_message'),
]

RejectedProfile = [
    path('api/rejectd/', create_rejectd, name='create_rejectd'),
    path('api/rejectd/all/', get_all_rejectd, name='get_all_rejectd'),
    path('api/rejectd/<str:from_address>/', get_rejectd, name='get_rejectd'),
    path('api/rejectd/<str:from_address>/update/', update_rejectd, name='update_rejectd'),
    path('api/rejectd/<str:from_address>/delete/', delete_rejectd, name='delete_rejectd'),
]

FavoriteProfile = [
    path('api/favorites/', create_favorite, name='create_favorite'),
    path('api/favorites/all/', get_all_favorites, name='get_all_favorites'),
    path('api/favorites/<str:to_address>/', get_favorite, name='get_favorite'),
    path('api/favorites/<str:to_address>/update/', update_favorite, name='update_favorite'),
    path('api/favorites/<str:to_address>/delete/', delete_favorite, name='delete_favorite'),
]

urlpatterns += profiles
urlpatterns += chat
urlpatterns += RejectedProfile
urlpatterns += FavoriteProfile
