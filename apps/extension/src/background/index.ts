console.log('*****7777*****');
import browser from 'webextension-polyfill';
import type { Message, SuggestionResponse } from '../types';

console.log('*****Background script loaded*****');
const API_BASE_URL = 'http://localhost:8000/api';

// // Handle messages from content script
browser.runtime.onMessage.addListener(async (message: Message) => {
  console.log('Background script received message:', message);
  if (message.type === 'GET_SUGGESTION') {
    try {
      console.log('Sending request to API:', message.data);
      const response = await fetch(`${API_BASE_URL}/suggest`, {
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
        throw new Error(`API request failed: ${response.status} ${errorText}`);
      }
      const data = (await response.json()) as SuggestionResponse;
      console.log('API response:', data);
      return data.suggestion;
    } catch (error) {
      console.error('Error fetching suggestion:', error);
      throw error;
    }
  }
  return null;
});
