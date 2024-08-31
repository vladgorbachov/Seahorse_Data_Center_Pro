// dp_days_calendar.js
document.addEventListener('DOMContentLoaded', () => {
    const calendarContainer = document.getElementById('calendar');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthButton = document.getElementById('prevMonth');
    const nextMonthButton = document.getElementById('nextMonth');
    const hoursInputWindow = document.getElementById('hoursInputWindow');
    const dpHoursInput = document.getElementById('dpHoursInput');
    const saveHoursButton = document.getElementById('saveHours');
    const cancelHoursButton = document.getElementById('cancelHours');
    const monthHoursElement = document.getElementById('monthHours');
    const yearHoursElement = document.getElementById('yearHours');
    const backButton = document.getElementById('backButton');

    let currentDate = new Date();
    let selectedDate = null;

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();

        currentMonthElement.textContent = `${date.toLocaleString('default', { month: 'long' })} ${year}`;

        let calendarHTML = '<table><tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr><tr>';

        for (let i = 0; i < firstDay.getDay(); i++) {
            calendarHTML += '<td></td>';
        }

        for (let day = 1; day <= daysInMonth; day++) {
            if ((day + firstDay.getDay() - 1) % 7 === 0) {
                calendarHTML += '</tr><tr>';
            }
            calendarHTML += `<td data-date="${year}-${month + 1}-${day}">${day}<span class="dp-hours"></span></td>`;
        }

        calendarHTML += '</tr></table>';
        calendarContainer.innerHTML = calendarHTML;

        // Add click event listeners to date cells
        document.querySelectorAll('#calendar td[data-date]').forEach(cell => {
            cell.addEventListener('click', () => {
                selectedDate = cell.dataset.date;
                hoursInputWindow.style.display = 'block';
            });
        });

        updateDPHours();
    }

    function updateDPHours() {
        // Fetch DP hours from the server and update the calendar
        fetch(`/api/dp_hours/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/`)
            .then(response => response.json())
            .then(data => {
                data.forEach(entry => {
                    const cell = document.querySelector(`td[data-date="${entry.date}"]`);
                    if (cell) {
                        cell.querySelector('.dp-hours').textContent = entry.hours;
                    }
                });
                updateSummary();
            });
    }

    function updateSummary() {
        // Fetch and update monthly and yearly DP hours
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth() + 1;

        fetch(`/api/dp_hours_summary/${year}/${month}/`)
            .then(response => response.json())
            .then(data => {
                monthHoursElement.textContent = data.month_hours;
                yearHoursElement.textContent = data.year_hours;
            });
    }

    function saveDPHours(date, hours) {
        fetch('/api/save_dp_hours/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ date, hours })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateDPHours();
                hoursInputWindow.style.display = 'none';
            } else {
                alert('Failed to save DP hours. Please try again.');
            }
        });
    }

    prevMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    saveHoursButton.addEventListener('click', () => {
        const hours = parseInt(dpHoursInput.value);
        if (hours >= 2 && hours <= 24) {
            saveDPHours(selectedDate, hours);
        } else {
            alert('Please enter a number between 2 and 24.');
        }
    });

    cancelHoursButton.addEventListener('click', () => {
        hoursInputWindow.style.display = 'none';
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/bridge/';
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    renderCalendar(currentDate);
});