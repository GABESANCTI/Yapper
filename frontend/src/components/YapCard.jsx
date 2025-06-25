// frontend/src/components/YapCard.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Para criar links para o perfil do usuário
import api from '../api'; // Importa nossa instância do Axios
import LikeButton from './LikeButton'; // Componente de Curtir
import CommentSection from './CommentSection'; // Componente de Comentários

const YapCard = ({ yap, onYapDeleted }) => { // <-- Sintaxe correta de arrow function
  const [showComments, setShowComments] = useState(false); // Estado para mostrar/esconder a seção de comentários
  const [currentYap, setCurrentYap] = useState(yap); // Estado para gerenciar dados do Yap (likes/comments) localmente

  // Função para deletar um Yap
  const handleDelete = async () => {
    if (window.confirm('Tem certeza que quer deletar este Yap?')) {
      try {
        // Faz a requisição DELETE para a API
        await api.delete(`/api/yaps/${currentYap.id}/delete/`); // Rota: DELETE /api/yaps/<id>/delete/
        if (onYapDeleted) {
          onYapDeleted(); // Notifica o componente pai (TimelineScreen) para atualizar a lista
        }
      } catch (error) {
        console.error('Erro ao deletar Yap:', error.response || error);
        alert('Erro ao deletar Yap. Você pode não ter permissão ou o Yap já foi removido.');
      }
    }
  };

  // Função de callback para atualizar a contagem de likes
  const handleLikeToggle = (newLikesCount) => {
    setCurrentYap({ ...currentYap, likes_count: newLikesCount });
  };

  // Função de callback para atualizar a contagem de comentários
  const handleCommentAdded = (newCommentsCount) => {
    setCurrentYap({ ...currentYap, comments_count: newCommentsCount });
    setShowComments(true); // Abre a seção de comentários após adicionar um
  };

  // --- ATENÇÃO: Autenticação de Autor ---
  // Para fins de demonstração, 'window.currentUser' é uma simulação.
  // Em uma aplicação real, você obteria o usuário logado de um contexto de autenticação do React
  // (ex: de um `AuthContext` que você criaria e populária no App.jsx após o login).
  // Substitua `window.currentUser` pela forma real de obter o usuário logado.
  // Por agora, apenas para evitar erros, vamos simular um usuário temporário:
  // Em um cenário real, você teria um estado global para o usuário autenticado.
  const loggedInUser = { username: 'seu_usuario_logado_aqui' }; // <-- SUBSTITUA ISSO pelo usuário real
  const isAuthor = loggedInUser && loggedInUser.username === currentYap.autor.username;


  return (
    <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '16px', border: '1px solid #e0e0e0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        {/* Link para o perfil do autor */}
        <Link to={`/profile/${currentYap.autor.username}`} style={{ fontSize: '18px', fontWeight: '600', color: '#007bff', textDecoration: 'none' }}>
          @{currentYap.autor.username}
        </Link>
        {/* Data e hora de criação */}
        <span style={{ fontSize: '14px', color: '#666' }}>
          {new Date(currentYap.criado_em).toLocaleDateString()} {new Date(currentYap.criado_em).toLocaleTimeString()}
        </span>
      </div>
      <p style={{ color: '#333', fontSize: '16px', lineHeight: '1.5', marginBottom: '16px' }}>{currentYap.conteudo}</p>

      {/* Seção de Ações (Curtir, Comentar, Deletar) */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #eee', paddingTop: '12px' }}>
        <div style={{ display: 'flex', gap: '16px' }}>
          {/* Botão de Curtir (componente LikeButton) */}
          <LikeButton yapId={currentYap.id} currentLikesCount={currentYap.likes_count} onLikeToggle={handleLikeToggle} />

          {/* Botão para Comentários (com ícone SVG simples) */}
          <button
            onClick={() => setShowComments(!showComments)}
            style={{ color: '#666', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', background: 'none', border: 'none' }}
          >
            <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            <span>{currentYap.comments_count}</span>
          </button>
        </div>
        {/* Botão de Excluir (visível apenas se o usuário logado for o autor) */}
        {isAuthor && (
          <button
            onClick={handleDelete}
            style={{ color: '#dc3545', cursor: 'pointer', background: 'none', border: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
          </button>
        )}
      </div>

      {showComments && (
        <CommentSection yapId={currentYap.id} onCommentAdded={handleCommentAdded} />
      )}
    </div>
  );
}; 

export default YapCard;