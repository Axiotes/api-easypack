# EasyPack — API

Backend do EasyPack: sistema de controle de pacotes e correções aplicados em
ambientes de clientes, com rastreabilidade de quem fez o quê (aprovação de
code review, aprovação do Gerente de Projeto, aplicação do pacote, histórico
de operações). Projeto da disciplina de Fábrica de Software.

Repositório do frontend (Angular): [app-easypack](https://github.com/Axiotes/app-easypack).

## Stack

- **Python 3.13** + [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/) (migrações)
- **MySQL 8**
- Autenticação via JWT (`PyJWT`) + senhas com `bcrypt`
- [pyopencl](https://documen.tician.de/pyopencl/) — checksum de integridade calculado em paralelo
  na GPU (ou CPU, se não houver GPU) nas listagens mais acessadas; ver `app/core/opencl_utils.py`
- [pytest](https://docs.pytest.org/) — testes automatizados com SQLite em memória

## Pré-requisitos

- Python 3.13+
- MySQL 8 rodando localmente (ou acessível via rede)
- Opcional: um driver/runtime OpenCL instalado (GPU da Intel/NVIDIA/AMD, ou um runtime de CPU).
  Sem isso, o sistema continua funcionando normalmente — só deixa de calcular o checksum de
  integridade nas listagens.

## Configuração do ambiente

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

Crie o banco `EasyPack` no MySQL e copie `.env.example` para `.env`, ajustando as credenciais:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=EasyPack

SECRET_KEY=troque-por-uma-chave-secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Aplique as migrações (criam as tabelas e já inserem um catálogo de exemplo — setores,
produtos, subsetores, usuários, clientes, correções e pacotes):

```bash
alembic upgrade head
```

## Executando

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa (Swagger) em
`http://localhost:8000/docs`, e Redoc em `http://localhost:8000/redoc`.

### Usuários de exemplo (seed)

Todos com senha `admin123`:

| usuário | cargo | subsetor | produto |
|---|---|---|---|
| maria.silva | Coordenador | Gerencia GPs ST | — |
| bruno.silva | Gerente de Projeto | Dev Soul ST | Soul |
| henrique.melo | Pleno | Dev Soul FB | Soul |
| lucas.barros | Coordenador | Gerencia GPs FB | — |

(a lista completa está na migração `9b7c3d1e2f4a_seed_release_governance_catalog.py`)

## Testes automatizados

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes rodam contra um banco SQLite em memória (não usam o MySQL configurado em `.env`)
e cobrem as principais regras de negócio: autenticação, aprovação de code review, aplicação
de pacote, gestão de usuários/clientes e histórico de operações.

## Estrutura do projeto

```
app/
  api/v1/endpoints/   rotas (FastAPI routers)
  core/               config, segurança (JWT/bcrypt), regras transversais (cargo, produto, auditoria, OpenCL)
  models/             entidades (SQLAlchemy)
  repositories/       acesso a dados
  schemas/            contratos de entrada/saída (Pydantic)
  services/           regras de negócio
alembic/versions/     migrações do banco
tests/                testes automatizados (pytest)
```

## Principais regras de negócio

- Code review de uma correção só pode ser aprovado por um usuário de cargo de
  desenvolvimento (Especialista, Senior, Pleno ou Junior) do setor Fábrica, no mesmo produto.
- Uma correção só pode ser marcada como mergeada se o code review já estiver aprovado, e só
  por um usuário do mesmo setor (Fábrica/Serviços Técnicos) da correção.
- Um pacote só pode ser aprovado pelo Gerente de Projeto após o code review aprovado, e só
  pode ser aplicado após as duas aprovações.
- Usuário só aplica pacote do seu próprio produto (com acesso cruzado: Soul/PEP também
  cobrem Pagu; Soul também cobre Portaria); Gerente de Projeto fica isento dessa regra.
- Estagiário precisa da aprovação de outro usuário do mesmo subsetor (Pleno, Senior,
  Especialista ou Coordenador) para aplicar um pacote.
- Coordenador só gerencia usuários do próprio subsetor, com cargo abaixo de Coordenador.
- Apenas Gerente de Projeto gerencia clientes (cadastro/edição/exclusão).
- Todas essas operações (e as de usuários/clientes) ficam registradas no histórico de
  operações (`/logs`), consultável por Coordenador e Gerente de Projeto.
