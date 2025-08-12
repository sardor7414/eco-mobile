from django.contrib import admin
from django.urls import path, include
from .views import MaterialListCreateAPIView, MaterialDetailAPIView, MaterialRetrieveUpdateDestroyAPIView, \
    MaterialsMapView, MaterialContactInfoView, FilterByMaterialTypeAPIView, FilterByLocationAPIView, \
    FilterByQuantityAPIView

urlpatterns = [
    path('materials/', MaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('materials/<int:pk>/', MaterialDetailAPIView.as_view(), name='material-detail'),
    path('materials/destroy/<int:pk>/', MaterialRetrieveUpdateDestroyAPIView.as_view(), name='material-destroy'),
    path('materials-map/', MaterialsMapView.as_view(), name='materials-map'),
    path('materials/<int:pk>/contact/', MaterialContactInfoView.as_view(), name='material-contact'),
    path('filter-material-type/', FilterByMaterialTypeAPIView.as_view(), name='filter-material-type'),
    path('filter-material-location/', FilterByLocationAPIView.as_view(), name='filter-material-location'),
    path('filter-by-qty/', FilterByQuantityAPIView.as_view(), name='filter-by-qty')
]
