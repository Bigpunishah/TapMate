from django.urls import path
from . import views

# route, view, name 
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('taptags', views.users_tags, name='taptags'),
    # May need to update poorimary key to a a string for the object id.
    path('tag/<int:primary_key>', views.individual_tap_tag, name='tag'),
    path('claim_tag/<int:primary_key>', views.claim_tag, name='claim_tag'),


]