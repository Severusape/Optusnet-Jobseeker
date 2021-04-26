#!/bin/python3
import getpass
from crontab import CronTab

# Create a cronjob to run optusnet_jobseeker.py every reboot
job = None
with CronTab(user=getpass.getuser()) as cron:
    job = cron.new(command="python3 optusnet_jobseeker.py")
    job.every_reboot()
job.run()