# E3 CRM — Mini-CRM WhatsApp

Mini-CRM com integração WhatsApp, autenticação Google e isolamento de dados por unidade de negócio.

**Frontend (Firebase Hosting):** https://e3-crm.web.app  
**Backend (Railway):** https://e3-crm-production.up.railway.app

---

## Setup local

### Pré-requisitos

- Node.js 20+ (via nvm recomendado)
- Python 3.11+
- pnpm (`npm install -g pnpm`)
- Docker e Docker Compose
- Conta Firebase com projeto criado

### 1. Clone o repositório

```bash
git clone https://github.com/GabrielLacerda00/e3-crm.git
cd e3-crm
```

### 2. Variáveis de ambiente

Crie `apps/api/.env`:

```env
DATABASE_URL=postgresql://e3user:e3pass@localhost:5432/e3crm
EVOLUTION_URL=http://localhost:8080
EVOLUTION_API_KEY=e3-evolution-key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

Adicione o arquivo `apps/api/firebase-credentials.json` com as credenciais do Firebase Admin SDK (obtido no Console Firebase → Configurações do projeto → Contas de serviço).

> Em produção (Railway), a variável `FIREBASE_CREDENTIALS_PATH` é substituída por `FIREBASE_CREDENTIALS` contendo o JSON das credenciais diretamente como string.

Crie `apps/web/.env.local`:

```env
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=...
NEXT_PUBLIC_FIREBASE_PROJECT_ID=...
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=...
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=...
```

### 3. Sobe o banco e a Evolution API

```bash
docker compose up -d
```

Isso inicia o PostgreSQL na porta 5432, o Redis na porta 6379 e a Evolution API na porta 8080.

> Em produção, o PostgreSQL é gerenciado pelo Railway, não é necessário rodar o Docker para o banco. A Evolution API continua rodando localmente via Docker e é exposta publicamente com ngrok.

### 4. Backend

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py        # cria as unidades e usuários iniciais
uvicorn main:app --reload --port 8000
```

O backend está deployado em produção no Railway em https://e3-crm-production.up.railway.app. O deploy é automático a cada push na branch `main`. Para rodar o seed em produção, acesse o Console do serviço no Railway e execute `python seed.py`.

### 5. Frontend

Na raiz do projeto, instale as dependências e inicie o frontend:

```bash
pnpm install
pnpm --filter web dev
```

Acesse http://localhost:3000.

O frontend utiliza Firebase Authentication para login com Google. As credenciais do Firebase (configuradas em `apps/web/.env.local`) conectam ao projeto Firebase em produção, o mesmo usado pelo deploy em https://e3-crm.web.app.

Para fazer o deploy do frontend em produção:

```bash
cd apps/web
pnpm build
firebase deploy
```

### 6. Conectar WhatsApp

Com a Evolution API rodando, acesse o painel em http://localhost:8080/manager e crie uma instância. Escaneie o QR Code com um número descartável.

Exponha a Evolution API publicamente com ngrok para que o backend em produção consiga enviar as auto-respostas:

```bash
ngrok http --url=sua-url.ngrok-free.dev 8080
```

Configure o webhook da instância para apontar para o backend em produção:

```
https://e3-crm-production.up.railway.app/webhook/{unit_id}
```

Defina `EVOLUTION_URL=https://sua-url.ngrok-free.dev` nas variáveis de ambiente do Railway.

---

## Decisões de arquitetura

O projeto foi estruturado como monorepo com pnpm workspaces, separando o frontend (`apps/web`) do backend (`apps/api`). Essa abordagem facilita o compartilhamento de tipos e configurações no futuro, mantém um único repositório para revisão de código e reflete como times maiores organizam projetos full-stack com múltiplos serviços.

Para o backend escolhi **FastAPI com Python** pela velocidade de desenvolvimento, tipagem nativa com Pydantic e suporte assíncrono. O banco de dados é **PostgreSQL** — relacional, maduro e ideal para o modelo de dados deste projeto (unidades → usuários → mensagens), com integridade referencial garantida por chaves estrangeiras. Para a integração WhatsApp usei a **Evolution API**, que permite conectar qualquer número via QR Code sem burocracia de aprovação, adequado para o contexto de teste.

O isolamento multi-unidade é implementado no backend: ao autenticar via Firebase, o sistema busca a `unit_id` do usuário e filtra todas as queries por essa unidade. O frontend é uma SPA estática exportada pelo Next.js e servida pelo Firebase Hosting, enquanto o backend roda no Railway com PostgreSQL gerenciado, separação limpa entre camadas sem custo de infraestrutura.

---

## O que faria diferente com mais tempo

- **Testes automatizados:** adicionaria testes nos endpoints críticos (webhook, autenticação, isolamento por unidade) com pytest e um banco de teste isolado.
- **Painel de conexão WhatsApp no frontend:** atualmente o QR Code é gerado via Evolution API diretamente. Com mais tempo, exibiria o QR Code dentro do próprio CRM para o gestor de cada unidade conectar seu número sem precisar acessar ferramentas externas.
- **WebSocket para mensagens em tempo real:** hoje o dashboard exibe mensagens ao fazer login. Implementaria uma conexão WebSocket para atualizar a lista em tempo real conforme novas mensagens chegam, sem necessidade de recarregar a página.
- **Gestão de usuários e unidades via painel:** o vínculo usuário→unidade hoje é feito via seed. Criaria uma interface simples de administração para gerenciar isso sem precisar rodar scripts.