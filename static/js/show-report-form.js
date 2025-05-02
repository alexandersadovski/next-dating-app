document.addEventListener('DOMContentLoaded', function () {
    const reportButtons = document.querySelectorAll('.btn.btn-report');
    const modalOverlay = document.querySelector('.modal-overlay');
    const modalContent = document.querySelector('.report-modal-content');
    const cancelBtn = document.querySelector('.btn.btn-cancel');
    const userIdField = document.getElementById('report-user-id');

    if (!modalOverlay || !modalContent || !userIdField) {
        console.error('Modal overlay, modal content, or user ID field not found in the DOM.');
        return;
    }

    const openModal = (userId) => {
        if (userId) {
            userIdField.value = userId;
        } else {
            console.warn('User ID is not provided.');
        }

        modalOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        modalContent.classList.remove('slideOut');
        void modalContent.offsetWidth;
        modalContent.classList.add('slideIn');
    };

    const closeModal = () => {
        modalContent.classList.remove('slideIn');
        modalContent.classList.add('slideOut');
        modalContent.addEventListener('animationend', handleAnimationEnd);
    };

    const handleAnimationEnd = (event) => {
        if (event.animationName === 'slideOut') {
            modalOverlay.style.display = 'none';
            document.body.style.overflow = '';
            modalContent.classList.remove('slideOut');
            modalContent.removeEventListener('animationend', handleAnimationEnd);
        }
    };

    reportButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const userId = button.getAttribute('data-user-id');
            if (userId) {
                openModal(userId);
            } else {
                console.warn('data-user-id attribute is missing on the report button.');
                openModal('');
            }
        });
    });

    cancelBtn.addEventListener('click', () => {
        closeModal();
    });
});
