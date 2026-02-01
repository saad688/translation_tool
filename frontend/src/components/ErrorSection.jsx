import PropTypes from 'prop-types';
import './ErrorSection.css';

function ErrorSection({ message, onRetry }) {
    return (
        <div className="error-section">
            <div className="error-message">
                <span className="error-icon">⚠</span>
                <span>{message}</span>
            </div>
            <button className="reset-btn" onClick={onRetry}>
                <span>Try Again</span>
            </button>
        </div>
    );
}

ErrorSection.propTypes = {
    message: PropTypes.string.isRequired,
    onRetry: PropTypes.func.isRequired,
};

export default ErrorSection;
