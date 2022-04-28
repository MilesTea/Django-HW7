from rest_framework.permissions import BasePermission

from advertisements.models import Advertisement


class IsOwnerOrReadOnly(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method == 'GET':
			return True
		return request.user == obj.user