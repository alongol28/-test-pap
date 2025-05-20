const chat = document.getElementById('chat');
const form = document.getElementById('input-form');
const userInput = document.getElementById('user-input');

let state = 0;
let formData = {};

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function botSay(text) {
    addMessage(text, 'bot');
}

function nextStep(input) {
    if (state === 0) {
        botSay('Hi! What\'s your name?');
        state = 1;
    } else if (state === 1) {
        formData.name = input;
        botSay('Nice to meet you, ' + input + '! What\'s your email?');
        state = 2;
    } else if (state === 2) {
        formData.email = input;
        botSay('Great. Which date would you like? (YYYY-MM-DD)');
        state = 3;
    } else if (state === 3) {
        formData.date = input;
        botSay('And what time? (HH:MM)');
        state = 4;
    } else if (state === 4) {
        formData.time = input;
        fetch('/schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
            .then(res => res.json())
            .then(data => botSay(data.message));
        state = 5;
    } else {
        botSay('Thanks! Feel free to schedule another meeting by refreshing the page.');
    }
}

form.addEventListener('submit', e => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    userInput.value = '';
    nextStep(text);
});

window.addEventListener('load', () => {
    nextStep();
});
