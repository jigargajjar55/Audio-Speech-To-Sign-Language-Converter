// Enhanced webkitSpeechRecognition with better error handling and UI feedback
function record() {
    const micButton = document.getElementById('micButton');
    const statusDisplay = document.getElementById('statusDisplay');
    const speechToText = document.getElementById('speechToText');

    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window)) {
        statusDisplay.textContent = "Speech recognition not supported in your browser";
        statusDisplay.style.color = "var(--error-color)";
        if (typeof showToast === 'function') showToast('Speech recognition not supported in your browser', 'error');
        return;
    }

    // Toggle recording state
    if (micButton.classList.contains('recording')) {
        // Stop recording
        micButton.classList.remove('recording');
        micButton.innerHTML = '<i class="fas fa-microphone"></i>';
        statusDisplay.textContent = "Recording stopped";
        statusDisplay.style.color = "var(--accent-color)";
        return;
    }

    // Start recording
    micButton.classList.add('recording');
    micButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
    statusDisplay.textContent = "Listening... Speak now";
    statusDisplay.style.color = "var(--accent-color)";

    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        speechToText.value = transcript;

        if (event.results[0].isFinal) {
            micButton.classList.remove('recording');
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            statusDisplay.textContent = "Speech recognized: " + transcript;
            statusDisplay.style.color = "var(--accent-color)";
        }
    };

    recognition.onerror = function(event) {
        micButton.classList.remove('recording');
        micButton.innerHTML = '<i class="fas fa-microphone"></i>';
        statusDisplay.textContent = "Error: " + event.error;
        statusDisplay.style.color = "var(--error-color)";

        // Auto-retry for common errors
        if (event.error === 'not-allowed') {
            setTimeout(() => {
                statusDisplay.textContent = "Please allow microphone access and try again";
                if (typeof showToast === 'function') showToast('Please allow microphone access and try again', 'error');
            }, 2000);
        }
    };

    recognition.onend = function() {
        if (micButton.classList.contains('recording')) {
            micButton.classList.remove('recording');
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            statusDisplay.textContent = "Recording ended";
            statusDisplay.style.color = "var(--text-secondary)";
        }
    };

    recognition.start();
}

// Enhanced video playback for stitched seamless videos
let isPlaying = false;

function play() {
    const videoPlayer = document.getElementById('videoPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const statusDisplay = document.getElementById('statusDisplay');
    const wordList = document.getElementById('wordList');
    const words = wordList ? wordList.getElementsByClassName('word-item') : [];

    // UI HCD Updates
    const videoEmptyState = document.getElementById('videoEmptyState');
    if (videoEmptyState) videoEmptyState.style.display = 'none';
    videoPlayer.style.display = 'block';

    // Highlight all words to show they are in the video
    for (let i = 0; i < words.length; i++) {
        words[i].classList.add('active');
    }

    if (!window.djangoContext || !window.djangoContext.stitched_video_path) {
        statusDisplay.textContent = "No stitched video available to animate";
        statusDisplay.style.color = "var(--error-color)";
        if (typeof showToast === 'function') showToast('No stitched video available', 'warning');
        return;
    }

    statusDisplay.textContent = "Playing animation...";
    statusDisplay.style.color = "var(--accent-color)";
    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
    isPlaying = true;

    videoPlayer.src = window.djangoContext.stitched_video_path;
    videoPlayer.load();
    
    videoPlayer.play().catch(error => {
        console.error("Video play error:", error);
        statusDisplay.textContent = "Error playing video: " + error.message;
        statusDisplay.style.color = "var(--error-color)";
    });

    videoPlayer.onended = function() {
        isPlaying = false;
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        statusDisplay.textContent = "Animation complete!";
        statusDisplay.style.color = "var(--accent-color)";
        
        for (let i = 0; i < words.length; i++) {
            words[i].classList.remove('active');
        }

        // Restore Empty State
        if (videoEmptyState) videoEmptyState.style.display = 'flex';
        videoPlayer.style.display = 'none';
    };
}

function playPause() {
    const videoPlayer = document.getElementById('videoPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const statusDisplay = document.getElementById('statusDisplay');

    if (videoPlayer.paused) {
        if (videoPlayer.src && videoPlayer.currentTime > 0) {
            // Continue
            videoPlayer.play().catch(error => {
                console.error("Play error:", error);
                statusDisplay.textContent = "Error: " + error.message;
                statusDisplay.style.color = "var(--error-color)";
            });
            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
            statusDisplay.textContent = "Playing...";
            statusDisplay.style.color = "var(--accent-color)";
            isPlaying = true;
        } else if (window.djangoContext && window.djangoContext.stitched_video_path) {
            play();
        } else {
            statusDisplay.textContent = "Please enter text first";
            statusDisplay.style.color = "var(--error-color)";
            if (typeof showToast === 'function') showToast('Please enter text first', 'warning');
        }
    } else {
        videoPlayer.pause();
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        statusDisplay.textContent = "Paused";
        statusDisplay.style.color = "var(--text-secondary)";
        isPlaying = false;
    }
}

function stopVideo() {
    const videoPlayer = document.getElementById('videoPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const statusDisplay = document.getElementById('statusDisplay');
    const wordList = document.getElementById('wordList');
    const words = wordList ? wordList.getElementsByClassName('word-item') : [];

    videoPlayer.pause();
    videoPlayer.currentTime = 0;
    videoPlayer.src = "";

    playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
    statusDisplay.textContent = "Stopped";
    statusDisplay.style.color = "var(--text-secondary)";
    isPlaying = false;
    
    // Restore Empty State
    const videoEmptyState = document.getElementById('videoEmptyState');
    if (videoEmptyState) videoEmptyState.style.display = 'flex';
    videoPlayer.style.display = 'none';

    // Reset word highlighting
    for (let i = 0; i < words.length; i++) {
        words[i].classList.remove('active');
    }
}

function toggleFullscreen() {
    const videoPlayer = document.getElementById('videoPlayer');

    if (!document.fullscreenElement) {
        if (videoPlayer.requestFullscreen) {
            videoPlayer.requestFullscreen().catch(err => {
                console.error("Error attempting to enable fullscreen:", err);
            });
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Auto-focus on text input when page loads
document.addEventListener('DOMContentLoaded', function() {
    const speechToText = document.getElementById('speechToText');
    if (speechToText) {
        speechToText.focus();
    }

    // Add fade-in animation to all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Autoplay if we just rendered a stitched video
    if (window.djangoContext && window.djangoContext.stitched_video_path) {
        play();
    }
});

// Handle form submission with better feedback
document.querySelector('form').addEventListener('submit', function(e) {
    const statusDisplay = document.getElementById('statusDisplay');
    const textInput = document.getElementById('speechToText');
    const submitBtn = this.querySelector('button[type="submit"]');
    const spinner = document.getElementById('convertSpinner');
    const icon = document.getElementById('convertIcon');
    const text = document.getElementById('convertText');

    if (!textInput.value.trim()) {
        e.preventDefault();
        statusDisplay.textContent = "Please enter some text to convert";
        statusDisplay.style.color = "var(--error-color)";
        if (typeof showToast === 'function') showToast('Please enter some text to convert', 'error');
        textInput.focus();
    } else {
        // Show loading state
        if (spinner) spinner.style.display = 'inline-block';
        if (icon) icon.style.display = 'none';
        if (text) text.textContent = 'Processing...';
        
        submitBtn.style.opacity = '0.8';
        submitBtn.style.cursor = 'not-allowed';
        
        statusDisplay.textContent = "Converting text to sign language...";
        statusDisplay.style.color = "var(--accent-color)";
        if (typeof showToast === 'function') showToast('Converting text to sign language...', 'info');
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === ' ') {
        e.preventDefault();
        playPause();
    } else if (e.key === 'Escape') {
        stopVideo();
    }
});
