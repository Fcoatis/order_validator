# Order Validator (Financial Compliance Engine)

Este projeto é um motor de validação de ordens financeiras de alta performance, desenhado para demonstrar a evolução de código legado ("spaghetti") para uma arquitetura limpa, modular e testável, seguindo princípios **SOLID** e **Specification Pattern**.

## 🚀 Tecnologias

- **Python 3.14+** (Linguagem base)
- **uv** (Gerenciador de pacotes e ambientes virtuais ultrarrápido)
- **Pytest** (Framework de testes)
- **Pytest-Cov** (Análise de cobertura de código)

## 🏗 Arquitetura

O projeto utiliza o **Specification Pattern** para desacoplar as regras de negócio da lógica de orquestração. Isso permite que novas regras de compliance sejam adicionadas sem modificar o código existente (Open/Closed Principle).

### Estrutura de Pastas

```text
order_validator/
├── app/
│   ├── main.py       # Orquestrador: Combina as specs para tomar decisão
│   ├── models.py     # Domínio: Definição de Order, User, Item
│   └── rules.py      # Motor de Regras: Specifications puras (Lego blocks)
├── tests/
│   └── test_main.py  # Testes de unidade e integração
├── pyproject.toml    # Dependências e metadados (gerenciado pelo uv)
└── uv.lock           # Versões travadas (reprodutibilidade)
```

## 🛠 Como Executar

Este projeto utiliza o uv para gestão zero-config. Não é necessário criar venv manualmente.

### 1. Instalação

```bash
# Instala dependências e cria ambiente virtual automaticamente
uv sync
```

### 2. Rodar Testes

```bash
# Executa a suíte de testes completa
uv run pytest -v
```

### 3. Verificar Cobertura

```bash
# Gera relatório de cobertura (Meta: 100%)
uv run pytest --cov=app tests/
```

## 🧠 Regras de Negócio Implementadas

O motor valida ordens combinando as seguintes especificações lógicas:

### Regras de Perfil

- Usuários Admin aprovam automaticamente (se não forem Premium).
- Usuários Premium têm fluxo diferenciado.

### Regras de Valor

- Baixo Valor (<= 1000): Aprovado se for "Bulk" e usuário não for Trial.
- Alto Valor (> 1000): Proibido descontos.

### Compliance Regional

- EU (Europa): Moeda deve ser obrigatoriamente EUR.
- Global (Non-EU): Validação de sanidade de preços (item price >= 0).

### Segurança de Ativos (Global Constraint)

- Bitcoin (BTC): Se valor > 2000, exige usuário Premium (Trava de Segurança).

## 📜 Histórico de Refatoração

Este repositório documenta a jornada de refatoração:

- Legacy: Código monolítico com ifs aninhados (Arrow Code).
- Guard Clauses: Achatamento da lógica condicional.
- Extract Method: Separação de responsabilidades (SRP).
- Specification Pattern: Transformação de regras em objetos componíveis.
- Modularização: Separação física em models, rules e orchestrator.

---

### Passo 2: Commit da Documentação

Agora, vamos salvar essa documentação no histórico do Git.

No terminal:

```bash
git add README.md
git commit -m "docs: adiciona documentação técnica do projeto e arquitetura"
```
