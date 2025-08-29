# INFODOMUS
## Visão geral

O INFODOMUS é um sistema composto por **três aplicações** principais: uma **aplicação desktop** (cliente para laboratórios), um **backend** (API REST em FastAPI) e um **frontend web** (SPA em React + Tailwind CSS). O objetivo do sistema é gerenciar sessões de uso de computadores em laboratórios, tarefas associadas, cadastro de estudantes e configuração de máquinas.

Este README descreve a finalidade de cada aplicação, as tecnologias utilizadas, instruções de instalação (desenvolvimento e produção), variáveis de ambiente relevantes, estrutura do repositório e recomendações operacionais.

---

## Sumário

* [Visão geral](#visão-geral)  
* [Composição do projeto](#composição-do-projeto)  
* [Tecnologias principais](#tecnologias-principais)  
* [Pré-requisitos](#pré-requisitos)  
* [Instalação e Execução](#instalação-e-execução)  
  * [Desenvolvimento](#desenvolvimento)  
    * [Backend (API)](#backend-api)  
    * [Frontend (Web)](#frontend-web)  
    * [Desktop (Cliente)](#desktop-cliente)  
  * [Produção com Docker](#produção-com-docker)  
  * [Funcionalidades Implementadas no Nginx](#funcionalidades-implementadas-no-nginx)  
* [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)  
  * [Backend (.env)](#backend-env)  
  * [Frontend (.env)](#frontend-env)  
  * [Desktop App (.env)](#desktop-app-env)  
* [Estrutura do Projeto](#estrutura-do-projeto)  
* [Configurações / Variáveis de ambiente importantes](#configurações--variáveis-de-ambiente-importantes)  


---

## Composição do projeto

1. **Desktop Client(`desktop-app/`)**

   * Aplicação Python para Windows
   * Monitora sessões e coleta dados das máquinas
   * Comunica-se com o backend via API REST

2. **Backend API (`web-app/backend/`)**

   * API REST em FastAPI
   * Gerencia autenticação, dados e operações do sistema
   * Banco SQLite (para desenvolvimento)

3. **Frontend (`web-app/frontend`)**

   * Interface React
   * Painel administrativo para gestão do sistema
   * Comunica-se com o backend via API REST

---

## Tecnologias principais

* **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Uvicorn
* **Frontend**: React 18, Vite, TailwindCSS, Axios
* **Desktop**: Python 3.11+, CustomTkinter, WMI (Windows)
* **Infraestrutura**: Docker, Docker Compose, Nginx
* **Banco de Dados**: SQLite (dev), PostgreSQL (prod recomendado)

---

## Pré-requisitos

* Docker e Docker Compose
* Python 3.11+ (para desenvolvimento)
* Node.js 18+ (para desenvolvimento frontend)

---

## Instalação e Execução

### Desenvolvimento
### Backend (API)
```bash
cd web-app/backend
python -m venv .venv 
source .venv/bin/activate #(Linux/Mac)
# .\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python -m main --create-db 
python -m main --run-server 
```

### Frontend (Web)
```bash
cd web-app/frontend
npm install # instalando dependências 
npm run dev # rodando ambiente de dev com Vite
```

### Desktop (Cliente)
```bash
cd desktop-app
python -m venv .venv
# Ativar venv conforme seu OS
pip install -r requirements.txt
# Configurar .env com BASE_URL e WEB_API_KEY
python -m main --run-app
```

### Produção com Docker
O projeto inclui um arquivo `docker-compose.yml` para orquestração de containers, seu funcionamento é:

1. **Frontend Service:**
* Constrói a imagem a partir do Dockerfile no diretório `frontend`
* Expõe a porta 8080 para acesso web
* Expõe a porta 8080 para acesso web
* Configurado para reinício automático

2. **Backend Service:**
* Constrói a imagem a partir do Dockerfile no diretório `backend`
* Expõe a porta 8000 para acesso web
* Carrega variáveis de ambiente do arquivo `backend/.env`
* Monta volume persistente para o banco de dados
* Configurado para reinício automático

Execução em Produção:

1. Clone o repositório

2. Configure as variáveis de ambiente (veja seção abaixo)

3. Execute:
```bash
cd web-app
docker-compose up --build -d
```

O sistema estará acessível em:

* Frontend: http://localhost:8080

* Backend API: http://localhost:8000

* Documentação da API: http://localhost:8000/docs

### Funcionalidades Implementadas no Nginx
O projeto inclui um arquivo `nginx.conf` que é crucial para segurança, performance e funcionamento adequado do sistema.

1. **Proxy Reverso:**
* Encaminha requisições `/api/` para o backend na porta 8000
* Encamiha requisições `/desktop-api/` para endpoints específicos para desktop
* Preserva headers originais para logs e auditoria

2. **Otimização de Performance:**
* Compressão GZIP para reduzir o tamanho de transferência
* Configuração de cache para arquivos estáticos (JS, CSS, imagens )

3. **Segurança**
* Headers de segurança (X-Frame-Options, X-Content-Type-Options, etc.)
* Prevenção de acesso a arquivos sensíveis (.env, .log, .git)
* Limite de tamanho para uploads (100MB)
* Configuração de CORS para recursos estáticos

## Configuração de Variáveis de Ambiente

### Backend (.env)
Crie o arquivo `web-app/backend/.env` com as seguintes variáveis:
```bash
WEB_API_KEY=sua_chave_secreta_aqui_32_caracteres
```
### Frontend (.env)
Crie o arquivo `web-app/frontend/.env` com as seguintes variáveis:
```bash
VITE_API_KEY=sua_chave_secreta_aqui_32_caracteres
VITE_API_URL=/api
```
### Desktop App (.env)
Crie o arquivo `desktop-app/.env` com as seguintes variáveis:
```bash
BASE_URL=http://localhost:8000
WEB_API_KEY=sua_chave_secreta_aqui_32_caracteres
```
---
## Estrutura do Projeto
```
tcc/
├── desktop-app/
│   ├── views/
│   ├── utils/
│   ├── api.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env
│   └── InfoDomusDesktop.bat
├── web-app/
│   ├── backend/
│   │   ├── routers/
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── .env
│   ├── frontend/
│   │   ├── src/
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .env
│   └── docker-compose.yml
└── README.md
```


## Configurações / Variáveis de ambiente importantes

Principais variáveis (exemplos encontrados no pacote):

* `WEB_API_KEY` — chave usada pelo cliente desktop para autenticar requisições ao backend.
* `BASE_URL` — URL base para a API (ex.: `http://localhost:8000` ou URL remota).
* `API_URL` — pode apontar para endpoints externos (ver `backend/.env`).
* `MACHINE_KEY` — chave identificadora de uma máquina específica.
* `PASSWORD`, `LAB_ID` — valores de configuração administrativa/identificação.

Coloque cada variável em um `.env` local e **não** comite essas informações.


