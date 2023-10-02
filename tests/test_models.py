import unittest
from django.test import TestCase
from app.models import Meeting, User

class MeetingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            start_time='2022-01-01 10:00:00',
            end_time='2022-01-01 11:00:00',
            organizer=self.user
        )

    def test_meeting_creation(self):
        self.assertEqual(self.meeting.title, 'Test Meeting')
        self.assertEqual(self.meeting.start_time, '2022-01-01 10:00:00')
        self.assertEqual(self.meeting.end_time, '2022-01-01 11:00:00')
        self.assertEqual(self.meeting.organizer, self.user)

    def test_meeting_str(self):
        self.assertEqual(str(self.meeting), 'Test Meeting')

    def test_meeting_duration(self):
        duration = self.meeting.get_duration()
        self.assertEqual(duration, 60)

if __name__ == '__main__':
    unittest.main()