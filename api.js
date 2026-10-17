// ==========================================================
// LUMOS — cliente da API Python (Sprint 4)
// Toda comunicação Interface -> Backend Python passa por aqui.
// ==========================================================

async function lumosApi(caminho, opcoes) {
  let resp;
  try {
    resp = await fetch(caminho, Object.assign({ headers: { 'Content-Type': 'application/json' } }, opcoes || {}));
  } catch (e) {
    throw new Error('Backend Python offline. Rode "python app.py" e abra http://localhost:5000');
  }
  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(dados.erro || ('Erro ' + resp.status));
  return dados;
}

function lumosGet(caminho) { return lumosApi(caminho); }
function lumosPost(caminho, corpo) { return lumosApi(caminho, { method: 'POST', body: JSON.stringify(corpo || {}) }); }

function brl(v) { return 'R$ ' + Number(v || 0).toFixed(2).replace('.', ','); }
