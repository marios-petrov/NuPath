from calendarEvent import CalendarEvent

class CollegeClass:
    def __init__(self, class_name: str, calendar_event: CalendarEvent, class_description: str = ""):
        self.class_name = class_name
        self.calendar_event = calendar_event
        self.class_description = class_description
