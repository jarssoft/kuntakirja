import axios from "axios";
//const baseUrl = "http://localhost:3001/api/kylat";
const baseUrl = "https://kuntakirja.onrender.com/api/kylat";

const getAll = () => {
  return axios.get(baseUrl);
};

export default {
  getAll: getAll,
};
