// Levanta todas as frases fixas que o assistente fala, rodando a própria lógica do Main.dc.html
// em cada tela e cenário. Não chama nenhum serviço e não gasta crédito.
// Uso: node scripts/coletar-frases.mjs   ->  escreve scripts/frases-demo.json
import fs from 'node:fs';
import { textoFalado } from '../src/voz/normalizar.mjs';

const raw = fs.readFileSync(new URL('../referencia/Main.dc.html', import.meta.url), 'utf8');
const m = /<script type="text\/x-dc" data-dc-script[^>]*>([\s\S]*?)<\/script>/.exec(raw);
class DCLogic {
  constructor() { this.props = {}; this.state = {}; }
  setState(p) { this.state = Object.assign({}, this.state, typeof p === 'function' ? p(this.state) : p); }
}
globalThis.window = { innerWidth: 1440, localStorage: { getItem() { return null; }, setItem() {} }, addEventListener() {}, removeEventListener() {} };
const Component = new Function('DCLogic', m[1] + '\nreturn Component;')(DCLogic);

const frases = new Map(); // texto falado (normalizado) -> texto original
const add = (t) => { if (t && String(t).trim()) frases.set(textoFalado(t), String(t)); };

const novo = (state) => {
  const c = new Component();
  c.toast = () => {};
  c.fala = (t) => add(t);
  Object.assign(c.state, state);
  return c;
};

const telas = ['inicio', 'cobrancas', 'criar', 'confirmacao', 'pix', 'extrato', 'notas', 'links'];
const combos = [];
for (const dados of [true, false]) for (const nfDone of [false, true]) combos.push({ dados, nfDone });

for (const { dados, nfDone } of combos) {
  for (const tela of telas) {
    const estado = { tela, dados, nfDone, nudgeFor: tela + '|' + dados };
    // 1. frase de abertura do painel (a primeira mensagem)
    const v = novo(estado).renderVals();
    const msgs = v.ag.msgs;
    add(msgs[msgs.length - 1].text);
    // 2. respostas dos botões da abertura (ex.: "Reenviar as 3")
    const nAcoes = (msgs[msgs.length - 1].actions || []).length;
    for (let i = 0; i < nAcoes; i++) {
      const c = novo(estado);
      const a = c.renderVals().ag.msgs.slice(-1)[0].actions[i];
      try { a.go(); } catch (e) { /* ação só de navegação */ }
    }
    // 3. respostas às perguntas sugeridas
    const nSug = v.ag.sugs.length;
    for (let i = 0; i < nSug; i++) {
      const c = novo(estado);
      try { c.renderVals().ag.sugs[i].go(); } catch (e) { /* ignora */ }
    }
  }
}
add('Voz ativada.');

await new Promise((r) => setTimeout(r, 1300)); // respostas do assistente saem após ~1 s

const lista = [...frases.entries()].map(([falado, original]) => ({ falado, original }));
fs.writeFileSync(new URL('./frases-demo.json', import.meta.url), JSON.stringify(lista, null, 2) + '\n');
const chars = lista.reduce((a, f) => a + f.falado.length, 0);
console.log('frases distintas:', lista.length, '| caracteres no total:', chars);
