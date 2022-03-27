from django.conf.urls import url

from . import views

urlpatterns = [
    url('empresa', views.EmpresaView.as_view(), name='empresa'),
    url('', views.HomeView.as_view(), name='home'),
]