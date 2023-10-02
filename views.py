
from django.shortcuts import render
from django.http import JsonResponse

def schedule_meeting(request):
    if request.method == 'POST':
        # Logic to schedule a meeting
        return JsonResponse({'message': 'Meeting scheduled successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def cancel_meeting(request):
    if request.method == 'POST':
        # Logic to cancel a meeting
        return JsonResponse({'message': 'Meeting cancelled successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_meeting_details(request, meeting_id):
    if request.method == 'GET':
        # Logic to retrieve meeting details
        return JsonResponse({'meeting_id': meeting_id, 'title': 'Sample Meeting'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

