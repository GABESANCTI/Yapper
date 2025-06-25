// frontend/src/components/TimelineScreen.jsx
import React, { useEffect, useState } from 'react';
import api from '../api'; // Importa nossa instância do Axios
// Importaremos os componentes CreateYapForm e YapCard aqui (serão criados a seguir)
import CreateYapForm from './CreateYapForm';
import YapCard from './YapCard';

function TimelineScreen() {
  const [yaps, setYaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para buscar os Yaps da API
  const fetchYaps = async () => {
    try {
      setLoading(true); // Ativa o loading ao iniciar a busca
      const response = await api.get('/yaps/api/yaps/'); // Rota: GET /yaps/api/yaps/
      setYaps(response.data); // Atualiza o estado com os Yaps recebidos
      setError(null); // Limpa erros anteriores
    } catch (err) {
      setError('Erro ao carregar Yaps. Por favor, tente novamente.');
      console.error('Erro ao buscar Yaps:', err);
    } finally {
      setLoading(false); // Desativa o loading, independente do resultado
    }
  };

  // useEffect para buscar os Yaps quando o componente é montado
  useEffect(() => {
    fetchYaps();
  }, []); // O array vazio [] garante que esta função só roda uma vez

  // Função de callback para quando um novo Yap for criado, recarrega a timeline
  const handleNewYap = () => {
    fetchYaps();
  };

  // Renderização condicional para estados de carregamento e erro
  if (loading) return <div style={{ textAlign: 'center', padding: '16px', color: '#666' }}>Carregando timeline...</div>;
  if (error) return <div style={{ textAlign: 'center', padding: '16px', color: 'red' }}>{error}</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#333', marginBottom: '16px' }}>O que está acontecendo?</h2>
      
      {/* Formulário para criar novos Yaps */}
      <CreateYapForm onYapCreated={handleNewYap} />

      {/* Lista de Yaps */}
      <div style={{ marginTop: '32px' }}>
        {yaps.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>Nenhum Yap por aqui ainda. Seja o primeiro a postar!</p>
        ) : (
          yaps.map(yap => (
            <YapCard key={yap.id} yap={yap} onYapDeleted={fetchYaps} /> // onYapDeleted para atualizar após deleção
          ))
        )}
      </div>
    </div>
  );
}

export default TimelineScreen;