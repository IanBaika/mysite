from django.contrib.auth.models import User, Group
from shop.models import *
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'title']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['title', 'description']


class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'title', 'dish_type', 'categories', 'description', 'price']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['title', 'image']


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['session_key', 'user', 'total_cost']


class CartContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['cart', 'product', 'qty']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']