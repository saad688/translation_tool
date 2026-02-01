import PropTypes from 'prop-types';
import './ResultSection.css';

function ResultSection({ filename, onDownload, onReset }) {
    return (
        <div className="result-section">
            <div className="success-message">
                <span className="success-icon">✓</span>
                <span>Translation complete!</span>
            </div>
            <button className="download-btn" onClick={() => onDownload(filename)}>
                <span>⬇ Download Translated Document</span>
            </button>
            <button className="reset-btn" onClick={onReset}>
                <span>Process Another File</span>
            </button>
        </div>
    );
}

ResultSection.propTypes = {
    filename: PropTypes.string.isRequired,
    onDownload: PropTypes.func.isRequired,
    onReset: PropTypes.func.isRequired,
};

export default ResultSection;
