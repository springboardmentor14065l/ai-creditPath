import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Make prediction call to FastAPI backend
 * @param {Object} data - Loan application data
 * @param {number} data.income - Annual income
 * @param {number} data.loan_amount - Loan amount requested
 * @param {number} data.credit_score - Credit score
 * @param {number} data.months_employed - Months employed
 * @returns {Promise<Object>} - API response with probability, risk, and action
 */
export const predict = async (data) => {
    try {
        const response = await apiClient.post('/predict', data);
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        
        // Handle different error scenarios
        if (error.response) {
            // Server responded with error status
            throw new Error(
                error.response.data?.detail || 
                `API Error: ${error.response.status} - ${error.response.statusText}`
            );
        } else if (error.request) {
            // Request made but no response received
            throw new Error(
                'No response from server. Make sure the backend is running on http://127.0.0.1:8000'
            );
        } else {
            // Error in request setup
            throw new Error(`Request Error: ${error.message}`);
        }
    }
};

export default apiClient;
