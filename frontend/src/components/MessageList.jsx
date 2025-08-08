import React, { useEffect, useState } from "react";
import "./MessageList.scss";
import axios from "axios";

const MessageList = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = () => {
    axios
      .get("http://localhost:8000/api/messages")
      .then((res) => setMessages(res.data.messages))
      .catch((err) => console.error("Error:", err));
  };

  const handleSearch = () => {
    if (query.trim() === "") {
      fetchMessages(); // fallback to all
      return;
    }

    axios
      .post("http://localhost:8000/api/search", { query })
      .then((res) => setMessages(res.data.results))
      .catch((err) => console.error("Search failed:", err));
  };

  return (
    <div className="message-list">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search messages..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {messages.map((msg, idx) => (
        <div key={idx} className={`message ${msg.sender.toLowerCase()}`}>
          <div className="message-meta">
            <strong>{msg.sender}</strong> <span>{msg.timestamp}</span>
          </div>
          <div className="message-text">{msg.text}</div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
