from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Core page view (/)
def core_page(request):
    return render(request, 'index.html')


urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Core page route
    path('', core_page, name='core'),

    # Token routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API v1 routes
    path('api/v1/accounts/', include('accounts.api.v1.urls', namespace='accounts_v1')),
    path('api/v1/posts/', include('posts.api.v1.urls', namespace='posts_v1')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)