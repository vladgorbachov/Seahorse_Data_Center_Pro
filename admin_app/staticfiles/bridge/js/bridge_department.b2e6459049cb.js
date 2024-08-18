document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    const createFolderButton = document.getElementById('createFolderButton');
    const foldersContainer = document.getElementById('foldersContainer');
    const inputWindow = document.querySelector('.input-window');
    const folderNameInput = document.getElementById('folderNameInput');
    const inputSaveButton = document.getElementById('inputSaveButton');
    const inputCloseButton = document.getElementById('inputCloseButton');
    const mainPageButton = document.getElementById('mainPageButton');

    // Добавляем обработчик события для кнопки "Main Page"
    if (mainPageButton) {
        mainPageButton.addEventListener('click', () => {
            console.log('Main Page button clicked');
            window.location.href = 'http://127.0.0.1:8000';
        });
    } else {
        console.error('Main Page button not found');
    }

    createFolderButton.addEventListener('click', () => {
        inputWindow.style.display = 'block';
        folderNameInput.focus();
    });

    inputSaveButton.addEventListener('click', () => {
        const folderName = folderNameInput.value.trim();
        if (folderName) {
            bridge_getMaxFolderIndex().then(maxIndex => {
                const newIndex = maxIndex + 1;
                bridge_saveFolderToServer(newIndex, folderName).then(data => {
                    const folderId = data.id;
                    const folder = document.createElement('div');
                    folder.className = 'folder';
                    folder.textContent = folderName;
                    folder.dataset.index = newIndex;
                    folder.dataset.id = folderId;
                    folder.dataset.url = data.link;  // Установить значение data-url
                    foldersContainer.appendChild(folder);
                    bridge_addFolderEventHandlers(folder);
                    inputWindow.style.display = 'none';
                    folderNameInput.value = ''; // Очистить поле ввода
                });
            });
        }
    });

    inputCloseButton.addEventListener('click', () => {
        inputWindow.style.display = 'none';
        folderNameInput.value = ''; // Очистить поле ввода
    });

    window.onerror = function(message, source, lineno, colno, error) {
        console.error('An error occurred:', message, 'Source:', source, 'Line:', lineno);
    };

    function bridge_addFolderEventHandlers(folder) {
        folder.addEventListener('click', () => {
            const folderId = folder.dataset.id;
            const url = folder.dataset.url;
            console.log('Folder URL:', url);
            if (url && url.startsWith('file://')) {
                window.location.href = `/bridge/bridge_explorer/${folderId}/`;
            } else {
                window.location.href = `/bridge/bridge_folder/${folderId}/`;
            }
        });

        folder.addEventListener('contextmenu', (e) => {
            e.preventDefault();

            const existingMenu = document.querySelector('.context-menu');
            if (existingMenu) {
                document.body.removeChild(existingMenu);
            }

            const menu = document.createElement('div');
            menu.className = 'context-menu dropdown-content';
            menu.innerHTML = `
                <a href="#" class="open">Open</a>
                <a href="#" class="rename">Rename</a>
                <a href="#" class="delete">Delete</a>
                <a href="#" class="add-link">Add Link</a>
            `;
            document.body.appendChild(menu);

            menu.style.left = `${e.pageX}px`;
            menu.style.top = `${e.pageY}px`;
            menu.style.display = 'block';

            const openLink = menu.querySelector('.open');
            const renameLink = menu.querySelector('.rename');
            const deleteLink = menu.querySelector('.delete');
            const addLinkLink = menu.querySelector('.add-link');

            openLink.addEventListener('click', () => {
                const folderId = folder.dataset.id;
                if (folderId) {
                    window.location.href = `/bridge/bridge_folder/${folderId}/`;
                } else {
                    console.error('Folder ID is missing');
                }
                document.body.removeChild(menu);
            });

            renameLink.addEventListener('click', () => {
                const newName = prompt("Enter new folder name:", folder.textContent);
                if (newName) {
                    folder.textContent = newName;
                    bridge_updateFolderOnServer(folder.dataset.id, { name: newName });
                }
                document.body.removeChild(menu);
            });

            deleteLink.addEventListener('click', () => {
                if (foldersContainer.contains(folder)) {
                    foldersContainer.removeChild(folder);
                }
                bridge_deleteFolderFromServer(folder.dataset.id);
                document.body.removeChild(menu);
            });

            addLinkLink.addEventListener('click', () => {
                const linkInput = document.createElement('div');
                linkInput.className = 'link-input';
                linkInput.innerHTML = `
                    <input type="text" placeholder="Enter link" class="link-url">
                    <button class="link-ok">OK</button>
                `;
                folder.appendChild(linkInput);

                const linkUrlInput = linkInput.querySelector('.link-url');
                const linkOkButton = linkInput.querySelector('.link-ok');

                linkOkButton.addEventListener('click', () => {
                    const url = linkUrlInput.value;
                    if (url) {
                        bridge_updateFolderOnServer(folder.dataset.id, { link: url }).then(data => {
                            folder.dataset.url = data.link;  // Установить значение data-url
                            bridge_showAlert('Link added successfully');
                        });
                    }
                    folder.removeChild(linkInput);
                });

                document.body.removeChild(menu);
            });

            document.addEventListener('click', () => {
                if (menu && document.body.contains(menu)) {
                    document.body.removeChild(menu);
                }
            }, { once: true });
        });
    }

    function bridge_getMaxFolderIndex() {
        return fetch('/bridge/bridge_get_max_folder_index/')
            .then(response => response.json())
            .then(data => {
                return data.max_index;
            });
    }

    function bridge_saveFolderToServer(index, name) {
        return fetch('/bridge/bridge_add_folder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ index: index, name: name })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Folder saved:', data);
            return data;  // Возвращаем данные папки, включая ссылку
        });
    }

    function bridge_updateFolderOnServer(id, updates) {
        return fetch(`/bridge/bridge_update_folder/${id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(updates)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Folder updated:', data);
            return data;  // Возвращаем обновленные данные папки, включая ссылку
        });
    }

    function bridge_deleteFolderFromServer(id) {
        if (id === undefined) {
            console.error('Folder ID is undefined');
            return;
        }
        fetch(`/bridge/bridge_delete_folder/${id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Folder deleted:', data);
        });
    }

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

    // Добавляем обработчики событий ко всем существующим папкам
    document.querySelectorAll('.folder').forEach(bridge_addFolderEventHandlers);
});

function bridge_openLocalDirectory(url) {
    // Placeholder function, no longer needed since we are handling directory display server-side
}

function bridge_showAlert(message) {
    const alertBox = document.createElement('div');
    alertBox.className = 'alert-box';
    alertBox.textContent = message;
    document.body.appendChild(alertBox);
    setTimeout(() => {
        document.body.removeChild(alertBox);
    }, 3000);
}