import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext'; // Ajuste o caminho se necessário
import { FiUser, FiLogOut, FiLogIn } from 'react-icons/fi';

const Header = ({ pageTitle }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <header 
      className="fixed top-0 left-0 right-0 bg-gray-800 text-white z-50 shadow-lg 
                 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-full after:h-[1px] after:bg-blue-500/50"
    >
      <div className="container mx-auto flex items-center justify-between p-4 h-20">

        {/* --- Coluna da Esquerda (Logo) --- */}
        <div className="flex-1">
          <h1 
            className="text-3xl font-bold text-white cursor-pointer w-fit"
            onClick={() => navigate('/')}
          >
            infoDomus
          </h1>
        </div>

        {/* --- Coluna Central (Título da Página) --- */}
        <div className="flex-1 text-center">
          {pageTitle && (
            <h2 className="text-xl text-gray-300 font-medium">{pageTitle}</h2>
          )}
        </div>

        {/* --- Coluna da Direita (Botões de Autenticação) --- */}
        <div className="flex-1 flex justify-end">
          <div className="flex items-center gap-x-5">
            {user ? (
              // Botões para usuário LOGADO
              <>
                <div className="flex items-center gap-x-2 text-gray-200">
                  <FiUser />
                  <span className="font-medium">{user.username || 'Usuário'}</span>
                </div>

                <button 
                  className="flex items-center gap-x-2 bg-gray-700/50 px-4 py-2 rounded-lg text-gray-300 hover:bg-red-500 hover:text-white transition-all duration-300"
                  onClick={logout}
                >
                  <FiLogOut />
                  <span>Log out</span>
                </button>
              </>
            ) : (
              // Botões para usuário DESLOGADO
              <>
                <button 
                  className="flex items-center gap-x-2 text-gray-300 hover:text-white transition-colors duration-300"
                  onClick={() => navigate('/login')}
                >
                  <FiLogIn />
                  <span>Login</span>
                </button>
                <button 
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-300"
                  onClick={() => navigate('/register')}
                >
                  Cadastro
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;