from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
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