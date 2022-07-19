from django.urls import path, include

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view()),

]
