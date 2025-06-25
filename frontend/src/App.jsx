// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import api from './api'; // Importa nossa instância do Axios configurada

// Importe seus componentes de tela/formulário aqui (vamos criá-los a seguir neste roteiro)
import LoginForm from './components/LoginForm';
import TimelineScreen from './components/TimelineScreen';

// Componentes Placeholder: Serão substituídos por componentes reais mais tarde.
const RegisterScreen = () => (
  <div style={{ padding: '20px', textAlign: 'center', backgroundColor: 'white', margin: '50px auto', maxWidth: '400px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
    <h2>Tela de Registro (a ser implementada)</h2>
    <p style={{marginTop: '10px'}}>Você pode criar um formulário aqui.</p>
    <p style={{marginTop: '20px'}}><a href="/login" style={{color: '#007bff', textDecoration: 'none'}}>Já tem conta? Entrar</a></p>
  </div>
);
const UserProfileScreen = () => (
  <div style={{ padding: '20px', textAlign: 'center', backgroundColor: 'white', margin: '50px auto', maxWidth: '600px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
    <h2>Tela de Perfil do Usuário (a ser implementada)</h2>
    <p style={{marginTop: '10px'}}>Exibirá os Yaps de um usuário específico.</p>
  </div>
);


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loadingApp, setLoadingApp] = useState(true); // Para verificar o estado de autenticação inicial

  // useEffect para verificar se o usuário já está autenticado ao carregar a aplicação
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        // Tenta acessar uma rota protegida (a timeline geral, por exemplo) para verificar a sessão.
        // Se a requisição for bem-sucedida (status 200), o usuário está logado.
        const response = await api.get('/yaps/api/yaps/');
        if (response.status === 200) {
          setIsAuthenticated(true);
        }
      } catch (error) {
        // Se der erro (ex: 401 Unauthorized), o usuário não está logado
        setIsAuthenticated(false);
      } finally {
        setLoadingApp(false); // Finaliza o loading, independente do resultado
      }
    };
    checkAuthStatus();
  }, []); // O array vazio garante que este useEffect roda apenas uma vez, na montagem do componente

  // Função para lidar com o sucesso do login (passada como prop para o LoginForm)
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    // Poderia adicionar lógica para redirecionar ou mostrar uma mensagem de sucesso
  };

  // Função para lidar com o logout
  const handleLogout = async () => {
    try {
      await api.post('/users/logout/'); // Faz a requisição de logout para o backend
      setIsAuthenticated(false); // Atualiza o estado de autenticação no frontend
      // Opcional: redirecionar para a página de login após o logout
      // window.location.href = '/login';
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      alert('Erro ao fazer logout. Tente novamente.');
    }
  };

  // Renderiza uma tela de carregamento enquanto verifica o status de autenticação
  if (loadingApp) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', fontSize: '20px', color: '#666' }}>
        Carregando aplicação...
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen" style={{ backgroundColor: '#f8f9fa', fontFamily: 'sans-serif', WebkitFontSmoothing: 'antialiased' }}>
        {/* Cabeçalho/Navegação */}
        <header style={{ backgroundColor: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff' }}>Yapper</h1>
          <div style={{ display: 'flex', gap: '8px' }}>
            {isAuthenticated ? (
              // Se autenticado, mostra o botão de Sair
              <button
                onClick={handleLogout}
                style={{ backgroundColor: '#dc3545', color: 'white', padding: '8px 16px', borderRadius: '4px', border: 'none', cursor: 'pointer' }}
              >
                Sair
              </button>
            ) : (
              // Se não autenticado, mostra botões de Login e Registrar
              <>
                <a
                  href="/login" // Link para a rota de login
                  style={{ backgroundColor: '#007bff', color: 'white', padding: '8px 16px', borderRadius: '4px', textDecoration: 'none', cursor: 'pointer' }}
                >
                  Login
                </a>
                <a
                  href="/register" // Link para a rota de registro
                  style={{ backgroundColor: '#28a745', color: 'white', padding: '8px 16px', borderRadius: '4px', textDecoration: 'none', cursor: 'pointer' }}
                >
                  Registrar
                </a>
              </>
            )}
          </div>
        </header>

        {/* Conteúdo Principal (Rotas) */}
        <main style={{ maxWidth: '960px', margin: '0 auto', padding: '16px' }}>
          <Routes>
            {/* Rota para Login: Se autenticado, redireciona para a home; caso contrário, mostra o formulário de login */}
            <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <LoginForm onLoginSuccess={handleLoginSuccess} />} />
            {/* Rota para Registro: Se autenticado, redireciona para a home; caso contrário, mostra o placeholder de registro */}
            <Route path="/register" element={isAuthenticated ? <Navigate to="/" /> : <RegisterScreen />} />
            {/* Rota Home: Se autenticado, mostra a Timeline; caso contrário, redireciona para o login */}
            <Route path="/" element={isAuthenticated ? <TimelineScreen /> : <Navigate to="/login" />} />
            {/* Rota de Perfil do Usuário: Protegida, mostra o placeholder */}
            <Route path="/profile/:username" element={isAuthenticated ? <UserProfileScreen /> : <Navigate to="/login" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;