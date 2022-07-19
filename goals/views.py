from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from goals.models import GoalCategory
from goals.serializers import GoalCategoryCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer
