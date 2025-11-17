import PropTypes from "prop-types";
import "./SummarySection.scss";

const SummarySection = ({ conversationId, summary, onSummarize }) => {
  return (
    <div className="summary-section">
      <div className="summary-section__actions">
        <button
          className="summary-section__button"
          onClick={() => onSummarize(conversationId)}
        >
          Summarize Conversation
        </button>
      </div>

      {summary && (
        <div className="summary-section__box">
          <h4 className="summary-section__title">Conversation Summary</h4>
          <p className="summary-section__text">{summary.summary}</p>
          <div className="summary-section__highlights">
            {summary.highlights.map((highlight, hIdx) => (
              <span key={hIdx} className="summary-section__highlight">
                #{highlight}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

SummarySection.propTypes = {
  conversationId: PropTypes.string.isRequired,
  summary: PropTypes.shape({
    summary: PropTypes.string.isRequired,
    highlights: PropTypes.arrayOf(PropTypes.string).isRequired,
  }),
  onSummarize: PropTypes.func.isRequired,
};

export default SummarySection;
