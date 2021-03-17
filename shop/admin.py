from django.contrib import admin
from .models import Dish, Category, Cart, CartContent

admin.site.register(Category)


#регистрация модели в админке
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    # список отображаемых полей модели
    list_display = ['id', 'title', 'dish_type', 'description']


admin.site.register(Cart)
admin.site.register(CartContent)

