from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/appliances/", include("appliances.urls")),
    path("api/v1/calculations/", include("calculations.urls")),
    path("api/v1/recommendations/", include("recommendations.urls")),
    path("api/v1/admin/", include("solar_api.admin_urls")),


 # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Redoc
    path(
        "api/redoc/",   
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

]
urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
