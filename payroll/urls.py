from django.urls import path

from .views import (
    PostDeleteView,
    PostUpdateView,
    PostDetailView,
    PostListView,
)
from . import views 

# app name needed so that i can use payroll:name_of_pattern in the html because 
# the other url.py file includes this 
app_name = 'payroll'
urlpatterns = [
    path('', PostListView.as_view(), name="index"),
    path('shift/<int:pk>/', PostDetailView.as_view(), name="shift"),
    path('shift/<int:pk>/update/', PostUpdateView.as_view(), name="shift-update"),
    path('shift/<int:pk>/delete/', PostDeleteView.as_view(), name="shift-delete"),

]
