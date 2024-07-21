from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """ Разрешает доступ только активным сотрудникам."""
    def has_permission(self, request, view):
        return request.user and request.user.is_active
