import { useState } from 'react';
import TranslationForm from './components/TranslationForm';
import ProgressIndicator from './components/ProgressIndicator';
import ResultSection from './components/ResultSection';
import ErrorSection from './components/ErrorSection';
import { processFile, downloadFile } from './services/api';
import './App.css';

// State machine states
const STATES = {
  IDLE: 'idle',
  PROCESSING: 'processing',
  SUCCESS: 'success',
  ERROR: 'error',
};

function App() {
  const [state, setState] = useState(STATES.IDLE);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [resultFilename, setResultFilename] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async ({ translationType, file }) => {
    setState(STATES.PROCESSING);
    setProgress(0);
    setProgressMessage('Starting...');

    try {
      const result = await processFile(translationType, file, (prog, msg) => {
        setProgress(prog);
        setProgressMessage(msg);
      });

      if (result.success) {
        setResultFilename(result.filename);
        setState(STATES.SUCCESS);
      } else {
        throw new Error(result.error || 'Processing failed');
      }
    } catch (error) {
      setErrorMessage(error.message || 'An unexpected error occurred');
      setState(STATES.ERROR);
    }
  };

  const handleDownload = (filename) => {
    downloadFile(filename);
  };

  const handleReset = () => {
    setState(STATES.IDLE);
    setProgress(0);
    setProgressMessage('');
    setResultFilename('');
    setErrorMessage('');
  };

  return (
    <div className="container">
      <header className="header">
        <h1>📚 Urdu Translation Helper</h1>
        <p className="subtitle">Transform your documents with AI-powered Urdu translations</p>
      </header>

      <main className="card">
        <TranslationForm
          onSubmit={handleSubmit}
          disabled={state === STATES.PROCESSING}
        />

        {state === STATES.PROCESSING && (
          <ProgressIndicator progress={progress} message={progressMessage} />
        )}

        {state === STATES.SUCCESS && (
          <ResultSection
            filename={resultFilename}
            onDownload={handleDownload}
            onReset={handleReset}
          />
        )}

        {state === STATES.ERROR && (
          <ErrorSection message={errorMessage} onRetry={handleReset} />
        )}
      </main>

      <aside className="info-card">
        <h3>How it works</h3>
        <ol className="info-list">
          <li>
            <span className="step-number">1</span>
            <span>Choose translation type</span>
          </li>
          <li>
            <span className="step-number">2</span>
            <span>Upload your .docx document</span>
          </li>
          <li>
            <span className="step-number">3</span>
            <span>AI identifies English words and adds Urdu translations</span>
          </li>
          <li>
            <span className="step-number">4</span>
            <span>Download your enhanced document</span>
          </li>
        </ol>
      </aside>
    </div>
  );
}

export default App;
