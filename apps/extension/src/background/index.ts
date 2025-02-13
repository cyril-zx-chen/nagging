import type { Message, SuggestionResponse } from '../types';

console.log('*****Background script loaded*****');
const API_BASE_URL = 'http://localhost:8000/api';

// // Handle messages from content script
chrome.runtime.onMessage.addListener(
  (message: Message, sender, sendResponse) => {
    console.log('Background script received message:', message);
    if (message.type === 'GET_SUGGESTION') {
      // Handle the API request asynchronously
      (async () => {
        try {
          console.log('Sending request to API:', message.data);
          const response = await fetch(`${API_BASE_URL}/suggest/test`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              text: message.data.text,
              max_tokens: 20,
              temperature: 0.6,
            }),
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error('API error:', response.status, errorText);
            sendResponse({
              error: `API request failed: ${response.status} ${errorText}`,
            });
            return;
          }

          const data = (await response.json()) as SuggestionResponse;
          console.log('API response:', data);
          sendResponse({ suggestion: data.suggestion });
        } catch (error) {
          console.error('Error fetching suggestion:', error);
          sendResponse({ error: 'Fetching error - no suggestion founds' });
        }
      })();

      // Return true to indicate we will send a response asynchronously
      return true;
    }
    return false;
  },
);
