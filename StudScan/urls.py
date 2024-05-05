from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from User.views import LoginView, LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    # spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # optional ui:
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # djoser
    path("auth/", include("djoser.urls")),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
