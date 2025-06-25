// frontend/src/components/LoginForm.jsx
import React, { useState } from 'react';
import api from '../api'; // Importa nossa instância do Axios configurada

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Impede o recarregamento padrão da página
    setError(''); // Limpa erros anteriores
    setLoading(true); // Ativa o estado de carregamento

    try {
      // Faz a requisição POST para o endpoint de login do seu backend Django
      // A URL base ('http://127.0.0.1:8000/') já está configurada no 'api.js'
      const response = await api.post('/users/login/', { // Rota: POST /users/login/
        username,
        password,
      });

      console.log('Login bem-sucedido:', response.data);
      if (onLoginSuccess) {
        onLoginSuccess(response.data); // Chama a função de callback no componente pai (App.jsx)
      }
      // Após o sucesso, o 'App.jsx' cuidará do redirecionamento
    } catch (err) {
      console.error('Erro no login:', err.response ? err.response.data : err.message);
      // Extrai a mensagem de erro específica do backend ou usa uma genérica
      setError(err.response && err.response.data && err.response.data.non_field_errors
                ? err.response.data.non_field_errors[0]
                : 'Usuário ou senha inválidos.');
    } finally {
      setLoading(false); // Desativa o estado de carregamento
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', backgroundColor: 'white' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#333' }}>Entrar no Yapper</h2>
      {error && <p style={{ color: 'red', textAlign: 'center', marginBottom: '15px' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="username" style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Nome de Usuário:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
        </div>
        <div style={{ marginBottom: '20px' }}>
          <label htmlFor="password" style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Senha:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
        </div>
        <button
          type="submit"
          disabled={loading} // Desabilita o botão enquanto carrega
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer', // Muda o cursor
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', // Para centralizar o spinner/texto
            opacity: loading ? 0.7 : 1 // Reduz a opacidade quando carregando
          }}
        >
          {loading ? (
            <>
              {/* Spinner CSS inline (gambiarra simples) */}
              <div style={{
                border: '3px solid rgba(255, 255, 255, 0.3)',
                borderTop: '3px solid #fff', // Cor do spinner
                borderRadius: '50%',
                width: '16px',
                height: '16px',
                animation: 'spin 1s linear infinite' // Animação
              }}></div>
              Carregando...
            </>
          ) : (
            'Entrar'
          )}
        </button>
      </form>
      <p style={{ textAlign: 'center', marginTop: '20px', color: '#555' }}>
        Não tem uma conta? <a href="/register" style={{ color: '#007bff', textDecoration: 'none' }}>Cadastre-se aqui</a>.
      </p>
      {/* Estilos para a animação do spinner (pode ser movido para um arquivo CSS) */}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default LoginForm;