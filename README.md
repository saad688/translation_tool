# Urdu Translation Tool

AI-powered document translation tool that transforms English words in .docx files to include Urdu translations.

## Project Structure

```
translation_tool/
├── backend/                 # Flask API (Deploy to Render)
│   ├── app.py              # Main Flask application with CORS
│   ├── backend.py          # Translation logic using Gemini API
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render deployment config
│   └── Procfile           # Gunicorn command
│
├── frontend/               # React SPA (Deploy to Cloudflare Pages)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   ├── App.jsx        # Main application
│   │   └── App.css        # Global styles
│   ├── .env.development   # Local API URL
│   ├── .env.production    # Production API URL (UPDATE THIS!)
│   └── wrangler.json      # Cloudflare config
│
└── gui.py                 # Desktop app (optional, still works)
```

## Quick Start (Local Development)

### 1. Start Backend
```powershell
cd translation_tool
pip install -r requirements.txt
python app.py
```
Backend runs at: http://localhost:5000

### 2. Start Frontend
```powershell
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

## Deployment

### Backend → Render

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repo
5. Render will auto-detect `render.yaml` and deploy

**Environment Variables (set in Render dashboard):**
- `ALLOWED_ORIGINS`: Your Cloudflare Pages URL (e.g., `https://urdu-translation.pages.dev`)
- `GEMINI_API_KEY`: Your Google Gemini API key

### Frontend → Cloudflare Pages

1. Update `frontend/.env.production`:
   ```
   VITE_API_URL=https://your-app-name.onrender.com/api
   ```

2. Deploy via Cloudflare Dashboard:
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages
   - Create new project → Connect to Git
   - Set build command: `npm run build`
   - Set output directory: `dist`
   - Set root directory: `frontend`

Or via Wrangler CLI:
```powershell
cd frontend
npm run build
npx wrangler pages deploy dist
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/process` | POST | Process .docx file (requires translation_type and file) |
| `/api/download/<filename>` | GET | Download translated file |

## Tech Stack

- **Backend**: Flask, Flask-CORS, Gunicorn, Google Gemini API
- **Frontend**: React 18, Vite, CSS3
- **Deployment**: Render (backend), Cloudflare Pages (frontend)
