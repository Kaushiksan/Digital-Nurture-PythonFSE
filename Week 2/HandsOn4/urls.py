from django.urls import path

from .views import (
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView
)

urlpatterns = [

    path(
        "courses/",
        CourseListCreateAPIView.as_view(),
        name="course-list"
    ),

    path(
        "courses/<int:pk>/",
        CourseRetrieveUpdateDestroyAPIView.as_view(),
        name="course-detail"
    ),

]
