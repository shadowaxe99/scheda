class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'