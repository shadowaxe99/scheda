import datetime


class Scheduler:
    def schedule_email(self, recipient, subject, body, date_time):
        scheduled_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.datetime.now()

        if scheduled_time <= current_time:
            print('Invalid scheduled time. Please choose a future date and time.')
            return

        # TODO: Implement email scheduling logic
        print(f'Scheduled email to {recipient} for {date_time}')
