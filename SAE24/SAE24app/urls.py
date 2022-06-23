from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("display_all/",views.display_all_data),
    path('display_all/update/<int:id>/', views.update),
    path('updatetraitement/<int:id>/', views.updatetraitement),
    path('filter_by/', views.filter),
    path('export/', views.export),
    path('graph/', views.graph),
    path('image/', views.image),
]
