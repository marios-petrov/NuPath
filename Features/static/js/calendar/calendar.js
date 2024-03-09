// calendar.js (Tre)
// from here, same one nate used: https://fullcalendar.io/docs/multimonth-stack

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    timeZone: 'GMT-5', // our time zone (starting march 10th, before that its GMT-6)
    initialView: 'dayGridMonth',
    events: 'https://fullcalendar.io/api/demo-feeds/events.json',
    editable: true,
    selectable: true
  });

  calendar.render();
});
