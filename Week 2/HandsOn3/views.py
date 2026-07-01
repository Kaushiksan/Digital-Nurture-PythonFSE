from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Course
from .forms import CourseForm


class CourseListView(ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "course_form.html"
    success_url = reverse_lazy("course_list")
