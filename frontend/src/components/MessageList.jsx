import axios from "axios";
import { useEffect, useState } from "react";
import "./MessageList.scss";

const MessageList = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [useAI, setUseAI] = useState(false);
  const [summaries, setSummaries] = useState({}); // ✅ store summaries per conversationId

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = () => {
    axios
      .get("http://localhost:8000/api/messages")
      .then((res) => {
        setMessages(res.data.messages);
        setSummaries({}); // reset summaries on reload
      })
      .catch((err) => console.error("Error:", err));
  };

  const handleSearch = () => {
    if (query.trim() === "") {
      fetchMessages();
      return;
    }

    const url = useAI
      ? "http://localhost:8000/api/semantic-search"
      : "http://localhost:8000/api/search";

    const payload = useAI ? { query, top_k: 5 } : { query };

    axios
      .post(url, payload)
      .then((res) => {
        setMessages(res.data.results);
        setSummaries({});
      })
      .catch((err) => console.error("Search failed:", err));
  };

  const handleSummarize = (conversationId) => {
    axios
      .post("http://localhost:8000/api/summarize", {
        conversationId,
        scope: "all",
      })
      .then((res) =>
        setSummaries((prev) => ({
          ...prev,
          [conversationId]: res.data, // ✅ store by conversationId
        }))
      )
      .catch((err) => console.error("Summarize failed:", err));
  };

  return (
    <div className="message-list">
      {/* Search + toggle */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search messages..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
        <label className="ai-toggle">
          <input
            type="checkbox"
            checked={useAI}
            onChange={(e) => setUseAI(e.target.checked)}
          />
          AI Search
        </label>
      </div>

      {/* Messages */}
      {messages.map((msg, idx) => {
        const sender = msg.sender
          ? msg.sender.toUpperCase()
          : msg.participant || "UNKNOWN";

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
          <div key={idx} className={`message-block`}>
            {/* Single message */}
            <div className={`message ${sender.toLowerCase()}`}>
              <div className="message-header">
                <span className="message-sender">{sender}</span>
                <span className="message-meta">{formattedTime}</span>
              </div>
              <div className="message-text">{msg.text || msg.snippet}</div>
            </div>

            {/* ✅ Summarize button for this conversation */}
            {msg.conversationId && (
              <div className="summary-actions">
                <button
                  className="summarize-btn"
                  onClick={() => handleSummarize(msg.conversationId)}
                >
                  Summarize Conversation
                </button>
              </div>
            )}

            {/* ✅ Summary box for this conversation */}
            {summaries[msg.conversationId] && (
              <div className="summary-box">
                <h4>Conversation Summary</h4>
                <p>{summaries[msg.conversationId].summary}</p>
                <div className="highlights">
                  {summaries[msg.conversationId].highlights.map((h, hIdx) => (
                    <span key={hIdx} className="highlight">
                      #{h}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default MessageList;
