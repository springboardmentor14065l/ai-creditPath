import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000
});

export const pingApi = async () => {
  const response = await client.get("/health");
  return response.data;
};

export const predict = async (data) => {
  const response = await client.post("/predict", data);
  return response.data;
};

export const predictBatch = async (records) => {
  const response = await client.post("/predict/batch", { records });
  return response.data;
};
