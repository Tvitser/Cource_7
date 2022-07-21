from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from goals.models import GoalCategory
from goals.serializers import GoalCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCreateSerializer

