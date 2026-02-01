import PropTypes from 'prop-types';
import './ProgressIndicator.css';

function ProgressIndicator({ progress, message }) {
    return (
        <div className="progress-section">
            <div className="progress-bar">
                <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                />
            </div>
            <p className="progress-text">{message}</p>
        </div>
    );
}

ProgressIndicator.propTypes = {
    progress: PropTypes.number.isRequired,
    message: PropTypes.string,
};

ProgressIndicator.defaultProps = {
    message: 'Processing your document...',
};

export default ProgressIndicator;
