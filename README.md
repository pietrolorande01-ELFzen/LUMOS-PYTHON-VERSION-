# LUMOS-PYTHON-VERSION-



#  Lumos — Sistema de Gerenciamento de Sessões de Recarga

Sistema que registra, armazena, busca, ordena e analisa sessões de recarga de
veículos elétricos. A interface é **Web (HTML/CSS/JS)** e **todo o processamento
— regras de negócio, tarifação, armazenamento, busca, ordenação e estatísticas —
é feito em Python**, exposto por uma API Flask.

```
Interface Web  ──fetch()──▶  app.py (rota Flask)  ──▶  SPRINT_DSA_Completa.py
     ▲                                                        │
     └──────────────── JSON com o resultado ◀─────────────────┘
```

---

##  Problema

Estações de recarga precisam controlar muitas sessões ao mesmo tempo: quem
carregou, quanto de energia foi entregue, quanto custou e de onde veio essa
energia (solar, bateria ou rede). Sem um sistema, fica difícil encontrar uma
sessão específica, comparar consumo entre sessões e fechar o faturamento.

O Lumos simula um **totem de recarga inteligente** com bateria de apoio
(Lynx) e energia solar. Cada recarga vira uma **sessão** com tarifa calculada
automaticamente, e o operador da estação consegue listar, buscar, ordenar e
gerar estatísticas e relatórios dessas sessões.

### Evolução do projeto

| Versão | Entrega |
|---|---|
| 1 | Simulador de recarga no terminal (uma sessão, tarifa por bandeira) |
| 2 | Múltiplas sessões, persistência em JSON, simulação OCPP/Modbus, relatórios |
| 3 | Busca (sequencial e binária), ordenação (Bubble Sort) e estatísticas |
| 4 | API Flask + interface Web integrada, Merge Sort, contador de operações e laboratório de complexidade |

---

##  Estrutura do projeto

```
lumos/
├── app.py                  ← API Flask: recebe os pedidos do site e chama o Python
├── SPRINT_DSA_Completa.py  ← backend: sessões, tarifação, busca, ordenação, estatísticas
├── requirements.txt        ← dependência (Flask)
├── .gitignore
├── sessoes_totem.json      ← criado automaticamente: onde as sessões ficam salvas
└── site/                   ← interface Web
    ├── api.js              ← funções fetch() que conversam com a API
    ├── index.html          ← login
    ├── home.html           ← painel do usuário (lista as sessões vindas do Python)
    ├── carregamento.html   ← nova recarga (cria a sessão no Python)
    ├── estacao.html        ← Painel da Estação: busca, ordenação, estatísticas,
    │                          relatório e laboratório de complexidade
    └── ...                 ← demais páginas (consumo, pagamento, Lummi, Lumos Corp…)
```

| Arquivo | Responsabilidade |
|---|---|
| `SPRINT_DSA_Completa.py` | Toda a lógica: `criar_sessao()`, `calcular_tarifa()`, `calcular_potencia_disponivel()`, `busca_sequencial()`, `busca_binaria()`, `bubble_sort_sessoes()`, `merge_sort_sessoes()`, `calcular_estatisticas()`, `exportar_relatorio_txt()`, além do menu de terminal |
| `app.py` | Define as rotas `/api/...`, converte o pedido do site em chamada de função Python e devolve JSON. Também imprime um log de cada operação no terminal |
| `site/api.js` | `lumosGet()` / `lumosPost()`: centraliza o `fetch()` para a API |
| `site/carregamento.html` | Fluxo de recarga: pagamento → conexão → carregando → concluído. Envia `POST /api/sessoes` |
| `site/estacao.html` | Painel do operador: mostra os algoritmos rodando e quantas comparações cada um fez |

---

##  Tecnologias

- **Backend:** Python 3.10+, Flask
- **Interface:** HTML, CSS e JavaScript puro (`fetch` para a API)
- **Persistência:** arquivo JSON

---

##  Como rodar

### Pré-requisito

**Python 3.10 ou superior.** Confira com:

```bash
python --version      # Windows
python3 --version     # macOS / Linux
```

Se não tiver, baixe em <https://www.python.org/downloads/> (no Windows, marque
**"Add python.exe to PATH"** na instalação).

### Baixar o projeto

```bash
git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
cd <seu-repositorio>/lumos
```

Ou baixe o ZIP pelo botão **Code → Download ZIP** no GitHub e extraia.

### Windows (PowerShell ou Prompt de Comando)

```powershell
cd caminho\para\lumos
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

> Se o PowerShell bloquear o `activate` com erro de "execução de scripts",
> rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
> e tente de novo. Ou use o Prompt de Comando (cmd), que não tem essa trava.

### macOS / Linux

```bash
cd caminho/para/lumos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Abrir o sistema

Com o servidor rodando, abra no navegador: **<http://localhost:5000>**

O terminal deve mostrar:

```
============================================================
  LUMOS — backend Python rodando
  Abra no navegador: http://localhost:5000
  Sessoes carregadas do JSON: 0
============================================================
```

Para parar o servidor: **Ctrl + C** no terminal.

Da próxima vez, basta entrar na pasta, ativar o ambiente (`.venv\Scripts\activate`
ou `source .venv/bin/activate`) e rodar `python app.py`.

### Modo terminal (versão anterior, sem interface Web)

```bash
python SPRINT_DSA_Completa.py
```

Abre o menu de texto com as mesmas funções. Os dois modos usam o mesmo
`sessoes_totem.json`.

### Problemas comuns

| Sintoma | Solução |
|---|---|
| Página abre mas aparece "Backend offline" | O site foi aberto com duplo clique no `.html`. Abra pelo endereço `http://localhost:5000` com o `app.py` rodando |
| `Address already in use` / porta 5000 ocupada (comum no macOS) | Desligue o **Receptor AirPlay** em Ajustes do Sistema → Geral → AirDrop e Handoff, ou troque `port=5000` por `port=5001` na última linha do `app.py` e acesse `http://localhost:5001` |
| `ModuleNotFoundError: No module named 'flask'` | O ambiente virtual não está ativo ou o `pip install -r requirements.txt` não foi rodado |
| `python` não é reconhecido (Windows) | Use `py app.py` ou reinstale o Python marcando "Add to PATH" |
| Sessões "somem" ou aparecem em outro lugar | Rode o `app.py` **de dentro da pasta `lumos/`**: o `sessoes_totem.json` é salvo na pasta de onde o comando foi executado |

---

##  Como usar

1. **Login** (`index.html`): nome, e-mail, token de 6 dígitos e veículo.
2. **Nova recarga** (`carregamento.html`): escolha o pagamento → conecte o
   veículo → a sessão é criada no Python e a animação mostra a recarga.
3. **Home**: a sessão aparece na listagem (vinda de `GET /api/sessoes`).
4. **Estação** (`estacao.html`):
   - **Buscar sessão por ID** com busca sequencial ou binária;
   - **Ordenar** por energia, custo, duração ou ID com Bubble Sort ou Merge Sort;
   - **Estatísticas** no topo (total, energia, faturamento, ticket médio, maior/menor consumo);
   - **Relatório final (.txt)** gerado pelo Python;
   - **Laboratório de complexidade**: `+10`, `+100`, `+1000` sessões e **Medir**.

---

## Rotas da API

| Ação na interface | Rota | Função Python |
|---|---|---|
| Iniciar recarga | `POST /api/sessoes` | `criar_sessao()` → `calcular_tarifa()`, `calcular_potencia_disponivel()` |
| Listar sessões | `GET /api/sessoes` | lista `sessoes` |
| Buscar por ID | `GET /api/sessoes/busca?id=...&algoritmo=sequencial\|binaria` | `busca_sequencial()` / `busca_binaria()` |
| Ordenar | `GET /api/sessoes/ordenar?criterio=...&ordem=asc\|desc&algoritmo=bubble\|merge` | `bubble_sort_sessoes()` / `merge_sort_sessoes()` |
| Estatísticas | `GET /api/estatisticas` | `calcular_estatisticas()` |
| Relatório final | `GET /api/relatorio.txt` | `exportar_relatorio_txt()` |
| Gerar dados de teste | `POST /api/sessoes/gerar` | `criar_sessao()` × N |
| Zerar sessões | `DELETE /api/sessoes` | `sessoes.clear()` |

---

##  Estrutura de dados

**Uma sessão é um dicionário** (criado em `criar_sessao()`):

```python
sessao = {
    "id": "SESS-0001-20261017",   # chave de busca
    "usuario": "Usuário Exemplo",
    "token": "000000",
    "data": "17/10/2026", "inicio": "15:39:04", "fim": "17:09:04",
    "duracao_min": 90,
    "marca_carro": "BYD Dolphin",
    "bateria_inicial": 68, "bateria_final": 79.1,
    "bateria_lynx": 23, "fonte": "Rede de Apoio", "bandeira": "Verde",
    "potencia_kw": 7.4,
    "energia_kwh": 11.097,
    "tarifa": 1.6, "taxa_fixa": 15,
    "valor_energia": 17.76, "valor_total": 32.76,
    "co2_evitado_kg": 2.33,
    "pagamento_nome": "PIX (Governo)",
    ...
}
```

**Várias sessões ficam em uma lista** (`sessoes`), carregada do
`sessoes_totem.json` ao iniciar e salva a cada alteração.

**Por quê:**
- o dicionário dá nome a cada campo e o acesso `sessao["id"]` é **O(1)** (tabela hash);
- a lista mantém a **ordem de cadastro**, aceita `append()` em **O(1)** e permite
  acesso por índice, que a busca binária e os algoritmos de ordenação precisam;
- lista de dicionários vira JSON direto, tanto para salvar em arquivo quanto
  para enviar ao site.

---

##  Busca (chave: `id`)

| Algoritmo | Como funciona | Termina quando | Big-O |
|---|---|---|---|
| `busca_sequencial()` | Percorre a lista do índice 0 até o fim comparando `sessoes[i]["id"]` | Acha o ID ou chega ao fim | **O(n)** |
| `busca_binaria()` | Olha o meio; se o ID procurado é maior, descarta a metade esquerda; se menor, a direita | Acha o ID ou `baixo > alto` (intervalo vazio) | **O(log n)** |

A busca binária exige a lista ordenada por ID. Como os IDs são gerados em
ordem crescente (`SESS-0001`, `SESS-0002`…), `preparar_busca_binaria()` apenas
**confere** a ordem em O(n). Só se estiver fora de ordem ela ordena uma cópia
com Merge Sort.

##  Ordenação (campos: `energia_kwh`, `valor_total`, `duracao_min`, `id`)

Implementações próprias, **sem `sort()` nem `sorted()`**:

| Algoritmo | Como funciona | Big-O |
|---|---|---|
| `bubble_sort_sessoes()` | Compara vizinhos `j` e `j+1`; se estão fora de ordem, troca. Cada passada leva o maior para o fim. A flag `trocou` encerra cedo se a lista já estiver ordenada | **O(n²)** (melhor caso O(n)) |
| `merge_sort_sessoes()` | Divide a lista ao meio recursivamente até sobrar 1 elemento e intercala as metades comparando o primeiro de cada | **O(n log n)** |

A ordenação é feita numa **cópia** (`sessoes[:]`), então a lista original
continua em ordem de ID, e a busca binária continua barata.

## 📈 Complexidade medida (pior caso)

Busca por ID inexistente e ordenação por energia, números de comparações
contados pelo próprio código:

| n | Sequencial O(n) | Binária O(log n) | Bubble Sort O(n²) | Merge Sort O(n log n) |
|---:|---:|---:|---:|---:|
| 10 | 10 | 4 | ~45 | ~25 |
| 100 | 100 | 7 | ~4.800 | ~540 |
| 1.000 | 1.000 | 10 | ~498.000 | ~8.700 |

(Os valores de ordenação variam um pouco porque os dados de teste são aleatórios.)

**Leitura:** multiplicar n por 10 multiplica a busca sequencial por 10
(linear), soma ~3 comparações na binária (logarítmica), multiplica o Bubble
Sort por ~100 (quadrático) e o Merge Sort por pouco mais de 10 (n log n).

Exemplos de **O(1)** no código: `sessoes.append(sessao)`, `len(sessoes)` e
`sessao["id"]`.

`calcular_estatisticas()` é **O(n)**: uma única passada pela lista somando
energia e faturamento e guardando maior e menor consumo (sem `max()`/`min()`).

---

##  Tarifação (`calcular_tarifa()`)

| Bateria Lynx | Fonte | Tarifa |
|---|---|---|
| ≥ 70% | Solar + Bateria Lynx | R$ 0,85/kWh |
| 40% a 69% | Bateria Parcial | R$ 1,20/kWh |
| < 40% | Rede de Apoio | R$ 1,60/kWh + bandeira (Verde +0, Amarela +0,20, Vermelha +0,45) |

- Madrugada (00h–06h): **−R$ 0,20/kWh**
- **Valor total = energia (kWh) × tarifa + taxa fixa de R$ 15,00**
- Potência limitada pela bandeira (22 / 15 / 7,4 kW), pela carga da bateria
  Lynx e pelo número de sessões simultâneas (`calcular_potencia_disponivel()`).

---

##  Evoluções futuras

- Persistência em banco de dados (SQLite/PostgreSQL) com índice por ID;
- Autenticação real de usuários (hoje o login fica no navegador);
- Integração OCPP com carregadores reais;
- Tarifação dinâmica por horário e demanda da rede;
- Múltiplas estações e app Mobile;
- Lumos Corp: gestão de frotas e relatórios por veículo.

---

## Funcionalidades × onde estão no código

| Funcionalidade | Onde |
|---|---|
| Backend em Python | `SPRINT_DSA_Completa.py` + `app.py` |
| Cadastro / início de sessão | Nova recarga → `POST /api/sessoes` → `criar_sessao()` |
| Armazenamento de múltiplas sessões | lista `sessoes` + `sessoes_totem.json` |
| Listagem | Home e Estação → `GET /api/sessoes` |
| Busca | Estação → `busca_sequencial()` / `busca_binaria()` |
| Ordenação (algoritmo próprio) | Estação → `bubble_sort_sessoes()` / `merge_sort_sessoes()` |
| Estatísticas | Estação → `calcular_estatisticas()` |
| Tarifação | `calcular_tarifa()` |
| Relatório final | Estação → `exportar_relatorio_txt()` |
| Integração interface ↔ backend | `site/api.js` → `app.py` → funções Python → JSON |

---

##  Dados locais

O `sessoes_totem.json` e os `relatorio_*.txt` são gerados na sua máquina e
podem conter nomes e tokens digitados no site. Eles estão no `.gitignore` para
não irem para o GitHub.
