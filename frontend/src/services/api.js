/**
 * API Service for Urdu Translation Tool
 * Handles all communication with the Flask backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Check if the API server is healthy
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
        throw new Error('API server is not healthy');
    }
    return response.json();
}

/**
 * Process a DOCX file for translation
 * @param {string} translationType - Type of translation (basic/grammar)
 * @param {File} file - DOCX file to process
 * @param {Function} onProgress - Progress callback (optional)
 * @returns {Promise<Object>} Processing result with filename
 */
export async function processFile(translationType, file, onProgress) {
    const formData = new FormData();
    formData.append('translation_type', translationType);
    formData.append('file', file);

    // Simulate progress tracking
    if (onProgress) {
        onProgress(10, 'Uploading document...');
    }

    const response = await fetch(`${API_URL}/process`, {
        method: 'POST',
        body: formData,
    });

    if (onProgress) {
        onProgress(30, 'Processing with Gemini AI...');
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Processing failed');
    }

    if (onProgress) {
        onProgress(100, 'Complete!');
    }

    return data;
}

/**
 * Get the download URL for a translated file
 * @param {string} filename - Name of the translated file
 * @returns {string} Download URL
 */
export function getDownloadUrl(filename) {
    return `${API_URL}/download/${encodeURIComponent(filename)}`;
}

/**
 * Download a translated file
 * @param {string} filename - Name of the translated file
 */
export function downloadFile(filename) {
    window.location.href = getDownloadUrl(filename);
}

export default {
    checkHealth,
    processFile,
    getDownloadUrl,
    downloadFile,
};
