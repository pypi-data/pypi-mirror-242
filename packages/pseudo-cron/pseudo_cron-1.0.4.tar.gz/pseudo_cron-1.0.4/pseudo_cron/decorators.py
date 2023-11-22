import inspect

from .service.models import Job


cron_jobs = []


def schedule_job(frequency: int):

    def decorator(func):
        job_name = '{}.{}'.format(inspect.getmodule(func).__name__, func.__name__)
        cron_jobs.append(Job(job_name=job_name, func=func, frequency=frequency))

        return func

    return decorator
