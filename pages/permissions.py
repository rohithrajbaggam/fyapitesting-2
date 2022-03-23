from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Page


class IsPageAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.page_admin == request.user



class IsPagePostAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): # pk to get pageadmin 
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.admin_user == request.user

