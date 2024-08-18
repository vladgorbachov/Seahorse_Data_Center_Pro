// Глобальные переменные
let fileList, viewMode, sortBy, searchInput, contextMenu;
let currentFolderId, currentPath;

// Глобальные функции
function loadFolderContents(folderId, subfolderPath = null) {
    currentFolderId = folderId;
    currentPath = subfolderPath || '';

    let url = `/bridge/get_folder_contents/?folder_id=${encodeURIComponent(folderId)}`;
    if (subfolderPath) {
        url = `/bridge/get_folder_contents/?subfolder_path=${encodeURIComponent(subfolderPath)}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayFiles(data.contents);
                document.getElementById('currentPath').value = data.current_path;
                sortFiles(sortBy.value);
                viewMode.value = 'grid';
                fileList.className = 'file-list grid-view';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error loading folder contents:', error);
            alert('An error occurred while loading folder contents.');
        });
}

// Остальные функции остаются без изменений, за исключением URL-путей

function renameFile(file) {
    const newName = prompt('Enter new name:', file.name);
    if (newName && newName !== file.name) {
        fetch('/bridge/rename_file/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ file_id: file.id, new_name: newName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadFolderContents(currentFolderId, currentPath);
            } else {
                alert(data.message);
            }
        });
    }
}

function deleteFile(file) {
    if (confirm(`Are you sure you want to delete ${file.name}?`)) {
        fetch('/bridge/delete_file/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ file_id: file.id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadFolderContents(currentFolderId, currentPath);
            } else {
                alert(data.message);
            }
        });
    }
}

function showFileInfo(file) {
    fetch(`/bridge/get_file_info/?path=${encodeURIComponent(file.id)}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const info = data.file_info;
                const infoWindow = document.createElement('div');
                infoWindow.className = 'info-window';
                infoWindow.innerHTML = `
                    <h3>File Information</h3>
                    <p><strong>Name:</strong> ${info.name}</p>
                    <p><strong>Type:</strong> ${info.file_type}</p>
                    <p><strong>Size:</strong> ${formatFileSize(info.size)}</p>
                    <p><strong>Created:</strong> ${formatDate(info.created)}</p>
                    <p><strong>Modified:</strong> ${formatDate(info.modified)}</p>
                    <p><strong>Full Path:</strong> ${info.full_path}</p>
                    <button id="closeInfoWindow">Close</button>
                `;
                document.body.appendChild(infoWindow);

                document.getElementById('closeInfoWindow').onclick = () => {
                    document.body.removeChild(infoWindow);
                };
            } else {
                alert(data.message);
            }
        });
}

function openFile(file) {
    const fileExtension = getFileExtension(file.name).toLowerCase();
    if (file.is_dir) {
        loadFolderContents(currentFolderId, file.id);
    } else if (fileExtension === 'pdf') {
        const fileUrl = `/bridge/file_action/?action=open&path=${encodeURIComponent(file.id)}`;
        window.open(fileUrl, '_blank');
    } else {
        fetch(`/bridge/file_action/?action=open&path=${encodeURIComponent(file.id)}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'error') {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while trying to open the file.');
            });
    }
}

function goBack() {
    if (currentPath) {
        const parentPath = currentPath.split('/').slice(0, -1).join('/');
        loadFolderContents(currentFolderId, parentPath || null);
    } else {
        window.location.href = '/bridge/';
    }
}

// Остальной код остается без изменений

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    fileList = document.getElementById('fileList');
    viewMode = document.getElementById('viewMode');
    sortBy = document.getElementById('sortBy');
    searchInput = document.getElementById('searchInput');
    contextMenu = document.getElementById('contextMenu');

    if (fileList) {
        fileList.className = 'file-list grid-view';
    }

    if (viewMode) {
        viewMode.value = 'grid';
        viewMode.addEventListener('change', () => {
            if (fileList) {
                fileList.className = `file-list ${viewMode.value}-view`;
            }
        });
    }

    if (sortBy) {
        sortBy.value = 'name';
        sortBy.addEventListener('change', () => {
            sortFiles(sortBy.value);
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();
            Array.from(fileList.children).forEach(file => {
                const fileName = file.querySelector('.file-name').textContent.toLowerCase();
                file.style.display = fileName.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    document.addEventListener('click', (e) => {
        if (!contextMenu.contains(e.target) && !e.target.closest('.file-item')) {
            contextMenu.style.display = 'none';
        }
    });

    const currentPathElement = document.getElementById('currentPath');
    if (currentPathElement) {
        const folderId = currentPathElement.dataset.folderId;
        if (folderId) {
            loadFolderContents(folderId);
        }
    }

    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.addEventListener('click', goBack);
    }
});