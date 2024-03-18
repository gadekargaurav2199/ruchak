from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('makebill/<int:table_id>/', views.make_bill, name='make_bill'),
    path('generate/<int:table_id>/', views.generate, name='generate'),


    path('save_bill/', views.save_bill),
    path('delete_bill_item/<int:pk>/<int:table_id>/', views.delete_bill_item, name='delete_bill_item'),
    path('cust_details/', views.cust_details, name='cust_details'),
    path('delete_bill/', views.delete_bill, name='delete_bill'),

    path('item/', views.item_details),
    path('item-update/<int:item_id>/',views.update_item),
    path('item-delete/<int:item_id>/',views.delete_item),


    path('collections/', views.collections),
]
