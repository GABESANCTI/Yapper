// frontend/src/components/CommentSection.jsx
import React, { useEffect, useState } from 'react';
import api from '../api';

// Use a sintaxe de arrow function completa:
const CommentSection = ({ yapId, onCommentAdded }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loadingComments, setLoadingComments] = useState(true);
  const [submittingComment, setSubmittingComment] = useState(false);
  const [error, setError] = useState(null);

  const fetchComments = async () => {
    try {
      setLoadingComments(true);
      const response = await api.get(`/api/yaps/${yapId}/comments/`);
      setComments(response.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar comentários.');
      console.error('Erro ao buscar comentários:', err.response || err);
    } finally {
      setLoadingComments(false);
    }
  };

  useEffect(() => {
    fetchComments();
  }, [yapId]);

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) {
      setError('O comentário não pode estar vazio.');
      return;
    }

    setSubmittingComment(true);
    setError(null);

    try {
      await api.post('/api/comments/create/', { yap: yapId, conteudo: newComment });
      setNewComment('');
      fetchComments();
      if (onCommentAdded) onCommentAdded(comments.length + 1);
    } catch (err) {
      setError('Erro ao enviar comentário. Verifique se está logado.');
      console.error('Erro ao enviar comentário:', err.response || err);
    } finally {
      setSubmittingComment(false);
    }
  };

  return (
    <div style={{ marginTop: '16px', borderTop: '1px solid #eee', paddingTop: '16px' }}>
      <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#333', marginBottom: '12px' }}>Comentários</h3>
      {loadingComments ? (
        <p style={{ color: '#666' }}>Carregando comentários...</p>
      ) : (
        comments.length === 0 ? (
          <p style={{ color: '#666', fontSize: '14px' }}>Nenhum comentário ainda. Seja o primeiro!</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {comments.map(comment => (
              <div key={comment.id} style={{ backgroundColor: '#f9f9f9', padding: '12px', borderRadius: '6px', border: '1px solid #eee' }}>
                <p style={{ fontSize: '14px', fontWeight: '500', color: '#333' }}>@{comment.user}
                  <span style={{ color: '#666', fontWeight: 'normal', marginLeft: '8px', fontSize: '12px' }}>
                    {new Date(comment.criado_em).toLocaleDateString()}
                  </span>
                </p>
                <p style={{ color: '#555', fontSize: '14px', marginTop: '4px' }}>{comment.conteudo}</p>
              </div>
            ))}
          </div>
        )
      )}

      <form onSubmit={handleSubmitComment} style={{ marginTop: '16px' }}>
        {error && <p style={{ color: 'red', marginBottom: '12px' }}>{error}</p>}
        <textarea
          style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', resize: 'vertical', fontSize: '14px' }}
          placeholder="Adicione um comentário..."
          rows="2"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          maxLength="280"
          disabled={submittingComment}
        ></textarea>
        <button
          type="submit"
          style={{ backgroundColor: '#007bff', color: 'white', fontWeight: 'bold', padding: '6px 16px', borderRadius: '6px', border: 'none', fontSize: '14px', marginTop: '8px', cursor: 'pointer', opacity: submittingComment ? 0.5 : 1 }}
          disabled={submittingComment}
        >
          {submittingComment ? 'Enviando...' : 'Comentar'}
        </button>
      </form>
    </div>
  );
}

export default CommentSection;