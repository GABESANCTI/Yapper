// frontend/src/components/CreateYapForm.jsx
import React, { useState } from 'react';
import api from '../api'; // Importa nossa instância do Axios

const CreateYapForm = ({ onYapCreated }) => { // <-- Sintaxe correta de arrow function
  const [conteudo, setConteudo] = useState('');
  const [loading, setLoading] = useState(false); // Estado para controlar o envio do Yap
  const [error, setError] = useState(null); // Estado para mensagens de erro

  const handleSubmit = async (e) => {
    e.preventDefault(); // Impede o recarregamento da página
    if (!conteudo.trim()) { // Não permite Yaps vazios
      setError('O Yap não pode estar vazio.');
      return;
    }

    setLoading(true); // Ativa o loading
    setError(null); // Limpa erros anteriores

    try {
      // Faz a requisição POST para criar um novo Yap
      await api.post('/yaps/api/yaps/', { conteudo }); // Rota: POST /yaps/api/yaps/
      setConteudo(''); // Limpa o campo de texto após o sucesso
      if (onYapCreated) {
        onYapCreated(); // Notifica o componente pai (TimelineScreen) para recarregar a lista
      }
    } catch (err) {
      setError('Erro ao criar Yap. Você está logado?');
      console.error('Erro ao criar Yap:', err.response || err);
    } finally {
      setLoading(false); // Desativa o loading
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '24px' }}>
      {error && <p style={{ color: 'red', marginBottom: '16px', textAlign: 'center' }}>{error}</p>}
      <textarea
        style={{ width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px', resize: 'vertical' }}
        placeholder="No que está pensando?"
        rows="3"
        value={conteudo}
        onChange={(e) => setConteudo(e.target.value)}
        maxLength="280" // Limite de caracteres como no Twitter
        disabled={loading} // Desabilita enquanto envia
      ></textarea>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
        <span style={{ fontSize: '14px', color: '#666' }}>{conteudo.length}/280</span>
        <button
          type="submit"
          style={{ backgroundColor: '#007bff', color: 'white', fontWeight: 'bold', padding: '8px 20px', borderRadius: '9999px', border: 'none', cursor: 'pointer', opacity: loading ? 0.5 : 1 }}
          disabled={loading}
        >
          {loading ? 'Yappando...' : 'Yappar!'}
        </button>
      </div>
    </form>
  );
}; // <-- Não esquecer o ponto e vírgula aqui para arrow functions

export default CreateYapForm;