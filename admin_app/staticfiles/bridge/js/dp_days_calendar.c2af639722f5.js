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
    const mainPageButton = document.getElementById('mainPageButton');
    const backButton = document.getElementById('backButton');


    if (backButton) {
        backButton.addEventListener('click', goBack);
    }
});

    if (mainPageButton) {
        mainPageButton.addEventListener('click', () => {
            console.log('Main Page button clicked');
            window.location.href = '/';  // Изменено на корневой путь
        });
    } else {
        console.error('Main Page button not found');
    }


    let currentDate = new Date();
    let selectedDate = null;



    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();

        currentMonthElement.textContent = `${date.toLocaleString('default', { month: 'long' })} ${year}`;

        calendarContainer.innerHTML = '';

        for (let i = 0; i < firstDay.getDay(); i++) {
            calendarContainer.appendChild(document.createElement('div'));
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.textContent = day;
            dayElement.dataset.date = `${year}-${month + 1}-${day}`;
            dayElement.addEventListener('click', () => {
                selectedDate = dayElement.dataset.date;
                hoursInputWindow.style.display = 'block';
            });
            calendarContainer.appendChild(dayElement);
        }

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

