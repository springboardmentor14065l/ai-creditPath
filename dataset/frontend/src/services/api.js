import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const predict = async (data) => {
  return axios.post(`${BASE_URL}/predict`, data);
};

export const predictBatch = async (records) => {
  return axios.post(`${BASE_URL}/predict-batch`, { records });
};

export const healthCheck = async () => {
  return axios.get(`${BASE_URL}/health`);
};

export const getRiskInfo = async () => {
  return axios.get(`${BASE_URL}/risk-info`);
};
