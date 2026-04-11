# CreditPathAI - Frontend Dashboard

A modern, production-ready React dashboard for AI-based loan risk prediction system.

## 🚀 Features

- **Loan Application Form**: Input fields for income, loan amount, credit score, and employment duration
- **Risk Assessment Dashboard**: Color-coded risk levels (Low/Green, Medium/Yellow, High/Red)
- **Interactive Charts**: Plotly-based visualizations showing risk distribution and probability breakdown
- **Loading States**: Spinner animation during API calls
- **Error Handling**: User-friendly error messages
- **Form Validation**: Client-side validation with helpful error messages
- **Responsive Design**: Mobile-friendly layout
- **Clean UI**: Modern, minimal design with proper spacing and typography

## 📋 Project Structure

```
creditpath-frontend/
├── public/
│   ├── index.html          # Main HTML file
│   └── index.js            # React DOM render
├── src/
│   ├── components/
│   │   ├── Form.js         # Loan application form
│   │   ├── Dashboard.js    # Risk assessment display
│   │   └── Charts.js       # Interactive charts
│   ├── services/
│   │   └── api.js          # API service with axios
│   ├── styles/
│   │   ├── App.css         # Main app styles
│   │   ├── Form.css        # Form component styles
│   │   ├── Dashboard.css   # Dashboard component styles
│   │   └── Charts.css      # Charts component styles
│   └── App.js              # Main application component
├── package.json            # Project dependencies
└── README.md              # This file
```

## 🛠️ Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- FastAPI backend running on `http://127.0.0.1:8000`

## 📦 Installation

1. Navigate to the project directory:
   ```bash
   cd creditpath-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## 🚀 Running the Application

### Development Mode

```bash
npm start
```

The application will open at `http://localhost:3000`

### Production Build

```bash
npm build
```

This creates an optimized production build in the `build` directory.

## 🔌 API Endpoints

The frontend communicates with the backend API:

- **Base URL**: `http://127.0.0.1:8000`
- **Endpoint**: `/predict`
- **Method**: `POST`

### Request Format

```json
{
  "income": 50000,
  "loan_amount": 15000,
  "credit_score": 720,
  "months_employed": 24
}
```

### Response Format

```json
{
  "probability": 0.25,
  "risk": "Low",
  "action": "Approve"
}
```

## 🎨 Component Details

### Form Component (`Form.js`)
- Takes loan application inputs
- Validates data before submission
- Handles form reset
- Shows loading state during submission

**Input Fields:**
- Annual Income: Financial capability of applicant
- Loan Amount: Amount requested
- Credit Score: Applicant's creditworthiness (300-850)
- Months Employed: Employment stability indicator

### Dashboard Component (`Dashboard.js`)
- Displays prediction results
- Color-coded risk levels
- Probability visualization
- Recommended action display
- Risk level guide and legend

**Risk Colors:**
- 🟢 Green: Low Risk (Safe to approve)
- 🟡 Yellow: Medium Risk (Review carefully)
- 🔴 Red: High Risk (Consider declining)

### Charts Component (`Charts.js`)
- Risk distribution bar chart
- Default probability breakdown
- Portfolio statistics summary
- Dynamic data based on predictions

### API Service (`api.js`)
- Encapsulates all API communication
- Error handling with user-friendly messages
- Axios instance configuration
- Request/response handling

## 🎯 Key Features Implementation

### 1. Form Validation
- Required field checks
- Value range validation
- Real-time error clearing
- Helpful error messages

### 2. Error Handling
- Network error detection
- Backend error messages
- User-friendly error display
- Error dismissal

### 3. Loading States
- Spinner animation during API calls
- Button disabled state
- Input field disable during loading
- Clear loading indication

### 4. Responsive Design
- Mobile-first approach
- Grid-based layout
- Breakpoints for different screen sizes
- Flexible spacing and typography

## 🎨 Styling

The application uses:
- **CSS Variables**: Consistent color scheme and spacing
- **CSS Grid & Flexbox**: Modern responsive layouts
- **Gradients**: Modern visual appeal
- **Animations**: Smooth transitions and interactions
- **No External CSS Framework**: Clean, custom CSS

## 🔐 Security Considerations

- Input validation on client-side
- Error messages don't expose sensitive information
- No credentials stored in frontend
- CORS handled by backend

## 🐛 Troubleshooting

### Backend Not Responding
- Ensure FastAPI backend is running on `http://127.0.0.1:8000`
- Check CORS is enabled in backend
- Verify network connectivity

### Port 3000 Already in Use
```bash
# Use a different port
PORT=3001 npm start
```

### Dependencies Installation Issues
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🛣️ Future Enhancements

- Export results as PDF
- Historical prediction records
- User authentication
- Advanced analytics dashboard
- Real-time prediction notifications
- Multi-language support

## 📄 License

This project is part of the CreditPathAI system.

## 🤝 Support

For issues or questions, please refer to the backend API documentation or contact the development team.

---

**Built with ❤️ using React, Axios, and Plotly.js**
