# CreditPathAI - Setup Instructions

Complete setup guide for running the full-stack CreditPathAI application with backend and frontend together.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed
- **Node.js v14+** and npm installed
- **Git** installed and configured
- **Two terminal windows** (one for backend, one for frontend)

## 🎯 Step-by-Step Setup

### Phase 1: Repository Setup

```bash
# Navigate to your project root
cd "e:\Infosys spring board\ai-creditPath"

# Verify git is initialized
git status

# You should see both backend/ and frontend/ folders
ls  # Windows: dir
```

### Phase 2: Backend Setup

#### 2.1 Install Python Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2.2 Install Backend Dependencies

```bash
# Install all Python packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- fastapi
- uvicorn
- pandas
- scikit-learn
- xgboost
- lightgbm
- pydantic

#### 2.3 Prepare Backend Files

Ensure these files exist in the `backend/` directory:
- `model.pkl` - Trained ML model
- `pipeline.pkl` - Preprocessing pipeline
- `Loan_default.csv` - Dataset (if needed)
- `final_features.csv` - Processed features

#### 2.4 Start Backend Server

```bash
# From backend directory with venv activated
python -m uvicorn milestone5_api:app --reload --port 8000
```

✅ Expected output:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Keep this terminal running!** Do not close it.

### Phase 3: Frontend Setup (NEW TERMINAL)

#### 3.1 Navigate to Frontend

```bash
# Open a NEW terminal/command prompt
cd "e:\Infosys spring board\ai-creditPath\frontend"
```

#### 3.2 Install Frontend Dependencies

```bash
# Install npm packages
npm install

# This will take 2-3 minutes for first-time installation
```

Expected packages:
- react & react-dom
- axios
- react-plotly.js
- plotly.js

#### 3.3 Start Frontend Development Server

```bash
# From frontend directory
npm start
```

✅ Expected output:
```
Compiled successfully!

You can now view creditpath-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

The dashboard will automatically open in your browser!

## ✅ Verification Checklist

### Backend Verification

1. Check if API is running:
   ```bash
   # Open browser and visit
   http://127.0.0.1:8000/
   ```
   Expected response: `{"message": "CreditPathAI API is running"}`

2. Check Swagger documentation:
   ```
   http://127.0.0.1:8000/docs
   ```
   Should show interactive API documentation

### Frontend Verification

1. Check if dashboard loads:
   ```
   http://localhost:3000
   ```
   Should show the loan application form

2. Try a test prediction:
   - Fill in sample data in the form
   - Click "Get Risk Assessment"
   - Should see risk results and charts

## 🎮 Testing the Full Application

### Test Case 1: Low Risk Loan

```
Income: 100000
Loan Amount: 20000
Credit Score: 780
Months Employed: 60
```

Expected: Low Risk

### Test Case 2: Medium Risk Loan

```
Income: 50000
Loan Amount: 30000
Credit Score: 650
Months Employed: 24
```

Expected: Medium Risk

### Test Case 3: High Risk Loan

```
Income: 30000
Loan Amount: 50000
Credit Score: 550
Months Employed: 6
```

Expected: High Risk

## 🔧 Troubleshooting

### Issue: Backend Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Use different port
python -m uvicorn milestone5_api:app --reload --port 8001

# Update frontend API URL in src/services/api.js
# Change: const API_BASE_URL = 'http://127.0.0.1:8001';
```

### Issue: Frontend Cannot Connect to Backend

**Error**: `Error: No response from server`

**Solution**:
1. Check if backend is running on port 8000
2. Check if CORS is enabled in backend
3. Clear browser cache: Ctrl+Shift+Delete

### Issue: Python Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: npm ERR!

**Error**: `npm ERR! code ERESOLVE`

**Solution**:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📊 Development Workflow

### Daily Startup

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
python -m uvicorn milestone5_api:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

### Making Changes

**Frontend Changes**:
- Edit files in `frontend/src/`
- React will auto-reload in browser
- No need to restart

**Backend Changes**:
- Edit files in `backend/`
- FastAPI will auto-reload
- No need to restart (with `--reload` flag)

### Committing Changes

```bash
# Both frontend and backend changes
git add .
git commit -m "[both] Add new feature description"
git push origin main

# Or specific changes
git add backend/
git commit -m "[backend] Update API logic"
```

## 🚀 Production Deployment

### Build Frontend for Production

```bash
cd frontend
npm run build
```

Creates `frontend/build/` directory with optimized code.

### Backend Production Mode

```bash
# Stop development server (Ctrl+C)
python -m uvicorn milestone5_api:app --host 0.0.0.0 --port 8000
```

## 📝 Environment Configuration

### Create `.env` file for sensitive data

**backend/.env**:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
```

**frontend/.env.local**:
```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
```

## 🆘 Getting Help

### Check Logs

**Backend Logs**:
```bash
# Available in terminal where uvicorn is running
# Look for error messages and tracebacks
```

**Frontend Logs**:
```bash
# Press F12 in browser
# Go to Console tab
# Look for error messages
```

### Common Issues Checklist

- [ ] Backend venv is activated?
- [ ] Backend port 8000 is available?
- [ ] Frontend port 3000 is available?
- [ ] All dependencies installed?
- [ ] API files (model.pkl, pipeline.pkl) exist?
- [ ] CORS enabled in backend?
- [ ] Git repository properly initialized?

## ✨ Next Steps

1. **Customize the UI**: Edit styles in `frontend/src/styles/`
2. **Add more features**: Create new React components
3. **Improve the model**: Train better models in `backend/`
4. **Deploy to cloud**: Use Azure, AWS, or Heroku
5. **Add authentication**: Implement user login
6. **Database**: Add persistent data storage

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start backend | `python -m uvicorn milestone5_api:app --reload --port 8000` |
| Start frontend | `npm start` |
| Build frontend | `npm run build` |
| Check API docs | `http://127.0.0.1:8000/docs` |
| View dashboard | `http://localhost:3000` |
| Stop servers | `Ctrl+C` in terminal |
| Activate venv | `venv\Scripts\activate` (Windows) |
| Deactivate venv | `deactivate` |

---

**Happy developing with CreditPathAI! 🚀**

For more detailed information, see individual `README.md` files in `backend/` and `frontend/` directories.
