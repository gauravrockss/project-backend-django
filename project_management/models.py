from django.db import models
from accounts.models import User
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    lead = models.ForeignKey(User, related_name='lead_projects', on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=0)
    imageURL = models.URLField()
    priority = models.CharField(
        max_length=10,
        choices=[('Lowest', 'Lowest'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Highest', 'Highest')],
        default='Medium'
    )
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)

class Issue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('Backlog', 'Backlog'), ('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Review', 'Review'), ('Done', 'Done')],
        default='To Do'
    )
    issueType = models.CharField(
        max_length=20,
        choices=[('Task', 'Task'), ('Bug', 'Bug'), ('Subtask', 'Subtask'), ('Epic', 'Epic')],
        default='Task'
    )
    priority = models.CharField(
        max_length=10,
        choices=[('Lowest', 'Lowest'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Highest', 'Highest')],
        default='Medium'
    )
    labels = models.ManyToManyField('Label', blank=True)
    assignee = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.SET_NULL, null=True, blank=True)
    reporter = models.ForeignKey(User, related_name='reported_issues', on_delete=models.SET_NULL, null=True, blank=True)
    startDate = models.DateTimeField(default=timezone.now)
    imageIds = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        if not self.startDate:
            self.startDate = timezone.now()
        super().save(*args, **kwargs)

class Label(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='labels', on_delete=models.CASCADE)
