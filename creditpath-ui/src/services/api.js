import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const submitLoanApplication = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, data);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      throw new Error('Could not reach the server. Please check your connection.');
    } else {
      throw new Error('An error occurred during the request.');
    }
  }
};
