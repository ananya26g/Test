from django.conf import settings
from rest_framework.permissions import BasePermission

QUIZ_API_KEY = settings.QUIZ_API_KEY

class PreSharedPermissionForQuiz(BasePermission):

    def has_permission(self, request, view):
        """
        header: "api-key" get as "HTTP_API_KEY"
        """
        api_key = request.META['HTTP_API_KEY']
        return api_key == QUIZ_API_KEY