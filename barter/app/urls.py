from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_details, name='post_details'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('search/', views.search_post, name='search_post'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', views.exit, name='logout'),
    path('post/<int:post_id>/exchange/', views.exchange_post, name='exchange_post'),
    path('exchange/', views.exchange_list, name='exchange_list'),
    path('exchange/update/<int:offer_id>/', views.update_exchange, name='update_exchange'),
    path('exchange/cancel/<int:offer_id>/', views.cancel_exchange, name='cancel_exchange'),
]