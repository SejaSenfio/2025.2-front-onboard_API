# 🎟️ Challenge Backend - Sistema de Resgate de Cupons

## 📋 Sobre o Projeto

Este é um sistema backend desenvolvido para gerenciar **cupons de desconto** e **resgates de usuários**. O projeto foi desenvolvido como parte do desafio de onboarding da **Senfio**, utilizando Django REST Framework com autenticação JWT.

### 🎯 Funcionalidades Principais

- **Autenticação de Usuários**: Sistema completo de login/logout com JWT
- **Gestão de Cupons**: Criação e gerenciamento de cupons de desconto
- **Sistema de Resgates**: Controle de resgates por usuário com validações
- **Controle de Permissões**: Diferenciação entre usuários comuns e administradores
- **API RESTful**: Endpoints bem documentados com Swagger/OpenAPI
- **Validações de Negócio**: Controle de limites de uso e disponibilidade

## 🏗️ Arquitetura do Sistema

### 🎪 Modelos Principais

#### 👤 User (Usuário)
- **Email**: Identificação única do usuário
- **Team**: Equipe do usuário (Tecnologia, Marketing, Vendas, etc.)
- **Works Since**: Data de entrada na empresa
- **Permissões**: Controle de acesso (staff/admin)

#### 🎟️ Coupon (Cupom)
- **Code**: Código único de resgate
- **Description**: Descrição do cupom
- **Max Redemptions**: Limite máximo de resgates
- **Available**: Status de disponibilidade
- **Validações**: Controle de limites e disponibilidade

#### 🎁 Redemption (Resgate)
- **User**: Usuário que realizou o resgate
- **Coupon**: Cupom resgatado
- **Redeemed At**: Data/hora do resgate
- **Validações**: Controle de limites por usuário e cupom

### 🔐 Sistema de Autenticação JWT

O projeto utiliza **Django REST Framework Simple JWT** com as seguintes configurações:

```python
# Configurações JWT
ACCESS_TOKEN_LIFETIME = 2 minutos      # Token de acesso
REFRESH_TOKEN_LIFETIME = 1 dia         # Token de refresh
ALGORITHM = "HS384"                    # Algoritmo de criptografia
ROTATE_REFRESH_TOKENS = True           # Rotação automática de tokens
BLACKLIST_AFTER_ROTATION = True       # Blacklist de tokens antigos
```

#### 🔑 Endpoints de Autenticação
- `POST /api/v1/auth/login` - Login do usuário
- `POST /api/v1/auth/refresh` - Renovação do token
- `POST /api/v1/auth/logout` - Logout com blacklist do token
- `POST /api/v1/auth/register` - Registro de novo usuário
- `GET /api/v1/auth/me` - Dados do usuário autenticado
- `POST /api/v1/auth/change-password` - Alteração de senha
- `GET /api/v1/auth/users` - Listagem de usuários (admin)

#### 🛡️ Como Usar o JWT

1. **Login**: Envie email e senha para `/auth/login`
2. **Resposta**: Receba `access_token` e `refresh_token`
3. **Autenticação**: Use o header `Authorization: Bearer <access_token>`
4. **Renovação**: Use o `refresh_token` em `/auth/refresh` quando necessário

### 🎟️ Sistema de Cupons

#### 📋 Endpoints de Cupons
- `GET /api/v1/coupons/` - Listar cupons disponíveis
- `POST /api/v1/coupons/` - Criar cupom (apenas admin)
- `GET /api/v1/coupons/{id}/` - Detalhes de um cupom
- `PUT/PATCH /api/v1/coupons/{id}/` - Atualizar cupom (apenas admin)
- `DELETE /api/v1/coupons/{id}/` - Deletar cupom (apenas admin)

#### 🎁 Endpoints de Resgates
- `GET /api/v1/coupons/redemptions/` - Listar resgates do usuário
- `POST /api/v1/coupons/redemptions/` - Resgatar cupom
- `GET /api/v1/coupons/redemptions/{id}/` - Detalhes de um resgate
- `GET /api/v1/coupons/balance/` - Saldo de cupons do usuário
- `GET /api/v1/coupons/recent-redemptions/` - Resgates recentes

#### ⚡ Regras de Negócio

1. **Criação de Cupons**: Apenas administradores podem criar cupons
2. **Limite de Resgates**: 
   - Se `max_redemptions` for `null`: cupom de uso único por usuário
   - Se `max_redemptions` for um número: limite específico por usuário
3. **Disponibilidade**: Cupons podem ser ativados/desativados
4. **Validações**: Sistema impede resgates duplicados e excesso de limites

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos

- **Docker** e **Docker Compose**
- **Python 3.12+** (para desenvolvimento local)
- **Poetry** (gerenciador de dependências)

### 🐳 Execução com Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone <repository-url> challenge-backend
cd challenge-backend
```

2. **Execute com Docker Compose**
```bash
# Subir os serviços
docker-compose up 

# OU usando Makefile
make up
```

3. **Acesse a aplicação**
- **API**: http://localhost
- **Documentação**: http://localhost/api/v1/docs

4. **Auto criação de dados**
- O arquivo `infra/scripts/run.sh (Entrypoint do projeto)` já cria diversos usuários e cupons para uso inicial. Todos os dados de criação são exibidos nos logs do container.

### 🏗️ Estrutura do Projeto

```
src/
├── authentication/     # Módulo de autenticação
├── coupons/           # Módulo de cupons e resgates
├── config/            # Configurações do Django
├── shared/            # Utilitários compartilhados
└── api/               # Configurações da API
```

## 📊 Banco de Dados

O projeto usa **PostgreSQL** como banco de dados principal. As principais tabelas são:

- `authentication_user` - Usuários do sistema
- `coupons_coupon` - Cupons disponíveis
- `coupons_redemption` - Resgates realizados

## 🧪 Testes

Execute os testes com:

```bash
# Com Docker
make test
```

## 📚 Documentação da API

A documentação completa da API está disponível em:
- **Swagger UI**: http://localhost/api/v1/docs
- **OpenAPI Schema**: http://localhost/api/v1/schema/

## 📄 Licença

Este projeto foi desenvolvido como parte do processo de onboarding da **Senfio**.
Uso EXCLUSIVO para Senfio e não deve ser utilizado para fins comerciais sem autorização prévia.

---

### 🎯 Principais Tecnologias

- **Django 5.2+**
- **Django REST Framework**
- **Simple JWT**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Poetry**
- **Pytest**
- **drf-spectacular (Swagger)**

---

**Desenvolvido com ❤️ para o desafio de onboarding da Senfio**