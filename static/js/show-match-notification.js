document.addEventListener('DOMContentLoaded', () => {
    const matchModal = document.getElementById('match-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const matchNameSpan = document.getElementById('match-name');
    const body = document.body;
    const nextUrl = matchModal?.dataset.nextUrl;

    function openModal() {
        matchNameSpan.textContent = matchModal.dataset.name;
        matchModal.style.display = 'flex';
        void matchModal.offsetWidth;
        matchModal.classList.remove('hide');
        matchModal.classList.add('show');
        body.classList.add('no-scroll');
    }

    function closeModalAndNavigate() {
        matchModal.classList.remove('show');
        matchModal.classList.add('hide');
        body.classList.remove('no-scroll');
    }

    closeModalBtn?.addEventListener('click', () => {
        closeModalAndNavigate();
    });

    matchModal?.addEventListener('animationend', (event) => {
        if (event.animationName === 'slideOut') {
            matchModal.style.display = 'none';
            matchModal.classList.remove('hide');

            if (nextUrl) {
                window.location.href = nextUrl;
            }
        }
    });

    if (matchModal?.dataset.name) {
        openModal();
    }
});
