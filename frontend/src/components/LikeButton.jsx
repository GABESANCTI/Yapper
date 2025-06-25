// frontend/src/components/LikeButton.jsx
import React, { useState } from 'react';
import api from '../api'; // Importa nossa instância do Axios

function LikeButton({ yapId, currentLikesCount, onLikeToggle }) {
  const [likesCount, setLikesCount] = useState(currentLikesCount);
  const [isLiked, setIsLiked] = useState(false); // Estado para verificar se o usuário logado já curtiu este Yap

  // Em uma aplicação real, você faria uma chamada GET inicial para verificar se o user já curtiu este Yap
  // useEffect(() => { /* Lógica para buscar o status de "curtido" */ }, [yapId]);

  const handleLike = async () => {
    try {
      // Faz a requisição POST para curtir um Yap
      // Para um toggle (curtir/descurtir), a lógica seria mais complexa aqui e no backend
      await api.post('/api/likes/create/', { yap: yapId }); // Rota: POST /api/likes/create/
      setLikesCount(likesCount + 1); // Incrementa a contagem de likes localmente
      setIsLiked(true); // Marca como curtido
      if (onLikeToggle) onLikeToggle(likesCount + 1); // Notifica o pai para atualizar a contagem
    } catch (error) {
      console.error('Erro ao curtir:', error.response || error);
      alert('Erro ao curtir. Você pode já ter curtido ou não estar logado.');
    }
  };

  return (
    <button
      onClick={handleLike}
      style={{
        display: 'flex', alignItems: 'center', gap: '4px', background: 'none', border: 'none', cursor: 'pointer',
        color: isLiked ? '#dc3545' : '#666' // Muda a cor se estiver curtido
      }}
      disabled={isLiked} // Desabilita o botão se já estiver curtido
    >
      {/* Ícone de coração (SVG simples) */}
      <svg style={{ width: '20px', height: '20px' }} fill={isLiked ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
      <span>{likesCount}</span> {/* Contagem de likes */}
    </button>
  );
}

export default LikeButton;