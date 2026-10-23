// Gera design-system/index.html a partir de tokens/tokens.css (fonte única dos valores).
// Os contrastes são CALCULADOS aqui (fórmula de luminância relativa do WCAG 2.2), não copiados.
// Uso: node scripts/gerar-design-system.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = fileURLToPath(new URL('..', import.meta.url));
const css = fs.readFileSync(path.join(raiz, 'tokens/tokens.css'), 'utf8');

// --- leitura dos tokens ---------------------------------------------------
const bloco = (re) => { const m = re.exec(css); return m ? m[1] : ''; };
const vars = (txt) => Object.fromEntries([...txt.matchAll(/--([a-z0-9-]+):\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const claro = vars(bloco(/:root\s*\{([\s\S]*?)\n\}/));
const escuro = Object.assign({}, claro, vars(bloco(/\[data-theme='dark'\]\s*\{([\s\S]*?)\n\}/)));

// --- contraste WCAG ---------------------------------------------------------
const hex = (h) => { const v = h.replace('#', ''); const n = v.length === 3 ? v.split('').map((c) => c + c).join('') : v; return [0, 2, 4].map((i) => parseInt(n.slice(i, i + 2), 16) / 255); };
const lum = (h) => { const [r, g, b] = hex(h).map((c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4))); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const razao = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const PARES = [
  ['Texto principal', 'color-text-primary', 'color-bg-surface'],
  ['Texto principal no fundo', 'color-text-primary', 'color-bg-ground'],
  ['Texto de apoio', 'color-text-secondary', 'color-bg-surface'],
  ['Texto de legenda', 'color-text-muted', 'color-bg-surface'],
  ['Link e marca em texto', 'color-brand-text', 'color-bg-surface'],
  ['Item selecionado', 'color-brand-text', 'color-brand-tint'],
  ['Botão principal', 'color-action-on-cta', 'color-action-cta'],
  ['Status recebida', 'color-success-text', 'color-success-bg'],
  ['Status vencida e erro', 'color-danger', 'color-danger-bg'],
  ['Status chargeback', 'color-warning-text', 'color-warning-bg'],
  ['Status aguardando', 'color-info-text', 'color-info-bg'],
  ['Menu lateral: texto', 'color-nav-bg', 'color-nav-bg']
];
PARES.pop(); // o texto do menu é branco fixo sobre color-nav-bg; tratado abaixo
const extras = (t) => [
  ['Menu lateral: texto branco', '#FFFFFF', t['color-nav-bg']],
  ['Menu lateral: item ativo', t['color-nav-active-text'], t['color-nav-active-bg']]
];
const tabela = (t) => [...PARES.map(([nome, fg, bg]) => [nome, t[fg], t[bg]]), ...extras(t)].map(([nome, fg, bg]) => {
  const r = razao(fg, bg);
  return { nome, fg, bg, r, ok: r >= 4.5 };
});
const T_CLARO = tabela(claro);
const T_ESCURO = tabela(escuro);

// --- agrupamento de cores com o uso de cada uma ----------------------------
const USO = {
  'color-bg-ground': 'fundo da página', 'color-bg-surface': 'cards e painéis', 'color-bg-subtle': 'linhas e blocos', 'color-bg-sunken': 'campos e áreas rebaixadas',
  'color-border': 'divisores', 'color-border-strong': 'bordas de campo', 'color-card-border': 'borda de card',
  'color-text-primary': 'texto', 'color-text-secondary': 'texto de apoio', 'color-text-muted': 'legendas',
  'color-brand-primary': 'marca, seleção e CTA no escuro', 'color-brand-support': 'gráficos e foco', 'color-brand-tint': 'fundo de item selecionado', 'color-brand-text': 'link e marca em texto',
  'color-action-cta': 'botão principal', 'color-action-on-cta': 'texto do botão principal',
  'color-nav-bg': 'menu lateral', 'color-nav-muted': 'texto secundário do menu', 'color-nav-active-bg': 'item ativo do menu', 'color-nav-active-text': 'texto do item ativo',
  'color-success-text': 'recebida (texto)', 'color-success-bg': 'recebida (fundo)', 'color-success-fill': 'gráficos',
  'color-warning-text': 'chargeback (texto)', 'color-warning-bg': 'chargeback (fundo)',
  'color-danger': 'vencida e erro (texto)', 'color-danger-bg': 'vencida e erro (fundo)',
  'color-info-text': 'aguardando (texto)', 'color-info-bg': 'aguardando (fundo)', 'color-focus': 'anel de foco', 'color-overlay': 'fundo de modal e drawer'
};
const GRUPOS = [
  ['Superfícies e bordas', ['color-bg-ground', 'color-bg-surface', 'color-bg-subtle', 'color-bg-sunken', 'color-border', 'color-border-strong', 'color-card-border']],
  ['Texto', ['color-text-primary', 'color-text-secondary', 'color-text-muted']],
  ['Marca e ação', ['color-brand-primary', 'color-brand-support', 'color-brand-tint', 'color-brand-text', 'color-action-cta', 'color-action-on-cta']],
  ['Menu lateral', ['color-nav-bg', 'color-nav-muted', 'color-nav-active-bg', 'color-nav-active-text']],
  ['Status', ['color-success-text', 'color-success-bg', 'color-success-fill', 'color-warning-text', 'color-warning-bg', 'color-danger', 'color-danger-bg', 'color-info-text', 'color-info-bg']],
  ['Foco e sobreposição', ['color-focus', 'color-overlay']]
];
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const swatches = (nomes) => nomes.map((n) => `<div class="sw"><span class="chip" style="background: var(--${n})"></span><span class="sw-t"><code>--${n}</code><span class="sw-v"><b class="v-claro">${esc(claro[n])}</b><b class="v-escuro">${esc(escuro[n])}</b></span><span class="sw-u">${USO[n] || ''}</span></span></div>`).join('');
const linhas = (tab) => tab.map((l) => `<tr><td>${esc(l.nome)}</td><td><span class="amostra" style="color:${l.fg};background:${l.bg}">Aa 123</span></td><td><code>${l.fg}</code> sobre <code>${l.bg}</code></td><td class="num">${l.r.toFixed(1).replace('.', ',')}:1</td><td>${l.ok ? '<span class="ok">passa AA (4,5:1)</span>' : '<span class="falha">abaixo de 4,5:1</span>'}</td></tr>`).join('');

const tipos = [...css.matchAll(/--(text-[a-z]+):\s*(\d+)\s+(\d+)px\/(\d+)px/g)].map((m) => ({ token: m[1], peso: m[2], tam: m[3], alt: m[4] }));
const EX = { 'text-display': 'Olá, Paulo!', 'text-h1': 'Cobranças', 'text-h2': 'Precisa da sua atenção', 'text-metric': 'R$ 12.480,35', 'text-body': 'Crie, acompanhe e resolva pendências.', 'text-label': 'Vencimento', 'text-caption': '2 cobranças em aberto' };
const espacos = [...css.matchAll(/--(space-\d+):\s*(\d+)px/g)].map((m) => ({ t: m[1], v: m[2] }));
const raios = [...css.matchAll(/--(radius-[a-z]+):\s*(\d+)px/g)].map((m) => ({ t: m[1], v: m[2] }));
const sombras = [...css.matchAll(/--(shadow-[a-z]+):\s*([^;]+);/g)].map((m) => ({ t: m[1], v: m[2] }));

const html = `<!doctype html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Asaas · Design system do redesenho</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../tokens/tokens.css">
<style>
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--color-bg-ground);color:var(--color-text-primary);font:var(--text-body);-webkit-font-smoothing:antialiased}
code{font:600 12px ui-monospace,Menlo,monospace}
:focus-visible{outline:3px solid var(--color-focus);outline-offset:2px}
.topo{position:sticky;top:0;z-index:5;background:var(--color-bg-ground);border-bottom:1px solid var(--color-border)}
.topo-in{max-width:1240px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.topo nav{display:flex;gap:4px;flex-wrap:wrap;flex:1}
.topo a{color:var(--color-text-secondary);text-decoration:none;font:var(--text-label);padding:10px 12px;border-radius:var(--radius-md)}
.topo a:hover{background:var(--color-bg-subtle)}
.marca{font:800 18px var(--font-family);letter-spacing:-.01em}
.btn{min-height:var(--touch-min);padding:0 16px;border-radius:var(--radius-md);border:1px solid var(--color-border);background:var(--color-bg-surface);color:var(--color-text-primary);font:var(--text-label);cursor:pointer}
.btn:hover{filter:brightness(.95)}
main{max-width:1240px;margin:0 auto;padding:32px 24px 96px;display:flex;flex-direction:column;gap:48px}
h1{font:var(--text-h1);letter-spacing:-.02em;margin:0}
h2{font:var(--text-h1);font-size:28px;margin:0 0 4px;letter-spacing:-.02em}
h3{font:var(--text-h2);margin:0 0 12px}
p{margin:0;color:var(--color-text-secondary);max-width:760px}
.lead{font-size:17px;line-height:1.55}
section{display:flex;flex-direction:column;gap:20px}
.card{background:var(--color-bg-surface);border:1px solid var(--color-card-border);border-radius:var(--radius-card);box-shadow:var(--shadow-card);padding:24px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.sw{display:flex;gap:12px;align-items:center;padding:10px;border-radius:var(--radius-md);background:var(--color-bg-subtle)}
.chip{width:44px;height:44px;border-radius:12px;border:1px solid var(--color-border-strong);flex:none}
.sw-t{display:flex;flex-direction:column;gap:2px;min-width:0}
.sw-v b{font:600 12px ui-monospace,Menlo,monospace;color:var(--color-text-secondary)}
.sw-u{font:var(--text-caption);color:var(--color-text-muted)}
html[data-theme=light] .v-escuro,html[data-theme=dark] .v-claro{display:none}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font:var(--text-label);color:var(--color-text-secondary);padding:8px 10px;border-bottom:1px solid var(--color-border)}
td{padding:10px;border-bottom:1px solid var(--color-border);vertical-align:middle}
.num{font-weight:700;white-space:nowrap}
.amostra{display:inline-block;padding:4px 10px;border-radius:8px;font-weight:700}
.ok{color:var(--color-success-text);font-weight:700}.falha{color:var(--color-danger);font-weight:700}
.rolagem{overflow-x:auto}
.tipo{display:flex;align-items:baseline;gap:20px;border-top:1px solid var(--color-border);padding:12px 0;flex-wrap:wrap}
.tipo code{width:150px;flex:none;color:var(--color-text-secondary)}
.esp{display:flex;align-items:center;gap:14px;padding:4px 0}.esp i{display:block;height:14px;background:var(--color-brand-primary);border-radius:4px}
.raios,.sombras{display:flex;gap:20px;flex-wrap:wrap}
.raio{width:72px;height:72px;background:var(--color-brand-tint);border:2px solid var(--color-brand-primary)}
.som{width:120px;height:76px;background:var(--color-bg-surface);border-radius:16px}
.col{display:flex;flex-direction:column;align-items:center;gap:8px;font:var(--text-caption)}
.demo{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.cta{min-height:var(--touch-min);padding:0 18px;border-radius:var(--radius-md);border:0;background:var(--color-action-cta);color:var(--color-action-on-cta);font:var(--text-label);cursor:pointer}
.cta.hover{filter:brightness(1.2)}.cta[disabled]{opacity:.45;cursor:not-allowed}
.cta.foco{outline:3px solid var(--color-focus);outline-offset:2px}
.sec{background:var(--color-bg-surface);color:var(--color-text-primary);border:1px solid var(--color-border);min-height:var(--touch-min);padding:0 18px;border-radius:var(--radius-md);font:var(--text-label)}
.sel{background:var(--color-brand-tint);color:var(--color-brand-text);border:1.5px solid var(--color-brand-primary);min-height:var(--touch-min);padding:0 18px;border-radius:var(--radius-md);font:var(--text-label)}
.perigo{background:var(--color-bg-surface);color:var(--color-danger);border:1px solid var(--color-danger);min-height:var(--touch-min);padding:0 18px;border-radius:var(--radius-md);font:var(--text-label)}
.status{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font:700 12px var(--font-family)}
.status i{width:6px;height:6px;border-radius:50%;background:currentColor}
.s-aguardando{background:var(--color-info-bg);color:var(--color-info-text)}.s-vencida{background:var(--color-danger-bg);color:var(--color-danger)}
.s-recebida{background:var(--color-success-bg);color:var(--color-success-text)}.s-chargeback{background:var(--color-warning-bg);color:var(--color-warning-text)}
.s-cancelada{background:var(--color-bg-sunken);color:var(--color-text-secondary)}
.campo{display:flex;flex-direction:column;gap:6px;min-width:220px}
.campo label{font:var(--text-label)}
.campo input{min-height:var(--touch-min);padding:0 14px;border-radius:var(--radius-md);border:1px solid var(--color-border-strong);background:var(--color-bg-surface);color:var(--color-text-primary);font:var(--text-body)}
.campo.erro input{border:1.5px solid var(--color-danger)}.campo .msg{font:var(--text-caption);color:var(--color-danger)}
.campo.foco input{box-shadow:0 0 0 3px rgba(0,111,240,.4)}
.metrica{background:var(--color-bg-surface);border:1px solid var(--color-card-border);border-radius:var(--radius-card);padding:20px;min-width:220px;display:flex;flex-direction:column;gap:6px}
.metrica.risco{border-color:var(--color-danger)}.metrica b{font:var(--text-metric)}.metrica.risco b{color:var(--color-danger)}
.metrica span{font:var(--text-caption);color:var(--color-text-secondary)}
.banner{display:flex;gap:12px;align-items:center;background:var(--color-info-bg);color:var(--color-text-primary);border-radius:var(--radius-lg);padding:14px 16px;max-width:560px}
.modal{background:var(--color-bg-surface);border-radius:var(--radius-panel);box-shadow:var(--shadow-overlay);padding:24px;max-width:420px;display:flex;flex-direction:column;gap:12px;border:1px solid var(--color-border)}
.modal .acoes{display:flex;gap:10px;flex-wrap:wrap}
.modal .conf{background:var(--color-danger);color:#fff;border:0;min-height:var(--touch-min);padding:0 16px;border-radius:var(--radius-md);font:var(--text-label)}
.toast{display:inline-block;background:#1D2125;color:#fff;border-radius:14px;padding:12px 16px;box-shadow:var(--shadow-toast);font:var(--text-label)}
.alvo{display:inline-flex;align-items:center;justify-content:center;width:var(--touch-min);height:var(--touch-min);border:1px dashed var(--color-brand-primary);border-radius:var(--radius-md);color:var(--color-brand-text);font:700 11px var(--font-family)}
.nota{font:var(--text-caption);color:var(--color-text-muted)}
</style>
</head>
<body>
<header class="topo"><div class="topo-in">
<span class="marca">Asaas · Design system</span>
<nav aria-label="Seções">
<a href="#cores">Cores</a><a href="#contraste">Contraste</a><a href="#tipografia">Tipografia</a><a href="#espacos">Espaço, raio e sombra</a><a href="#componentes">Componentes</a><a href="#acessibilidade">Acessibilidade</a>
</nav>
<button class="btn" type="button" id="tema" aria-pressed="false">Tema claro (clique para o escuro)</button>
</div></header>
<main>
<section>
<h1>Design system do redesenho do painel</h1>
<p class="lead">Os valores desta página vêm de <code>tokens/tokens.css</code>, o mesmo arquivo usado pelo painel e pela landing. A paleta parte das cores da marca (azul #0038E5, azul de apoio #006FF0, verde #91C651, vermelho #B02A37 e neutros). Onde uma cor original não alcança contraste suficiente para texto, o token de texto usa um tom mais escuro derivado dela, e a cor original fica para gráficos e preenchimentos.</p>
<p class="nota"><b>Simulação:</b> os valores de exemplo (R$, nomes, datas, taxas) usados nos componentes são fictícios e não representam dados reais.</p>
<p class="nota">Esta página é gerada por <code>scripts/gerar-design-system.mjs</code>. Os contrastes são calculados na geração, pela fórmula do WCAG 2.2.</p>
</section>

<section id="cores"><div><h2>Cores</h2><p>Cada token tem valor no modo claro e no escuro. Use o botão do topo para alternar.</p></div>
${GRUPOS.map(([g, n]) => `<div class="card"><h3>${g}</h3><div class="grid">${swatches(n)}</div></div>`).join('\n')}
</section>

<section id="contraste"><div><h2>Contraste de texto</h2><p>Razão calculada para cada par de texto e fundo usado na interface. O critério 1.4.3 do WCAG (nível AA) pede 4,5:1 para texto normal.</p></div>
<div class="card"><h3>Modo claro</h3><div class="rolagem"><table><thead><tr><th>Uso</th><th>Amostra</th><th>Cores</th><th>Razão</th><th>Resultado</th></tr></thead><tbody>${linhas(T_CLARO)}</tbody></table></div></div>
<div class="card"><h3>Modo escuro</h3><div class="rolagem"><table><thead><tr><th>Uso</th><th>Amostra</th><th>Cores</th><th>Razão</th><th>Resultado</th></tr></thead><tbody>${linhas(T_ESCURO)}</tbody></table></div></div>
</section>

<section id="tipografia"><div><h2>Tipografia</h2><p>Plus Jakarta Sans, pesos de 400 a 800. A escala tem sete níveis, todos definidos por token.</p></div>
<div class="card">${tipos.map((t) => `<div class="tipo"><code>${t.token}<br>${t.tam}/${t.alt} · ${t.peso}</code><span style="font:var(--${t.token});letter-spacing:${t.tam >= 24 ? '-0.02em' : '0'}">${EX[t.token] || 'Texto de exemplo'}</span></div>`).join('')}</div>
</section>

<section id="espacos"><div><h2>Espaço, raio e sombra</h2><p>Espaçamento em base 4. Raios maiores nos cartões e painéis, menores nos controles.</p></div>
<div class="card"><h3>Espaçamento</h3>${espacos.map((e) => `<div class="esp"><code style="width:90px">${e.t}</code><i style="width:${e.v}px"></i><span class="nota">${e.v}px</span></div>`).join('')}</div>
<div class="card"><h3>Raios</h3><div class="raios">${raios.map((r) => `<div class="col"><span class="raio" style="border-radius:${r.v}px"></span><code>${r.t}</code><span>${r.v}px</span></div>`).join('')}</div></div>
<div class="card" style="background:var(--color-bg-subtle)"><h3>Sombras</h3><div class="sombras">${sombras.map((s) => `<div class="col"><span class="som" style="box-shadow:var(--${s.t})"></span><code>${s.t}</code></div>`).join('')}</div></div>
</section>

<section id="componentes"><div><h2>Componentes e estados</h2><p>Os mesmos componentes do painel. O status nunca depende só da cor: cada um tem ponto, texto e cor.</p></div>
<div class="card"><h3>Botões</h3><div class="demo">
<button class="cta" type="button">Padrão</button><button class="cta hover" type="button">Hover</button><button class="cta foco" type="button">Foco (teclado)</button>
<button class="sel" type="button" aria-pressed="true">Selecionado</button><button class="cta" type="button" disabled>Desabilitado</button>
<button class="sec" type="button">Secundário</button><button class="perigo" type="button">Perigo</button>
</div><p class="nota">Foco: anel de 3 px (<code>--color-focus</code>) com afastamento de 2 px, visível só pelo teclado.</p></div>
<div class="card"><h3>Status</h3><div class="demo">
<span class="status s-aguardando"><i></i>Aguardando</span><span class="status s-vencida"><i></i>Vencida</span><span class="status s-recebida"><i></i>Recebida</span><span class="status s-chargeback"><i></i>Chargeback</span><span class="status s-cancelada"><i></i>Cancelada</span>
</div></div>
<div class="card"><h3>Campos</h3><div class="demo">
<div class="campo"><label for="c1">Valor</label><input id="c1" value="" placeholder="0,00"></div>
<div class="campo foco"><label for="c2">Valor (foco)</label><input id="c2" value="1.200,00"></div>
<div class="campo erro"><label for="c3">Valor (erro)</label><input id="c3" value="2,00" aria-invalid="true" aria-describedby="m3"><span class="msg" id="m3">O valor mínimo é R$ 5,00.</span></div>
</div></div>
<div class="card"><h3>Card de métrica</h3><div class="demo">
<div class="metrica"><span>Saldo disponível</span><b>R$ 12.480,35</b><span>Atualizado às 09:42</span></div>
<div class="metrica risco"><span>Vencidas</span><b>R$ 1.340,00</b><span>3 cobranças · ação necessária</span></div>
</div></div>
<div class="card"><h3>Banner dispensável, modal de confirmação e toast</h3><div class="demo" style="align-items:flex-start">
<div class="banner">Antecipação automática disponível. Taxas: 1,15% a.m. à vista e 1,6% a.m. parcelado.</div>
<div class="modal"><b>Cancelar a cobrança de R$ 450,00?</b><span class="nota" style="font-size:13px">Esta ação não pode ser desfeita.</span><div class="acoes"><button class="sec" type="button">Voltar</button><button class="conf" type="button">Sim, cancelar cobrança</button></div></div>
<span class="toast">Link copiado</span>
</div><p class="nota">No modal de ação irreversível, o foco começa em "Voltar" e Esc fecha.</p></div>
</section>

<section id="acessibilidade"><div><h2>Acessibilidade</h2><p>Regras aplicadas em todas as telas.</p></div>
<div class="card"><div class="demo"><span class="alvo">44 px</span><p>Alvos de toque com 44 × 44 px ou mais (<code>--touch-min</code>). Esse tamanho corresponde ao critério 2.5.5 do WCAG, que está no nível AAA.</p></div></div>
<div class="card"><p>Elementos nativos (<code>button</code>, <code>a</code>, <code>input</code>, <code>select</code>, <code>table</code>, <code>label</code>), rótulo em todos os campos, <code>aria-invalid</code> nos erros, <code>aria-label</code> nos botões só com ícone, distintivos com texto acessível, modais com <code>role="dialog"</code> ou <code>alertdialog</code>, foco devolvido ao gatilho e animações desligadas quando a pessoa pede movimento reduzido.</p></div>
</section>
</main>
<script>
(function(){
var h=document.documentElement,b=document.getElementById('tema');
function aplicar(t){h.setAttribute('data-theme',t);h.style.colorScheme=t;b.setAttribute('aria-pressed',t==='dark'?'true':'false');b.textContent=t==='dark'?'Tema escuro (clique para o claro)':'Tema claro (clique para o escuro)';}
b.addEventListener('click',function(){aplicar(h.getAttribute('data-theme')==='light'?'dark':'light');});
aplicar('light');
})();
</script>
</body>
</html>
`;
fs.mkdirSync(path.join(raiz, 'design-system'), { recursive: true });
fs.writeFileSync(path.join(raiz, 'design-system/index.html'), html);

const falhas = [...T_CLARO.map((l) => ['claro', l]), ...T_ESCURO.map((l) => ['escuro', l])].filter(([, l]) => !l.ok);
console.log('design-system/index.html gerado');
for (const [tema, l] of [...T_CLARO.map((l) => ['claro', l]), ...T_ESCURO.map((l) => ['escuro', l])]) console.log(tema.padEnd(7), l.r.toFixed(2).padStart(6) + ':1', l.ok ? 'ok ' : 'ABAIXO', l.nome);
console.log('pares abaixo de 4,5:1:', falhas.length);
