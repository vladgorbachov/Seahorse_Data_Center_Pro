// Глобальные переменные
let fileList, viewMode, sortBy, searchInput, contextMenu;
let currentFolderId;

// Глобальные функции
function loadFolderContents(folderId) {
    currentFolderId = folderId;
    fetch(`/deck/get_folder_contents/?folder_id=${encodeURIComponent(folderId)}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayFiles(data.contents);
                document.getElementById('currentPath').value = data.current_path;
                sortFiles(sortBy.value);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error loading folder contents:', error);
            alert('An error occurred while loading folder contents.');
        });
}

function displayFiles(files) {
    fileList.innerHTML = '';
    files.forEach(file => {
        if (!file || typeof file !== 'object') {
            console.error('Invalid file object:', file);
            return;  // Пропускаем некорректные файлы
        }

        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.dataset.fileId = file.id;
        fileItem.innerHTML = `
            <div class="file-icon ${getFileIconClass(file.file_type, file.name)}"></div>
            <div class="file-name">${file.name || 'Unknown'}</div>
            <div class="file-size">${formatFileSize(file.size || 0)}</div>
            <div class="file-date">${formatDate(file.last_modified || new Date())}</div>
            <div class="file-type" style="display: none;">${getFileExtension(file.name)}</div>
        `;
        fileItem.addEventListener('click', (e) => handleFileClick(e, file));
        fileItem.addEventListener('dblclick', () => handleFileDblClick(file));
        fileItem.addEventListener('contextmenu', (e) => handleContextMenu(e, file));
        fileList.appendChild(fileItem);
    });
}

function getFileIconClass(fileType, fileName) {
    if (!fileType) {
        // Если тип файла не определен, пытаемся определить его по расширению
        const extension = fileName.split('.').pop().toLowerCase();
        if (['doc', 'docx'].includes(extension)) return 'word';
        if (['xls', 'xlsx'].includes(extension)) return 'excel';
        if (['zip', 'rar', '7z'].includes(extension)) return 'archive';
        if (['jpg', 'jpeg', 'png', 'gif'].includes(extension)) return 'image';
        if (['mp3', 'wav', 'ogg'].includes(extension)) return 'audio';
        if (['mp4', 'avi', 'mov'].includes(extension)) return 'video';
        if (extension === 'pdf') return 'pdf';
        if (extension === 'txt') return 'text';
        return 'unknown';
    }

    if (fileType === 'folder') return 'folder';
    if (fileType.startsWith('image/')) return 'image';
    if (fileType.startsWith('audio/')) return 'audio';
    if (fileType.startsWith('video/')) return 'video';
    if (fileType === 'application/pdf') return 'pdf';
    if (fileType === 'application/msword' || fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return 'word';
    if (fileType === 'application/vnd.ms-excel' || fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') return 'excel';
    if (fileType === 'application/zip' || fileType === 'application/x-rar-compressed') return 'archive';
    if (fileType.startsWith('text/')) return 'text';

    return 'unknown';
}

function formatFileSize(size) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let unitIndex = 0;
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    return `${size.toFixed(1)} ${units[unitIndex]}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function getFileExtension(fileName) {
    return fileName.split('.').pop().toLowerCase();
}

function handleFileClick(e, file) {
    // Выделение файла
    const selectedFile = fileList.querySelector('.selected');
    if (selectedFile) {
        selectedFile.classList.remove('selected');
    }
    e.currentTarget.classList.add('selected');
}

function handleFileDblClick(file) {
    if (file.is_dir) {
        loadFolderContents(file.id);
    } else {
        openFile(file);
    }
}

function handleContextMenu(e, file) {
    e.preventDefault();
    const selectedFile = fileList.querySelector('.selected');
    if (selectedFile) {
        selectedFile.classList.remove('selected');
    }
    e.currentTarget.classList.add('selected');

    contextMenu.style.display = 'block';
    contextMenu.style.left = `${e.pageX}px`;
    contextMenu.style.top = `${e.pageY}px`;

    const openFileLink = document.getElementById('openFile');
    const renameFileLink = document.getElementById('renameFile');
    const deleteFileLink = document.getElementById('deleteFile');

    openFileLink.onclick = () => { openFile(file); contextMenu.style.display = 'none'; };
    renameFileLink.onclick = () => { renameFile(file); contextMenu.style.display = 'none'; };
    deleteFileLink.onclick = () => { deleteFile(file); contextMenu.style.display = 'none'; };
}

function openFile(file) {
    if (file.is_dir) {
        loadFolderContents(file.id);
    } else {
        window.open(`/deck/open_file/?path=${encodeURIComponent(file.id)}`, '_blank');
    }
}

function renameFile(file) {
    const newName = prompt('Enter new name:', file.name);
    if (newName && newName !== file.name) {
        fetch('/deck/rename_file/', {
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
                loadFolderContents(currentFolderId);
            } else {
                alert(data.message);
            }
        });
    }
}

function deleteFile(file) {
    if (confirm(`Are you sure you want to delete ${file.name}?`)) {
        fetch('/deck/delete_file/', {
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
                loadFolderContents(currentFolderId);
            } else {
                alert(data.message);
            }
        });
    }
}

function sortFiles(criteria) {
    const files = Array.from(fileList.children);
    files.sort((a, b) => {
        let aValue, bValue;
        if (criteria === 'date') {
            aValue = new Date(a.querySelector('.file-date').textContent);
            bValue = new Date(b.querySelector('.file-date').textContent);
        } else if (criteria === 'size') {
            aValue = parseFloat(a.querySelector('.file-size').textContent);
            bValue = parseFloat(b.querySelector('.file-size').textContent);
        } else if (criteria === 'type') {
            aValue = a.querySelector('.file-type').textContent;
            bValue = b.querySelector('.file-type').textContent;
        } else { // name
            aValue = a.querySelector('.file-name').textContent.toLowerCase();
            bValue = b.querySelector('.file-name').textContent.toLowerCase();
        }

        if (aValue < bValue) return -1;
        if (aValue > bValue) return 1;
        return 0;
    });
    files.forEach(file => fileList.appendChild(file));
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

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
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
        sortBy.value = 'date';
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

    // Закрытие контекстного меню при клике вне его
    document.addEventListener('click', (e) => {
        if (!contextMenu.contains(e.target) && !e.target.closest('.file-item')) {
            contextMenu.style.display = 'none';
        }
    });

    // Инициализация загрузки содержимого папки
    const currentPath = document.getElementById('currentPath');
    if (currentPath) {
        const folderId = currentPath.dataset.folderId;
        if (folderId) {
            loadFolderContents(folderId);
        }
    }
});