import axios from "axios";
import { useCallback, useState } from "react";

const API_BASE_URL = "http://localhost:8000/api";

export const useMessages = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMessages = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/messages`);
      setMessages(response.data.messages);
      return response.data.messages;
    } catch (err) {
      setError(err.message || "Failed to fetch messages");
      console.error("Error fetching messages:", err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    messages,
    loading,
    error,
    fetchMessages,
    setMessages,
  };
};

export const useSearch = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchMessages = useCallback(async (query, useAI = false) => {
    if (!query.trim()) {
      throw new Error("Search query cannot be empty");
    }

    setLoading(true);
    setError(null);

    try {
      const url = useAI
        ? `${API_BASE_URL}/semantic-search`
        : `${API_BASE_URL}/search`;
      const payload = useAI ? { query, top_k: 5 } : { query };

      const response = await axios.post(url, payload);
      return response.data.results;
    } catch (err) {
      setError(err.message || "Search failed");
      console.error("Search failed:", err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    searchMessages,
  };
};

export const useSummarize = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const summarizeConversation = useCallback(async (conversationId) => {
    if (!conversationId) {
      throw new Error("Conversation ID is required");
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/summarize`, {
        conversationId,
        scope: "all",
      });
      return response.data;
    } catch (err) {
      setError(err.message || "Summarization failed");
      console.error("Summarize failed:", err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    summarizeConversation,
  };
};
