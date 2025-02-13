import type { Message } from '../types';

const article = document.querySelector('article');

// Initialize content script
console.log('Nagging content script loaded');

// `document.querySelector` may return null if the selector doesn't match anything.
if (article) {
  const text = article.textContent ?? '';
  const wordMatchRegExp = /[^\s]+/g; // Regular expression
  const words = text.matchAll(wordMatchRegExp);
  // matchAll returns an iterator, convert to array to get word count
  const wordCount = [...words].length;
  const readingTime = Math.round(wordCount / 200);
  const badge = document.createElement('p');
  // Use the same styling as the publish information in an article's header
  badge.classList.add('color-secondary-text', 'type--caption');
  badge.textContent = `⏱️ ${readingTime} min read`;

  // Support for API reference docs
  const heading = article.querySelector('h1');
  // Support for article docs with date
  const date = article.querySelector('time')?.parentNode as HTMLElement;

  const inputContainer = document.createElement('div');
  const textInput = document.createElement('input');
  textInput.type = 'text';
  textInput.placeholder = 'Type here for suggestions...';
  textInput.classList.add('suggestion-input');

  inputContainer.appendChild(textInput);
  (date ?? heading)?.insertAdjacentElement('afterend', inputContainer);

  (date ?? heading)?.insertAdjacentElement('afterend', badge);
}

// Track active input element
let activeInput: HTMLInputElement | HTMLTextAreaElement | null = null;
let debounceTimer: number | null = null;

// // Listen for input events
document.addEventListener('focusin', (event) => {
  const target = event.target as HTMLElement;
  if (
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement
  ) {
    console.log('Input focused:', target);
    activeInput = target;
  }
});

document.addEventListener('focusout', () => {
  console.log('Input blurred');
  activeInput = null;
});

// Handle text input with debouncing
function handleInput() {
  if (!activeInput) {
    console.log('No active input');
    return;
  }
  const text = activeInput.value;
  const cursorPosition = activeInput.selectionStart || 0;
  console.log('Sending request:', { text, cursorPosition });
  // Send message to background script
  const message: Message = {
    type: 'GET_SUGGESTION',
    data: {
      text,
      cursorPosition,
    },
  };

  chrome.runtime
    .sendMessage(message)
    .then((response) => {
      console.log('Suggestion received:', response);
      if (response && activeInput) {
        activeInput.value = activeInput.value + response;
      }
    })
    .catch((error) => {
      console.error('Error getting suggestion:', error);
    });
}

// Debounce input handling
document.addEventListener('input', () => {
  if (debounceTimer) {
    window.clearTimeout(debounceTimer);
  }
  debounceTimer = window.setTimeout(handleInput, 500); // 500ms debounce
});
