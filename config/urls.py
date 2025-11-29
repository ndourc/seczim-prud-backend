from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Prudential Regulatory Backend System API",
        default_version='v1',
        description="API documentation for the Prudential Regulatory Backend System (PRBS)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@prbs.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/core/', include('apps.core.urls')),
    path('api/auth/', include('apps.auth_module.urls')),
    path('api/compliance/', include('apps.compliance_module.urls')),
    path('api/returns/', include('apps.returns_module.urls')),
    path('api/risk-assessment/', include('apps.risk_assessment_module.urls')),
    path('api/case-management/', include('apps.case_management_module.urls')),
    path('api/va-vasp/', include('apps.va_vasp_module.urls')),
    path('api/licensing/', include('apps.licensing_module.urls')),
    path('api/v1/', include('apps.smi_module.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)