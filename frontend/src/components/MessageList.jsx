import { useEffect, useState } from "react";
import { useMessages, useSearch, useSummarize } from "../hooks";
import { ConversationBlock, SearchBar } from "./";
import "./MessageList.scss";

const MessageList = () => {
  const [query, setQuery] = useState("");
  const [useAI, setUseAI] = useState(false);
  const [summaries, setSummaries] = useState({});
  const [displayMessages, setDisplayMessages] = useState([]);

  const { messages, fetchMessages } = useMessages();
  const { searchMessages } = useSearch();
  const { summarizeConversation } = useSummarize();

  useEffect(() => {
    fetchMessages();
  }, [fetchMessages]);

  useEffect(() => {
    setDisplayMessages(messages);
  }, [messages]);

  const handleSearch = async () => {
    if (query.trim() === "") {
      setDisplayMessages(messages);
      setSummaries({});
      return;
    }

    try {
      const results = await searchMessages(query, useAI);
      setDisplayMessages(results);
      setSummaries({});
    } catch (err) {
      console.error("Search failed:", err);
    }
  };

  const handleSummarize = async (conversationId) => {
    try {
      const summary = await summarizeConversation(conversationId);
      setSummaries((prev) => ({
        ...prev,
        [conversationId]: summary,
      }));
    } catch (err) {
      console.error("Summarize failed:", err);
    }
  };

  // Group messages by conversationId
  const groupedMessages = displayMessages.reduce((acc, msg) => {
    const cid = msg.conversationId || "unknown";
    if (!acc[cid]) acc[cid] = [];
    acc[cid].push(msg);
    return acc;
  }, {});

  return (
    <div className="message-list">
      <SearchBar
        query={query}
        onQueryChange={setQuery}
        onSearch={handleSearch}
        useAI={useAI}
        onToggleAI={setUseAI}
      />

      <div className="message-list__conversations">
        {Object.entries(groupedMessages).map(([conversationId, convMsgs]) => (
          <ConversationBlock
            key={conversationId}
            conversationId={conversationId}
            messages={convMsgs}
            summary={summaries[conversationId]}
            onSummarize={handleSummarize}
          />
        ))}
      </div>
    </div>
  );
};

export default MessageList;
