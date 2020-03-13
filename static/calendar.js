"use strict";

// Initialize Google OAuth client.
//
// It also sets up sign-in state listeners.
function initClient() {
  gapi.client.init({
    apiKey: API_KEY,
    clientId: CLIENT_ID,
    discoveryDocs: [
      'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
    ],
    scope: SCOPES
  }).then(
    () => {
      // Listen for sign-in stat changes & handle initial
      // sign-in state.
      gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
      updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());

      $('#authorize_button').on('click', () => {
        gapi.auth2.getAuthInstance().signIn();
      });

      $('#signout_button').on('click', () => {
        gapi.auth2.getAuthInstance().signOut();
      });
    },
    (err) => {
      alert(`We couldn't log you in for some reason.\n${JSON.stringify(error, null, 2)}`);
    }
  );
}

// Handle sign-in or sign-out
function updateSigninStatus(isSignedin) {
  if (isSignedin) {
    $('#authorize_button').hide();
    $('#signout_button').show();

    // Initialize calendar
    initCalendar();
  } else {
    $('#authorize_button').show();
    $('#signout_button').hide();
  }
}

// Update calendar with events from a certain month
function updateCalendar(calendar, month) {
  gapi.client.calendar.events.list({
      'calendarId': 'primary',
      'timeMin': getFirstOfMonth(month).toISOString(),
      'timeMax': getLastOfMonth(month).toISOString(),
      'showDeleted': false,
      'singleEvents': true,
      'orderBy': 'startTime'
    }).then((res) => {
      const toastEvents = [];
      for (const event of res.result.items) {
        toastEvents.push({
          id: event.id,
          title: event.summary,
          category: 'time',
          start: event.start.dateTime || event.start.date,
          end: event.end.dateTime || event.end.date
        });
      }

      calendar.clear();
      calendar.createSchedules(toastEvents, true);
      calendar.render();

      calendar.setDate(getFirstOfMonth(month).toDate());
    });;
}

// Initialize calendar with events from current month
function initCalendar() {
  const today = moment();
  const calendarEl = $('#calendar');

  // Attach today's date to data attribute
  calendarEl.data('currDate', today.toISOString());

  const calendar = createCalendar();

  // Get events for this month and attach to calendar
  gapi.client.calendar.events.list({
    'calendarId': 'primary',
    'timeMin': getFirstOfMonth(today).toISOString(),
    'timeMax': getLastOfMonth(today).toISOString(),
    'showDeleted': false,
    'singleEvents': true,
    'orderBy': 'startTime'
  }).then((res) => {
    const toastEvents = [];
    for (const event of res.result.items) {
      toastEvents.push({
        id: event.id,
        title: event.summary,
        category: 'time',
        start: event.start.dateTime || event.start.date,
        end: event.end.dateTime || event.end.date
      });
    }

    calendar.createSchedules(toastEvents);
  });

  // Attach event handlers for getting previous month's
  // events and next month's events
  $('#prev').on('click', () => {
    // Get current date that's showing now
    const currDate = moment(calendarEl.data('currDate'));
    const prevMonth = currDate.subtract('month', 1);

    // Update current date
    calendarEl.data('currDate', prevMonth.toISOString());

    updateCalendar(calendar, prevMonth)
  });

  $('#next').on('click', () => {
    // Get current date that's showing now
    const currDate = moment(calendarEl.data('currDate'));
    const nextMonth = currDate.add('month', 1);

    // Update current date
    calendarEl.data('currDate', nextMonth.toISOString());

    updateCalendar(calendar, nextMonth)
  })
}

// Get a moment object for the first day of the month
function getFirstOfMonth(currDate) {
  const firstOfMonth = moment({
    year: currDate.get('year'),
    month: currDate.get('month'),
    day: 0
  });

  return firstOfMonth;
}

// Get a moment object for the last day of the month
function getLastOfMonth(currDate) {
  const lastOfMonth = moment({
    year: currDate.get('year'),
    month: currDate.get('month'),
    day: 31
  });

  return lastOfMonth;
}


// Create a calendar, attach it to #content
function createCalendar() {
  const calendar = new tui.Calendar('#calendar', {
    isReadOnly: true,
    defaultView: 'month',
    taskView: true,
    scheduleView: true,
    useDetailPopup: true,
    template: {
      monthDayName: (dayname) => {
        return (`
          <span
            class="calendar-week-dayname-name"
          >
            ${dayname.label}
          </span>
        `);
      }
    }
  });

  return calendar;
}