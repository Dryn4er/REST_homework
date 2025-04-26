from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner