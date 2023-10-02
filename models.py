from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Meeting(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attendees = models.ManyToManyField(User, related_name='meetings_attending')

    def __str__(self):
        return self.title

class Transcript(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Transcript for {self.meeting.title}"