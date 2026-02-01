import { useState } from 'react';
import PropTypes from 'prop-types';
import './TranslationForm.css';

function TranslationForm({ onSubmit, disabled }) {
    const [translationType, setTranslationType] = useState('basic');
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState('');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            setFile(selectedFile);
            setFileName(selectedFile.name);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (file) {
            onSubmit({ translationType, file });
        }
    };

    return (
        <form className="translation-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="translation_type">
                    <span className="label-icon">⚙️</span>
                    Translation Type
                </label>
                <select
                    id="translation_type"
                    value={translationType}
                    onChange={(e) => setTranslationType(e.target.value)}
                    disabled={disabled}
                    className="translation-select"
                >
                    <option value="basic">Basic Translation</option>
                    <option value="grammar">Translation + Grammar Correction</option>
                </select>
                <small className="help-text">
                    Choose whether to include grammar correction along with translation
                </small>
            </div>

            <div className="form-group">
                <label htmlFor="file">
                    <span className="label-icon">📄</span>
                    Document File (.docx)
                </label>
                <div className="file-upload-wrapper">
                    <input
                        type="file"
                        id="file"
                        accept=".docx"
                        onChange={handleFileChange}
                        required
                        disabled={disabled}
                    />
                    <label htmlFor="file" className="file-upload-label">
                        <span className="file-upload-icon">📎</span>
                        <span className="file-upload-text">Choose a .docx file</span>
                    </label>
                    {fileName && (
                        <div className="file-name active">📄 {fileName}</div>
                    )}
                </div>
            </div>

            <button type="submit" className="submit-btn" disabled={disabled || !file}>
                <span className="btn-text">Start Translation</span>
                <span className="btn-icon">→</span>
            </button>
        </form>
    );
}

TranslationForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    disabled: PropTypes.bool,
};

TranslationForm.defaultProps = {
    disabled: false,
};

export default TranslationForm;
