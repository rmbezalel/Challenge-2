// SmartMeet Frontend - Connect to Flask Backend

const API_URL = 'http://localhost:5050';
let meetings = [];

// Set today's date as default
document.addEventListener('DOMContentLoaded', function() {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('meetingDate').value = today;
});

function timeToDecimal(timeStr) {
  if (!timeStr) return 0;
  const [hours, minutes] = timeStr.split(':').map(Number);
  return hours + minutes / 60;
}

function decimalToTime(decimal) {
  const hours = Math.floor(decimal);
  const minutes = Math.round((decimal - hours) * 60);
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

function addMeeting() {
  const title = document.getElementById('meetingTitle').value.trim();
  const date = document.getElementById('meetingDate').value;
  const startTime = document.getElementById('startTime').value;
  const endTime = document.getElementById('endTime').value;
  const priority = parseInt(document.getElementById('priority').value);

  if (!title || !date || !startTime || !endTime) {
    alert('❌ Please fill in all fields');
    return;
  }

  const start = timeToDecimal(startTime);
  const end = timeToDecimal(endTime);

  if (start >= end) {
    alert('❌ End time must be after start time');
    return;
  }

  const meeting = {
    title,
    date,
    start,
    end,
    priority
  };

  meetings.push(meeting);
  
  // Clear form
  document.getElementById('meetingTitle').value = '';
  document.getElementById('startTime').value = '';
  document.getElementById('endTime').value = '';
  document.getElementById('priority').value = '2';

  updateMeetingsList();
  alert(`✅ "${title}" added successfully!`);
}

function updateMeetingsList() {
  const listContainer = document.getElementById('meetingsList');
  const clearBtn = document.getElementById('clearBtn');

  if (meetings.length === 0) {
    listContainer.innerHTML = '<p class="empty-state">No meetings added yet</p>';
    clearBtn.style.display = 'none';
    return;
  }

  clearBtn.style.display = 'block';

  listContainer.innerHTML = meetings.map((meeting, index) => `
    <div class="meeting-item">
      <div class="meeting-title">${meeting.title}</div>
      <div class="meeting-details">
        <span>📅 ${meeting.date}</span>
        <span>⏰ ${meeting.start.toFixed(2)} - ${meeting.end.toFixed(2)}</span>
        <span>⭐ ${['Low', 'Medium', 'High'][meeting.priority - 1]}</span>
      </div>
      <button class="remove-btn" onclick="removeMeeting(${index})">🗑️ Remove</button>
    </div>
  `).join('');
}

function removeMeeting(index) {
  meetings.splice(index, 1);
  updateMeetingsList();
}

function clearMeetings() {
  if (confirm('⚠️ Clear all meetings?')) {
    meetings = [];
    updateMeetingsList();
    document.getElementById('output').style.display = 'none';
  }
}

function optimizeSchedule() {
  if (meetings.length === 0) {
    alert('❌ Please add at least one meeting');
    return;
  }

  const workStart = timeToDecimal(document.getElementById('workStart').value);
  const workEnd = timeToDecimal(document.getElementById('workEnd').value);

  if (workStart >= workEnd) {
    alert('❌ End work hour must be after start hour');
    return;
  }

  // Show loading state
  document.getElementById('loading').style.display = 'block';
  document.getElementById('output').style.display = 'none';

  const payload = {
    meetings,
    preferred_hours: {
      start: workStart,
      end: workEnd
    }
  };

  fetch(`${API_URL}/api/optimize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }
    return response.json();
  })
  .then(data => {
    displayResults(data);
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('loading').style.display = 'none';
    alert(`❌ Error connecting to backend: ${error.message}\n\nMake sure the Flask server is running: python3 scheduler.py`);
  });
}

function displayResults(data) {
  document.getElementById('loading').style.display = 'none';

  // Display conflicts
  const conflictSection = document.getElementById('conflictSection');
  const successSection = document.getElementById('successSection');
  const conflictsList = document.getElementById('conflictsList');

  if (data.has_conflicts) {
    conflictSection.style.display = 'block';
    successSection.style.display = 'none';
    conflictsList.innerHTML = data.conflicts.map(c => `<li>${c}</li>`).join('');
  } else {
    conflictSection.style.display = 'none';
    successSection.style.display = 'block';
  }

  // Display optimized meetings
  const resultsList = document.getElementById('resultsList');
  resultsList.innerHTML = data.optimized_meetings.map((meeting, i) => `
    <div class="result-item">
      <div class="result-header">
        <span class="result-number">${i + 1}.</span>
        <span class="result-title">${meeting.title}</span>
      </div>
      <div class="result-details">
        <p>⏰ ${meeting.start.toFixed(2)} – ${meeting.end.toFixed(2)}</p>
        <p>⭐ Priority: ${meeting.priority}</p>
        <p>📊 AI Score: <span class="ai-score">${meeting.efficiency_score}</span>/100</p>
      </div>
    </div>
  `).join('');

  // Update summary
  document.getElementById('totalMeetings').textContent = data.total_meetings;
  document.getElementById('averageScore').textContent = data.average_score;

  // Show results
  document.getElementById('output').style.display = 'block';
}

