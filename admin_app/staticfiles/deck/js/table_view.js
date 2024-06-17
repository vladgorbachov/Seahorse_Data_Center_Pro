document.addEventListener('DOMContentLoaded', () => {
    const tableButton = document.getElementById('tableButton');
    const tableInputWindow = document.getElementById('tableInputWindow');
    const saveTableDimensionsButton = document.getElementById('saveTableDimensionsButton');
    const cancelTableDimensionsButton = document.getElementById('cancelTableDimensionsButton');
    const tableRowsInput = document.getElementById('tableRows');
    const tableColumnsInput = document.getElementById('tableColumns');

    tableButton.addEventListener('click', () => {
        tableInputWindow.style.display = 'block';
    });

    saveTableDimensionsButton.addEventListener('click', () => {
        const rows = tableRowsInput.value;
        const columns = tableColumnsInput.value;
        if (rows && columns) {
            createTable(rows, columns);
        }
    });

    cancelTableDimensionsButton.addEventListener('click', () => {
        tableInputWindow.style.display = 'none';
    });

    function createTable(rows, columns) {
        fetch('/deck/save_table/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ folder_id: folderId, rows: rows, columns: columns })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            } else {
                console.error('Failed to create table:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

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
});
