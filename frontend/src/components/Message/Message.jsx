import PropTypes from "prop-types";
import "./Message.scss";

const Message = ({ message }) => {
  const sender = message.sender
    ? message.sender.toUpperCase()
    : message.participant || "UNKNOWN";

  // Determine if this is a patient or provider message
  const isProvider =
    sender.includes("DR_") ||
    sender.includes("DOCTOR") ||
    sender.includes("PHYSICIAN");
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
    sender: PropTypes.string,
    participant: PropTypes.string,
    timestamp: PropTypes.string,
    text: PropTypes.string,
    snippet: PropTypes.string,
  }).isRequired,
};

export default Message;
