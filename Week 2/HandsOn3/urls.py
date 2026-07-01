from django.urls import path

from .views import (
    CourseListView,
    CourseCreateView
)

urlpatterns = [

    path(
        "",
        CourseListView.as_view(),
        name="course_list"
    ),

    path(
        "add/",
        CourseCreateView.as_view(),
        name="course_add"
    ),

]
