import PropTypes from "prop-types";
import { Message, SummarySection } from "../";
import "./ConversationBlock.scss";

const ConversationBlock = ({
  conversationId,
  messages,
  summary,
  onSummarize,
}) => {
  return (
    <div className="conversation-block">
      <h3 className="conversation-block__title">
        Conversation {conversationId}
      </h3>

      <div className="conversation-block__messages">
        {messages.map((msg, idx) => (
          <Message key={idx} message={msg} />
        ))}
      </div>

      <SummarySection
        conversationId={conversationId}
        summary={summary}
        onSummarize={onSummarize}
      />
    </div>
  );
};

ConversationBlock.propTypes = {
  conversationId: PropTypes.string.isRequired,
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      sender: PropTypes.string,
      participant: PropTypes.string,
      timestamp: PropTypes.string,
      text: PropTypes.string,
      snippet: PropTypes.string,
    })
  ).isRequired,
  summary: PropTypes.shape({
    summary: PropTypes.string.isRequired,
    highlights: PropTypes.arrayOf(PropTypes.string).isRequired,
  }),
  onSummarize: PropTypes.func.isRequired,
};

export default ConversationBlock;
