import PropTypes from "prop-types";
import "./Message.scss";

const Message = ({ message }) => {
  const sender = message.sender
    ? message.sender.toUpperCase()
    : message.participant || "UNKNOWN";

  // Determine if this is a patient or provider message
  // Check for provider indicators: "Dr_", "DOCTOR", "PHYSICIAN", "MD", or automated messages
  const isProvider =
    sender.includes("DR_") ||
    sender.includes("DOCTOR") ||
    sender.includes("PHYSICIAN") ||
    sender.includes("MD") ||
    sender.includes("AUTOMATED");
  const messageType = isProvider ? "provider" : "patient";

  let formattedTime = message.timestamp;
  if (message.timestamp) {
    try {
      const dateObj = new Date(message.timestamp);
      formattedTime = dateObj.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      // Keep original timestamp if formatting fails
    }
  }

  return (
    <div className={`message message--${messageType}`}>
      <div className="message__header">
        <span className="message__sender">{sender}</span>
        <span className="message__meta">{formattedTime}</span>
      </div>
      <div className="message__text">{message.text || message.snippet}</div>
    </div>
  );
};

Message.propTypes = {
  message: PropTypes.shape({
    messageId: PropTypes.string,
    messageType: PropTypes.string,
    sender: PropTypes.string,
    participant: PropTypes.string,
    timestamp: PropTypes.string,
    text: PropTypes.string,
    snippet: PropTypes.string,
    purpose: PropTypes.string,
    participants: PropTypes.arrayOf(PropTypes.string),
    hasAttachments: PropTypes.bool,
    seen: PropTypes.bool,
  }).isRequired,
};

export default Message;
