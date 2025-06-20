import React, { useContext } from 'react'; // Removido useState e useEffect, não são mais necessários
import { useNavigate } from 'react-router-dom';
import { FiMonitor, FiLogIn, FiUserPlus, FiGrid } from 'react-icons/fi';
import { AuthContext } from '../contexts/AuthContext.jsx'; // Certifique-se que o caminho está correto

const HomePage = () => {
  const navigate = useNavigate();
  
  // 1. Chame o useContext no nível superior do componente.
  // Ele nos dá acesso direto ao valor do token (e outras coisas) do nosso contexto.
  const { token,user } = useContext(AuthContext);
  // 2. Não precisamos mais do estado 'isLoggedIn' nem do 'useEffect'.
  // A existência do 'token' já é o nosso estado. Se o token mudar no contexto,
  // este componente será re-renderizado automaticamente.

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0D1117] text-white p-6">
      <div className="text-center max-w-2xl">
        
        <FiMonitor className="mx-auto text-blue-500 mb-6" size={72} />

        <h1 className="text-5xl font-bold mb-4">
          Bem-vindo ao <span className="text-blue-400">infoDomus</span>
        </h1>
        <p className="text-lg text-gray-400 mb-12">
          A solução completa e simplificada para o gerenciamento de laboratórios e salas de informática. Controle máquinas, tarefas e estudantes em um só lugar.
        </p>

        {/* 3. Use o 'token' diretamente para a renderização condicional */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          {user ? (
            // SE o token existir no contexto, mostra este botão
            <button
              onClick={() => navigate('/user_labs')}
              className="flex items-center justify-center w-full sm:w-auto gap-x-3 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105"
            >
              <FiGrid size={20} />
              <span>Acessar seus Labs</span>
            </button>
          ) : (
            // SENÃO (token é nulo ou undefined), mostra os botões de login/registro
            <>
              <button
                onClick={() => navigate('/login')}
                className="flex items-center justify-center w-full sm:w-auto gap-x-3 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105"
              >
                <FiLogIn size={20} />
                <span>Entrar</span>
              </button>
              <button
                onClick={() => navigate('/register')}
                className="flex items-center justify-center w-full sm:w-auto gap-x-3 bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105"
              >
                <FiUserPlus size={20} />
                <span>Registrar</span>
              </button>
            </>
          )}
        </div>
      </div>

      <footer className="absolute bottom-6 text-gray-500 text-sm">
        <p>&copy; {new Date().getFullYear()} infoDomus. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
};

export default HomePage;