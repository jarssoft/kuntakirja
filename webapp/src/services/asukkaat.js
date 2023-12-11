import axios from "axios";
const baseUrl = "http://localhost:3001/api/talot";
//const baseUrl = "https://kuntakirja.onrender.com/api/notes";

const getAll = (pattern) => {
  return axios.get(baseUrl, { params: { pattern: pattern } });
};

const get = (id) => {
  console.log(baseUrl + "/" + id);
  return axios.get(baseUrl + "/" + id);
};

export default {
  get: get,
  getAll: getAll,
};
