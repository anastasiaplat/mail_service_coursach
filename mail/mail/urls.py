from django.contrib import admin
from django.urls import include, path
from catalog import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import *

urlpatterns = [
    path('', user_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('input/', user_views.input, name='input'),
    path('output/', user_views.output, name='output'),
    path('main/', user_views.main, name='main'),
    path('letters/', user_views.LetterCreateView.as_view(template_name='letter_form.html'), name='create'),
    path('letter_detail/(?P<pk>\d+)$', user_views.LetterDetailView.as_view(template_name='letter_detail.html'), name='letter_detail'),
    path('export/', user_views.export_users, name='export_users'),
    path('export2/', user_views.export_letters, name='export_letters'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
