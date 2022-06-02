from django.urls import path, include

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('user/', include('user.urls')),
]
