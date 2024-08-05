from rest_framework import generics, permissions, status
from .models import Project, Issue, Label
from .serializers import ProjectSerializer, IssueSerializer, LabelSerializer
from .functions import BaseResponseView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView

class ProjectListCreateView(generics.ListCreateAPIView, BaseResponseView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return self.success_response("Project created successfully", response.data, status.HTTP_201_CREATED)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView, BaseResponseView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return self.success_response("Project retrieved successfully", response.data)
        except NotFound:
            return self.error_response("Project not found", status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.success_response("Project updated successfully", response.data)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return self.success_response("Project deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return self.error_response("Project not found", status.HTTP_404_NOT_FOUND)

class IssueListCreateView(generics.ListCreateAPIView, BaseResponseView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project__id=project_id, project__owner=self.request.user)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id, owner=self.request.user)
        serializer.save(project=project)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return self.success_response("Issue created successfully", response.data, status.HTTP_201_CREATED)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

class IssueDetailView(generics.RetrieveUpdateDestroyAPIView, BaseResponseView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project__id=project_id, project__owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return self.success_response("Issue retrieved successfully", response.data)
        except NotFound:
            return self.error_response("Issue not found", status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.success_response("Issue updated successfully", response.data)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return self.success_response("Issue deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return self.error_response("Issue not found", status.HTTP_404_NOT_FOUND)

class LabelListCreateView(generics.ListCreateAPIView, BaseResponseView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return self.success_response("Label created successfully", response.data, status.HTTP_201_CREATED)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

class LabelDetailView(generics.RetrieveUpdateDestroyAPIView, BaseResponseView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return self.success_response("Label retrieved successfully", response.data)
        except NotFound:
            return self.error_response("Label not found", status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.success_response("Label updated successfully", response.data)
        except ValidationError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return self.success_response("Label deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return self.error_response("Label not found", status.HTTP_404_NOT_FOUND)

class ProjectIssueStatsView(APIView, BaseResponseView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id=None, *args, **kwargs):
        try:
            if project_id:
                project = Project.objects.get(id=project_id, owner=request.user)
                todo_count = Issue.objects.filter(project_id=project.id, status='To Do').count()
                in_progress_count = Issue.objects.filter(project_id=project.id, status='In Progress').count()
                review_count = Issue.objects.filter(project_id=project.id, status='Review').count()
                done_count = Issue.objects.filter(project_id=project.id, status='Done').count()

                project_stats = {
                    'project_id': project.id,
                    'project_name': project.name,
                    'todo_count': todo_count,
                    'in_progress_count': in_progress_count,
                    'review_count': review_count,
                    'done_count': done_count
                }
                return self.success_response("Project statistics retrieved successfully", project_stats)
            else:
                project_stats = []
                projects = Project.objects.filter(owner=request.user)

                for project in projects:
                    todo_count = Issue.objects.filter(project_id=project.id, status='To Do').count()
                    in_progress_count = Issue.objects.filter(project_id=project.id, status='In Progress').count()
                    review_count = Issue.objects.filter(project_id=project.id, status='Review').count()
                    done_count = Issue.objects.filter(project_id=project.id, status='Done').count()

                    project_stats.append({
                        'project_id': project.id,
                        'project_name': project.name,
                        'todo_count': todo_count,
                        'in_progress_count': in_progress_count,
                        'review_count': review_count,
                        'done_count': done_count
                    })

                return self.success_response("Project statistics retrieved successfully", project_stats)

        except NotFound:
            return self.error_response("Projects not found", status.HTTP_404_NOT_FOUND)



#  list all user
