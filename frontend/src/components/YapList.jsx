import React, { useEffect, useState } from 'react';

const YapList = () => {
  const [yaps, setYaps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/yaps/api/yaps/')
      .then(response => response.json())
      .then(data => {
        setYaps(data.results || data);  // com ou sem paginação
        setLoading(false);
      })
      .catch(error => {
        console.error('Erro ao buscar yaps:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Carregando Yaps...</p>;

  return (
    <div>
      <h2>Timeline Yapper</h2>
      <ul>
        {yaps.map(yap => (
          <li key={yap.id} style={{ borderBottom: '1px solid #ccc', margin: '1rem 0' }}>
            <p><strong>{yap.author}:</strong> {yap.conteudo}</p>
            <small>{new Date(yap.criado_em).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default YapList;
// This component fetches and displays a list of Yaps from the API.
// It handles loading state and displays each Yap with author, content, and creation date.