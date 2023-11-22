from django.db import models
from django.utils.module_loading import autodiscover_modules

from .utils import timestamp_to_datetime


class Job(models.Model):

    job_name = models.CharField(max_length=100, unique=True)

    frequency = models.PositiveIntegerField()

    max_run_time = models.PositiveIntegerField()  # TODO: Remove

    last_run = models.PositiveIntegerField(default=0)

    error = models.TextField(blank=True)

    class Meta:
        ordering = ('job_name',)

    def __str__(self):
        return self.job_name

    def save(self, *args, **kwargs):
        self.max_run_time = 0  # TODO: Remove
        super().save(*args, **kwargs)

    @property
    def last_run_time(self):
        return timestamp_to_datetime(self.last_run)

    @property
    def next_run_time(self):
        return timestamp_to_datetime(self.last_run + self.frequency)


autodiscover_modules('cron')
