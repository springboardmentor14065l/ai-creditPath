import axios from 'axios';

export const predict = async(data) => {
  return axios.post('http://127.0.0.1:8000/predict', data);
}
