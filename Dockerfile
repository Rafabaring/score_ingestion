FROM python:3.8
COPY . /.

COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Install cron and make the script executable
RUN apt-get update && apt-get -y install cron
RUN crontab /etc/cron.d/crontab
RUN chmod +x /analytics_job/student_avg_score.py
RUN chmod +x /analytics_job/exam_avg_score.py

RUN python3.8 -m pip install -r /requirements.txt

# Create a log file for cron
RUN touch /var/log/cron.log

# Start cron and tail the log file
CMD cron && tail -f /var/log/cron.log