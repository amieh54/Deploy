from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index),
url(r'^regprocess$', views.regprocess),
url(r'^logprocess$', views.logprocess),
url(r'^logout$', views.logout),
url(r'^dashboard$', views.dashboard),
url(r'^add_item$', views.add_item),
url(r'^items$', views.items),
url(r'^addwish/(?P<id>\d+)$', views.addwish, name='addwish'),
url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
url(r'^viewitem(?P<id>\d+)$', views.viewitem, name='viewitem')
]
