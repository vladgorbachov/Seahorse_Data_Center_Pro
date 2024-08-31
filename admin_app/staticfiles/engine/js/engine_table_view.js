document.addEventListener('DOMContentLoaded', () => {
    const tableButton = document.getElementById('tableButton');
    const tableInputWindow = document.getElementById('tableInputWindow');
    const saveTableDimensionsButton = document.getElementById('saveTableDimensionsButton');
    const cancelTableDimensionsButton = document.getElementById('cancelTableDimensionsButton');
    const tableRowsInput = document.getElementById('tableRows');
    const tableColumnsInput = document.getElementById('tableColumns');
    const saveTableButton = document.getElementById('saveTableButton');
    const deleteTableButton = document.getElementById('deleteTableButton');

    let tableId = null;

    tableButton.addEventListener('click', () => {
        tableInputWindow.style.display = 'block';
    });

    saveTableDimensionsButton.addEventListener('click', () => {
        const rows = parseInt(tableRowsInput.value);
        const columns = parseInt(tableColumnsInput.value);
        if (rows && columns) {
            createTable(rows, columns);
        }
    });

    cancelTableDimensionsButton.addEventListener('click', () => {
        tableInputWindow.style.display = 'none';
    });

    function fetchWithTimeout(url, options, timeout = 7000) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), timeout))
        ]);
    }

    function createTable(rows, columns) {
        fetchWithTimeout('/engine/save_table/', {
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
                tableId = data.table_id;  // Инициализация tableId
                location.reload();  // Перезагружаем страницу для отображения таблицы
            } else {
                alert('Error creating table');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    saveTableButton.addEventListener('click', () => {
        const cells = [];
        document.querySelectorAll('td[data-cell-id]').forEach(cell => {
            cells.push({
                id: cell.dataset.cellId,
                content: cell.textContent
            });
        });
        fetchWithTimeout('/engine/save_table_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ table_id: tableId, cells: cells })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Table data saved successfully');
            } else {
                alert('Error saving table data');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    deleteTableButton.addEventListener('click', () => {
        const confirmDelete = confirm('Are you sure you want to delete this table?');
        if (confirmDelete) {
            fetchWithTimeout(`/engine/delete_table_in_folder/${folderId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const tableElement = document.querySelector('table');
                    if (tableElement) {
                        tableElement.remove();
                    }
                    alert('Table deleted successfully');
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; cookies.length > i; i++) {
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
