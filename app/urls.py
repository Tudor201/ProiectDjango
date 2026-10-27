from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('info', views.info, name="info"),
    path("log", views.log, name="log"),
    
    path('istoric', views.istoric, name="istoric"),
    path('despre', views.despre, name="despre"),
    path('produse', views.in_lucru, name='produse'),
    path('contact', views.in_lucru, name='contact'),
    path('cos_virtual', views.in_lucru, name='cos_virtual'),
    
    path('exemplu_template', views.exemplu_template, name="exemplu_template"),
    path('exemplu_template2', views.exemplu_template2, name="exemplu_template2"),
    
    re_path(r'^accesare(?P<id>\d+)$', views.detalii_accesare, name="detalii_accesare"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )