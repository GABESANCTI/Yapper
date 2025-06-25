// frontend/src/api.js
import axios from 'axios';

// Cria uma instância do Axios com configurações padrão para a sua API Django.
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/', // Altere esta URL se o seu backend Django estiver em outro endereço/porta
  withCredentials: true, // Importante: Permite que o Axios envie e receba cookies de sessão (para autenticação baseada em sessão e CSRF)
});

// Opcional: Este é um "interceptor" (código que roda antes de cada requisição).
// Seria usado se você for implementar autenticação por Token/JWT.
// Por enquanto, está comentado.
/*
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token'); // Supondo que você armazena o token aqui
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Adiciona o token no cabeçalho Authorization
  }
  return config;
});
*/

export default api; // Exporta a instância configurada para ser usada em outros componentes