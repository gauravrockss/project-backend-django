from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    IssueListCreateView,
    IssueDetailView,
    LabelListCreateView,
    LabelDetailView,
    ProjectIssueStatsView,
)

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('projects/<int:project_id>/issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('labels/', LabelListCreateView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelDetailView.as_view(), name='label-detail'),
    path('project-issue-stats/', ProjectIssueStatsView.as_view(), name='project-issue-stats'),
    path('project-issue-stats/<int:project_id>/', ProjectIssueStatsView.as_view(), name='specific-project-issue-stats')
]
