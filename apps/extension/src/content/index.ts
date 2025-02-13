import type { Message } from '../types';

let suggestionOverlay: HTMLDivElement;

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
  inputContainer.classList.add('suggestion-container');
  const textInput = document.createElement('input');
  textInput.type = 'text';
  textInput.placeholder = 'Type here for suggestions...';
  textInput.classList.add('suggestion-input');

  suggestionOverlay = document.createElement('div');
  suggestionOverlay.classList.add('suggestion-overlay');
  suggestionOverlay.style.display = 'none';

  inputContainer.appendChild(textInput);
  inputContainer.appendChild(suggestionOverlay);
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
  hideSuggestion();
});

function insertSuggestion(
  originalText: string,
  suggestion: string,
  cursorPosition: number,
) {
  if (!activeInput) return;

  const beforeCursor = originalText.slice(0, cursorPosition);
  const afterCursor = originalText.slice(cursorPosition);
  activeInput.value = beforeCursor + suggestion + afterCursor;

  // Place cursor after the inserted suggestion
  const newPosition = cursorPosition + suggestion.length;
  activeInput.setSelectionRange(newPosition, newPosition);
  activeInput.focus();
}

let currentSuggestion = '';

function showSuggestion(suggestion: string, cursorPosition: number) {
  if (!activeInput) return;

  currentSuggestion = suggestion;
  const textWidth = measureText(activeInput.value.slice(0, cursorPosition));

  suggestionOverlay.textContent = suggestion;
  suggestionOverlay.style.display = 'block';
  suggestionOverlay.style.left = `${textWidth}px`;
}

function hideSuggestion() {
  suggestionOverlay.style.display = 'none';
  currentSuggestion = '';
}

function measureText(text: string): number {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  if (!context || !activeInput) return 0;

  const computedStyle = window.getComputedStyle(activeInput);
  context.font = `${computedStyle.fontSize} ${computedStyle.fontFamily}`;
  return context.measureText(text).width;
}

function handleInput() {
  if (!activeInput) {
    console.log('No active input');
    return;
  }

  const text = activeInput.value;
  const cursorPosition = activeInput.selectionStart || 0;

  console.log('Requesting suggestion:', { text, cursorPosition });
  hideSuggestion();

  const message: Message = {
    type: 'GET_SUGGESTION',
    data: {
      text,
      cursorPosition,
    },
  };

  chrome.runtime.sendMessage(message, (response) => {
    console.log('Received response:', response);

    if (response?.error) {
      console.error('Suggestion error:', response.error);
      return;
    }

    if (response?.suggestion) {
      showSuggestion(response.suggestion, cursorPosition);
    } else {
      console.log('No suggestion received');
    }
  });
}

// Debounce input handling
document.addEventListener('input', () => {
  if (debounceTimer) {
    window.clearTimeout(debounceTimer);
  }
  debounceTimer = window.setTimeout(handleInput, 1000); // 1000ms debounce
});

// Update tab key handler to include right arrow
document.addEventListener('keydown', (event) => {
  if (
    (event.key === 'Tab' || event.key === 'ArrowRight') &&
    currentSuggestion &&
    activeInput
  ) {
    event.preventDefault();
    const cursorPosition = activeInput.selectionStart || 0;
    insertSuggestion(activeInput.value, currentSuggestion, cursorPosition);
    hideSuggestion();
  }
});
