import unittest
from django.test import TestCase, Client
from django.urls import reverse
from .models import Meeting

class MeetingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            date='2022-01-01',
            start_time='09:00',
            end_time='10:00',
            location='Meeting Room 1',
            organizer='John Doe',
            attendees='jane@example.com, bob@example.com',
            description='This is a test meeting'
        )

    def test_meeting_list_view(self):
        response = self.client.get(reverse('meeting-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Test Meeting')

    def test_meeting_detail_view(self):
        response = self.client.get(reverse('meeting-detail', args=[self.meeting.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertContains(response, 'Test Meeting')

    def test_meeting_create_view(self):
        response = self.client.post(reverse('meeting-create'), {
            'title': 'New Meeting',
            'date': '2022-01-02',
            'start_time': '10:00',
            'end_time': '11:00',
            'location': 'Meeting Room 2',
            'organizer': 'Jane Doe',
            'attendees': 'john@example.com',
            'description': 'This is a new meeting'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Meeting.objects.count(), 2)

    def test_meeting_update_view(self):
        response = self.client.post(reverse('meeting-update', args=[self.meeting.id]), {
            'title': 'Updated Meeting',
            'date': '2022-01-01',
            'start_time': '09:00',
            'end_time': '10:00',
            'location': 'Meeting Room 1',
            'organizer': 'John Doe',
            'attendees': 'jane@example.com, bob@example.com',
            'description': 'This is an updated meeting'
        })
        self.assertEqual(response.status_code, 302)
        self.meeting.refresh_from_db()
        self.assertEqual(self.meeting.title, 'Updated Meeting')

    def test_meeting_delete_view(self):
        response = self.client.post(reverse('meeting-delete', args=[self.meeting.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Meeting.objects.count(), 0)

if __name__ == '__main__':
    unittest.main()