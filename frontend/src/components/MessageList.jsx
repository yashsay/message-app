import axios from "axios";
import { useEffect, useState } from "react";
import "./MessageList.scss";

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

      {messages.map((msg, idx) => {
        const sender = msg.sender ? msg.sender.toUpperCase() : "";
        let formattedTime = msg.timestamp;
        if (msg.timestamp) {
          try {
            const dateObj = new Date(msg.timestamp);
            formattedTime = dateObj.toLocaleString(undefined, {
              year: "numeric",
              month: "short",
              day: "2-digit",
              hour: "2-digit",
              minute: "2-digit",
            });
          } catch {}
        }
        return (
          <div key={idx} className={`message ${msg.sender.toLowerCase()}`}>
            <div className="message-header">
              <span className="message-sender">{sender}</span>
              <span className="message-meta">{formattedTime}</span>
            </div>
            <div className="message-text">{msg.text}</div>
          </div>
        );
      })}
    </div>
  );
};

export default MessageList;
