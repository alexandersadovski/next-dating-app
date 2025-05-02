// **API Module**
const api = {
    /**
     * Fetches messages for a specific chat.
     * @param {string} chatId - The ID of the chat.
     * @returns {Promise<string>} - The HTML content of the messages.
     */
    fetchMessages: async (chatId) => {
        const response = await fetch(`/dashboard/chats/${chatId}/messages/`, {
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        });
        if (!response.ok) throw new Error('Failed to load messages.');
        return response.text();
    },

    /**
     * Sends a message within a chat.
     * @param {FormData} formData - The form data containing the message and CSRF token.
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    sendMessage: async (formData) => {
        // Extract and validate CSRF token
        const csrfToken = formData.get('csrfmiddlewaretoken');
        const csrfTokenString = typeof csrfToken === 'string' ? csrfToken : '';

        const response = await fetch('/dashboard/chats/send-message/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfTokenString,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });
        if (!response.ok) throw new Error('Failed to send message.');
        return response.json();
    },

    /**
     * Deletes a specific chat.
     * @param {string} chatId - The ID of the chat to delete.
     * @param {string} csrfToken - The CSRF token for the request.
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    deleteChat: async (chatId, csrfToken) => {
        const response = await fetch(`/dashboard/chats/${chatId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        });
        if (!response.ok) throw new Error('Failed to delete chat.');
        return response.json();
    }
};

// **Main Script**
document.addEventListener('DOMContentLoaded', () => {
    // **Variables and DOM Elements**
    const chatLinks = document.querySelectorAll('.chat-link');
    const currentChat = document.getElementById('current-chat');
    let currentChatId = null;

    const deleteButtons = document.querySelectorAll('.chat-delete');
    const modal = document.getElementById('delete-confirmation-modal');
    const cancelDeleteButton = document.getElementById('cancel-delete-button');
    const deleteForm = modal.querySelector('form');
    let chatIdToDelete = null;

    // **Helper Functions**

    /**
     * Hides the delete confirmation modal and resets the chatIdToDelete.
     */
    const hideModal = () => {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        chatIdToDelete = null;
    };

    /**
     * Displays the delete confirmation modal for a specific chat.
     * @param {string} chatId - The ID of the chat to delete.
     */
    const showModal = (chatId) => {
        chatIdToDelete = chatId;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    };

    /**
     * Fetches and displays the messages for a specific chat.
     * @param {string} chatId - The ID of the chat to load.
     */
    const loadChat = async (chatId) => {
        try {
            currentChat.innerHTML = await api.fetchMessages(chatId);
            scrollToLatestMessage();
            currentChatId = chatId;
            attachSendMessageHandler();
        } catch (error) {
            currentChat.innerHTML = `<p>Error: ${error.message}</p>`;
            console.error('Error loading chat:', error);
        }
    };

    /**
     * Attaches the sendMessage event handler to the send message form.
     */
    const attachSendMessageHandler = () => {
        const form = currentChat.querySelector('#send-message-form');
        if (form) {
            form.addEventListener('submit', sendMessage);
        }
    };

    /**
     * Sends a message in the current chat.
     * @param {Event} event - The submit event.
     * @property message_html - HTML to render.
     */
    const sendMessage = async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const formData = new FormData(form);

        try {
            const data = await api.sendMessage(formData);

            if (data.error) {
                alert('Error sending message.');
                console.error('Form errors:', data.error);
            } else {
                appendMessage(data.message_html);
                form.reset();
                scrollToLatestMessage();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while sending the message.');
        }
    };

    /**
     * Appends a new message to the chat messages container.
     * @param {string} messageHtml - The HTML of the message to append.
     */
    const appendMessage = (messageHtml) => {
        const messages = currentChat.querySelector('.chat-messages');
        if (messages) {
            messages.insertAdjacentHTML('beforeend', messageHtml);
        }
    };

    /**
     * Scrolls the chat messages container to the latest message.
     */
    const scrollToLatestMessage = () => {
        const messages = currentChat.querySelector('.chat-messages');
        if (messages) {
            messages.scrollTop = messages.scrollHeight;
        }
    };

    /**
     * Deletes a chat with the given chatId.
     * @param {string} chatId - The ID of the chat to delete.
     */
    const deleteChat = async (chatId) => {
        const csrfToken = deleteForm.querySelector('input[name="csrfmiddlewaretoken"]').value;

        try {
            const data = await api.deleteChat(chatId, csrfToken);

            if (data.success) {
                removeChatFromDOM(chatId);
                resetCurrentChatIfDeleted(chatId);

                /**
                 * @property {boolean} is_conversations
                 */
                if (data.is_conversations === false) {
                    const contentElement = document.querySelector('.content');
                    const divElement = document.createElement('div');
                    const pElement = document.createElement('p');

                    divElement.classList.add('no-chats');
                    pElement.textContent = 'No chats available.';
                    divElement.appendChild(pElement);

                    contentElement.innerHTML = '';
                    contentElement.appendChild(divElement);
                }
            } else {
                alert('Error deleting chat.');
            }
        } catch (error) {
            console.error('Error deleting chat:', error);
            alert('An error occurred while deleting the chat.');
        }
    };

    /**
     * Removes the chat element from the DOM.
     * @param {string} chatId - The ID of the chat to remove.
     */
    const removeChatFromDOM = (chatId) => {
        const chatItem = document.querySelector(`.chat-delete[data-chat-id="${chatId}"]`)
            ?.closest('.chat-link');
        if (chatItem) {
            chatItem.remove();
        }
    };

    /**
     * Resets the current chat display if the deleted chat was active.
     * @param {string} chatId - The ID of the chat that was deleted.
     */
    const resetCurrentChatIfDeleted = (chatId) => {
        if (currentChatId === chatId) {
            currentChat.innerHTML = '<p>Select a chat to view messages.</p>';
            currentChatId = null;
        }
    };

    // **Event Listeners**

    // Handle clicking on chat links to load chats
    chatLinks.forEach(link => {
        link.addEventListener('click', async (event) => {
            event.preventDefault();
            const chatId = link.dataset.chatId;
            try {
                await loadChat(chatId);
                console.log('Chat loaded successfully.');
            } catch (error) {
                console.error('Error loading chat:', error);
            }
        });
    });

    // Automatically load a new chat if present
    const newChatElement = document.getElementById('new-chat');
    const newChatId = newChatElement?.dataset.chatId;

    if (newChatElement && newChatId) {
        loadChat(newChatId)
            .then(() => console.log('Chat loaded successfully.'))
            .catch(error => console.error('Error loading chat:', error));
    }

    // Handle delete button clicks to show the confirmation modal
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
            const chatId = button.dataset.chatId;
            showModal(chatId);
        });
    });

    // Handle form submission for deleting a chat
    deleteForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (chatIdToDelete) {
            await deleteChat(chatIdToDelete);
            hideModal();
        }
    });

    // Handle cancel button click in the modal
    cancelDeleteButton.addEventListener('click', hideModal);

    // Handle clicking outside the modal to close it
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            hideModal();
        }
    });
});
