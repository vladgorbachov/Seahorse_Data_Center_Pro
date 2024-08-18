document.addEventListener('DOMContentLoaded', function() {
    const fileList = document.getElementById('fileList');
    const breadcrumbList = document.getElementById('breadcrumbList');
    const viewMode = document.getElementById('viewMode');
    const sortBy = document.getElementById('sortBy');
    const searchInput = document.getElementById('searchInput');
    const filePreview = document.getElementById('filePreview');

    function loadFolderContents(folderId) {
    fetch(`/deck/get_folder_contents/?folder_id=${folderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayFiles(data.contents);
                updateBreadcrumb(data.current_path);
                document.getElementById('currentPath').value = data.current_path;
            } else {
                alert(data.message);
            }
        });
}

    function displayFiles(files) {
        fileList.innerHTML = '';
        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-icon ${getFileIconClass(file.file_type, file.name)}"></div>
                <div class="file-name">${file.name}</div>
                <div class="file-size">${formatFileSize(file.size)}</div>
                <div class="file-date">${formatDate(file.last_modified)}</div>
            `;
            fileItem.addEventListener('click', () => handleFileClick(file));
            fileList.appendChild(fileItem);
        });
    }

    function getFileIconClass(fileType, fileName) {
        if (fileType === 'folder') return 'folder';
        if (fileType.startsWith('image/')) return 'image';
        if (fileType.startsWith('audio/')) return 'audio';
        if (fileType.startsWith('video/')) return 'video';
        if (fileType === 'application/pdf') return 'pdf';
        if (fileType === 'application/msword' || fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return 'word';
        if (fileType === 'application/vnd.ms-excel' || fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') return 'excel';
        if (fileType === 'application/zip' || fileType === 'application/x-rar-compressed') return 'archive';
        if (fileType.startsWith('text/')) return 'text';

        const extension = fileName.split('.').pop().toLowerCase();
        if (['doc', 'docx'].includes(extension)) return 'word';
        if (['xls', 'xlsx'].includes(extension)) return 'excel';
        if (['zip', 'rar', '7z'].includes(extension)) return 'archive';

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

    function handleFileClick(file) {
        if (file.is_dir) {
            loadFolderContents(file.id);
        } else {
            previewFile(file);
        }
    }

    function previewFile(file) {
        filePreview.innerHTML = `<h3>File Preview</h3><p>${file.name}</p>`;
        // Здесь может быть логика для отображения содержимого файла
    }

    function updateBreadcrumb(path, currentFolderId) {
        const parts = path.split('/').filter(Boolean);
        breadcrumbList.innerHTML = `<li><a href="#" data-folder-id="${currentFolderId}">Root</a></li>`;
        let currentPath = '/';
        parts.forEach((part, index) => {
            currentPath += `${part}/`;
            breadcrumbList.innerHTML += `<li><a href="#" data-folder-id="${index === parts.length - 1 ? currentFolderId : ''}">${part}</a></li>`;
        });

        breadcrumbList.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const folderId = e.target.dataset.folderId;
                if (folderId) {
                    loadFolderContents(folderId);
                }
            });
        });
    }

    viewMode.addEventListener('change', () => {
        fileList.className = `file-list ${viewMode.value}-view`;
    });

    sortBy.addEventListener('change', () => {
        const files = Array.from(fileList.children);
        files.sort((a, b) => {
            const aValue = a.querySelector(`.file-${sortBy.value}`).textContent;
            const bValue = b.querySelector(`.file-${sortBy.value}`).textContent;
            return aValue.localeCompare(bValue, undefined, {numeric: true, sensitivity: 'base'});
        });
        files.forEach(file => fileList.appendChild(file));
    });

    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        Array.from(fileList.children).forEach(file => {
            const fileName = file.querySelector('.file-name').textContent.toLowerCase();
            file.style.display = fileName.includes(searchTerm) ? '' : 'none';
        });
    });
});