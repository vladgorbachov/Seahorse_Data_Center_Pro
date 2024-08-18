document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.getElementById('saveButton');
    const deleteButton = document.getElementById('deleteButton');
    const tableContainer = document.getElementById('tableContainer');
    const folderId = tableContainer.dataset.folderId;
    const tableId = tableContainer.dataset.tableId;

    if (saveButton) {
        saveButton.addEventListener('click', function() {
            const rows = document.querySelectorAll('.table-row');
            const cells = [];
            rows.forEach(row => {
                const inputs = row.querySelectorAll('input');
                inputs.forEach(input => {
                    cells.push({
                        id: input.dataset.cellId,
                        content: input.value
                    });
                });
            });

            fetch('/bridge/save_table_data/', {  // Обновлен URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    table_id: tableId,
                    cells: cells
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Table saved successfully!');
                } else {
                    alert('Error saving table: ' + data.message);
                }
            });
        });
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this table?')) {
                fetch(`/bridge/delete_table_in_folder/${folderId}/`, {  // Обновлен URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.href = `/bridge/folder/${folderId}/`;  // Обновлен URL
                    } else {
                        alert('Error deleting table: ' + data.message);
                    }
                });
            }
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