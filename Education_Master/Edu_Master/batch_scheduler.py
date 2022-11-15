from Schedule_time import *
from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(minute='*/10', day_of_week="mon-fri"))
def every_Ten_min_For_Account_Activation():
    
    pass

