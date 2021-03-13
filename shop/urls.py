from django.urls import path
import shop.views as v
from django.conf import settings
from django.contrib.auth import logout


urlpatterns = [
    path('', v.HomeView.as_view(), name="index"),
    path('add/', v.add_dish, name="add"),
    path('register/', v.register, name="register"),
    path('login/', v.log_in, name="login"),
    path('logout/', v.logout_view, name="logout"),
    path('edit/', v.edit, name="edit"),
    path('upload/', v.image_upload_view, name='upload'),
    path('dish_edit/',v.dish_edit, name='dish_edit'),
    path('cart/', v.CartView.as_view(), name='cart'),

]