# LunatiX Insurance Platform - Setup Guide

This guide will help you set up and run the LunatiX Insurance Platform locally and deploy it to Google Cloud Platform.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Google Cloud Platform account
- Git

## Project Overview

LunatiX is an AI-powered insurance claims management platform with:
- **Document Verification**: Automatically verify claim documents using Vertex AI
- **Claims Tracking**: Real-time status tracking of insurance claims
- **AI Chatbot**: RAG-powered chatbot for insurance questions using Vertex AI
- **Minimalist UI**: Clean, intuitive React interface

## Step 1: Clone and Setup

```bash
cd LunatiX
```

## Step 2: Google Cloud Platform Setup

### 2.1 Create a GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your PROJECT_ID

### 2.2 Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

Or enable manually in the console:
- Vertex AI API
- Cloud Storage API

### 2.3 Create a Service Account

```bash
# Create service account
gcloud iam service-accounts create lunatix-service-account \
    --display-name="LunatiX Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:lunatix-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:lunatix-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create lunatix-key.json \
    --iam-account=lunatix-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

Move the key file to a secure location and note the path.

### 2.4 Create a Cloud Storage Bucket

```bash
gsutil mb -l us-central1 gs://lunatix-documents-YOUR_PROJECT_ID
```

Or create via console:
- Go to Cloud Storage
- Create bucket
- Name: `lunatix-documents-YOUR_PROJECT_ID`
- Location: `us-central1`
- Storage class: Standard

## Step 3: Backend Setup

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Configure Environment

Create a `.env` file in the `backend` directory:

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
GCS_BUCKET_NAME=lunatix-documents-your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/lunatix-key.json

# Database
DATABASE_URL=sqlite:///./insurance.db

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=LunatiX Insurance Platform
DEBUG=True

# Security (change in production)
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 3.5 Initialize Database

```bash
python init_db.py
```

You should see:
```
Creating database tables...
Database tables created successfully!

Tables created:
- claims
- documents
- chat_messages
```

### 3.6 Run Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Step 4: Frontend Setup

### 4.1 Open New Terminal and Navigate to Frontend

```bash
cd frontend
```

### 4.2 Install Dependencies

```bash
npm install
```

### 4.3 Configure Environment

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000
```

### 4.4 Run Frontend Development Server

```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

## Step 5: Test the Application

1. **Open the application**: Navigate to `http://localhost:5173`

2. **Create a test claim**:
   - Click "File a New Claim"
   - Fill in the form
   - Submit

3. **Upload documents**:
   - Go to the claim detail page
   - Select document type
   - Upload a test image or PDF
   - Watch AI verification in action

4. **Test the chatbot**:
   - Click "Help Chat" in navigation
   - Ask questions about insurance terms
   - Try: "What is a deductible?" or "How does the claim process work?"

## Step 6: Development Tips

### Backend Development

- **Auto-reload**: The server auto-reloads when you make changes
- **API docs**: Visit `/docs` for interactive API documentation
- **Database**: SQLite database is stored as `insurance.db`
- **Logs**: Check console for errors and logs

### Frontend Development

- **Hot reload**: Changes auto-refresh in the browser
- **DevTools**: Use React DevTools browser extension
- **API calls**: Check Network tab for API requests

## Common Issues and Solutions

### Issue: Vertex AI Authentication Errors

**Solution**: Ensure your service account key path is correct in `.env`:
```bash
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/lunatix-key.json
```

### Issue: CORS Errors

**Solution**: Make sure frontend URL is in BACKEND_CORS_ORIGINS in backend `.env`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### Issue: Database Errors

**Solution**: Delete `insurance.db` and run `python init_db.py` again

### Issue: npm Install Fails

**Solution**: Clear npm cache and try again:
```bash
npm cache clean --force
npm install
```

## Production Deployment

### Backend Deployment (Cloud Run)

1. **Build Docker image** (create Dockerfile first):
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lunatix-backend
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy lunatix-backend \
  --image gcr.io/YOUR_PROJECT_ID/lunatix-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend Deployment (Firebase Hosting or Cloud Storage)

1. **Build production bundle**:
```bash
npm run build
```

2. **Deploy to Firebase Hosting**:
```bash
firebase init hosting
firebase deploy
```

## Security Considerations

### For Production:

1. **Change SECRET_KEY**: Generate a strong random key
2. **Use PostgreSQL**: Replace SQLite with Cloud SQL PostgreSQL
3. **Enable authentication**: Add user authentication system
4. **Use HTTPS**: Enable SSL/TLS
5. **Restrict CORS**: Only allow production domains
6. **Secure service account**: Use minimal permissions
7. **Environment variables**: Use Secret Manager for sensitive data

## Architecture

```
LunatiX/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   │   └── routes/  # Claims, Documents, Chatbot
│   │   ├── core/        # Config, Database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic & AI
│   ├── init_db.py       # Database initialization
│   └── requirements.txt
│
├── frontend/            # React + TypeScript
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json
│
└── README.md
```

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **AI**: Google Cloud Vertex AI
- **Storage**: Google Cloud Storage

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Next Steps

1. **Add user authentication**: Implement JWT-based auth
2. **Add email notifications**: Notify users of claim status changes
3. **Enhance RAG**: Connect to a vector database for better responses
4. **Add analytics**: Track claim processing metrics
5. **Mobile app**: Build React Native version
6. **Admin dashboard**: Create admin interface for claim management

## Support

For issues or questions:
- Check the [README.md](./README.md)
- Review API docs at `/docs`
- Check backend logs for errors
- Verify GCP permissions and quotas

## License

MIT
