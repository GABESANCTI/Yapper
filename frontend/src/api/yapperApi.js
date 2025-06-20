//comunicação com a Yapi
import axios from "axios";

const api = axios.create({  
  baseURL: "http://localhost:8000/api/", //trocar para o endereço do backend
    timeout: 10000, // tempo limite de 10 segundos
  withCredentials: true, // se usar sessões e CSRF
});

export default api;
