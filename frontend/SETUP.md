# CreditPathAI Frontend - Quick Start Guide

## 🚀 Quick Setup Instructions

### Step 1: Install Dependencies
```bash
cd creditpath-frontend
npm install
```

This will install all required packages:
- react & react-dom
- axios (for API calls)
- react-plotly.js & plotly.js (for charts)
- react-scripts (for build tools)

**Installation Time**: ~2-3 minutes (first time)

### Step 2: Verify Backend is Running

Ensure your FastAPI backend is running:
```bash
# In your Python project directory
python -m uvicorn milestone5_api:app --reload --port 8000
```

Or use your preferred FastAPI startup method.

**Check Backend**: Visit http://127.0.0.1:8000/docs to see Swagger docs

### Step 3: Start the Development Server
```bash
npm start
```

The application will automatically open at: http://localhost:3000

**First Load**: May take 30-60 seconds for React to compile

### Step 4: Test the Dashboard

1. **Fill the Form**:
   - Annual Income: 50000
   - Loan Amount: 15000
   - Credit Score: 720
   - Months Employed: 24

2. **Click "Get Risk Assessment"**

3. **View Results**:
   - Risk level with color coding
   - Default probability
   - Recommended action
   - Analytics charts

## 📊 Project Files Overview

### Core Components
| File | Purpose |
|------|---------|
| `src/App.js` | Main app logic & state management |
| `src/components/Form.js` | Loan application form |
| `src/components/Dashboard.js` | Results display |
| `src/components/Charts.js` | Interactive charts |
| `src/services/api.js` | Backend API communication |

### Styling
- `src/styles/App.css` - Global styles
- `src/styles/Form.css` - Form layout
- `src/styles/Dashboard.css` - Results display
- `src/styles/Charts.css` - Charts layout

### Configuration
- `package.json` - Dependencies & scripts
- `public/index.html` - HTML template
- `public/index.js` - React DOM render

## 🔧 Available Scripts

| Command | Purpose |
|---------|---------|
| `npm start` | Run dev server (port 3000) |
| `npm build` | Create production build |
| `npm test` | Run tests (if configured) |

## ⚙️ Environment Setup

1. **Copy env template**:
   ```bash
   copy .env.example .env.local
   ```

2. **Edit as needed** (optional):
   - API base URL (defaults to http://127.0.0.1:8000)
   - Port configuration

## 🔌 API Integration

The frontend connects to your FastAPI backend at:
- **Base URL**: http://127.0.0.1:8000
- **Endpoint**: /predict
- **Method**: POST

**Example Request**:
```json
{
  "income": 50000,
  "loan_amount": 15000,
  "credit_score": 720,
  "months_employed": 24
}
```

**Expected Response**:
```json
{
  "probability": 0.25,
  "risk": "Low",
  "action": "Approve"
}
```

## 🎯 Features Included

✅ Form with input validation
✅ Real-time error messages
✅ Loading spinner during API calls
✅ Color-coded risk levels (Green/Yellow/Red)
✅ Interactive Plotly charts
✅ Risk distribution analysis
✅ Probability breakdown
✅ Responsive mobile design
✅ Error handling & recovery
✅ Reset functionality

## 🚨 Troubleshooting

### Issue: "Cannot GET /predict"
**Solution**: Make sure FastAPI backend is running on port 8000

### Issue: CORS Error
**Solution**: Check that CORS is enabled in your FastAPI app:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Port 3000 Already in Use
```bash
# Windows: Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
set PORT=3001 && npm start
```

### Issue: Dependencies Installation Failed
```bash
npm cache clean --force
rmdir /s node_modules
npm install
```

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🎨 Customization

### Change Colors
Edit CSS variables in `src/styles/App.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

### Add Form Fields
Edit `src/components/Form.js` to add new input fields

### Modify Charts
Edit `src/components/Charts.js` to customize Plotly charts

## 📚 Resources

- [React Documentation](https://react.dev)
- [Axios Documentation](https://axios-http.com)
- [Plotly.js Documentation](https://plotly.com/javascript)
- [CSS Guide](https://developer.mozilla.org/en-US/docs/Web/CSS)

## ✅ Pre-Flight Checklist

Before running the application:

- [ ] Node.js installed (v14+)
- [ ] FastAPI backend running on port 8000
- [ ] CORS enabled in backend
- [ ] Port 3000 is available
- [ ] Dependencies installed (`npm install`)

## 🎓 Learning Path

1. **Start**: Run `npm start` and test the form
2. **Explore**: Check `src/components/` to understand structure
3. **Modify**: Edit form fields or styling
4. **Deploy**: Build with `npm build` for production

## 🤝 Next Steps

- [ ] Test with various loan scenarios
- [ ] Customize styling to match brand
- [ ] Add more analytics charts
- [ ] Implement PDF export
- [ ] Add user authentication
- [ ] Deploy to production

## 📝 Notes

- All validation happens on the client-side
- Errors from backend are displayed to users
- Loading state prevents double-submission
- Charts update dynamically based on predictions

---

**Happy analyzing with CreditPathAI! 🚀**

For issues, check the backend API or React console (F12 → Console tab)
