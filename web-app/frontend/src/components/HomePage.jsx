import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiMonitor, FiLogIn, FiUserPlus } from 'react-icons/fi';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen  text-white p-6">
      <div className="text-center max-w-2xl">
        
        {/* Ícone Principal */}
        <FiMonitor className="mx-auto text-blue-500 mb-6" size={72} />

        {/* Título e Subtítulo */}
        <h1 className="text-5xl font-bold mb-4">
          Bem-vindo ao <span className="text-blue-400">infoDomus</span>
        </h1>
        <p className="text-lg text-gray-400 mb-12">
          A solução completa e simplificada para o gerenciamento de laboratórios e salas de informática. Controle máquinas, tarefas e estudantes em um só lugar.
        </p>

        {/* Botões de Ação */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
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
        </div>
      </div>

      {/* Footer Simples */}
      <footer className="absolute bottom-6 text-gray-500 text-sm">
        <p>&copy; {new Date().getFullYear()} infoDomus. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
};

export default HomePage;