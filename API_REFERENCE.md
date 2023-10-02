# ScheduleAI API Reference

This document provides detailed information about the ScheduleAI API endpoints and their usage.

## Authentication

All API endpoints require authentication. To authenticate, include your API token in the `Authorization` header of your requests.

## Endpoints

### GET /api/calendars

Retrieve a list of calendars.

#### Parameters

- None

#### Response

- Status: 200 OK
- Body: Array of calendar objects

### POST /api/events

Create a new event.

#### Parameters

- title (string): The title of the event
- start_time (string): The start time of the event
- end_time (string): The end time of the event

#### Response

- Status: 201 Created
- Body: The created event object

### DELETE /api/events/{event_id}

Delete an event.

#### Parameters

- event_id (integer): The ID of the event to delete

#### Response

- Status: 204 No Content

For more information, please refer to the [ScheduleAI API Documentation](https://example.com/api-docs).