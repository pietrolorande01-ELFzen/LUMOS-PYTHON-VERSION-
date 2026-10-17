# Lumos — Sprint 4: integração Interface Web ↔ Backend Python

## Estrutura

```
lumos/
├── app.py                  ← API Flask (a "ponte" entre o site e o Python)
├── SPRINT_DSA_Completa.py  ← backend: estruturas, busca, ordenação, tarifação
├── requirements.txt
└── site/                   ← interface Web (HTML/CSS/JS)
    ├── api.js              ← funções fetch() que chamam a API
    ├── estacao.html        ← NOVO: Painel da Estação (busca, ordenação, estatísticas, relatório)
    ├── carregamento.html   ← agora cria a sessão no Python (POST /api/sessoes)
    ├── home.html           ← agora lista as sessões vindas do Python
    └── ... demais páginas
```

## Como rodar (3 comandos)

```bash
cd lumos
pip install -r requirements.txt
python app.py
```

Depois abra **http://localhost:5000** no navegador.

> Importante: abra pelo endereço `http://localhost:5000`. Abrir o `.html` com
> duplo clique não funciona, porque a página precisa do servidor Python.

O terminal mostra cada pedido que chega do site, por exemplo:

```
[LUMOS API][19:39:00] POST /api/sessoes -> SESS-0001-20261007 criada | 11.097 kWh x R$ 1.2/kWh + R$ 15 = R$ 28.32
[LUMOS API][19:39:00] GET /api/sessoes/busca -> Busca binária por 'SESS-0501...' | n=1000 | 9 comparacoes | achou
```

Deixe esse terminal visível ao lado do navegador no vídeo: é a prova da integração.

O menu de terminal antigo continua funcionando com `python SPRINT_DSA_Completa.py`.
Os dois modos usam o mesmo arquivo `sessoes_totem.json`.

## Rotas da API

| Ação na interface | Rota | Função Python chamada |
|---|---|---|
| Iniciar recarga | `POST /api/sessoes` | `criar_sessao()` → `calcular_tarifa()`, `calcular_potencia_disponivel()` |
| Listar sessões | `GET /api/sessoes` | lista `sessoes` |
| Buscar por ID | `GET /api/sessoes/busca?id=...&algoritmo=sequencial\|binaria` | `busca_sequencial()` / `busca_binaria()` |
| Ordenar | `GET /api/sessoes/ordenar?criterio=...&ordem=asc\|desc&algoritmo=bubble\|merge` | `bubble_sort_sessoes()` / `merge_sort_sessoes()` |
| Estatísticas | `GET /api/estatisticas` | `calcular_estatisticas()` |
| Relatório final | `GET /api/relatorio.txt` | `exportar_relatorio_txt()` |
| Gerar dados de teste | `POST /api/sessoes/gerar` | `criar_sessao()` × N |

## O que mudou no Python

- **`criar_sessao()`**: a mesma regra de negócio de `executar_sessao()`, sem `input()`/`sleep()`, para a API poder chamar. Valida nome, token (6 dígitos), forma de pagamento, bateria e tempo.
- **`calcular_tarifa()`**: a regra de tarifação foi isolada em uma função.
- **`merge_sort_sessoes()`**: novo, O(n log n), para comparar com o Bubble Sort O(n²).
- **Contador de comparações** (parâmetro opcional `contador`) nas buscas e ordenações. É assim que o site mostra quantas operações cada algoritmo fez.
- **Busca binária corrigida**: antes, o menu rodava Bubble Sort (O(n²)) antes de toda busca binária. Agora `preparar_busca_binaria()` primeiro verifica se a lista já está ordenada por ID, em O(n). Ela normalmente está, porque os IDs são gerados em ordem crescente. Só ordena (com Merge Sort, numa cópia) se precisar.
- **Ordenação não altera mais a lista original**: ordena uma cópia, então a lista principal continua em ordem de ID.
- **`calcular_estatisticas()`**: devolve um dicionário, usado pelo terminal e pela API.

## Medições reais (pior caso: busca por ID inexistente, ordenação por energia)

| n | Busca sequencial O(n) | Busca binária O(log n) | Bubble Sort O(n²) | Merge Sort O(n log n) |
|---:|---:|---:|---:|---:|
| 10 | 10 | 3 | 42 | 23 |
| 100 | 100 | 6 | 4.922 | 548 |
| 1.000 | 1.000 | 9 | 499.364 | 8.725 |

Leitura para o vídeo: multiplicar n por 10 multiplica a busca sequencial por 10 (linear), soma ~3 comparações na binária (logarítmica), multiplica o Bubble Sort por ~100 (quadrática) e multiplica o Merge Sort por pouco mais de 10 (n log n).

Exemplos de **O(1)** no código: `sessoes.append(sessao)`, `len(sessoes)` e o acesso `sessao["id"]` (o dicionário é uma tabela hash).

## Roteiro sugerido para o vídeo (5–8 min, 6 integrantes)

1. **Abertura (~40 s):** disciplina, turma, nomes, RMs, projeto Lumos. Problema e evolução das Sprints (simulador → gerenciador de sessões → integração Web).
2. **Demo (~1 min 30):** `python app.py` no terminal; login no site; **Nova recarga** (pagamento → conectar → carregando); mostrar o terminal registrando o `POST /api/sessoes` e o valor calculado em Python. Voltar à Home e mostrar a sessão na listagem.
3. **Estrutura de dados (~1 min):** no código, o dicionário da sessão em `criar_sessao()`, a lista `sessoes`, o `append()` e o JSON. Fluxo: `api.js` (fetch) → `app.py` (rota) → função Python → JSON → tela.
4. **Busca (~1 min):** no Painel da Estação, buscar um ID com sequencial e com binária; mostrar o código das duas funções e a condição de parada.
5. **Ordenação (~1 min):** ordenar por energia com Bubble e com Merge; mostrar o código; explicar comparação e troca/intercalação.
6. **Complexidade + considerações finais (~1 min 30):** Laboratório: +10 → Medir, +100 → Medir, +1000 → Medir; ler a tabela. Fechar com evoluções futuras: banco de dados, autenticação real, app mobile, integração OCPP com carregadores reais, Lumos Corp para frotas.
