from django.db import models

# Create your models here.

class QuizCreation(models.Model):
    status_type = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Finished', 'Finished')
    )
    question = models.TextField(null = True, blank = True)
    options = models.JSONField()
    right_answer = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=status_type, max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'quiz_creation'