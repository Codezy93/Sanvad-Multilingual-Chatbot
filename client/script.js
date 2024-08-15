document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    let recognition = initSpeechRecognition(); // Declare recognition variable at the top
    let isRecording = false;

    startBtn.addEventListener('click', () => {
        if (!isRecording) {
            recognition.start();
            isRecording = true;
            console.log("Recording started...");
        }
    });

    stopBtn.addEventListener('click', () => {
        if (isRecording) {
            recognition.stop();
            isRecording = false;
            console.log("Recording stopped.");
        }
    });

    recognition.onresult = function(event) {
        const speechToText = event.results[0][0].transcript;
        console.log("You said: ", speechToText);
        sendTextToAPI(speechToText);
    };

    recognition.onend = function() {
        // Reset the recognition object so it can be started again
        recognition = initSpeechRecognition();
        isRecording = false;
    };

    recognition.onerror = function(event) {
        console.error("Speech Recognition Error", event.error);
        recognition = initSpeechRecognition(); // Reset on error
        isRecording = false;
    };
});

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    return recognition;
}

function sendTextToAPI(text) {
    $.ajax({
        url: 'http://127.0.0.1:5000/generate',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ speech: text }), 
        success: function(response) {
            speakText(response.reply);
        },
        error: function(xhr) {
            console.error("Error sending text to API: ", xhr.responseText);
        }
    });
}

function speakText(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.onend = () => {
        console.log("Speech synthesis finished.");
        enableButtons();  // Re-enable buttons after speaking is done
    };

    utterance.onerror = (event) => {
        console.error("Speech Synthesis Error:", event.error);
        enableButtons();  // Re-enable buttons even on error
    };

    disableButtons();  // Disable buttons while speaking

    if (!synth.speaking) {
        synth.speak(utterance);
    } else {
        console.log('Synthesis engine is already speaking.');
    }
}

function disableButtons() {
    document.getElementById('start-btn').disabled = true;
    document.getElementById('stop-btn').disabled = true;
}

function enableButtons() {
    document.getElementById('start-btn').disabled = false;
    document.getElementById('stop-btn').disabled = false;
}