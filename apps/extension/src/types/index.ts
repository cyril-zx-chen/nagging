// Message types for extension communication
export interface GetSuggestionMessage extends Message {
  type: 'GET_SUGGESTION';
  data: {
    text: string;
    cursorPosition: number;
  };
}

export interface Message {
  type: string;
  data: {
    text: string;
    cursorPosition: number;
  };
}

// API response types
export interface SuggestionResponse {
  suggestion: string;
  cached: boolean;
}

// Settings types
export interface Settings {
  temperature: number;
  maxTokens: number;
}
