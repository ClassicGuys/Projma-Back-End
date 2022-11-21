from django.db import models
from colorfield.fields import ColorField
from accounts.models import Profile


# Create your models here.
class WorkSpace(models.Model):
    TYPE_CHOICES = [
        ("education", "آموزشی"),
        ("marketing", "بازاریابی"),
        ("small business", "سرمایه گذاری کوچک"),
        ("operations", "عملیاتی"),
        ("engineering-it", "مهندسی و IT"),
        ("finance", "مالی"),
        ("human resources", "منابع انسانی"),
        ("other", "سایر"),
    ]

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=256, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    members = models.ManyToManyField(to=Profile, related_name='workspaces')


class Board(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    background_pic = models.ImageField(blank=True, null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='boards')
    admins = models.ManyToManyField(Profile, related_name='administrating_boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    members = models.ManyToManyField(Profile, related_name='boards')


class TaskList(models.Model):
    title = models.CharField(max_length=256)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasklists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Task(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    estimate = models.FloatField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    out_of_estimate = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    labels = models.ManyToManyField(to='Label', related_name='tasks')
    workers = models.ManyToManyField(Profile, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class CheckList(models.Model):
    text = models.CharField(max_length=512)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='checklists')


class Label(models.Model):
    title = models.CharField(max_length=256)
    color = ColorField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')


class File(models.Model):
    file_url = models.URLField(max_length=1000, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


# class TaskLabel(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     label = models.ForeignKey(Label, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('task', 'label')


# class WorksOn(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'task')


# class BoardAdmin(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'board')


# class MemberShip(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'board')