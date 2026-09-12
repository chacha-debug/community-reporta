// ============= FONT SIZE CONTROLS =============
function changeFontSize(delta) {
    let currentSize = parseInt(localStorage.getItem('fontSize') || '16');
    let newSize = Math.min(Math.max(currentSize + delta, 12), 24);
    document.documentElement.style.fontSize = newSize + 'px';
    localStorage.setItem('fontSize', newSize);
    announce(`Font size changed to ${newSize} pixels`);
}

function resetFontSize() {
    document.documentElement.style.fontSize = '';
    localStorage.removeItem('fontSize');
    announce('Font size reset to default');
}

// Load saved font size on page load
if (localStorage.getItem('fontSize')) {
    document.documentElement.style.fontSize = localStorage.getItem('fontSize') + 'px';
}

// ============= TEXT TO SPEECH =============
let currentUtterance = null;

function toggleReadAloud() {
    if (currentUtterance && window.speechSynthesis.speaking) {
        stopReading();
        return;
    }

    const mainContent = document.querySelector('main') || document.body;
    const clone = mainContent.cloneNode(true);

    const removeSelectors = [
        '.accessibility-controls',
        '.accessibility-btn',
        '.menu-toggle',
        'button:not(.submit-btn):not(.location-btn)',
        'script', 'style',
        'nav .nav-menu'
    ];

    removeSelectors.forEach(selector => {
        clone.querySelectorAll(selector).forEach(el => el.remove());
    });

    const text = clone.innerText.trim();
    if (!text) {
        announce('No content to read');
        return;
    }

    currentUtterance = new SpeechSynthesisUtterance(text);
    currentUtterance.lang = 'en-ZA';
    currentUtterance.rate = 0.9;
    currentUtterance.pitch = 1;
    currentUtterance.volume = 1;

    currentUtterance.onstart = () => {
        document.getElementById('readAloudBtn').style.display = 'none';
        document.getElementById('stopReadingBtn').style.display = 'flex';
        announce('Reading started');
    };

    currentUtterance.onend = () => {
        document.getElementById('readAloudBtn').style.display = 'flex';
        document.getElementById('stopReadingBtn').style.display = 'none';
        currentUtterance = null;
        announce('Reading finished');
    };

    currentUtterance.onerror = () => {
        document.getElementById('readAloudBtn').style.display = 'flex';
        document.getElementById('stopReadingBtn').style.display = 'none';
        currentUtterance = null;
        announce('Reading stopped due to error');
    };

    window.speechSynthesis.speak(currentUtterance);
}

function stopReading() {
    if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
    }
    currentUtterance = null;
    const readBtn = document.getElementById('readAloudBtn');
    const stopBtn = document.getElementById('stopReadingBtn');
    if (readBtn) readBtn.style.display = 'flex';
    if (stopBtn) stopBtn.style.display = 'none';
    announce('Reading stopped');
}

// ============= SCREEN READER ANNOUNCEMENTS =============
function announce(message) {
    let announcer = document.getElementById('liveAnnouncer');
    if (!announcer) {
        announcer = document.createElement('div');
        announcer.id = 'liveAnnouncer';
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        Object.assign(announcer.style, {
            position: 'absolute', width: '1px', height: '1px',
            padding: '0', margin: '-1px', overflow: 'hidden',
            clip: 'rect(0, 0, 0, 0)', whiteSpace: 'nowrap', border: '0'
        });
        document.body.appendChild(announcer);
    }
    announcer.textContent = message;
    setTimeout(() => { announcer.textContent = ''; }, 3000);
}

// ============= KEYBOARD SHORTCUTS =============
document.addEventListener('keydown', function (e) {
    if (e.altKey && e.key === 'r') { e.preventDefault(); toggleReadAloud(); }
    if (e.altKey && e.key === '+') { e.preventDefault(); changeFontSize(2); }
    if (e.altKey && e.key === '-') { e.preventDefault(); changeFontSize(-2); }
    if (e.altKey && e.key === '0') { e.preventDefault(); resetFontSize(); }
});