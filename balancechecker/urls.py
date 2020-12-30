from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^$', views.homepage, name="home"),
    # re_path(r'^bank-auth/', views.bank_auth, name="bankauth"),
    re_path(r'^balance/', views.balance, name="balance"),
]

urlpatterns += staticfiles_urlpatterns()
