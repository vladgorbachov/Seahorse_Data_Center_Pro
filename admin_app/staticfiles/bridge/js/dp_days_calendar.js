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

    let currentDate = new Date();
    let selectedDate = null;
    let dpHours = {}; // Объект для хранения DP часов

    function loadDPHours() {
        fetch('/bridge/get_dp_hours/')
            .then(response => response.json())
            .then(data => {
                dpHours = {};
                data.forEach(item => {
                    dpHours[item.date] = item.hours;
                });
                renderCalendar(currentDate);
                updateSummary();
            })
            .catch(error => {
                console.error('Error loading DP hours:', error);
            });
    }

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
            const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dayElement.dataset.date = dateString;
            if (dpHours[dateString]) {
                const hours = dpHours[dateString];
                const hoursElement = document.createElement('span');
                hoursElement.classList.add('dp-hours');
                hoursElement.textContent = hours;
                dayElement.appendChild(hoursElement);
                if (hours > 0) {
                    dayElement.classList.add('has-dp-hours');
                }
            }
            dayElement.addEventListener('click', () => {
                selectedDate = dateString;
                dpHoursInput.value = dpHours[dateString] || 0;
                hoursInputWindow.style.display = 'block';
            });
            calendarContainer.appendChild(dayElement);
        }
    }

    function saveDPHours(date, hours) {
        console.log('Attempting to save DP hours:', date, hours);
        fetch('/bridge/save_dp_hours/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ date, hours })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('DP hours saved successfully');
                dpHours[date] = hours;
                renderCalendar(currentDate);
                updateSummary();
                closeHoursInputWindow();
            } else {
                console.error('Failed to save DP hours:', data.error);
                alert('Failed to save DP hours. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error saving DP hours:', error);
            alert('An error occurred while saving DP hours. Please try again.');
        });
    }

    function closeHoursInputWindow() {
        hoursInputWindow.style.display = 'none';
        dpHoursInput.value = 0;
    }

    function updateSummary() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        let monthTotal = 0;
        let yearTotal = 0;

        for (const [date, hours] of Object.entries(dpHours)) {
            const [y, m, d] = date.split('-').map(Number);
            if (y === year) {
                yearTotal += hours;
                if (m === month + 1) {
                    monthTotal += hours;
                }
            }
        }

        monthHoursElement.textContent = monthTotal;
        yearHoursElement.textContent = yearTotal;
    }

    prevMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
        updateSummary();
    });

    nextMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
        updateSummary();
    });

    saveHoursButton.addEventListener('click', () => {
        const hours = parseInt(dpHoursInput.value);
        if (hours >= 0 && hours <= 24) {
            saveDPHours(selectedDate, hours);
        } else {
            alert('Please enter a number between 0 and 24.');
        }
    });

    cancelHoursButton.addEventListener('click', closeHoursInputWindow);

    backButton.addEventListener('click', () => {
        window.location.href = '/bridge/';
    });

    mainPageButton.addEventListener('click', () => {
        window.location.href = '/';
    });

    // Загрузка данных при инициализации
    loadDPHours();
});