#!/usr/bin/env python3
"""Gera as páginas internas do site (soluções, preços, sobre nós, 2ª via, criar conta).

Fonte do conteúdo: textos do asaas.com (referencia/solucoes-original.json, extraído das páginas
originais) organizados abaixo. Visual: o mesmo da landing (estilos/site.css é gerado a partir do
<style> da landing + o CSS das páginas internas, para não haver duas fontes de verdade).

Uso: python3 scripts/gerar-paginas.py   (rode na raiz do projeto)
"""
import html, json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

E = lambda t: html.escape(str(t), quote=False)
A = lambda t: html.escape(str(t), quote=True)

LANDING = open('index.html', encoding='utf-8').read()
REF = json.load(open('referencia/solucoes-original.json', encoding='utf-8'))['paginas']

def _ficticio(v):
    """Troca contatos e domínios reais do Asaas por equivalentes fictícios (o site é só um conceito de design)."""
    if isinstance(v, str):
        v = re.sub(r'([A-Za-z0-9._+-]+)@(?:[a-z0-9-]+\.)*asaas\.com(?:\.br)?', r'\1@exemplo.com.br', v, flags=re.I)
        v = re.sub(r'\b(?:[a-z0-9-]+\.)*asaas\.com(?:\.br)?\b', 'exemplo.com.br', v, flags=re.I)
        v = re.sub(r'0800[ ]?009[ ]?0037', '0800 000 0000', v)
        return v
    if isinstance(v, list):
        return [_ficticio(x) for x in v]
    if isinstance(v, dict):
        return {k: _ficticio(x) for k, x in v.items()}
    return v

REF = _ficticio(REF)
LOGO = re.search(r'<span class="logo">(<svg.*?</svg>)</span>', LANDING, re.S).group(1)
LOGO_PATH = re.search(r'<path d="([^"]+)"', LOGO).group(1)

def logo(w=112, h=19, cor='currentColor'):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 100 17" fill="none" aria-hidden="true"><path d="{LOGO_PATH}" fill="{cor}"/></svg>'

def i(nome, s=20):
    return f'<i data-i="{nome}" data-s="{s}"></i>'

# ---------------------------------------------------------------- CSS
CSS_LANDING = re.search(r'<style>(.*?)</style>', LANDING, re.S).group(1)
CSS_INTERNAS = r'''
/* =================== páginas internas =================== */
[hidden]{display:none !important}
html,body.sub{overflow-x:clip}
.pcards[style*="--cols:1"]{max-width:420px;margin-left:auto;margin-right:auto}
.sub .hero{padding-bottom:88px}
.sub .hero h1{font:800 clamp(34px,4.4vw,56px)/1.06 var(--font-family);letter-spacing:-.035em;text-wrap:balance;opacity:0;animation:fadeUp .9s var(--ease-out) .15s forwards}
.crumb{display:flex;align-items:center;gap:6px;font:600 13px/18px var(--font-family);color:var(--color-text-muted);opacity:0;animation:fadeUp .8s var(--ease-out) .05s forwards}
.crumb a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;min-height:32px}
.crumb a:hover{color:var(--color-brand-text)}
.crumb [aria-current]{color:var(--color-text-primary)}
.sol-tag{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;padding:6px 14px 6px 6px;border-radius:999px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);font:var(--text-label);color:var(--color-text-secondary);opacity:0;animation:fadeUp .8s var(--ease-out) .1s forwards}
.sol-tag .tone{width:32px;height:32px;border-radius:10px}
.price-row{display:flex;flex-wrap:wrap;gap:12px;opacity:0;animation:fadeUp .9s var(--ease-out) .75s forwards}
.ph{display:flex;flex-direction:column;gap:2px;padding:14px 18px;border-radius:var(--radius-lg);background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);min-width:190px}
.ph small{font:600 12px/16px var(--font-family);color:var(--color-text-muted)}
.ph b{font:800 26px/32px var(--font-family);letter-spacing:-.02em;color:var(--color-brand-primary)}
[data-theme='dark'] .ph b{color:var(--color-brand-text)}
.ph s{font:600 13px/16px var(--font-family);color:var(--color-text-muted)}
.ph em{font-style:normal;font:500 12px/16px var(--font-family);color:var(--color-text-muted)}
.checks-row{display:flex;flex-wrap:wrap;gap:8px;opacity:0;animation:fadeUp .9s var(--ease-out) .95s forwards}
.checks-row span{display:inline-flex;align-items:center;gap:6px;padding:6px 12px 6px 8px;border-radius:999px;background:var(--glass);box-shadow:inset 0 0 0 1px var(--glass-border);font:600 13px/18px var(--font-family);color:var(--color-text-secondary)}
.checks-row i{color:var(--color-success-text)}
.hero-ctas{display:flex;flex-wrap:wrap;gap:12px;opacity:0;animation:fadeUp .9s var(--ease-out) .85s forwards}
.disc{font:var(--text-caption);color:var(--color-text-muted);max-width:620px}
.sub .stage{height:600px}
.sub .photo-hero{width:460px;height:540px;top:30px}
.sub .stage .hero-orbit{left:calc(100% - 230px);top:300px}
.sec-head .lead{max-width:680px}
.panel{background:var(--color-bg-surface);border-radius:48px;margin:0 16px;box-shadow:inset 0 0 0 1px var(--color-card-border)}
.panel + .panel{margin-top:16px}
.grid{display:grid;grid-template-columns:repeat(var(--cols,3),minmax(0,1fr));gap:16px;margin-top:48px}
.panel .card{background:var(--color-bg-subtle);box-shadow:inset 0 0 0 1px var(--color-card-border)}
.panel .card:hover{background:var(--color-bg-surface)}
.card h3.sm{font-size:18px;line-height:24px}
a.card{text-decoration:none;color:inherit}
a.card .link-arrow{margin-top:auto}
.nota{display:flex;gap:10px;align-items:flex-start;margin-top:20px;padding:12px 16px;border-radius:16px;background:var(--color-bg-subtle);font:500 13px/19px var(--font-family);color:var(--color-text-muted)}
.nota i{flex:none;margin-top:1px}
.nota.info{background:var(--color-info-bg);color:var(--color-info-text);font-weight:600}
/* passos */
.steps{display:grid;grid-template-columns:repeat(var(--cols,5),minmax(0,1fr));gap:20px;margin-top:56px;position:relative}
.steps::before,.steps::after{content:"";position:absolute;left:24px;right:24px;top:23px;height:2px;border-radius:2px;background:var(--color-border)}
.steps::after{background:linear-gradient(90deg,var(--color-brand-primary),var(--color-brand-support));transform:scaleX(0);transform-origin:0 50%;transition:transform 1.4s var(--ease-out) .2s}
.steps.in::after{transform:scaleX(1)}
.step{position:relative;z-index:1;display:flex;flex-direction:column;gap:10px}
.step .n{width:48px;height:48px;border-radius:16px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);display:flex;align-items:center;justify-content:center;font:800 16px/1 var(--font-family);color:var(--color-brand-primary);transition:background-color .4s ease,color .4s ease;transition-delay:calc(var(--k)*180ms + 200ms)}
.steps.in .step .n{background:var(--color-brand-primary);color:#fff}
.step b{font:800 17px/23px var(--font-family)}
.step p{font:400 14px/21px var(--font-family);color:var(--color-text-secondary)}
/* abas */
.tabs-box{display:flex;flex-direction:column;align-items:center;gap:28px;margin-top:40px}
.seg-scroll{max-width:100%;overflow-x:auto;scrollbar-width:none;padding:2px}
.seg-scroll::-webkit-scrollbar{display:none}
.tabs-box .seg button{display:inline-flex;align-items:center;gap:8px;white-space:nowrap}
.tabs-box .seg .pill{background:var(--color-brand-primary);box-shadow:0 8px 20px rgba(0,56,229,.3)}
.tabs-box .seg button[aria-selected=true]{color:#fff}
.tp{width:100%;display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding:40px;border-radius:32px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border)}
.panel .tp{background:var(--color-bg-subtle)}
.tp.on{animation:stepIn 420ms var(--ease-out) both}
@keyframes stepIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:none}}
.tp h3{font:800 clamp(22px,2.4vw,30px)/1.15 var(--font-family);letter-spacing:-.02em}
.tp .tp-txt{display:flex;flex-direction:column;gap:14px}
.tp .tp-txt p{color:var(--color-text-secondary);font:400 16px/25px var(--font-family)}
.tp .eyebrow{align-self:flex-start}
.tp-vis{position:relative;aspect-ratio:4/3;border-radius:24px;overflow:hidden;background:radial-gradient(120% 120% at 0% 0%,#1F5BF0,#0038E5 45%,#0A1F7A);display:flex;align-items:center;justify-content:center;color:#fff}
.tp-vis img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tp-vis .big-ic{width:120px;height:120px;border-radius:36px;background:rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center;animation:bob 6s ease-in-out infinite}
.tp-vis .ring{position:absolute;inset:18%;border-radius:50%;border:1.5px dashed rgba(255,255,255,.3);animation:spin 40s linear infinite}
.tp-vis .ring.r2{inset:30%;animation-direction:reverse;animation-duration:28s}
/* preços */
.pcards{display:grid;grid-template-columns:repeat(var(--cols,4),minmax(0,1fr));gap:16px;margin-top:48px}
.pcard{position:relative;display:flex;flex-direction:column;gap:8px;padding:24px;border-radius:var(--radius-card);background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);transition:transform var(--dur-base) var(--ease-out),box-shadow var(--dur-base) ease}
.panel .pcard{background:var(--color-bg-subtle)}
.pcard:hover{transform:translateY(-3px);box-shadow:0 14px 32px rgba(29,33,37,.14),inset 0 0 0 1px var(--color-card-border)}
.pcard .rot{font:700 14px/20px var(--font-family);color:var(--color-text-secondary)}
.pcard .v{font:800 30px/36px var(--font-family);letter-spacing:-.025em;color:var(--color-brand-primary)}
[data-theme='dark'] .pcard .v{color:var(--color-brand-text)}
.pcard s{font:600 14px/18px var(--font-family);color:var(--color-text-muted)}
.pcard .u{font:500 13px/18px var(--font-family);color:var(--color-text-muted)}
.pcard .tag{position:absolute;top:16px;right:16px;padding:4px 10px;border-radius:999px;background:var(--color-success-bg);color:var(--color-success-text);font:700 11px/14px var(--font-family)}
/* tabela */
.tbl{margin-top:40px;border-radius:var(--radius-card);overflow:hidden;overflow-x:auto;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border)}
.tbl table{width:100%;border-collapse:collapse;min-width:620px}
.tbl caption{text-align:left;padding:20px 24px 8px;font:800 18px/24px var(--font-family)}
.tbl th,.tbl td{padding:16px 24px;text-align:left;vertical-align:top;border-bottom:1px solid var(--color-border);font:500 14px/21px var(--font-family);color:var(--color-text-secondary)}
.tbl thead th{font:var(--text-label);color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.06em;background:var(--color-bg-subtle)}
.tbl tbody th{font:700 14px/20px var(--font-family);color:var(--color-text-primary)}
.tbl tr:last-child th,.tbl tr:last-child td{border-bottom:0}
.tbl td b{color:var(--color-text-primary)}
.tbl .ok{color:var(--color-success-text);font-weight:700}
.tbl tbody tr{transition:background-color .15s}
.tbl tbody tr:hover{background:var(--color-bg-subtle)}
/* lista com imagem */
.lista-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.lista-grid.inv>:first-child{order:2}
.lista{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.lista li{display:flex;align-items:center;gap:14px;padding:14px 16px;border-radius:18px;background:var(--color-bg-surface);box-shadow:var(--shadow-card);font:700 15px/21px var(--font-family)}
.panel .lista li{background:var(--color-bg-subtle);box-shadow:inset 0 0 0 1px var(--color-card-border)}
.lista li .tone{width:36px;height:36px;border-radius:12px}
.media{position:relative;border-radius:var(--radius-panel);overflow:hidden;aspect-ratio:4/3.2;background:var(--color-bg-sunken);box-shadow:0 30px 60px rgba(10,31,122,.14)}
.media img{position:absolute;inset:-8% 0;width:100%;height:116%;object-fit:cover;will-change:transform}
.media .float{position:absolute;left:16px;bottom:16px;animation:none}
.media.vis{display:flex;align-items:center;justify-content:center;background:radial-gradient(120% 120% at 0% 0%,#1F5BF0,#0038E5 45%,#0A1F7A);color:#fff}
/* faixa */
.faixa{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;padding:32px;border-radius:32px;background:radial-gradient(120% 140% at 100% 0%,#1F5BF0 0%,#0038E5 45%,#0A1F7A 100%);color:#fff;position:relative;overflow:hidden;isolation:isolate}
.faixa::after{content:"";position:absolute;right:-60px;top:-60px;width:240px;height:240px;border-radius:50%;background:rgba(255,255,255,.1);z-index:-1}
.faixa .tone{width:64px;height:64px;border-radius:20px;background:rgba(255,255,255,.16);color:#fff}
.faixa .eyebrow{background:rgba(255,255,255,.16);color:#fff;margin-bottom:8px}
.faixa .eyebrow b{background:#fff;color:#0030C8}
.faixa h3{font:800 clamp(20px,2.2vw,26px)/1.2 var(--font-family);letter-spacing:-.015em}
.faixa p{color:#C9D6FF;margin-top:6px}
/* depoimentos */
.quotes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:48px}
.qcard{position:relative;display:flex;flex-direction:column;gap:18px;padding:28px;border-radius:var(--radius-card);background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);overflow:hidden}
.panel .qcard{background:var(--color-bg-subtle)}
.qcard::before{content:"“";position:absolute;right:20px;top:-26px;font:800 150px/1 var(--font-family);color:var(--color-brand-tint)}
.qcard p{position:relative;font:600 16px/26px var(--font-family);color:var(--color-text-primary)}
.qcard .who{display:flex;align-items:center;gap:12px;margin-top:auto}
.qcard .who span{width:40px;height:40px;border-radius:12px;background:var(--color-brand-tint);color:var(--color-brand-text);display:flex;align-items:center;justify-content:center;font:800 13px/1 var(--font-family)}
.qcard .who b{display:block;font:700 14px/18px var(--font-family)}
.qcard .who small{font:var(--text-caption);color:var(--color-text-muted)}
/* simulador */
.sim{display:grid;grid-template-columns:1.1fr .9fr;margin-top:40px;border-radius:32px;overflow:hidden;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border)}
.sim-in{display:flex;flex-direction:column;gap:20px;padding:32px}
.sim-out{display:flex;flex-direction:column;gap:12px;padding:32px;background:radial-gradient(120% 140% at 100% 0%,#1F5BF0 0%,#0038E5 45%,#0A1F7A 100%);color:#fff}
.sim-out small{font:600 13px/18px var(--font-family);color:#C9D6FF}
.sim-out .big{font:800 clamp(34px,4vw,44px)/1.05 var(--font-family);letter-spacing:-.03em}
.sim-out .linha{display:flex;justify-content:space-between;gap:12px;padding:12px 0;border-top:1px solid rgba(255,255,255,.16);font:600 14px/20px var(--font-family)}
.sim-out .linha span:first-child{color:#C9D6FF;font-weight:500}
.sim-out.pop{animation:simPop .45s var(--ease-out)}
@keyframes simPop{from{opacity:.35;transform:translateY(6px)}to{opacity:1;transform:none}}
/* formulários (mesmos campos do painel) */
.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field>.lbl{font:var(--text-label);color:var(--color-text-secondary)}
.field input,.field select{width:100%;height:52px;border-radius:14px;border:0;box-shadow:inset 0 0 0 1px var(--color-border-strong);background:var(--color-bg-surface);color:var(--color-text-primary);padding:0 16px;font:500 15px/22px var(--font-family);outline:none;transition:box-shadow .15s ease}
.field select{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%235F6B7A' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:40px}
.field input:focus,.field select:focus{box-shadow:inset 0 0 0 2px var(--color-brand-support),0 0 0 3px rgba(0,111,240,.22)}
.field input::placeholder{color:var(--color-text-muted);opacity:.8}
.field .msg{display:none;align-items:center;gap:6px;font:600 12px/16px var(--font-family);color:var(--color-danger)}
.field.bad input,.field.bad select{box-shadow:inset 0 0 0 2px var(--color-danger)}
.field.bad .msg{display:flex}
.field .hint{font:var(--text-caption);color:var(--color-text-muted)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.row3{display:grid;grid-template-columns:2fr 1fr 1fr;gap:14px}
.radios{display:flex;flex-wrap:wrap;gap:8px}
.rad{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:999px;box-shadow:inset 0 0 0 1px var(--color-border-strong);background:var(--color-bg-surface);cursor:pointer;font:600 14px/1 var(--font-family);color:var(--color-text-secondary);transition:all .15s}
.rad input{accent-color:var(--color-brand-primary);width:16px;height:16px;margin:0}
.rad:has(input:checked){box-shadow:inset 0 0 0 2px var(--color-brand-primary);background:var(--color-brand-tint);color:var(--color-brand-text)}
.chk{display:flex;align-items:flex-start;gap:10px;font:500 14px/20px var(--font-family);color:var(--color-text-secondary);cursor:pointer}
.chk input{width:20px;height:20px;margin:0;flex:none;accent-color:var(--color-brand-primary)}
.chk a{font-weight:700}
.field.bad .chk{color:var(--color-danger)}
.toggle-row{display:flex;align-items:center;justify-content:space-between;gap:12px;font:600 14px/20px var(--font-family);color:var(--color-text-secondary)}
/* contato API */
.form-card{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:32px;border-radius:32px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border)}
.form-card .full{grid-column:1/-1}
/* sobre nós */
.valores{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.valores span{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 20px;border-radius:999px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);font:700 15px/1 var(--font-family);transition:transform .25s var(--ease-out)}
.valores span:hover{transform:translateY(-2px)}
.valores i{color:var(--color-brand-primary)}
.tl{position:relative;margin:56px auto 0;max-width:960px;display:flex;flex-direction:column;gap:20px}
.tl::before{content:"";position:absolute;left:50%;top:0;bottom:0;width:2px;margin-left:-1px;background:linear-gradient(180deg,var(--color-brand-primary),var(--color-brand-support),#91C651)}
.tl-item{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.tl-item .ano{justify-self:end;font:800 clamp(36px,4vw,52px)/1 var(--font-family);letter-spacing:-.04em;color:var(--color-brand-primary)}
[data-theme='dark'] .tl-item .ano{color:var(--color-brand-text)}
.tl-item:nth-child(even) .ano{order:2;justify-self:start}
.tl-item::after{content:"";position:absolute;left:50%;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:var(--color-bg-ground);box-shadow:0 0 0 4px var(--color-brand-primary)}
.tl-item .card{padding:22px}
.news{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:48px}
.news .card{padding:22px;gap:12px}
.news .card b{font:700 15px/22px var(--font-family)}
.contatos{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:40px}
.contatos .card h3{font-size:18px}
.contatos a{display:flex;align-items:center;gap:12px;min-height:48px;color:var(--color-text-primary);text-decoration:none}
.contatos a small{display:block;font:var(--text-caption);color:var(--color-text-muted)}
.contatos a b{display:block;font:800 16px/20px var(--font-family)}
/* preços: atalhos */
.atalhos{position:sticky;top:calc(var(--header-h) + 24px);z-index:20;display:flex;justify-content:center;margin:-28px 0 0;pointer-events:none}
.atalhos nav{pointer-events:auto;display:flex;gap:4px;padding:5px;border-radius:999px;max-width:100%;overflow-x:auto;scrollbar-width:none;background:var(--glass);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 10px 30px rgba(29,33,37,.10),inset 0 0 0 1px var(--glass-border)}
.atalhos nav::-webkit-scrollbar{display:none}
.atalhos a{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;white-space:nowrap;text-decoration:none;font:700 13px/1 var(--font-family);color:var(--color-text-secondary);transition:background-color .2s,color .2s}
.atalhos a:hover{background:rgba(0,56,229,.08);color:var(--color-brand-text)}
.atalhos a.on{background:var(--color-brand-primary);color:#fff}
.alvo{scroll-margin-top:150px}
.gratis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:48px}
.gratis .card ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.gratis .card li{display:flex;gap:8px;align-items:flex-start;font:500 14px/20px var(--font-family);color:var(--color-text-secondary)}
.gratis .card li i{color:var(--color-success-text);margin-top:1px}
.gratis .free{font:800 24px/28px var(--font-family);color:var(--color-success-text)}
/* 2ª via */
.sv-wrap{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.sv-form{display:flex;flex-direction:column;gap:16px;padding:32px;border-radius:32px;background:var(--color-bg-surface);box-shadow:var(--shadow-overlay),inset 0 0 0 1px var(--color-card-border)}
.sv-form h2{font:800 22px/28px var(--font-family)}
#svResultado.pop{animation:simPop .45s var(--ease-out)}
.sv-fatura,.sv-vazio{display:flex;flex-direction:column;gap:18px;padding:24px;border-radius:24px;background:var(--color-bg-subtle);box-shadow:inset 0 0 0 1px var(--color-card-border)}
.sv-vazio{align-items:center;text-align:center;color:var(--color-text-muted)}
.sv-vazio b{color:var(--color-text-primary);font:800 16px/22px var(--font-family)}
.sv-top{display:flex;align-items:center;gap:12px}
.sv-top small{display:block;font:var(--text-caption);color:var(--color-text-muted)}
.sv-top b{font:800 16px/20px var(--font-family)}
.badge{margin-left:auto;padding:4px 10px;border-radius:999px;font:700 12px/16px var(--font-family)}
.badge.warn{background:var(--color-warning-bg);color:var(--color-warning-text)}
.sv-valor small{display:block;font:var(--text-caption);color:var(--color-text-muted)}
.sv-valor strong{display:block;font:800 32px/38px var(--font-family);letter-spacing:-.02em}
.sv-acoes{display:flex;flex-wrap:wrap;gap:8px}
.sv-aviso{display:flex;gap:8px;align-items:flex-start;font:600 12px/17px var(--font-family);color:var(--color-warning-text)}
.sv-aviso svg{flex:none}
/* criar conta */
.cc-page{min-height:100vh;display:grid;grid-template-columns:minmax(320px,440px) minmax(0,1fr);gap:16px;padding:16px;background:var(--color-bg-ground)}
.cc-side{position:sticky;top:16px;height:calc(100vh - 32px);display:flex;flex-direction:column;gap:24px;padding:28px;border-radius:var(--radius-panel);background:var(--color-nav-bg);color:#fff;overflow:hidden;isolation:isolate}
.cc-side::before{content:"";position:absolute;right:-120px;bottom:-120px;width:360px;height:360px;border-radius:50%;background:rgba(255,255,255,.08);z-index:-1}
.cc-side .logo{color:#fff}
.cc-side h1{font:800 clamp(26px,2.6vw,32px)/1.15 var(--font-family);letter-spacing:-.025em}
.cc-side p{color:var(--color-nav-muted);font:500 15px/23px var(--font-family)}
.cc-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.cc-steps li{display:flex;align-items:center;gap:12px;min-height:48px;padding:0 12px;border-radius:14px;font:600 14px/1 var(--font-family);color:var(--color-nav-muted);transition:background-color .25s,color .25s}
.cc-steps li span{width:28px;height:28px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.14);font:800 12px/1 var(--font-family);transition:background-color .25s,color .25s}
.cc-steps li.atual{background:#fff;color:var(--color-nav-active-text)}
.cc-steps li.atual span{background:var(--color-brand-tint);color:var(--color-brand-text)}
.cc-steps li.feito{color:#fff}
.cc-steps li.feito span{background:#91C651;color:#1D2125}
.cc-side .mini-foto{margin-top:auto;position:relative;border-radius:22px;overflow:hidden;aspect-ratio:16/10}
.cc-side .mini-foto img{width:100%;height:100%;object-fit:cover;display:block}
.cc-side .mini-foto .float{position:absolute;left:12px;bottom:12px;animation:none;padding:10px 12px}
.cc-main{display:flex;flex-direction:column;min-width:0}
.cc-top{display:flex;align-items:center;justify-content:flex-end;gap:10px;min-height:56px;padding:0 8px;font:500 14px/20px var(--font-family);color:var(--color-text-muted)}
.cc-top .logo-m{display:none;margin-right:auto;color:var(--color-brand-primary)}
.cc-body{flex:1;display:flex;align-items:flex-start;justify-content:center;padding:32px 16px 56px;scroll-margin-top:16px}
.cc-card{width:100%;max-width:560px;display:flex;flex-direction:column;gap:22px}
.cc-barra{height:6px;border-radius:999px;background:var(--color-bg-sunken);overflow:hidden}
.cc-barra i{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--color-brand-primary),var(--color-brand-support));transition:width .5s var(--ease-out)}
.cc-passo{display:flex;flex-direction:column;gap:18px}
.cc-passo.step-in{animation:stepIn 380ms var(--ease-out) both}
.cc-passo h2{font:800 clamp(24px,2.6vw,30px)/1.15 var(--font-family);letter-spacing:-.02em}
.cc-passo .lead{font-size:16px;line-height:24px}
.cc-nav{display:flex;align-items:center;gap:10px;margin-top:6px}
.cc-nav .btn-cta{margin-left:auto}
.links-inline{display:flex;flex-wrap:wrap;gap:6px 16px;font:600 13px/18px var(--font-family)}
.links-inline a{color:var(--color-brand-text)}
.links-inline a.off{color:var(--color-text-muted);pointer-events:none;text-decoration:none}
.otp{display:flex;gap:10px}
.otp input{width:52px;height:60px;text-align:center;padding:0;font:800 22px/1 var(--font-family)}
.demo-note{display:flex;gap:8px;align-items:flex-start;padding:10px 14px;border-radius:14px;background:var(--color-warning-bg);color:var(--color-warning-text);font:600 12px/17px var(--font-family)}
.ok-final{align-items:center;text-align:center;padding:24px 0}
.ok-final .tone{width:72px;height:72px;border-radius:24px;animation:pulseOk 1.8s ease-out infinite}
@keyframes pulseOk{0%{box-shadow:0 0 0 0 rgba(145,198,81,.5)}70%{box-shadow:0 0 0 18px rgba(145,198,81,0)}100%{box-shadow:0 0 0 0 rgba(145,198,81,0)}}
/* responsivo */
@media (max-width:1099px){
  .grid{--cols:2 !important}
  .pcards{--cols:2 !important}
  .gratis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .news{grid-template-columns:repeat(2,minmax(0,1fr))}
  .steps{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:28px}
  .steps::before,.steps::after{display:none}
  .tp,.lista-grid,.sim,.sv-wrap{grid-template-columns:1fr}
  .lista-grid.inv>:first-child{order:0}
  .faixa{grid-template-columns:auto 1fr}
  .faixa .btn{grid-column:1/-1;justify-self:start}
  .sub .stage .hero-orbit{left:50%}
  .cc-page{grid-template-columns:1fr}
  .cc-side{position:relative;top:0;height:auto}
  .cc-side .mini-foto{display:none}
}
@media (max-width:759px){
  .grid,.pcards,.gratis,.news,.quotes,.contatos{grid-template-columns:1fr;--cols:1 !important}
  .steps{grid-template-columns:1fr;gap:20px}
  .tp{padding:24px;gap:24px}
  .tabs-box .seg button{padding:0 14px;font-size:13px}
  .form-card,.row2{grid-template-columns:1fr}
  .row3{grid-template-columns:1fr 1fr}
  .row3>:first-child{grid-column:1/-1}
  .tl::before{left:18px}
  .tl-item{grid-template-columns:1fr;gap:8px;padding-left:48px}
  .tl-item .ano,.tl-item:nth-child(even) .ano{order:0;justify-self:start;font-size:32px}
  .tl-item::after{left:18px;top:14px}
  .faixa{grid-template-columns:1fr;padding:24px}
  .sim-in,.sim-out,.sv-form{padding:24px}
  .cc-page{padding:0;gap:0}
  .cc-side{border-radius:0 0 28px 28px;padding:20px}
  .cc-side .cc-steps{flex-direction:row;overflow-x:auto;gap:6px}
  .cc-side .cc-steps li{flex:none;padding:0 10px;min-height:40px}
  .cc-side .cc-steps li b{display:none}
  .cc-side .cc-steps li.atual b{display:inline}
  .otp{gap:6px}
  .otp input{width:44px;height:54px}
  .sub .stage .photo-hero{width:100%;height:420px;top:auto}
}
'''

CSS_INTERNAS += '\n/* blog */\n.filtros{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:28px}\n.filtros button{min-height:40px;padding:0 16px;border-radius:999px;border:0;background:var(--color-bg-surface);box-shadow:inset 0 0 0 1px var(--color-border);font:600 13px/1 var(--font-family);color:var(--color-text-secondary);cursor:pointer;transition:all .2s}\n.filtros button:hover{color:var(--color-brand-text);box-shadow:inset 0 0 0 1px var(--color-brand-primary)}\n.filtros button[aria-pressed=true]{background:var(--color-brand-primary);color:#fff;box-shadow:0 8px 20px rgba(0,56,229,.25)}\n.busca{display:flex;align-items:center;gap:10px;max-width:520px;margin:24px auto 0;padding:0 16px;height:52px;border-radius:999px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);color:var(--color-text-muted)}\n.busca input{flex:1;min-width:0;border:0;background:transparent;font:500 15px/22px var(--font-family);color:var(--color-text-primary);outline:none}\n.busca:focus-within{box-shadow:var(--shadow-card),0 0 0 3px rgba(0,111,240,.3)}\n.destaques{display:grid;grid-template-columns:1.4fr 1fr;gap:16px;margin-top:40px}\n.destaques .lado{display:flex;flex-direction:column;gap:16px}\n.post{position:relative;display:flex;flex-direction:column;border-radius:var(--radius-card);overflow:hidden;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);text-decoration:none;color:inherit;transition:transform var(--dur-base) var(--ease-out),box-shadow var(--dur-base) ease}\n.post:hover{transform:translateY(-3px);box-shadow:0 14px 32px rgba(29,33,37,.14),inset 0 0 0 1px var(--color-card-border)}\n.post .capa{position:relative;aspect-ratio:16/9;overflow:hidden;background:radial-gradient(120% 140% at 0% 0%,#1F5BF0,#0038E5 45%,#0A1F7A);display:flex;align-items:center;justify-content:center;color:#fff}\n.post .capa img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease-out)}\n.post:hover .capa img{transform:scale(1.05)}\n.post .capa .big-ic{width:72px;height:72px;border-radius:22px;background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center;transition:transform .4s var(--ease-out)}\n.post:hover .capa .big-ic{transform:scale(1.08) rotate(-4deg)}\n.post .capa.c1{background:radial-gradient(120% 140% at 0% 0%,#006FF0,#0038E5 50%,#0A1F7A)}\n.post .capa.c2{background:radial-gradient(120% 140% at 0% 0%,#91C651,#3F7A12 60%,#1D2125)}\n.post .capa.c3{background:radial-gradient(120% 140% at 0% 0%,#37474F,#1D2125)}\n.post .corpo{display:flex;flex-direction:column;gap:10px;padding:20px 22px 22px;flex:1}\n.post .cat{align-self:flex-start;padding:4px 10px;border-radius:999px;background:var(--color-brand-tint);color:var(--color-brand-text);font:700 12px/16px var(--font-family)}\n.post h3{font:800 18px/24px var(--font-family);letter-spacing:-.01em}\n.post.grande h3{font-size:clamp(22px,2.4vw,30px);line-height:1.15}\n.post .meta{margin-top:auto;font:500 12px/16px var(--font-family);color:var(--color-text-muted)}\n.posts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:40px}\n.posts .post[hidden]{display:none}\n.vazio-busca{text-align:center;color:var(--color-text-muted);padding:40px 0}\n.materiais{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:32px}\n.materiais a{display:flex;align-items:center;gap:12px;min-height:64px;padding:12px 16px;border-radius:18px;background:var(--color-bg-subtle);box-shadow:inset 0 0 0 1px var(--color-card-border);text-decoration:none;color:var(--color-text-primary);font:700 14px/19px var(--font-family);transition:transform .2s var(--ease-out),background-color .2s}\n.materiais a:hover{transform:translateY(-2px);background:var(--color-bg-surface)}\n.materiais .tone{width:36px;height:36px;border-radius:12px}\n/* carreiras */\n.vagas-tools{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-top:32px}\n.vagas-tools .busca{margin:0;flex:1;max-width:460px}\n.vagas{display:flex;flex-direction:column;gap:10px;margin-top:20px}\n.vaga{display:flex;align-items:center;gap:16px;padding:16px 20px;border-radius:20px;background:var(--color-bg-surface);box-shadow:var(--shadow-card),inset 0 0 0 1px var(--color-card-border);text-decoration:none;color:inherit;transition:transform .2s var(--ease-out),box-shadow .2s}\n.panel .vaga{background:var(--color-bg-subtle)}\n.vaga:hover{transform:translateX(4px);box-shadow:0 10px 24px rgba(29,33,37,.12),inset 0 0 0 1px var(--color-brand-primary)}\n.vaga b{display:block;font:700 15px/21px var(--font-family)}\n.vaga small{font:500 13px/18px var(--font-family);color:var(--color-text-muted)}\n.vaga .tags{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}\n.vaga .tags span{padding:4px 10px;border-radius:999px;background:var(--color-bg-sunken);font:600 12px/16px var(--font-family);color:var(--color-text-secondary)}\n.vaga .tags span.rem{background:var(--color-success-bg);color:var(--color-success-text)}\n.vaga[hidden]{display:none}\n.vagas-cont{font:600 13px/18px var(--font-family);color:var(--color-text-muted)}\n@media (max-width:1099px){.destaques{grid-template-columns:1fr}.posts{grid-template-columns:repeat(2,minmax(0,1fr))}.materiais{grid-template-columns:repeat(2,minmax(0,1fr))}}\n@media (max-width:759px){.posts,.materiais{grid-template-columns:1fr}.vaga{flex-wrap:wrap}.vaga .tags{margin-left:0;justify-content:flex-start}}\n'
open('estilos/site.css', 'w', encoding='utf-8').write(
    '/* Gerado por scripts/gerar-paginas.py: <style> da landing + estilos das páginas internas. Não edite à mão. */\n'
    + CSS_LANDING + CSS_INTERNAS)

# ---------------------------------------------------------------- dados comuns
SOL = [
    ('pix', 'Pix', 'pix-asaas'), ('barcode', 'Boleto bancário', 'boleto-bancario'), ('card', 'Cobrança por cartão', 'cobranca-cartao'),
    ('pos', 'Asaas Tap', 'asaas-tap'), ('link', 'Link de pagamento', 'link-pagamento'), ('file', 'Nota fiscal', 'nota-fiscal'),
    ('wallet', 'Conta digital', 'conta-digital'), ('bell', 'Régua de Cobrança', 'regua-de-cobranca'), ('trend', 'Antecipação de recebíveis', 'antecipacao-de-recebiveis'),
    ('grid', 'ERP', 'erp'), ('code', 'API de pagamentos', 'api-de-pagamentos'), ('cash', 'Meios de pagamento', 'meios-de-pagamento'),
]
INV = ['23S', 'Parallax', 'Cventures', 'Spectra', 'Escala Capital', 'Quartzo Capital', 'Bond', 'SoftBank', 'Inovabra', 'Endeavor']
CLI = ['Würth', 'Cometa', 'Sebrae', 'Magazord', 'Next Fit', 'Tecnofit', 'Minerva Foods', 'Nuvemshop', 'Shopify', 'Rodobens', 'Mahle', 'Hostgator']
TAXA_PADRAO = 'As taxas apresentadas são padrão. Para conferir as condições aplicadas ao seu contrato, consulte-as diretamente na sua conta Asaas.'
SEGURO_TXT = 'Somos a 31ª instituição de pagamento autorizada a funcionar pelo Banco Central e nosso código é o 461. Isso garante mais segurança para você e o seu negócio.'
STATS = [(3.8, 1, '+', 'mi', 'de contas criadas'), (171.3, 1, '+R$ ', 'bi', 'movimentados'), (549.3, 1, '+', 'mi', 'de cobranças pagas')]

EMAIS_PADRAO = [
    ('file', 'Emissão de notas fiscais de serviço', 'Gere o boleto e selecione se deseja vincular a cobrança ao envio da NFS-e.', 'nota-fiscal'),
    ('trend', 'Antecipação de cobranças', 'Antecipe recebimentos futuros e garanta dinheiro no caixa.', 'antecipacao-de-recebiveis'),
    ('bell', 'Notificações personalizadas', 'Personalize os conteúdos das notificações de e-mail e SMS e deixe a comunicação com a cara do seu negócio.', 'regua-de-cobranca'),
    ('search', 'Consulta e Negativação via Serasa', 'Obtenha um histórico detalhado do cliente antes de fechar a venda ou negative os devedores.', None),
]
EMAIS_BOLETO = [('barcode', 'Cobrança por boleto', 'Gere boletos à vista, parcelados ou recorrentes e pague apenas pelas cobranças recebidas.', 'boleto-bancario')] + EMAIS_PADRAO[1:]
CANAIS = [
    ('chat', 'WhatsApp', 'Configure suas notificações na rede social mais popular entre os brasileiros e aproveite os benefícios de uma comunicação dinâmica e moderna.'),
    ('mail', 'E-mail', 'Envie lembretes de pagamento ao seus clientes em todas as etapas da régua de cobrança e aproveite o meio de comunicação mais formal utilizado hoje em dia.'),
    ('sms', 'SMS', 'Lembre de notificar seus consumidores por SMS e se beneficie deste canal de cobrança que possui alta taxa de visualização. Use a tecnologia a seu favor!'),
    ('volume', 'Ligação', 'Nosso sistema de robô de voz ajuda empresas a recuperar dívidas de cobranças vencidas, além de reduzir custos operacionais e evitar constrangimento com clientes.'),
    ('send', 'Correios', 'Utilize esse canal de acordo com a sua área de atuação e perfil de clientes, garantindo a entrega física de novos boletos emitidos.'),
]
NOTIF_PERS = ['Destaque seu negócio com conteúdos profissionais e persuasivos', 'Fortaleça a conexão com seus clientes',
              'Humanize a comunicação utilizando o tom e voz da sua marca', 'Aumente suas chances de receber pagamentos em dia']
NOTIF_NOTA = 'Recurso exclusivo para clientes PJ. Disponível na contratação do Plano Avançado por R$ 99,90 mensais.'

# ---------------------------------------------------------------- blocos
def head(titulo, desc):
    return f'''<!doctype html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<title>{E(titulo)}</title>
<meta name="description" content="{A(desc)}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/tokens/tokens.css" />
<link rel="stylesheet" href="/estilos/site.css" />
</head>
'''

def topo(R, ativo=''):
    def nav(href, rot, chave):
        cur = ' aria-current="page"' if ativo == chave else ''
        return f'<a href="{R}{href}"{cur}>{rot}</a>'
    return f'''<div class="sim-aviso" role="note"><b>Conceito de design · simulação.</b> Não é o site do Asaas, sem relação oficial. Dados fictícios: não digite dados reais.</div>
<div class="progress" aria-hidden="true"></div>
<header class="top" id="top">
  <div class="top-in">
    <a class="brand" href="{R}" aria-label="Asaas, ir para o início"><span class="logo">{logo()}</span></a>
    <nav class="nav" aria-label="Principal">
      <button class="nl" type="button" id="solBtn" aria-expanded="false" aria-controls="mega">Soluções {i('chevD',16).replace('<i ','<i class="chev" ')}</button>
      {nav('precos/','Preços','precos')}
      <div class="dd"><button class="nl" type="button" data-drop aria-expanded="false" aria-controls="ddSobre"{' aria-current="page"' if ativo in ('sobre','blog','carreiras') else ''}>Sobre nós {i('chevD',16).replace('<i ','<i class="chev" ')}</button>
        <div class="dd-menu" id="ddSobre" role="menu" aria-label="Sobre nós">
          <a role="menuitem" href="{R}sobre-nos/"><span class="tone">{i('users',20)}</span><span>Quem somos<small>Nossa história e valores</small></span></a>
          <a role="menuitem" href="{R}blog/"><span class="tone">{i('news',20)}</span><span>Blog<small>Gestão, finanças e negócios</small></span></a>
          <a role="menuitem" href="{R}carreiras/"><span class="tone">{i('star',20)}</span><span>Carreiras<small>Vagas e benefícios</small></span></a>
        </div>
      </div>
      {nav('solucoes/api-de-pagamentos/','Desenvolvedores','api')}
      {nav('segunda-via/','2ª Via','2via')}
    </nav>
    <div class="top-actions">
      <button class="icon-btn" type="button" id="themeBtn" aria-label="Usar tema escuro"></button>
      <a class="btn btn-ghost btn-sm hide-m" href="{R}painel/">Acessar minha conta</a>
      <a class="btn btn-cta btn-sm hide-t" href="{R}criar-conta/">Criar conta grátis</a>
      <button class="icon-btn burger" type="button" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="sheet">{i('menu',22)}</button>
    </div>
  </div>
  <div class="mega" id="mega" role="menu" aria-label="Soluções"></div>
</header>
'''

def rodape(R):
    return f'''<footer>
  <div class="wrap">
    <div class="f-grid">
      <div class="f-col f-contact">
        <a class="brand" href="{R}" aria-label="Asaas, ir para o início"><span class="logo">{logo()}</span></a>
        <h3 style="margin-top:20px">Canais de atendimento</h3>
        <b>0800 000 0000</b><small>(somente Pessoa Jurídica)</small>
        <b>0800 000 0000</b><small>(somente mensagens)</small>
        <b style="font-size:15px">contato@exemplo.com.br</b>
      </div>
      <div class="f-col"><h3>Ajuda</h3><ul><li><a href="#">Central de ajuda</a></li><li><a href="#">Ouvidoria</a></li><li><a href="#">Alerta de fraude</a></li></ul>
        <h3 style="margin-top:24px">Imprensa</h3><ul><li><a href="#">imprensa@exemplo.com.br</a></li></ul></div>
      <div class="f-col"><h3>Soluções</h3><ul id="fSol"></ul></div>
      <div class="f-col"><h3>Asaas</h3><ul><li><a href="{R}precos/">Preços e taxas</a></li><li><a href="{R}sobre-nos/">Sobre nós</a></li><li><a href="{R}blog/">Blog</a></li><li><a href="{R}carreiras/">Carreiras</a></li><li><a href="{R}segunda-via/">2ª Via</a></li><li><a href="#">Seja um parceiro</a></li><li><a href="#">Flapp Store</a></li></ul></div>
      <div class="f-col"><h3>Transparência</h3><ul><li><a href="#">Termos de uso</a></li><li><a href="#">Política de privacidade</a></li><li><a href="#">Políticas de segurança</a></li><li><a href="#">Documentos</a></li><li><a href="#">Canal de denúncias</a></li><li><a href="#">Reportar Vulnerabilidade</a></li></ul></div>
    </div>
    <div class="f-legal">
      <span>© 2026 Conceito de design para estudo. Todos os nomes, valores, contatos e endereços desta página são fictícios.</span>
      <span>Este não é o site do Asaas e não tem relação oficial com a empresa. Os textos de exemplo foram adaptados de páginas públicas do Asaas, só para um estudo de design.</span>
      <span class="concept">Simulação · não digite dados reais</span>
      <span class="f-estudo">Estudo de caso: <a href="{R}defesa/">apresentação da defesa</a> · <a href="{R}design-system/">design system</a> · <a href="{R}painel/">protótipo do painel</a> · <a href="https://github.com/cbitran/asaas/tree/main/docs">documentos no GitHub</a></span>
    </div>
  </div>
</footer>
<div class="overlay" id="overlay"></div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="grab" aria-hidden="true"></div>
  <div class="sh-head"><span aria-label="Asaas">{logo(96,16,'#fff')}</span><button type="button" id="sheetClose" aria-label="Fechar menu">{i('x')}</button></div>
  <div class="grp">Menu</div>
  <a href="{R}">Início</a><a href="{R}precos/">Preços</a><a href="{R}solucoes/api-de-pagamentos/">Desenvolvedores</a><a href="{R}segunda-via/">2ª Via</a>
  <div class="grp">Sobre nós</div>
  <a href="{R}sobre-nos/">Quem somos</a><a href="{R}blog/">Blog</a><a href="{R}carreiras/">Carreiras</a>
  <div class="grp">Soluções</div>
  <div id="sheetSol"></div>
  <div class="sh-cta"><a class="btn btn-white" href="{R}criar-conta/">Criar conta grátis</a><a class="btn" style="background:rgba(255,255,255,.14);color:#fff" href="{R}painel/">Acessar minha conta</a></div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite">{i('check',18)}<span></span></div>
<script type="module" src="/estilos/site.js"></script>
</body>
</html>
'''

def signup(rot='Criar conta grátis'):
    return f'''<form class="signup" novalidate data-form>
        <div class="signup-row">
          <label><span class="sr">Seu e-mail</span><input type="email" name="email" placeholder="Seu melhor e-mail" autocomplete="email" required /></label>
          <button class="btn btn-cta" type="submit">{E(rot)}</button>
        </div>
        <p class="err" role="alert">{i('alert',16)}<span>Informe um e-mail válido para continuar.</span></p>
        <p class="note">Ao clicar você aceita receber nossas comunicações, conforme <a href="#">Política de Privacidade</a></p>
      </form>'''

def stores():
    return f'''<div class="stores"><a class="store" href="#">{i('phone',26)}<span><small>Baixar na</small><b>App Store</b></span></a><a class="store" href="#">{i('play',26)}<span><small>Disponível no</small><b>Google Play</b></span></a></div>'''

def hero(R, p):
    crumb = f'<nav class="crumb" aria-label="Você está em"><a href="{R}">Início</a>{i("chevR",14)}' + \
            (f'<a href="{R}#inicio" onclick="document.getElementById(\'solBtn\').click();return false">Soluções</a>{i("chevR",14)}' if p.get('sol') else '') + \
            f'<span aria-current="page">{E(p["nome"])}</span></nav>'
    tag = f'<span class="sol-tag"><span class="tone">{i(p["ic"],18)}</span>{E(p["nome"])}</span>' if p.get('sol') else ''
    precos = ''
    if p.get('precos'):
        precos = '<div class="price-row">' + ''.join(
            f'<div class="ph"><small>{E(r)}</small>' + (f'<s>{E(ant)}</s>' if ant else '') + f'<b>{E(v)}</b>' + (f'<em>{E(u)}</em>' if u else '') + '</div>'
            for (r, v, ant, u) in p['precos']) + '</div>'
    checks = ''
    if p.get('chips'):
        checks = '<div class="checks-row">' + ''.join(f'<span>{i("check",16)}{E(c)}</span>' for c in p['chips']) + '</div>'
    if p.get('ctas'):
        acao = '<div class="hero-ctas">' + ''.join(f'<a class="btn {cls}" href="{href if href.startswith("#") else R + href}">{E(rot)}</a>' for (rot, href, cls) in p['ctas']) + '</div>'
    else:
        acao = signup()
    disc = f'<p class="disc">{E(p["disc"])}</p>' if p.get('disc') else ''
    floats = ''
    pos = ['left:-24px;top:90px', 'right:-18px;bottom:70px']
    for k, (fi, tone, t, s) in enumerate(p.get('floats', [])[:2]):
        floats += f'<div class="layer{" hide-xs" if k else ""}" data-depth="{22 + k * 8}" data-speed="{-0.16 - k * 0.06:.2f}" style="{pos[k]};z-index:3"><div class="float" style="animation-delay:-{k * 2 + 1}s"><span class="tone {tone}">{i(fi)}</span><div><b>{E(t)}</b><small>{E(s)}</small></div></div></div>'
    return f'''<section class="hero" id="inicio" aria-labelledby="h1">
  <div class="blob a" data-speed="0.2"></div><div class="blob b" data-speed="-0.1"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumb}
      {tag}
      <h1 id="h1">{E(p["h1"])}</h1>
      <p class="lead">{E(p["lead"])}</p>
      {precos}
      {acao}
      {checks}
      {disc}
    </div>
    <div class="stage" id="stage" aria-hidden="true">
      <div class="orbit o1 hero-orbit" data-depth="4">
        <div class="sat" style="--a:20deg;--r:330px"><span>{i(p["ic"],24)}</span></div>
        <div class="sat" style="--a:140deg;--r:330px"><span>{i(p.get("ic2","spark"),22)}</span></div>
        <div class="sat" style="--a:260deg;--r:330px"><span>{i(p.get("ic3","check"),22)}</span></div>
        <div class="sat small" style="--a:80deg;--r:330px"><span></span></div>
        <div class="sat small green" style="--a:200deg;--r:330px"><span></span></div>
      </div>
      <div class="orbit o2 hero-orbit" data-depth="8">
        <div class="sat small green" style="--a:60deg;--r:260px"><span></span></div>
        <div class="sat small" style="--a:240deg;--r:260px"><span></span></div>
      </div>
      <div class="layer photo-hero" data-depth="5" data-speed="-0.04"><img src="/img/{p["foto"]}.webp" alt="" width="1280" height="960" /></div>
      {floats}
    </div>
  </div>
</section>
'''

def cab(d, centro=False):
    estilo = '' if centro else ' style="align-self:flex-start"'
    eb = f'<span class="eyebrow"{estilo}><b>{E(d["eyebrow"][0])}</b> {E(d["eyebrow"][1])}</span>' if d.get('eyebrow') else ''
    lead = f'<p class="lead">{E(d["lead"])}</p>' if d.get('lead') else ''
    return f'<div class="sec-head{" center" if centro else ""} rv">{eb}<h2 class="h2">{E(d["titulo"])}</h2>{lead}</div>'

def nota(t, info=False):
    return f'<p class="nota{" info" if info else ""} rv">{i("alert" if not info else "spark",16)}<span>{E(t)}</span></p>' if t else ''

def wrap_sec(d, corpo, centro=True):
    cls = 'panel sec' if d.get('panel') else 'sec'
    ident = f' id="{d["id"]}"' if d.get('id') else ''
    alvo = ' alvo' if d.get('id') else ''
    return f'<section class="{cls}{alvo}"{ident}><div class="wrap">{cab(d, centro) if d.get("titulo") else ""}{corpo}</div></section>\n'

def b_cards(R, d):
    cols = d.get('cols', 3)
    itens = ''
    for k, it in enumerate(d['itens']):
        ic, t, desc = it[0], it[1], it[2] if len(it) > 2 else ''
        tone = it[3] if len(it) > 3 else ''
        itens += f'<article class="card rv" style="--d:{(k % cols) * 80}ms"><span class="tone {tone}">{i(ic,22)}</span><h3 class="sm">{E(t)}</h3>' + (f'<p>{E(desc)}</p>' if desc else '') + '</article>'
    return wrap_sec(d, f'<div class="grid" style="--cols:{cols}">{itens}</div>{nota(d.get("nota"))}')

def b_passos(R, d):
    itens = ''.join(f'<div class="step rv" style="--k:{k};--d:{k * 90}ms"><span class="n">{k + 1}</span><b>{E(t)}</b>' + (f'<p>{E(x)}</p>' if x else '') + '</div>'
                    for k, (t, x) in enumerate(d['itens']))
    cta = f'<div style="display:flex;justify-content:center;margin-top:40px" class="rv"><a class="btn btn-cta" href="{R}{d["cta"][1]}">{E(d["cta"][0])} {i("arrowR",18)}</a></div>' if d.get('cta') else ''
    return wrap_sec(d, f'<div class="steps rv" style="--cols:{min(len(d["itens"]), 5)}">{itens}</div>{cta}')

def b_abas(R, d):
    uid = d.get('uid', 'a')
    bts, pns = '', ''
    for k, ab in enumerate(d['abas']):
        rot, ic, tit, txt = ab[0], ab[1], ab[2], ab[3]
        extra = ab[4] if len(ab) > 4 else []
        foto = ab[5] if len(ab) > 5 else None
        bts += f'<button type="button" role="tab" id="t-{uid}{k}" aria-controls="p-{uid}{k}" aria-selected="{"true" if k == 0 else "false"}">{i(ic,18)}{E(rot)}</button>'
        paras = ''.join(f'<p>{E(x)}</p>' for x in (txt if isinstance(txt, list) else [txt]))
        lst = ('<ul class="lista">' + ''.join(f'<li><span class="tone ok">{i("check",18)}</span>{E(x)}</li>' for x in extra) + '</ul>') if extra else ''
        vis = f'<div class="tp-vis">' + (f'<img src="/img/{foto}.webp" alt="" loading="lazy" />' if foto else f'<span class="ring"></span><span class="ring r2"></span><span class="big-ic">{i(ic,52)}</span>') + '</div>'
        pns += f'<div class="tp" role="tabpanel" id="p-{uid}{k}" aria-labelledby="t-{uid}{k}"{"" if k == 0 else " hidden"}><div class="tp-txt"><h3>{E(tit)}</h3>{paras}{lst}</div>{vis}</div>'
    corpo = f'<div class="tabs-box rv" data-tabs><div class="seg-scroll"><div class="seg" role="tablist" aria-label="{A(d["titulo"])}"><span class="pill" aria-hidden="true"></span>{bts}</div></div>{pns}</div>'
    return wrap_sec(d, corpo)

def b_precos(R, d):
    cols = d.get('cols', min(len(d['itens']), 4))
    itens = ''
    for k, it in enumerate(d['itens']):
        rot, v, ant, u = it[0], it[1], it[2], it[3]
        ic = it[4] if len(it) > 4 else None
        tag = it[5] if len(it) > 5 else None
        itens += f'<article class="pcard rv" style="--d:{k * 80}ms">' + (f'<span class="tag">{E(tag)}</span>' if tag else '') + \
                 (f'<span class="tone">{i(ic,20)}</span>' if ic else '') + f'<span class="rot">{E(rot)}</span>' + \
                 (f'<s>{E(ant)}</s>' if ant else '') + f'<span class="v">{E(v)}</span>' + (f'<span class="u">{E(u)}</span>' if u else '') + '</article>'
    extra = d.get('depois', '')
    return wrap_sec(d, f'<div class="pcards" style="--cols:{cols}">{itens}</div>{extra}{nota(d.get("nota"))}')

def tabela(t):
    cab_ = ''.join(f'<th scope="col">{E(c)}</th>' for c in t['cab'])
    linhas = ''
    for l in t['linhas']:
        linhas += '<tr>' + f'<th scope="row">{E(l[0])}</th>' + ''.join(
            f'<td class="{"ok" if str(c).startswith("Grátis") else ""}">{E(c)}</td>' for c in l[1:]) + '</tr>'
    cap = f'<caption>{E(t["legenda"])}</caption>' if t.get('legenda') else ''
    return f'<div class="tbl rv"><table>{cap}<thead><tr>{cab_}</tr></thead><tbody>{linhas}</tbody></table></div>'

def b_tabela(R, d):
    corpo = ''.join(tabela(t) for t in d['tabelas'])
    return wrap_sec(d, corpo + nota(d.get('nota')))

def b_lista(R, d):
    itens = ''.join(f'<li class="rv" style="--d:{k * 70}ms"><span class="tone {"ok" if d.get("ok", True) else ""}">{i(d.get("ic_item","check"),18)}</span>{E(x)}</li>' for k, x in enumerate(d['itens']))
    eb = f'<span class="eyebrow" style="align-self:flex-start"><b>{E(d["eyebrow"][0])}</b> {E(d["eyebrow"][1])}</span>' if d.get('eyebrow') else ''
    lead = f'<p class="lead">{E(d["lead"])}</p>' if d.get('lead') else ''
    cta = f'<a class="btn btn-cta" style="align-self:flex-start" href="{d["cta"][1] if d["cta"][1].startswith("#") else R + d["cta"][1]}">{E(d["cta"][0])} {i("arrowR",18)}</a>' if d.get('cta') else ''
    if d.get('foto'):
        flt = f'<div class="float"><span class="tone ok">{i(d["float"][0])}</span><div><b>{E(d["float"][1])}</b><small>{E(d["float"][2])}</small></div></div>' if d.get('float') else ''
        vis = f'<div class="media rv"><img src="/img/{d["foto"]}.webp" alt="{A(d.get("alt",""))}" loading="lazy" data-speed="0.06" />{flt}</div>'
    else:
        vis = f'<div class="media vis rv"><div class="tp-vis" style="position:absolute;inset:0;border-radius:0"><span class="ring"></span><span class="ring r2"></span><span class="big-ic">{i(d.get("ic","spark"),52)}</span></div></div>'
    cls = 'panel sec' if d.get('panel') else 'sec'
    ident = f' id="{d["id"]}"' if d.get('id') else ''
    return f'''<section class="{cls}{" alvo" if d.get("id") else ""}"{ident}><div class="wrap lista-grid{" inv" if d.get("inv") else ""}">
  <div style="display:flex;flex-direction:column;gap:20px" class="rv">{eb}<h2 class="h2">{E(d["titulo"])}</h2>{lead}<ul class="lista">{itens}</ul>{nota(d.get("nota"))}{cta}</div>
  {vis}
</div></section>
'''

def b_emais(R, d):
    itens = ''
    for k, (ic, t, desc, slug) in enumerate(d['itens']):
        tag = 'a' if slug else 'article'
        href = f' href="{R}solucoes/{slug}/"' if slug else ''
        mais = f'<span class="link-arrow">Saiba mais {i("arrowR",16)}</span>' if slug else ''
        itens += f'<{tag} class="card rv"{href} style="--d:{k * 80}ms"><span class="tone">{i(ic,22)}</span><h3 class="sm">{E(t)}</h3><p>{E(desc)}</p>{mais}</{tag}>'
    d2 = dict(d)
    d2.setdefault('titulo', 'E mais...')
    return wrap_sec(d2, f'<div class="grid" style="--cols:{d.get("cols", 4)}">{itens}</div>')

def b_quotes(R, d):
    def ini(a):
        partes = [w for w in re.split(r'\s+', a.replace('da ', '').replace('do ', '')) if w]
        return (partes[0][0] + (partes[-1][0] if len(partes) > 1 else '')).upper()
    itens = ''.join(f'<figure class="qcard rv" style="margin:0;--d:{(k % 2) * 90}ms"><blockquote style="margin:0"><p>{E(t)}</p></blockquote><figcaption class="who"><span>{E(ini(a))}</span><div><b>{E(a)}</b>' + (f'<small>{E(c)}</small>' if c else '') + '</div></figcaption></figure>'
                    for k, (t, a, c) in enumerate(d['itens']))
    return wrap_sec(d, f'<div class="quotes">{itens}</div>')

def b_faixa(R, d):
    eb = f'<span class="eyebrow"><b>{E(d["eyebrow"][0])}</b> {E(d["eyebrow"][1])}</span>' if d.get('eyebrow') else ''
    cta = f'<a class="btn btn-white" href="{R}{d["cta"][1]}">{E(d["cta"][0])} {i("arrowR",18)}</a>' if d.get('cta') else ''
    return f'<section class="sec-sm" style="padding:24px 0"><div class="wrap"><div class="faixa rv"><span class="tone">{i(d["ic"],28)}</span><div>{eb}<h3>{E(d["titulo"])}</h3>' + (f'<p>{E(d["texto"])}</p>' if d.get('texto') else '') + f'</div>{cta}</div></div></section>\n'

def b_sim(R, d):
    if d['tipo'] == 'cartao':
        opts = '<option value="1">Crédito à vista</option>' + ''.join(f'<option value="{n}">Parcelado em {n}x</option>' for n in range(2, 22)) + '<option value="0">Débito</option>'
        corpo = f'''<form class="sim rv" data-sim="cartao" novalidate>
  <div class="sim-in">
    <h3 style="font:800 20px/26px var(--font-family)">Vendas no cartão</h3>
    <div class="field"><label for="sv-valor">Valor da venda</label><input id="sv-valor" name="valor" inputmode="numeric" data-moeda value="1.000,00" /></div>
    <div class="field"><label for="sv-par">Como deseja receber</label><select id="sv-par" name="parcelas">{opts}</select></div>
    <label class="chk"><input type="checkbox" name="promo" checked /> Aplicar condição dos 3 primeiros meses</label>
    <button class="btn btn-cta" type="submit" style="align-self:flex-start">Simular venda</button>
    <p class="disc">Para fazer uma nova simulação, basta alterar os campos acima e clicar em simular venda novamente. Valores não válidos para o Asaas Tap. *Toda antecipação está sujeita a análise de crédito.</p>
  </div>
  <div class="sim-out" aria-live="polite">
    <small>Com Asaas você recebe</small><span class="big" data-o="recebe">R$ 0,00</span>
    <div class="linha"><span>Seu cliente paga</span><span data-o="cliente"></span></div>
    <div class="linha"><span>Taxa</span><span data-o="taxa"></span></div>
    <div class="linha"><span>Recebimento</span><span data-o="prazo"></span></div>
    <div class="linha"><span>Bandeiras aceitas</span><span>Visa, Mastercard, Elo, Amex, Hipercard</span></div>
  </div>
</form>'''
    else:
        corpo = f'''<form class="sim rv" data-sim="antecipacao" novalidate>
  <div class="sim-in">
    <h3 style="font:800 20px/26px var(--font-family)">Simular antecipação</h3>
    <div class="field"><label for="sa-valor">Valor da cobrança</label><input id="sa-valor" name="valor" inputmode="numeric" data-moeda value="1.000,00" /></div>
    <div class="field"><span class="lbl">Forma de pagamento</span><div class="radios"><label class="rad"><input type="radio" name="tipo" value="boleto" checked /> Boleto bancário</label><label class="rad"><input type="radio" name="tipo" value="cartao" /> Cartão de crédito</label></div></div>
    <button class="btn btn-cta" type="submit" style="align-self:flex-start">Simular antecipação</button>
    <p class="disc">Valores não válidos para o Asaas Tap. Consulte a página de taxas para mais informações sobre esse produto. *Antecipação sujeita a análise de crédito.</p>
  </div>
  <div class="sim-out" aria-live="polite">
    <small>Você recebe</small><span class="big" data-o="recebe">R$ 0,00</span><small data-o="tipo"></small>
    <div class="linha"><span>Composição</span><span data-o="info" style="text-align:right"></span></div>
    <div class="linha"><span>Prazo</span><span data-o="prazo"></span></div>
  </div>
</form>'''
    return wrap_sec(d, corpo + nota(TAXA_PADRAO))

def b_kv(R, d):
    linhas = ''.join(f'<tr><th scope="row">{E(a)}</th><td class="{"ok" if b_.startswith(("Grátis","Sem")) else ""}"><b>{E(b_)}</b></td></tr>' for a, b_ in d['itens'])
    return wrap_sec(d, f'<div class="tbl rv" style="max-width:760px;margin-left:auto;margin-right:auto"><table style="min-width:0"><tbody>{linhas}</tbody></table></div>' +
                    (f'<p class="disc rv" style="text-align:center;margin:16px auto 0">{E(d["rodape"])}</p>' if d.get('rodape') else ''))

def b_codigo(R, d):
    code = [['c', '// Criar uma cobrança via Pix com split\n'], ['k', 'POST'], ['', ' /v3/payments\n{\n  '], ['s', '"customer"'], ['', ': '], ['s', '"cus_000005219613"'], ['', ',\n  '],
            ['s', '"billingType"'], ['', ': '], ['s', '"PIX"'], ['', ',\n  '], ['s', '"value"'], ['', ': '], ['n', '1200.00'], ['', ',\n  '], ['s', '"dueDate"'], ['', ': '], ['s', '"2026-10-30"'], ['', ',\n  '],
            ['s', '"split"'], ['', ': [{ '], ['s', '"walletId"'], ['', ': '], ['s', '"…"'], ['', ', '], ['s', '"percentualValue"'], ['', ': '], ['n', '10'], ['', ' }]\n}\n\n'], ['k', '→ 200 OK'], ['', '  status: '], ['s', '"PENDING"']]
    chips = ''.join(f'<span class="chip">{i(ic,16)}{E(t)}</span>' for ic, t in d['chips'])
    return f'''<section class="api sec" style="margin-top:0"><div class="wrap api-grid">
  <div style="display:flex;flex-direction:column;gap:22px">
    <span class="eyebrow rv" style="align-self:flex-start"><b>API</b> {E(d["eyebrow"])}</span>
    <h2 class="h2 rv">{E(d["titulo"])}</h2>
    <p class="lead rv">{E(d["lead"])}</p>
    <div class="methods rv">{chips}</div>
  </div>
  <div class="rv" data-speed="-0.06">
    <div class="term" aria-label="Exemplo ilustrativo de chamada à API"><div class="term-top"><span></span><span></span><span></span><em>api.exemplo.com.br · sandbox</em></div><pre id="code" data-code="{A(json.dumps(code, ensure_ascii=False))}"><span class="caret"></span></pre></div>
    <div class="hook" id="hook">{i("hook",18)}Webhook recebido · PAYMENT_RECEIVED · R$ 1.200,00</div>
  </div>
</div></section>
'''

def b_contato_api(R, d):
    return wrap_sec(d, f'''<form class="form-card rv" data-contato novalidate style="max-width:860px;margin:40px auto 0">
  <div class="field"><label for="c-nome">Nome</label><input id="c-nome" name="nome" autocomplete="name" required /><span class="msg">Campo obrigatório.</span></div>
  <div class="field"><label for="c-emp">Empresa</label><input id="c-emp" name="empresa" autocomplete="organization" required /><span class="msg">Campo obrigatório.</span></div>
  <div class="field"><label for="c-cnpj">CNPJ</label><input id="c-cnpj" name="cnpj" inputmode="numeric" placeholder="00.000.000/0000-00" required /><span class="msg">Campo obrigatório.</span></div>
  <div class="field"><label for="c-vol">Volume de transações mensais</label><select id="c-vol" name="volume" required><option value="">Selecione o volume de transações mensais</option><option>Até R$ 50 mil</option><option>De R$ 50 mil a R$ 500 mil</option><option>De R$ 500 mil a R$ 5 milhões</option><option>Acima de R$ 5 milhões</option></select><span class="msg">Campo obrigatório.</span></div>
  <div class="field"><label for="c-mail">E-mail corporativo</label><input id="c-mail" name="email" type="email" autocomplete="email" required /><span class="msg">Campo obrigatório.</span></div>
  <div class="field"><label for="c-tel">Telefone/WhatsApp</label><input id="c-tel" name="tel" type="tel" autocomplete="tel" required /><span class="msg">Campo obrigatório.</span></div>
  <div class="field full"><label for="c-obj">Qual seu objetivo com o Asaas?</label><select id="c-obj" name="objetivo" required><option value="">Selecione o seu objetivo com o Asaas</option><option>Gateway de pagamento</option><option>Infraestrutura BaaS</option><option>Split de pagamentos</option><option>Asaas Checkout</option><option>Outro</option></select><span class="msg">Campo obrigatório.</span></div>
  <div class="full" style="display:flex;justify-content:flex-end"><button class="btn btn-cta" type="submit">Fale com um especialista {i("arrowR",18)}</button></div>
</form>''')

def b_timeline(R, d):
    itens = ''.join(f'<div class="tl-item rv"><span class="ano">{E(a)}</span><div class="card">{E(t)}</div></div>' for a, t in d['itens'])
    return wrap_sec(d, f'<div class="tl">{itens}</div>')

def b_texto(R, d):
    paras = ''.join(f'<p class="lead rv">{E(x)}</p>' for x in d['paragrafos'])
    lst = ''
    if d.get('lista'):
        lst = (f'<h3 class="rv" style="font:800 18px/24px var(--font-family);margin-top:8px">{E(d["lista_titulo"])}</h3>' if d.get('lista_titulo') else '') + \
              '<ul class="lista">' + ''.join(f'<li class="rv"><span class="tone ok">{i("check",18)}</span>{E(x)}</li>' for x in d['lista']) + '</ul>'
    sub = ''.join(f'<h3 class="rv" style="font:800 20px/26px var(--font-family);margin-top:12px">{E(t)}</h3><p class="lead rv">{E(x)}</p>' for t, x in d.get('blocos', []))
    eb = f'<span class="eyebrow rv" style="align-self:flex-start"><b>{E(d["eyebrow"][0])}</b> {E(d["eyebrow"][1])}</span>' if d.get('eyebrow') else ''
    vis = f'<div class="media rv"><img src="/img/{d["foto"]}.webp" alt="{A(d.get("alt",""))}" loading="lazy" data-speed="0.06" /></div>' if d.get('foto') else ''
    cls = 'panel sec' if d.get('panel') else 'sec'
    return f'''<section class="{cls}"><div class="wrap lista-grid{" inv" if d.get("inv") else ""}" style="align-items:start">
  <div style="display:flex;flex-direction:column;gap:18px">{eb}<h2 class="h2 rv">{E(d["titulo"])}</h2>{paras}{sub}{lst}</div>
  {vis}
</div></section>
'''

def b_valores(R, d):
    vals = ''.join(f'<span class="rv" style="--d:{k * 60}ms">{i(ic,18)}{E(t)}</span>' for k, (ic, t) in enumerate(d['valores']))
    return wrap_sec(d, f'''<div class="grid" style="--cols:2"><article class="card rv"><span class="tone">{i("target",22)}</span><h3 class="sm">Nosso propósito</h3><p>{E(d["proposito"])}</p></article>
<article class="card rv" style="--d:80ms"><span class="tone ok">{i("heart",22)}</span><h3 class="sm">Nossos valores</h3><div class="valores">{vals}</div></article></div>''')

def b_midia(R, d):
    itens = ''.join(f'<article class="card rv" style="--d:{(k % 4) * 70}ms"><span class="tone">{i("news",20)}</span><b>{E(t)}</b><span class="link-arrow" style="margin-top:auto">Ler matéria {i("arrowR",16)}</span></article>' for k, t in enumerate(d['itens']))
    return wrap_sec(d, f'<div class="news">{itens}</div>')

def b_contatos(R, d):
    def bloco(tit, linhas):
        return f'<article class="card rv"><h3>{E(tit)}</h3>' + ''.join(f'<a href="{h}"><span class="tone">{i(ic,20)}</span><span><small>{E(r)}</small><b>{E(v)}</b></span></a>' for ic, r, v, h in linhas) + '</article>'
    return wrap_sec(d, '<div class="contatos">' + bloco('Pessoa física', [('chat', 'Whatsapp', '0800 000 0000', '#'), ('mail', 'E-mail', 'contato@exemplo.com.br', 'mailto:contato@exemplo.com.br')]) +
                    bloco('Pessoa Jurídica', [('phone', 'Telefone', '0800 000 0000', 'tel:08000000000'), ('chat', 'Whatsapp', '0800 000 0000', '#'), ('mail', 'E-mail', 'contato@exemplo.com.br', 'mailto:contato@exemplo.com.br')]) + '</div>')

def b_gratis(R, d):
    itens = ''
    for k, (ic, t, free, lst, extra) in enumerate(d['itens']):
        li = ''.join(f'<li>{i("check",16)}{E(x)}</li>' for x in lst)
        itens += f'<article class="card rv" style="--d:{k * 80}ms"><span class="tone ok">{i(ic,22)}</span><h3 class="sm">{E(t)}</h3><span class="free">{E(free)}</span><ul>{li}</ul>' + (f'<p class="disc">{E(extra)}</p>' if extra else '') + '</article>'
    return wrap_sec(d, f'<div class="gratis">{itens}</div>')

def b_atalhos(R, d):
    return '<div class="atalhos"><nav aria-label="Ir para">' + ''.join(f'<a href="#{a}">{E(t)}</a>' for a, t in d['itens']) + '</nav></div>\n'

def b_stats_extra(R, d):
    st = ''.join(f'<div class="stat rv" style="--d:{k * 100}ms"><strong>{E(pre)}<span data-count="{v}" data-dec="{dec}">0</span><small>{E(un)}</small></strong><p>{E(rot)}</p></div>' for k, (v, dec, pre, un, rot) in enumerate(d['itens']))
    return wrap_sec(d, f'<div class="stats">{st}</div>')

BLOCOS = {'cards': b_cards, 'passos': b_passos, 'abas': b_abas, 'precos': b_precos, 'tabela': b_tabela, 'lista': b_lista, 'emais': b_emais,
          'quotes': b_quotes, 'faixa': b_faixa, 'sim': b_sim, 'kv': b_kv, 'codigo': b_codigo, 'contato_api': b_contato_api, 'timeline': b_timeline,
          'texto': b_texto, 'valores': b_valores, 'midia': b_midia, 'contatos': b_contatos, 'gratis': b_gratis, 'atalhos': b_atalhos, 'stats': b_stats_extra}

def seguranca(R, p):
    stats = list(STATS)
    if p.get('stat3'):
        stats[2] = p['stat3']
    st = ''.join(f'<div class="stat rv" style="--d:{k * 100}ms"><strong>{E(pre)}<span data-count="{v}" data-dec="{dec}">0</span><small>{E(un)}</small></strong><p>{E(rot)}</p></div>' for k, (v, dec, pre, un, rot) in enumerate(stats))
    pills = lambda lst, ic: ''.join(f'<span class="logo-pill">{i(ic,18)}{E(n)}</span>' for n in lst) + ''.join(f'<span class="logo-pill" aria-hidden="true">{i(ic,18)}{E(n)}</span>' for n in lst)
    return f'''<section class="sec" aria-labelledby="h-seg" style="overflow:hidden">
  <div class="wrap">
    <div class="sec-head rv"><span class="eyebrow" style="align-self:flex-start"><b>Segurança</b> Regulado e auditado</span><h2 class="h2" id="h-seg">{E(p.get("seg_titulo","Seu dinheiro está seguro com o Asaas"))}</h2><p class="lead">{E(p.get("seg_txt", SEGURO_TXT))}</p></div>
    <div class="stats">{st}</div>
    <div class="logos">
      <div><h3>Investidores</h3></div>
      <div class="marquee"><div class="track">{pills(INV,'trend')}</div></div>
      <div style="margin-top:12px"><h3>Alguns clientes</h3></div>
      <div class="marquee rev"><div class="track">{pills(CLI,'spark')}</div></div>
    </div>
  </div>
</section>
'''

def app(R, p):
    return f'''<section class="app" id="app" aria-labelledby="h-app">
  <div class="cloud" style="width:420px;height:200px;left:-60px;top:40px" data-speed="0.12"></div>
  <div class="wrap app-grid">
    <div style="display:flex;flex-direction:column;gap:22px;padding:72px 0">
      <span class="eyebrow rv" style="align-self:flex-start"><b>App</b> iOS e Android</span>
      <h2 class="h2 rv" id="h-app">{E(p.get("app_titulo","Use o Asaas no seu celular"))}</h2>
      <p class="lead rv">{E(p.get("app_txt","Emita cobranças e acompanhe seus pagamentos em poucos cliques."))}</p>
      <div class="rv">{stores()}</div>
    </div>
    <div class="app-stage" aria-hidden="true"><img class="app-photo" src="/img/campanha-celular-cartao.webp" alt="" width="896" height="864" loading="lazy" /></div>
  </div>
</section>
'''

def faq(R, p):
    itens = REF.get(p['ref'], {}).get('faq', []) if p.get('ref') else []
    if not itens:
        return ''
    qa = ''.join(f'<div class="qa rv{" open" if k == 0 else ""}" style="--d:{min(k, 6) * 50}ms"><h3><button type="button" aria-expanded="{"true" if k == 0 else "false"}" aria-controls="ans{k}" id="q{k}">{E(x["q"])}<span class="pm-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></span></button></h3><div class="ans" id="ans{k}" role="region" aria-labelledby="q{k}"><div><p>{E(x["a"])}</p></div></div></div>'
                 for k, x in enumerate(itens))
    return f'''<section class="sec" id="faq" aria-labelledby="h-faq">
  <div class="wrap faq-grid">
    <div class="faq-side">
      <span class="eyebrow rv" style="align-self:flex-start"><b>FAQ</b> Perguntas frequentes</span>
      <h2 class="h2 rv" id="h-faq">{E(p.get("faq_titulo","Alguma dúvida?"))}</h2>
      <p class="lead rv">Você tem alguma dúvida que não foi respondida aqui? Acesse nossa <a href="#">Central de Ajuda</a></p>
      <div class="contact rv">
        <a href="tel:08000000000"><span class="tone">{i("phone",20)}</span><span><b>0800 000 0000</b><small>Somente Pessoa Jurídica</small></span></a>
        <a href="mailto:contato@exemplo.com.br"><span class="tone">{i("mail",20)}</span><span><b>contato@exemplo.com.br</b><small>Canais de atendimento</small></span></a>
      </div>
    </div>
    <div class="acc">{qa}</div>
  </div>
</section>
'''

def final(R, p):
    return f'''<section class="final" aria-labelledby="h-final">
  <div class="blob a" style="top:-200px;right:-160px"></div><div class="blob b" style="left:-140px;bottom:-140px"></div>
  <div class="wrap" style="display:flex;flex-direction:column;align-items:center;gap:22px;max-width:760px">
    <span class="eyebrow rv"><b>Grátis</b> Sem mensalidade</span>
    <h2 class="h2 rv" id="h-final">{E(p.get("final_titulo","Cadastre-se agora!"))}</h2>
    <p class="lead rv">Ofereça diferentes formas de pagamento, gerencie cobranças, emita notas, antecipe recebíveis e pague fornecedores. Tudo em um só lugar.</p>
    <div class="rv" style="width:100%">{signup()}</div>
  </div>
</section>
'''

def pagina(caminho, p):
    prof = caminho.count('/')  # 'solucoes/pix-asaas' -> 1 -> ../../
    R = '../' * (prof + 1)
    ativo = p.get('ativo', '')
    corpo = hero(R, p)
    for tipo, d in p['secoes']:
        corpo += BLOCOS[tipo](R, d)
    if p.get('seguranca', True):
        corpo += seguranca(R, p)
    if p.get('app', True):
        corpo += app(R, p)
    corpo += faq(R, p)
    corpo += final(R, p)
    out = head(p['titulo'], p.get('desc', p['lead'])) + f'<body class="sub" data-root="{R}" data-pagina="{p.get("slug","")}">\n' + topo(R, ativo) + '<main>\n' + corpo + '</main>\n' + rodape(R)
    os.makedirs(caminho, exist_ok=True)
    open(os.path.join(caminho, 'index.html'), 'w', encoding='utf-8').write(out)
    return caminho

# ================================================================ CONTEÚDO DAS SOLUÇÕES
P = {}

P['pix-asaas'] = dict(nome='Pix', ic='pix', ic2='qr', ic3='send', foto='freelancer-celular',
    titulo='Pix PJ: cobre sem taxa e receba o pagamento na hora | Asaas',
    h1='(Pix)cou? Seu dinheiro está na conta!',
    lead='Ofereça o Pix como forma de pagamento, aumente suas vendas e ainda receba o dinheiro em segundos, direto na sua conta digital.',
    chips=['Transações gratuitas todo mês', 'Sem mensalidade e taxa de emissão de cobrança', 'Disponível 24 horas por dia, 7 dias por semana'],
    floats=[('pix', 'ok', 'Pix recebido', 'R$ 1.200,00 · em segundos'), ('qr', '', 'QR code dinâmico', 'Na fatura, com validade')],
    secoes=[
        ('abas', dict(titulo='Como eu posso usar o Pix?', uid='pix', abas=[
            ('Cobrar', 'receipt', 'Use para cobrar', 'Seu cliente só precisa escanear o QR code ou copiar o código da cobrança para realizar o pagamento, sem necessidade de preencher dados manualmente.', [], 'freelancer-celular'),
            ('Transferir', 'send', 'Use para transferir', 'Transfira por chave Pix ou por inserção manual de dados, direto da sua conta Asaas. Só no Asaas você tem 30 transações grátis todo mês para usar em Pix.'),
            ('Pagar', 'qr', 'Use para pagar', 'Pague por QR code dinâmico ou estático direto da sua conta. Pagamentos por QR code dinâmico são gratuitos.'),
        ])),
        ('cards', dict(panel=True, titulo='Vantagens que o Asaas oferece', cols=3, itens=[
            ('gift', 'Recebimentos grátis todo mês', 'Todo mês você, pessoa física, ganha 100 transações grátis para usar no recebimento de recursos via Pix (chave, inserção manual e QR code estático).', 'ok'),
            ('send', 'Transferências e pagamentos de graça com o Pix', 'Só no Asaas você tem 30 transações grátis todo mês para usar em Pix e pagamentos por QR code estático.'),
            ('receipt', 'Sem taxa de emissão de cobrança', 'Crie cobranças ilimitadas com o Pix. Você só é taxado após o seu cliente realizar o pagamento da fatura.'),
        ])),
        ('cards', dict(titulo='Por que usar o Pix no Asaas?', cols=3, nota=TAXA_PADRAO, itens=[
            ('clock', 'Instantâneo', 'Adeus, prazo de compensação! Receba ou transfira em segundos.'),
            ('cash', 'Barato', 'Venda pelo Pix e pague apenas R$ 0,99 por transação recebida nos 3 primeiros meses. Depois, apenas R$ 1,99 por transação recebida. É uma taxa fixa, não cobramos nada a mais.', 'ok'),
            ('calendar', 'Sem interrupções', 'Disponível 24 horas por dia, inclusive aos sábados, domingos e feriados.'),
            ('list', 'Prático', 'Chega de extratos espalhados! Cada recebimento é vinculado a uma fatura, organizando as vendas em um único lugar.'),
            ('award', 'Profissional', 'Faça vendas à vista, parceladas e recorrentes. Seu cliente recebe um comprovante assim que o pagamento é concluído, transmitindo mais confiança no seu negócio.'),
            ('shield', 'Seguro', 'Pode confiar! Os dados da sua empresa e do seu cliente são protegidos seguindo todas as normas do Banco Central.'),
        ])),
        ('tabela', dict(panel=True, titulo='Quanto custa o Pix no Asaas?', nota=TAXA_PADRAO, tabelas=[
            dict(legenda='Pagar e transferir', cab=['Modalidade', 'Pessoa física', 'Pessoa jurídica'], linhas=[
                ['Pagamento por QR code dinâmico', 'Grátis e ilimitado', 'Grátis e ilimitado'],
                ['Pagamento por QR code estático, transferência por chave ou por inserção manual de dados', 'Grátis e ilimitado', '30 transações grátis ao mês*. Depois, R$ 2,00 por transação'],
            ]),
            dict(legenda='Receber de seus clientes', cab=['Modalidade', 'Pessoa física', 'Pessoa jurídica'], linhas=[
                ['Na fatura (QR code dinâmico)', '3 primeiros meses: R$ 0,99 por fatura · Após 3 meses: R$ 1,99 por fatura', '3 primeiros meses: R$ 0,99 por fatura · Após 3 meses: R$ 1,99 por fatura'],
                ['Recebimento por QR code estático, por chave ou por inserção manual de dados', '100 transações grátis ao mês*. Depois, R$ 1,99 por transação (R$ 0,99 nos 3 primeiros meses)', '3 primeiros meses: R$ 0,99 por transação · Após 3 meses: R$ 1,99 por transação'],
            ]),
        ])),
        ('emais', dict(itens=EMAIS_PADRAO)),
    ])

P['boleto-bancario'] = dict(nome='Boleto bancário', ic='barcode', ic2='bell', ic3='qr', foto='empreendedora-atelie',
    titulo='Gerar boleto bancário parcelado, avulso ou recorrente | Asaas',
    h1='Gerar boletos com o Asaas é simples, rápido e seguro',
    lead='Emita boletos bancários em poucos cliques e pague apenas pelas cobranças recebidas.',
    precos=[('Por boleto recebido nos primeiros 3 meses', 'R$ 0,99', 'R$ 1,99', '')],
    chips=['Sem mensalidade', 'Sem taxa de emissão', 'Sem taxa de cancelamento'], disc=TAXA_PADRAO,
    floats=[('barcode', 'ok', 'Boleto pago', 'R$ 980,00 · Oficina Boa Obra'), ('bell', '', 'Lembrete enviado', '3 dias antes do vencimento')],
    stat3=(137.2, 1, '+', 'mi', 'de boletos pagos'), app_titulo='Gere boletos pelo aplicativo',
    secoes=[
        ('abas', dict(titulo='Ofereça a melhor opção para seu cliente', uid='bol', abas=[
            ('Boleto avulso', 'receipt', 'Para pagamentos únicos', 'Cobre seu cliente através de um dos meios de pagamentos mais populares no Brasil.'),
            ('Parcelamento', 'calendar', 'Para dividir em parcelas', 'Gere boleto parcelado e imprima em formato de carnê (três cobranças por folha A4), com QR code Pix em cada boleto.'),
            ('Assinatura', 'clock', 'Para pagamentos recorrentes', 'Crie cobranças recorrentes no boleto bancário e deixe que o Asaas envia a fatura para seu cliente todo mês.'),
            ('Link de pagamento', 'link', 'Para vender online', 'Gere um link de pagamento e compartilhe em suas redes sociais ou site.'),
        ])),
        ('passos', dict(panel=True, titulo='Como funciona a cobrança por boleto', cta=('Começar agora', 'criar-conta/'), itens=[
            ('Faça seu cadastro', 'Crie uma conta como pessoa física ou jurídica no Asaas, de forma rápida e gratuita.'),
            ('Crie a cobrança', 'Informe o valor e a data de vencimento e escolha se o boleto será à vista, parcelado ou recorrente. Preencha os dados do cliente e configure multa, juros e descontos.'),
            ('Configure as notificações', 'O Asaas envia lembretes automáticos para seu cliente via e-mail e SMS, antes e depois do vencimento. Se desejar, você também pode ativar o robô de voz.'),
            ('Aguarde o pagamento', 'O boleto será enviado automaticamente para o e-mail do seu cliente. Pode deixar que o Asaas te avisa quando o pagamento for confirmado.'),
            ('Receba o dinheiro', 'No Asaas, você escolhe a melhor forma de receber seu dinheiro. Faça transferências bancárias, pagamento de contas ou recarregue seu Cartão Asaas para saques ou compras.'),
        ])),
        ('cards', dict(titulo='Por que gerar boletos com o Asaas?', cols=4, itens=[
            ('clock', 'Economize tempo e dinheiro', 'Emita boletos em poucos cliques, direto do seu computador, celular ou tablet e pague apenas quando receber.'),
            ('list', 'Controle as cobranças', 'Gerencie os boletos recebidos, pendentes ou vencidos do início ao fim e reduza a inadimplência.'),
            ('bell', 'Profissionalize a comunicação', 'Envie lembretes automáticos aos seus clientes antes e depois do vencimento e receba alertas sobre cobranças pagas e vencidas.'),
            ('code', 'Integre os sistemas', 'Conecte o Asaas ao seu site, e-commerce ou sistema de gestão financeira e facilite as cobranças dos clientes.'),
        ])),
        ('emais', dict(panel=True, itens=EMAIS_PADRAO)),
    ])

P['cobranca-cartao'] = dict(nome='Cobrança por cartão', ic='card', ic2='shield', ic3='trend', foto='cafe-cartao',
    titulo='Cobrança por cartão de crédito e débito sem maquininha | Asaas',
    h1='Venda no crédito e débito sem maquininha de cartão',
    lead='Com o Asaas, você oferece várias opções de pagamento com apenas 1 ferramenta.',
    precos=[('Cartão de crédito · a partir de', '1,99% + R$ 0,49', '', 'por cobrança recebida nos primeiros 3 meses'), ('Antecipação · a partir de', '1,25%', '', 'ao mês')],
    chips=['Sem mensalidade', 'Sem aluguel ou maquininhas', 'Vendas à vista, parceladas e recorrentes'], disc=TAXA_PADRAO,
    floats=[('card', 'ok', 'Venda aprovada', 'R$ 3.500,00 em 10x'), ('shield', '', 'Antifraude grátis', 'Menos risco de chargeback')],
    secoes=[
        ('sim', dict(tipo='cartao', titulo='Simulador de vendas no cartão', lead='Calcule o valor a receber e escolha a melhor negociação para você e seu cliente')),
        ('abas', dict(panel=True, titulo='Ofereça as melhores condições de pagamento', uid='car', abas=[
            ('Cobrança avulsa', 'receipt', 'Para pagamentos à vista.', 'Cobre seu cliente de forma fácil e rápida, usando apenas o seu celular.', [], 'cafe-cartao'),
            ('Parcelamento', 'calendar', 'Prestação que cabe no bolso.', 'Dê poder de compra ao seu cliente: parcele as vendas em até 21 vezes e faça seu negócio decolar.'),
            ('Assinatura', 'clock', 'Para pagamentos recorrentes.', 'Com o Asaas, você nunca mais precisará se preocupar em enviar a fatura para seu cliente. Configure uma única vez e deixe que o Asaas faça o resto!'),
            ('Link de pagamento', 'link', 'Aumente suas vendas online.', 'Venda de onde estiver e não perca nenhum negócio: gere um link de pagamento e compartilhe em suas redes sociais ou site.'),
        ])),
        ('passos', dict(titulo='Como funciona a cobrança por cartão', cta=('Começar agora', 'criar-conta/'), itens=[
            ('Faça seu cadastro', 'Crie uma conta como pessoa física ou jurídica no Asaas, de forma rápida e gratuita.'),
            ('Crie a cobrança', 'Informe o valor e a data de vencimento e escolha se a cobrança será à vista, parcelada ou recorrente. Preencha os dados do cliente e configure multa, juros e descontos.'),
            ('Configure as notificações', 'O Asaas envia lembretes automáticos para seu cliente via e-mail e SMS, antes e depois do vencimento. Se desejar, você também pode ativar o robô de voz.'),
            ('Aguarde o pagamento', 'A fatura será enviada automaticamente para o e-mail do seu cliente e, ao acessar, ele poderá preencher os dados do cartão. Pode deixar que o Asaas te avisa quando o pagamento for confirmado.'),
            ('Receba o dinheiro', 'No Asaas, você escolhe a melhor forma de receber seu dinheiro. Faça transferências bancárias, pagamento de contas ou recarregue seu Cartão Asaas para saques ou compras.'),
        ])),
        ('cards', dict(panel=True, titulo='Por que gerar cobranças por cartão com o Asaas?', cols=3, itens=[
            ('hash', 'Taxa fixa sobre o valor total', 'O Asaas oferece preço justo e acessível para maximizar os lucros do seu negócio. Nossa taxa de transação é fixa sobre o valor total, independente da quantidade de parcelas.', 'ok'),
            ('bell', 'Reduza a inadimplência', 'Envie notificações automáticas para seus clientes por e-mail e SMS, prevenindo a inadimplência por esquecimento.'),
            ('trend', 'Receba antecipadamente', 'Solicite a antecipação de recebíveis e, após a aprovação do pedido, receba o dinheiro em 2 dias úteis, deixando o caixa sempre no verde.'),
            ('shield', 'Aumente a segurança nas transações', 'O Asaas oferece um sistema antifraude gratuito para aumentar suas chances de aprovação e reduzir o risco de fraudes, golpes e chargeback.'),
            ('code', 'Escale as cobranças com a API do Asaas', 'Nossa API é amiga do seu desenvolvedor: simples, flexível e modular. Você pode conectar o Asaas ao seu site, e-commerce ou sistema financeiro. Oferecemos uma infraestrutura BaaS, documentação completa, checkout, split de pagamento e muito mais.'),
        ])),
        ('emais', dict(itens=EMAIS_PADRAO[:3] + [('card', 'Cartão Asaas sem anuidade', 'Leve o saldo da sua Conta Asaas no bolso. Realize compras no crédito à vista, cadastre o cartão em assinaturas ou faça saques nos caixas 24h.', 'conta-digital')])),
    ])

P['asaas-tap'] = dict(nome='Asaas Tap', ic='pos', ic2='wifi', ic3='card', foto='feira-tap',
    titulo='Asaas Tap: transforme o seu celular em maquininha de cartão | Asaas',
    h1='Com o Asaas Tap seu celular vira maquininha de cartão',
    lead='Receba pagamentos via cartão de crédito e débito por aproximação, direto do seu celular com o Asaas Tap. Sem aluguel, sem mensalidade.',
    chips=['Disponível para Android', 'Principais bandeiras e carteiras digitais'],
    ctas=[('Baixe o App', '#app', 'btn-cta'), ('Criar conta grátis', 'criar-conta/', 'btn-ghost')],
    floats=[('wifi', 'ok', 'Pagamento aprovado', 'Por aproximação · crédito'), ('card', '', 'Até 21x', 'À vista ou a prazo')],
    seg_titulo='Mais de 240 mil empresas confiam no Asaas', app_titulo='Baixe agora o Aplicativo do Asaas e transforme seu celular em maquininha de cartão',
    faq_titulo='Alguma dúvida sobre o Asaas Tap?',
    secoes=[
        ('lista', dict(titulo='Suas vendas presenciais ficaram ainda mais fáceis', foto='feira-tap', alt='Vendedora de feira recebendo pagamento por aproximação no celular',
            lead='O Asaas Tap é a solução que transforma seu celular em maquininha de cartão. Basta instalar o app do Asaas em um dispositivo Android com tecnologia NFC (aproximação) e começar a utilizar.',
            itens=['Aproveite as menores taxas de cartão do mercado', 'Venda no cartão sem maquininha', 'Reduza custos operacionais', 'Melhore a experiência do seu cliente'],
            float=('check', 'Venda concluída', 'Comprovante pronto para envio'), cta=('Criar conta grátis', 'criar-conta/'))),
        ('cards', dict(panel=True, titulo='Seu celular pronto pra vender com o Asaas Tap', lead='Impulsione suas vendas com uma solução moderna, rápida e segura. É só baixar o app do Asaas e começar a vender!', cols=3, itens=[
            ('calendar', 'À vista ou a prazo? Seu cliente que escolhe', 'Venda no crédito à vista ou parcelado em até 21x.'),
            ('shield', 'Segurança para você e seus clientes', 'Certificação PCI-DSS e PCI MPoC.', 'ok'),
            ('wallet', 'Dinheiro direto na conta Asaas', 'Centralize suas vendas em um único lugar, por meio de uma solução totalmente integrada à conta digital e gestão financeira do Asaas.'),
        ])),
        ('precos', dict(titulo='Venda no cartão com as menores taxas do mercado, direto do Asaas Tap', lead='Receba pagamentos no crédito e no débito com taxas que fazem o seu lucro render mais. Tudo pelo seu celular, sem custo de adesão, mensalidades ou cobranças escondidas.', cols=3, nota=TAXA_PADRAO, itens=[
            ('Cartão de débito', '1,25%', '', 'por transação recebida', 'card'),
            ('Crédito à vista', '2,99%', '', 'sobre o valor da venda', 'card'),
            ('Crédito de 2 a 6 parcelas', '3,49%', '', 'sobre o valor total da venda', 'calendar'),
            ('Crédito de 7 a 12 parcelas', '3,99%', '', 'sobre o valor total da venda', 'calendar'),
            ('Crédito de 13 a 21 parcelas', '4,29%', '', 'sobre o valor total da venda', 'calendar'),
            ('Antecipação no crédito à vista', 'Grátis', '', 'Recebimento em até 2 dias úteis. Sujeito a análise de crédito', 'trend', 'Taxa zero'),
        ], depois='<div class="checks-row rv" style="opacity:1;animation:none;justify-content:center;margin-top:24px"><span>' + i('check',16) + 'Funcionalidade sem custos adicionais</span><span>' + i('check',16) + 'Disponível para dispositivos Android com tecnologia NFC</span><span>' + i('check',16) + 'Para contas PF e PJ</span></div>')),
        ('passos', dict(panel=True, titulo='Como vender com o Asaas Tap usando o seu celular', itens=[
            ('Abra o app Asaas no seu celular', ''),
            ('Acesse Vender com Asaas Tap', 'Digite o valor da venda e selecione a forma de pagamento.'),
            ('Seu cliente aproxima o cartão', 'Ou a carteira digital, direto no seu celular.'),
            ('Pronto!', 'Transação efetuada e comprovante disponível para envio.'),
        ])),
        ('emais', dict(titulo='Uma gama de soluções para impulsionar suas vendas', itens=[
            ('trend', 'Antecipação de recebíveis', 'Antecipe recebimentos futuros e garanta dinheiro no caixa.', 'antecipacao-de-recebiveis'),
            ('bell', 'Notificações de cobrança', 'Envie lembretes automáticos antes e depois do vencimento.', 'regua-de-cobranca'),
            ('search', 'Consulta e negativação serasa', 'Consulte o histórico financeiro dos clientes e negative inadimplentes direto da sua conta Asaas. Tudo para proteger suas vendas.', None),
            ('link', 'Link de pagamento', 'Venda online e compartilhe em suas redes sociais ou site.', 'link-pagamento'),
        ])),
    ])

P['link-pagamento'] = dict(nome='Link de pagamento', ic='link', ic2='chat', ic3='card', foto='loja-link',
    titulo='Link de pagamento: venda online sem taxa de emissão | Asaas',
    h1='Venda online com o link de pagamento do Asaas',
    lead='Compartilhe em seu site ou redes sociais e venda mais sem sair de casa.',
    precos=[('Boleto bancário', 'R$ 0,99', '', 'por cobrança recebida nos primeiros 3 meses'), ('Cartão de crédito · a partir de', '1,99% + R$ 0,49', '', 'por cobrança recebida nos primeiros 3 meses')],
    chips=['Sem mensalidade ou taxa de adesão'], disc=TAXA_PADRAO,
    floats=[('link', 'ok', 'Link pago', 'R$ 189,90 · Camisa de linho'), ('chat', '', 'Compartilhe', 'WhatsApp, Instagram ou site')],
    secoes=[
        ('cards', dict(titulo='Vantagens que só o link de pagamento do Asaas oferece', cols=3, itens=[
            ('calendar', 'Crie cobranças avulsas, parceladas ou recorrentes.'),
            ('cash', 'Defina o valor ou deixe que seu cliente escolha.'),
            ('gift', 'Anexe fotos dos seus produtos ou serviços ao link de pagamento.'),
            ('bell', 'Envie notificações automáticas por e-mail e SMS.'),
            ('heart', 'Receba pagamentos ou doações de forma fácil e simples'),
            ('globe', 'Faça vendas pela internet sem ter um site ou loja virtual'),
        ])),
        ('passos', dict(panel=True, titulo='Como criar um link de pagamento no Asaas', cols=4, cta=('Começar agora', 'criar-conta/'), itens=[
            ('Preencha as informações', 'Escolha se a cobrança será à vista, parcelada ou recorrente e defina o valor. No caso de doações, você tem a opção de deixar esse campo em aberto.'),
            ('Anexe as fotos do seu produto ou serviço', 'Deixe seu link de pagamento mais atrativo: adicione fotos dos seus produtos ou serviços e aumente as chances de fechar novas vendas.'),
            ('Compartilhe o link com seu cliente', 'Pronto! Agora você pode vender online. Basta compartilhar o link em seu site ou redes sociais.'),
            ('Acompanhe os recebimentos', 'Visualize a situação das cobranças e receba uma notificação quando seu cliente realizar o pagamento. Use seu saldo para transferências, pagamentos e recargas no Cartão Asaas.'),
        ])),
        ('abas', dict(titulo='Escolha como usar seu link de pagamento', uid='lnk', abas=[
            ('Vendas online', 'cart', 'Vendas online', 'Quebre a barreira da distância! Com o link de pagamento, você vende de onde estiver para qualquer pessoa, direto do seu celular.', [], 'loja-link'),
            ('Doações', 'heart', 'Doações', 'Transforme suas ideias em ação! Crie um link de pagamento e arrecade dinheiro para sua ONG, campanhas ou igrejas.'),
        ])),
        ('emais', dict(panel=True, itens=EMAIS_BOLETO)),
    ])

P['nota-fiscal'] = dict(nome='Nota fiscal', ic='file', ic2='calendar', ic3='code', foto='gestora-notas',
    titulo='Emitir nota fiscal de serviço eletrônica é rápido com o Asaas',
    h1='Emitir nota fiscal com o Asaas é rápido e automático',
    lead='Torne sua empresa mais eficiente! O Asaas automatiza o envio de nota fiscal de serviço e você ganha tempo para focar no crescimento do seu negócio.',
    precos=[('Por nota emitida', 'R$ 0,49', '', 'Mais barato que um cafezinho')],
    chips=['Sem mensalidade', 'Sem taxa de cancelamento'], disc=TAXA_PADRAO,
    floats=[('file', 'ok', 'NFS-e emitida', 'Enviada ao cliente por e-mail'), ('calendar', '', 'Emissão agendada', 'Na data que você escolher')],
    secoes=[
        ('passos', dict(titulo='Nós emitimos as notas fiscais para você! Entenda como funciona:', itens=[
            ('Faça seu cadastro', 'Crie uma conta como pessoa jurídica no Asaas e cadastre as informações fiscais, seus dados de acesso ao portal da prefeitura e os serviços. Basta configurar apenas uma vez para começar a emitir notas!'),
            ('Escolha a forma de emissão', 'Só no Asaas você tem a opção de emitir as notas junto com a cobrança, poupando tempo no preenchimento de informações. Você também pode emitir a nota avulsa.'),
            ('Informe o tipo de serviço e os impostos', 'Selecione um serviço já cadastrado ou informe as alíquotas de imposto para que o Asaas faça o cálculo automático para você.'),
            ('Selecione a data de emissão', 'Emita notas de forma instantânea ou agende a emissão para o período mais conveniente.'),
            ('Aguarde a emissão da nota', 'Seu cliente receberá a nota por e-mail na data que você configurou. Você pode acompanhar o status das notas emitidas no sistema Asaas.'),
        ])),
        ('cards', dict(panel=True, titulo='Por que preciso emitir nota fiscal com o Asaas?', cols=3, nota=TAXA_PADRAO, itens=[
            ('spark', 'Emissão automática', 'No Asaas não tem burocracia! Você configura a emissão de NFS-e apenas uma vez e dá adeus à papelada.', 'ok'),
            ('cash', 'Sem mensalidade ou taxa de adesão', 'Pague apenas R$ 0,49 por NFS-e emitida. O agendamento ou cancelamento é gratuito.'),
            ('calendar', 'Notas instantâneas ou agendadas', 'Você escolhe quando o Asaas deve emitir a NFS-e, seja de forma imediata ou em uma data futura.'),
            ('users', 'Atendimento personalizado', 'Conte com o atendimento exclusivo de nossos especialistas em NFS-e.'),
            ('code', 'Integração fácil via API', 'Conecte a emissão de NFS-e ao seu site ou sistema de gestão financeira.'),
        ])),
        ('emais', dict(itens=EMAIS_BOLETO)),
    ])

P['conta-digital'] = dict(nome='Conta digital', ic='wallet', ic2='card', ic3='send', foto='campanha-celular-cartao',
    titulo='Conta digital completa e sem mensalidade | Criar conta Asaas',
    h1='Conta digital Asaas: livre-se das tarifas abusivas!',
    lead='Resolva tudo em um só lugar: cobre seus clientes por cartão, boleto ou Pix, receba direto na Conta Asaas, pague fornecedores e ainda gerencie todo o financeiro da sua empresa.',
    chips=['Zero mensalidade', 'Zero travamentos ou bloqueios da conta', 'Cuidamos da burocracia para você'],
    floats=[('send', 'ok', 'Pix enviado', 'Grátis · 30 por mês'), ('card', '', 'Cartão Asaas', 'Sem anuidade')],
    secoes=[
        ('cards', dict(titulo='No Asaas, você tem liberdade para usar seu dinheiro como quiser', cols=4, itens=[
            ('send', 'Transferências grátis todo mês com o Pix', 'Transfira seu dinheiro para outra conta sem pagar nada. Só no Asaas você tem 30 transferências via Pix gratuitas por mês.', 'ok'),
            ('barcode', 'Pagamento de contas gratuito', 'Pague boletos e quite impostos e contas de consumo direto do seu celular ou computador, sem custos de transação.'),
            ('card', 'Cartão Asaas de graça na sua casa, sem anuidade', 'Leve o saldo da sua Conta Asaas no bolso. Com o Cartão Asaas, você faz compras, saca dinheiro nos caixas 24h e cadastra seu cartão em assinaturas, como aplicativos de transporte e plataformas de streaming.'),
            ('trend', 'Dinheiro antecipado', 'Receba o dinheiro das cobranças por cartão de crédito em até 2 dias úteis e por boleto em até 3 dias úteis, e otimize o seu fluxo de caixa.'),
        ])),
        ('cards', dict(panel=True, titulo='Mais do que uma conta digital, uma nova forma de receber dinheiro de seus clientes', cols=3, itens=[
            ('receipt', 'Emissão de cobranças a custo zero', 'Crie cobranças únicas, parceladas e recorrentes e pague apenas pelas transações recebidas. A emissão é grátis.', 'ok'),
            ('cash', 'Várias opções de pagamento', 'Cobre seus clientes usando Pix, cartão de crédito ou débito, link de pagamento ou boleto bancário e aumente suas vendas.'),
            ('bell', 'Régua de cobrança automatizada', 'Envie lembretes aos seus clientes por WhatsApp, e-mail, SMS ou robô de voz e aumente suas chances de receber em dia.'),
        ])),
        ('cards', dict(titulo='Tudo que você precisa para gerenciar seu negócio', cols=4, itens=[
            ('trend', 'Retome o controle do seu financeiro', 'Acompanhe seu faturamento e monitore entradas e saídas através dos indicadores e relatórios personalizados do Asaas.'),
            ('file', 'Livre-se da burocracia ao emitir notas', 'Com a automação de NFS-e, você cadastra os dados da sua empresa apenas uma vez e se livra da papelada para sempre.'),
            ('search', 'Tome decisões baseadas em dados', 'Use o Asaas para consultar o nome do seu cliente no Serasa e obtenha um relatório detalhado sobre ele antes de fechar a venda.'),
            ('code', 'Tenha uma integração simples (de verdade)', 'Precisa conectar o Asaas ao seu ERP ou outro sistema? Nossa API é fácil, modular e amiga do seu desenvolvedor.'),
        ])),
        ('kv', dict(panel=True, titulo='Conta Asaas: sem mensalidade, mais benefícios para você', rodape='Pague apenas pelo uso.', itens=[
            ('Transferências', '30 grátis por mês'), ('Emissão de cobranças', 'Grátis'), ('Emissão e envio do Cartão Asaas', 'Grátis para Pessoa Jurídica'),
            ('Manutenção do Cartão Asaas', 'Sem anuidade'), ('Manutenção da Conta Asaas', 'Sem mensalidade'), ('Pague contas', 'Grátis'), ('Suporte multicanal', 'Grátis'),
        ])),
        ('passos', dict(titulo='Crie sua conta Asaas e comece a emitir sua primeira cobrança em minutos', cols=3, cta=('Criar conta grátis', 'criar-conta/'), itens=[
            ('Faça seu cadastro pelo aplicativo ou via web.', ''), ('Envie os documentos solicitados.', ''), ('Realize o primeiro acesso e comece a usar.', ''),
        ])),
        ('cards', dict(panel=True, titulo='Atendimento humanizado, feito por pessoas reais', cols=4, itens=[
            ('chat', 'Suporte multicanal', 'Fale com pessoas de verdade em nossos canais virtuais. Não perca mais tempo em filas ou no deslocamento até a agência. Nosso atendimento é feito de forma totalmente remota.'),
            ('users', 'Time de atendimento dedicado', 'No Asaas, você tem um time de atendimento exclusivo para tirar dúvidas, entender suas necessidades e resolver problemas.'),
            ('clock', 'Atendimento humano', 'Converse conosco de segunda a sexta, das 8h às 22h, e aos sábados, domingos e feriados, das 8h às 18h. Além disso, se precisar, nosso suporte automatizado está sempre disponível para tirar suas dúvidas.'),
            ('award', 'Excelência no atendimento', 'Temos o Selo RA1000, reconhecimento concedido a empresas que se destacam pelos excelentes índices de atendimento no Reclame Aqui.', 'ok'),
        ])),
    ])

P['regua-de-cobranca'] = dict(nome='Régua de cobrança', ic='bell', ic2='chat', ic3='mail', foto='freelancer-celular',
    titulo='Régua de cobrança automatizada Asaas: Inadimplência Zero',
    h1='Receba em dia com a régua de cobrança automatizada',
    lead='Envie lembretes de cobrança automáticos aos seus clientes por diversos canais, antes e depois do vencimento. Evite calotes e recupere dívidas.',
    chips=['Notificações por WhatsApp', 'Notificações por e-mail', 'Notificações por SMS', 'Notificações por ligação (robô de voz)', 'Notificações por Correios'],
    floats=[('chat', 'ok', 'WhatsApp enviado', 'Sua cobrança vence em 5 dias!'), ('check', '', 'O pagamento foi recebido!', 'Depois do lembrete')],
    seg_titulo='Asaas, levando tecnologia financeira para as empresas', seg_txt='O Asaas é uma fintech que cresce constantemente. Somos a 31ª instituição de pagamentos autorizada pelo Banco Central, código 461, com licença para atuar como sociedade de crédito, financiamento e investimento.',
    secoes=[
        ('cards', dict(titulo='Conheça os canais disponíveis na régua de cobrança do Asaas', eyebrow=('Multicanal', 'Régua de cobrança multicanal inteligente'),
            lead='Utilize nossa régua de cobrança automatizada e explore uma gestão financeira mais eficaz para o seu negócio', cols=3, itens=[c + ('',) for c in CANAIS])),
        ('lista', dict(panel=True, titulo='Notificações personalizadas com a cara da sua empresa', foto='freelancer-celular', inv=True, alt='Empreendedora conferindo no celular uma notificação de pagamento',
            lead='Personalize o conteúdo das notificações de e-mail e SMS de um jeito único para se conectar ainda mais com seus clientes.', itens=NOTIF_PERS, nota=NOTIF_NOTA,
            float=('bell', 'Lembrete personalizado', 'Com o tom de voz da sua marca'), cta=('Começar agora', 'criar-conta/'))),
        ('cards', dict(titulo='Receber em dia é mais simples com o Asaas', lead='Aproveite as vantagens da nossa régua de cobrança automatizada:', cols=4, itens=[
            ('trend', 'Reduz a inadimplência', 'Com as notificações, as chances de receber em dia são maiores, pois seus clientes são lembrados a cada etapa da régua de cobrança sobre pagar as contas.', 'ok'),
            ('heart', 'Bom relacionamento com clientes', 'Cobre os seus clientes de forma leve e crie uma experiência positiva com uma régua de cobrança personalizada.'),
            ('clock', 'Eficiência operacional', 'Torne seu processo de cobrança mais eficiente com uma régua de cobrança automatizada, economizando tempo e recursos da equipe financeira.'),
            ('award', 'Imagem e profissionalismo', 'Com a régua de cobrança automatizada você notifica seus clientes de maneira formal e profissional, trazendo mais credibilidade para o seu negócio.'),
        ])),
        ('precos', dict(panel=True, titulo='Quanto custa notificar clientes com a régua de cobrança?', cols=4, nota=TAXA_PADRAO, itens=[
            ('Notificações por WhatsApp', 'R$ 0,55', '', 'por notificação enviada', 'chat'),
            ('Notificações por e-mail e SMS', 'R$ 0,99', '', 'pelo pacote de notificações usado a cada transação', 'mail'),
            ('Robô de voz (notificações por ligação automatizada)', 'R$ 0,55', '', 'por ligação', 'volume'),
            ('Notificações por carta (Correios)', 'R$ 2,91', '', 'por boleto enviado', 'send'),
        ])),
        ('lista', dict(titulo='API amigável ao desenvolvedor, escalável e de alta performance', ic='code', ic_item='code', ok=False,
            lead='A API do Asaas é uma das mais completas e robustas do mercado. Com fácil integração, ela foi projetada para suportar grandes volumes de cobrança e processamento de dados, garantindo a estabilidade da sua operação.',
            itens=['Dev Friendly e API Restful', 'Respostas em JSON', '99% de uptime e ambiente 100% seguro', 'Suporte para integração'], cta=('Conhecer a API', 'solucoes/api-de-pagamentos/'))),
        ('quotes', dict(panel=True, titulo='Quem usa, recomenda', itens=[
            ('No meu negócio anterior, eu tinha que ficar ligando para os clientes e montando as planilhas. Além de ser uma ferramenta fácil, o Asaas já trouxe essa parte de cobrança automática. Eu nunca tive problemas com a minha equipe porque eles já pegaram rápido o processo de operação', 'CFO da Hauseful', ''),
            ('Se fosse para definir o Asaas em uma frase, seria: uma empresa de tecnologia que impulsiona bons negócios', 'CEO da Yellowling', ''),
            ('É muito transparente, não precisamos nos preocupar com a parte de pagamentos ou cobrar os nossos clientes, porque a gente tem certeza que o Asaas entrega o melhor que tem no mercado', 'CTO da Molde.me', ''),
            ('A régua de cobrança do Asaas ajudou a ProJuris a reduzir 50% do índice de churn (indicador que mede a perda de clientes). Assim, conseguimos estabilizar a saúde do caixa e, ainda, organizar os contratos da empresa.', 'CFO da ProJuris', ''),
        ])),
    ])

P['antecipacao-de-recebiveis'] = dict(nome='Antecipação de recebíveis', ic='trend', ic2='cash', ic3='calendar', foto='empreendedora-atelie',
    titulo='Antecipação de recebíveis: venda parcelado e receba à vista | Asaas',
    h1='Receba o dinheiro das suas vendas de forma antecipada',
    lead='Antecipe suas cobranças com taxas mínimas. Receba em até 2 dias úteis para cartão e 3 dias úteis para boleto, após análise. Ganhe flexibilidade para investir no seu negócio.',
    precos=[('Antecipação de cartão de crédito', 'A partir de 1,25%', '', 'ao mês'), ('Antecipação de boleto bancário', 'A partir de 5,79%', '', 'ao mês')], disc=TAXA_PADRAO,
    floats=[('trend', 'ok', 'Antecipação aprovada', 'R$ 4.900,00 em 2 dias úteis'), ('cash', '', 'Taxa zero', 'Crédito à vista no Asaas Tap')],
    stat3=(4782.0, 1, '+R$ ', 'bi', 'de antecipação de crédito'), seg_titulo='Conta digital PJ e gestão financeira segura',
    seg_txt='O Asaas é uma fintech que cresce constantemente. Somos a 31ª instituição de pagamentos autorizada pelo Banco Central, código 461, com licença para atuar como sociedade de crédito, financiamento e investimento.',
    secoes=[
        ('faixa', dict(ic='pos', eyebrow=('Lançamento', 'Asaas Tap'), titulo='Antecipação de crédito à vista com taxa zero no Asaas Tap', texto='Usando o Asaas Tap, você tem taxa zero de antecipação para crédito à vista e condições especiais para parcelamento.', cta=('Conhecer o Asaas Tap', 'solucoes/asaas-tap/'))),
        ('lista', dict(titulo='Antecipe recebíveis e tenha o dinheiro na mão em menos tempo', foto='cafe-cartao', alt='Dono de cafeteria recebendo pagamento com cartão',
            lead='Peça o adiantamento de recebíveis e garanta o capital de giro. Comece a vender parcelado e receber à vista!',
            itens=['Recebimento em 2 dias úteis para cartão', 'Recebimento em 3 dias úteis para boleto', 'Taxas competitivas', 'Antecipação automática de cartão'],
            float=('trend', 'Dinheiro no caixa', 'Antecipação automática ativada'))),
        ('sim', dict(panel=True, tipo='antecipacao', titulo='Simulador de antecipação de recebíveis', lead='Calcule o valor da taxa de antecipação de recebíveis do Asaas e garanta os recursos financeiros para manter a saúde do caixa da sua empresa.')),
        ('cards', dict(titulo='Use seu próprio dinheiro e liberte-se de outras fontes de crédito', cols=3, itens=[
            ('cash', 'Antecipe o recebimento de suas vendas, sem pagar altas taxas de juros.', '', 'ok'),
            ('shield', 'Faça antecipação de crédito e tenha capital de giro para usar em emergências ou investimentos.', ''),
            ('cart', 'Antecipe cobranças e negocie descontos maiores com fornecedores ao pagar à vista.', ''),
        ])),
        ('cards', dict(panel=True, titulo='Garanta as vantagens da antecipação de recebíveis no Asaas', lead='Tenha uma conta digital PJ completa, com recursos para otimizar a gestão financeira e antecipar recebíveis sempre que necessário.', cols=3, itens=[
            ('trend', 'Uma das taxas de antecipação mais competitivas do mercado', 'Antecipe vendas online a partir de 1,25% ao mês e vendas presenciais com taxa zero no crédito à vista pelo Asaas Tap.', 'ok'),
            ('file', 'Antecipação sem impostos', 'Peça o adiantamento de recebíveis e garanta o capital de giro. Comece a vender parcelado e receber à vista!'),
            ('card', 'Antecipação de boleto e cartão', 'Antecipe cobranças avulsas, parceladas ou recorrentes, no boleto bancário ou cartão de crédito.'),
        ])),
        ('cards', dict(titulo='Mais que uma plataforma de antecipação de recebíveis', lead='Além de antecipar recebíveis, no Asaas você tem um universo de recursos para otimizar a gestão financeira da sua empresa.', cols=3, itens=[
            ('search', 'Negative devedores no Serasa', 'Realize consultas e garanta o recebimento dos seus pagamentos com os recursos do Asaas + Serasa.'),
            ('shield', 'Tenha segurança nas transações', 'Use o sistema antifraude gratuito do Asaas e reduza o risco de fraudes, golpes e chargeback.'),
            ('split', 'Desfrute do split de pagamentos', 'Use o split de pagamentos para fazer a divisão dos recursos entre as subcontas e tenha um comissionamento automatizado.'),
            ('wallet', 'Gerencie o dinheiro com a conta digital PJ', 'Desfrute dos benefícios de uma conta digital completa e faça movimentações gratuitas.'),
            ('cash', 'Ofereça diferentes meios de pagamento', 'Faça cobrança por cartão de crédito, débito, Pix, Boleto bancário e link de pagamento.'),
            ('grid', 'Garanta a saúde do seu fluxo de caixa', 'Garanta a integração com o Base by Asaas, ERP na nuvem, com gestão financeira gratuita.'),
            ('file', 'Emita nota fiscal de serviço', 'Vincule as cobranças à emissão de notas ficais de forma fácil e prática.'),
            ('code', 'Faça a integração API', 'Conecte a API de pagamentos do Asaas ao seu site, e-commerce ou sistema financeiro.'),
            ('bell', 'Envie notificações e reduza a inadimplência', 'Envie notificações automáticas por WhatsApp, e-mail, SMS ou robô de voz, e garanta o recebimento em dia.'),
        ])),
        ('quotes', dict(panel=True, titulo='Quem antecipa com o Asaas', itens=[
            ('O Asaas não apenas fornece asas ao nosso negócio para voar, mas também compartilha conosco a filosofia de servir ao cliente e resolver problemas a qualquer custo. Essa parceria tem sido um elemento fundamental em nosso sucesso', 'CEO da Destra', ''),
            ('O suporte oferecido pelo Asaas é fundamental para o sucesso da integração, com uma abordagem 100% humanizada e eficiente. Nós estamos muito satisfeitos com essa parceria estabelecida. O Asaas facilitou muito nossa rotina', 'CEO da Revenda Mais', ''),
            ('É muito transparente, não precisamos nos preocupar com a parte de pagamentos ou cobrar os nossos clientes, porque a gente tem certeza que o Asaas entrega o melhor que tem no mercado', 'CTO da Molde.me', ''),
            ('O Asaas foi um ponto de agilidade, visibilidade e controle com relação a gestão de cobrança. 98% da operação é receita recorrente, o Asaas nos trouxe uma redução de tempo administrativo que nos permitiu focar em outras ações importantes para o negócio.', 'CTO da OSTEC', ''),
        ])),
    ])

P['erp'] = dict(nome='ERP', ic='grid', ic2='box', ic3='file', foto='gestora-notas',
    titulo='Base: ERP gratuito na nuvem, sem limites de usuários | Asaas',
    h1='Base, o ERP gratuito do Asaas',
    lead='Aumente seu faturamento e acelere o sucesso da sua empresa com um sistema de gestão empresarial 100% na nuvem.',
    chips=['Sem mensalidade', 'Sem limite de usuários', '100% na nuvem'],
    floats=[('box', 'ok', 'Pedido de venda', 'Faturado com NF-e'), ('users', '', 'Sem limite', 'de usuários')],
    secoes=[
        ('cards', dict(titulo='Um sistema ERP online e sem limite de usuários', cols=4, itens=[
            ('cash', 'ERP sem mensalidade', 'Faça a gestão da sua empresa sem pagar mensalidade ou taxa de adesão. Pague apenas pelos serviços que utilizar, quando utilizar e economize mais de R$ 2 mil por ano usando o Base.', 'ok'),
            ('globe', 'Armazenamento na nuvem', 'Acesse o ERP do Asaas de qualquer lugar ou dispositivo: basta ter internet.'),
            ('link', 'Integração com o Asaas', 'Centralize suas transações financeiras e conte com produtos do Asaas, como antecipação e régua de cobrança.'),
            ('shield', 'Segurança padrão Asaas', 'Por ser um sistema do Asaas, o Base ERP compartilha os mesmos padrões de segurança.'),
        ])),
        ('faixa', dict(ic='grid', eyebrow=('PJ', 'Base ERP'), titulo='Ei, PJ! Veja porque escolher o Base ERP', texto='O ERP do Asaas reúne recursos para automatizar processos de venda e centralizar informações de diversas áreas. Tenha ainda relatórios que oferecem uma visão clara das suas finanças, facilitando o controle e a tomada de decisões.', cta=('Criar conta grátis', 'criar-conta/'))),
        ('abas', dict(panel=True, titulo='ERP online fácil de usar', lead='Conheça os principais recursos disponíveis para simplificar a gestão da sua empresa.', uid='erp', abas=[
            ('Vendas e Serviços', 'cart', 'Para a gestão de vendas e serviços', 'Automatize processos de venda e centralize as informações do seu negócio.', ['Pedidos de vendas', 'Orçamentos e propostas comerciais', 'Ordens de serviço', 'Cadastro de clientes']),
            ('Estoque e Compras', 'box', 'Para o controle de estoque e compras', 'Gerencie os recebíveis, acompanhe as vendas e controle o estoque em um único lugar.'),
            ('Gestão Financeira', 'trend', 'Para a gestão financeira', 'Tenha relatórios que oferecem uma visão clara das suas finanças, facilitando o controle e a tomada de decisões.'),
            ('Controle Fiscal', 'file', 'Para o controle fiscal', 'Emita a Nota Fiscal de Produto Eletrônica (NF-e) e o Documento Auxiliar da Nota Fiscal Eletrônica (Danfe), disponíveis para todo o Brasil.'),
        ])),
        ('stats', dict(titulo='Simplificamos milhares de negócios', lead='Disponível para todo o Brasil', itens=[
            (27, 0, '', ' estados', 'Disponível para todo o Brasil'), (50, 0, '+', '', 'categorias de negócios'), (1000, 0, '+', '', 'clientes ativos, entre micro e pequenas empresas'),
        ])),
    ])
P['erp']['secoes'][3][1]['itens'][0] = (27, 0, '', '', 'estados: disponível para todo o Brasil')

P['api-de-pagamentos'] = dict(nome='API de pagamentos', ic='code', ic2='hook', ic3='split', foto='dev-api', ativo='api',
    titulo='API de pagamentos completa com integração simples | Asaas',
    h1='Escale sua operação com a API de pagamentos do Asaas',
    lead='Integre as soluções do Asaas com nossa API robusta e fácil de usar. Automatize processos, ofereça serviços financeiros aos seus clientes e fortaleça sua marca.',
    ctas=[('Fale com um especialista', '#especialista', 'btn-cta'), ('Criar conta grátis', 'criar-conta/', 'btn-ghost')],
    chips=['API REST', 'Sandbox para testes', 'Webhooks'],
    floats=[('code', 'ok', '200 OK', 'POST /v3/payments'), ('hook', '', 'Webhook', 'PAYMENT_RECEIVED')],
    seg_titulo='Levamos eficiência e tecnologia de ponta para as empresas', seg_txt='Somos uma instituição financeira regulamentada pelo Banco Central, código 461. Ajudamos pequenas e médias empresas a simplificar suas rotinas de pagamento com tecnologia e segurança.',
    final_titulo='+240 mil empresas já levaram a gestão financeira ao próximo nível',
    secoes=[
        ('cards', dict(titulo='Conheça os diferenciais da nossa API de pagamentos', cols=4, itens=[
            ('bank', 'BaaS Asaas: infraestrutura financeira completa, da operação ao compliance', 'Graças à API do Asaas, sua empresa consegue criar aplicações, oferecer e integrar serviços financeiros com todas as licenças e conformidades regulatórias por nossa conta.'),
            ('code', 'Crie suas próprias aplicações', 'Nossa API é robusta e fácil de integrar, perfeita para desenvolvedores e empresas que desejam construir aplicações de forma simples e segura.'),
            ('gift', 'Ofereça produtos financeiros', 'A solução BaaS do Asaas permite que sua empresa ofereça soluções sob medida, como meios de pagamento, antecipação de recebíveis e split de pagamento, para atender às necessidades dos seus clientes.'),
            ('trend', 'Integre para aumentar a eficiência', 'Integre as soluções do Asaas para automatizar e otimizar a operação da sua empresa. Ideal para negócios que lidam diariamente com alto volume de vendas e transações.'),
        ])),
        ('codigo', dict(eyebrow='Integração completa e fácil de integrar', titulo='Sua empresa cresceu? A gente te ajuda a escalar os pagamentos',
            lead='Use nossas soluções de recebimento e saída de dinheiro, antecipação, notificações e notas fiscais direto no seu sistema ou app.',
            chips=[('split', 'Split de pagamento'), ('bank', 'Infraestrutura BaaS'), ('hook', 'Webhooks')])),
        ('lista', dict(titulo='Gateway de pagamento completo e seguro para vendas online', eyebrow=('Gateway', 'Gateway de pagamento'), foto='dev-api', alt='Desenvolvedor integrando a API de pagamentos',
            lead='Aumente sua taxa de conversão e eleve a experiência de compra dos seus clientes com a tecnologia de ponta do nosso gateway de pagamento.',
            itens=['Ofereça Pix, boleto e cartão', 'Cobranças avulsas, parceladas e recorrentes', 'Integre em seu site, e-commerce, marketplace ou SaaS', 'Certificação PCI-DSS e sistema antifraude'],
            float=('check', 'Pagamento autorizado', 'Creditado na conta Asaas'), cta=('Fale com um especialista', '#especialista'))),
        ('passos', dict(panel=True, titulo='Como funciona um Gateway de Pagamento?', itens=[
            ('Cliente', 'O cliente escolhe o produto/serviço'), ('Sua empresa', 'Sua empresa utiliza o Gateway de pagamento Asaas para realizar a cobrança'),
            ('Gateway de pagamento Asaas', 'O cliente escolhe como deseja pagar e informa seus dados'), ('Envio das informações', 'O banco ou adquirente recebe e analisa as informações para viabilizar a transação'),
            ('Confirmação do pagamento', 'Pagamento autorizado? Ele será creditado em sua conta Asaas'),
        ])),
        ('lista', dict(titulo='Facilite suas vendas com o Asaas Checkout', eyebrow=('Checkout', 'Asaas Checkout'), ic='cart', inv=True,
            lead='Oferecemos um formulário de pagamento pronto para integrar ao seu e-commerce ou SaaS, de forma rápida e simples, sem a necessidade de desenvolvimento.',
            itens=['Automatize o preenchimento dos dados do cliente ou colete-os durante o checkout.', 'Defina o tempo de expiração do link de pagamento', 'Redirecione clientes automaticamente após a conclusão da venda', 'Utilize o split de pagamentos em conjunto com seu checkout.'])),
        ('cards', dict(panel=True, titulo='Plug and Play: aplicações e ferramentas prontas para conectar e usar!', eyebrow=('Plugins', 'Plugins e Apps'), lead='Integre facilmente suas ferramentas favoritas, sem precisar escrever uma única linha de código.', cols=4, itens=[
            ('cart', 'Integrações para vendas', ''), ('globe', 'Integrações para e-commerce', ''), ('spark', 'Automação de processos', ''), ('grid', 'E muito mais', ''),
        ])),
        ('abas', dict(titulo='Uma infinidade de soluções para potencializar seus recebimentos', uid='api', abas=[
            ('Split de pagamentos', 'split', 'Divida pagamentos de forma rápida e eficiente nas vendas online', 'Automatize a divisão de valores das suas vendas entre as partes envolvidas, seja vendedores, parceiros, franqueados, afiliados ou fornecedores. Poupe tempo e minimize falhas em seus repasses.', ['Personalize suas próprias regras de divisão', 'Fácil integração via API', 'Acompanhe o fluxo de splits pagos e recebidos']),
            ('Sandbox', 'code', 'Ambiente de testes seguro', 'O Sandbox é um ambiente de testes onde você consegue receber cobranças fictícias e testar suas integrações e Webhooks. Dessa forma você consegue ter mais segurança na hora de virar a chave para produção.'),
        ])),
        ('emais', dict(panel=True, titulo='Recursos integrados para simplificar suas rotinas e cobranças', cols=3, itens=[
            ('trend', 'Antecipação de recebíveis', 'Antecipe o recebimento das vendas de cartão e boleto (parceladas ou avulsas) e garanta capital de giro para investir na sua empresa.', 'antecipacao-de-recebiveis'),
            ('file', 'Automação de notas fiscais', 'Automatize a emissão e o envio de notas fiscais e livre-se da burocracia de uma vez por todas.', 'nota-fiscal'),
            ('bell', 'Régua de cobrança', 'Adeus, inadimplência! Programe o envio automático de notificações de cobrança aos seus clientes, antes, no dia ou após o vencimento.', 'regua-de-cobranca'),
        ])),
        ('quotes', dict(titulo='Quem integra, recomenda', itens=[
            ('Lá no início, quando a gente estava buscando ferramentas de pagamento, a facilidade de integrar com a API do Asaas foi um ponto que contribuiu para que a gente escolhesse o Asaas como nossa solução de pagamentos.', 'Maurício Montiel', 'CEO do Multipedidos'),
            ('Os outros gateways dificultavam a aprovação dos pagamentos, ou seja, a gente tentava vender e não conseguia. É por isso que eu digo que a chave de sucesso para qualquer produto é ter um bom gateway de pagamento. Assim, você resolve 80% dos problemas do seu negócio.', 'Salmeron Júnior', 'Diretor da CEAB'),
        ])),
        ('contato_api', dict(panel=True, id='especialista', titulo='Fale com um de nossos consultores', lead='Nossos especialistas estão preparados para entender as necessidades do seu negócio e oferecer as melhores soluções em pagamento e banking.')),
    ])

P['meios-de-pagamento'] = dict(nome='Meios de pagamento', ic='cash', ic2='pix', ic3='card', foto='loja-link',
    titulo='Não perca vendas por falta de opções de pagamento | Asaas',
    h1='Não perca vendas por falta de opções de pagamento',
    lead='Do boleto ao Pix, do cartão ao link de pagamento: conheça as soluções ideais para o seu negócio e aceite pagamentos de forma prática, totalmente segura e sem complicações.',
    chips=['Pix', 'Boleto', 'Cartão de crédito e débito', 'Link de pagamento'],
    floats=[('pix', 'ok', 'Pix recebido', 'Na hora, 24/7'), ('card', '', 'Parcele em até 21x', 'Sem juros para o seu cliente')],
    secoes=[
        ('faixa', dict(ic='pos', eyebrow=('Novo', 'Asaas Tap'), titulo='Transforme seu celular em maquininha de cartão com o Asaas Tap', texto='Receba pagamentos por aproximação direto do celular e ganhe agilidade nas vendas. Sem aluguel, sem mensalidades.', cta=('Conhecer o Asaas Tap', 'solucoes/asaas-tap/'))),
        ('abas', dict(titulo='Veja as principais tecnologias de pagamento que o Asaas tem para a sua empresa.', eyebrow=('Pagamentos', 'Falta pouco para você inovar a experiência de compra dos seus clientes'), uid='mei', abas=[
            ('Pix', 'pix', 'Pagamentos em um (Pix)car de olhos', 'Receba suas vendas de forma rápida e fácil, 24 horas por dia, 7 dias por semana. Sem prazos de compensação ou burocracia, o dinheiro cai diretamente na sua conta Asaas em questão de segundos.', [], 'freelancer-celular'),
            ('Boleto bancário', 'barcode', 'Boleto rápido, seguro e com emissão grátis', 'Ofereça aos seus clientes a opção de pagar com segurança e facilidade através do boleto. Além do tradicional código de barras, você pode receber pagamentos instantâneos ao inserir o QR Code Pix no boleto. Experimente agora mesmo.', ['Avulsos', 'Parcelados', 'Recorrentes']),
            ('Cartão de crédito e débito', 'card', 'Venda de onde quiser, como quiser e com as menores taxas', ['O cartão de crédito é um excelente meio de pagamento para aumentar suas vendas e fidelizar clientes, afinal, 82% das pessoas que compram online, usam o cartão de crédito.', 'Além da opção de fazer vendas por assinatura, você tem a possibilidade de parcelar em até 21 vezes sem juros, tornando a compra dos seus produtos ainda mais acessível.'], [], 'cafe-cartao'),
            ('Link de pagamento', 'link', 'Mais liberdade para receber suas cobranças', 'O link de pagamento é um método de cobrança versátil, que permite ao seu cliente escolher como deseja pagar: via boleto, Pix ou cartão de crédito. Uma vez criado, ele pode ser compartilhado em suas redes sociais, sites e onde você quiser.', [], 'loja-link'),
        ])),
        ('cards', dict(panel=True, titulo='Régua de cobrança multicanal inteligente', lead='Utilize nossa régua de cobrança automatizada e explore uma gestão financeira mais eficaz para o seu negócio', cols=5, itens=[(c[0], c[1], '') for c in CANAIS])),
        ('lista', dict(titulo='Notificações personalizadas com a cara da sua empresa', foto='freelancer-celular', alt='Empreendedora conferindo no celular uma notificação',
            lead='Personalize o conteúdo das notificações de e-mail e SMS de um jeito único para se conectar ainda mais com seus clientes.', itens=NOTIF_PERS, nota=NOTIF_NOTA, cta=('Começar agora', 'criar-conta/'),
            float=('bell', 'Lembrete enviado', 'Com a cara do seu negócio'))),
        ('faixa', dict(ic='spark', eyebrow=('E mais', 'E não pense que acabou…'), titulo='Experimente cobrar com o Asaas e economize com as menores taxas do mercado', texto='Aqui no Asaas você conta com split de pagamento, automatização de cobranças, gateway de pagamento e todas as soluções que entregam a melhor experiência em pagamentos para sua empresa e o seu cliente.', cta=('Começar agora', 'criar-conta/'))),
    ])

for slug, p in P.items():
    p['slug'] = slug
    p['sol'] = True
    p['ref'] = slug
    p.setdefault('desc', REF.get(slug, {}).get('descricao') or p['lead'])

# ================================================================ PREÇOS
PRECOS = dict(nome='Preços e taxas', ic='cash', ic2='card', ic3='trend', foto='campanha-celular-cartao', ativo='precos', slug='precos', ref='precos-e-taxas',
    titulo='Preços e taxas Asaas: conheça nossas soluções financeiras', desc=REF.get('precos-e-taxas', {}).get('descricao', ''),
    h1='Economize na gestão do seu negócio: o Asaas tem as menores taxas do mercado',
    lead='Aumente seus lucros já. Sem mensalidade e sem taxa de adesão: você paga apenas pelo que usar.',
    chips=['Sem mensalidade', 'Sem taxa de adesão', 'Pague apenas pelo uso'],
    floats=[('cash', 'ok', 'R$ 0,99', 'por Pix ou boleto recebido nos 3 primeiros meses'), ('gift', '', 'Serviços gratuitos', 'Conta, cobranças e suporte')],
    secoes=[
        ('atalhos', dict(itens=[('gratis', 'Serviços gratuitos'), ('recebimento', 'Recebimento'), ('tap', 'Asaas Tap'), ('notificacoes', 'Notificações e negativação'), ('antecipacao', 'Antecipação'), ('nota', 'Nota fiscal'), ('saques', 'Saques e saída de dinheiro')])),
        ('gratis', dict(id='gratis', titulo='Conheça nossos serviços gratuitos', itens=[
            ('receipt', 'Gestão de cobranças', 'Grátis', ['Emissão de cobranças', 'Alteração de cobranças', 'Cancelamento de cobranças', 'Personalização de fatura'], ''),
            ('card', 'Cartão Asaas', 'Grátis para Pessoa jurídica', [], 'Para cadastro de pessoa física, consultar taxas'),
            ('wallet', 'Conta digital', 'Grátis', ['Abertura da conta', 'Manutenção da conta', 'Extratos financeiros', 'Relatórios e indicadores', 'Pague contas', 'Transferências e pagamentos Pix (válido somente para cadastros de pessoa física)'], ''),
            ('shield', 'Segurança e suporte', 'Grátis', ['Importação de dados', 'Sistema antifraude', 'Suporte multicanal 24h'], ''),
        ])),
        ('faixa', dict(ic='link', eyebrow=('Pix | Boleto | Cartão de crédito', 'Ofereça diversas formas de pagamento'), titulo='Aumente suas vendas online com o link de pagamento', texto='Ofereça várias formas de pagamento com um único link e venda mais sem sair de casa.', cta=('Conhecer o link de pagamento', 'solucoes/link-pagamento/'))),
        ('precos', dict(id='recebimento', panel=True, titulo='Recebimento', lead='Taxas por transação recebida. Nos 3 primeiros meses, condições promocionais.', cols=3, itens=[
            ('Pix', 'R$ 0,99', 'R$ 1,99', 'por transação recebida (válido por 3 meses)', 'pix', '3 primeiros meses'),
            ('Boleto bancário', 'R$ 0,99', 'R$ 1,99', 'por transação recebida (válido por 3 meses)', 'barcode', '3 primeiros meses'),
            ('Cartão de débito', 'R$ 0,35 + 1,89%', '', 'por transação recebida', 'card'),
        ], depois=tabela(dict(legenda='Cartão de crédito', cab=['Parcelas', 'Taxa padrão', 'Nos 3 primeiros meses'], linhas=[
            ['À vista', 'R$ 0,49 + 2,99%', 'R$ 0,49 + 1,99%'], ['2 à 6 parcelas', 'R$ 0,49 + 3,49%', 'R$ 0,49 + 2,49%'],
            ['7 à 12 parcelas', 'R$ 0,49 + 3,99%', 'R$ 0,49 + 2,99%'], ['13 à 21 parcelas', 'R$ 0,49 + 4,29%', 'R$ 0,49 + 3,29%']])) +
            '<p class="disc rv" style="margin-top:12px">Sobre o valor total da venda para parcelamentos e por cobranças recebidas para assinaturas.</p>', nota=TAXA_PADRAO)),
        ('sim', dict(tipo='cartao', titulo='Simulador de vendas no cartão', lead='Calcule o valor a receber e escolha a melhor negociação para você e seu cliente')),
        ('precos', dict(id='tap', panel=True, titulo='Taxas menores e mais lucro nas suas vendas usando o Asaas Tap', cols=3, itens=[
            ('Cartão de débito', '1,25%', '', 'por transação recebida', 'card'),
            ('Antecipação no crédito à vista', 'Grátis', '', 'Recebimento em até 2 dias úteis. Sujeito a análise de crédito', 'trend', 'Taxa zero'),
            ('Crédito à vista', '2,99%', '', 'sobre o valor da venda', 'card'),
        ], depois=tabela(dict(legenda='Cartão de crédito no Asaas Tap', cab=['Parcelas', 'Taxa'], linhas=[['À vista', '2,99%'], ['2 à 6 parcelas', '3,49%'], ['7 à 12 parcelas', '3,99%'], ['13 à 21 parcelas', '4,29%']])) +
            '<p class="disc rv" style="margin-top:12px">Sobre o valor total da venda para parcelamentos e por cobranças recebidas para assinaturas.</p>', nota=TAXA_PADRAO)),
        ('precos', dict(id='notificacoes', titulo='Diminua a inadimplência do seu negócio', cols=3, nota=TAXA_PADRAO, itens=[
            ('Notificações por WhatsApp', 'R$ 0,55', '', 'por notificação enviada', 'chat'),
            ('Notificações por e-mail e SMS', 'R$ 0,99', '', 'pelo pacote de notificações usado a cada transação', 'mail'),
            ('Robô de voz (ligação automatizada)', 'R$ 0,55', '', 'por ligação', 'volume'),
            ('Notificações por carta (Correios)', 'R$ 2,91', '', 'por boleto enviado', 'send'),
            ('Consulta no Serasa', 'R$ 16,99', '', 'por consulta', 'search'),
            ('Negativação no Serasa', 'R$ 9,90', '', 'por cobrança negativada', 'alert'),
        ])),
        ('precos', dict(id='antecipacao', panel=True, titulo='Garanta dinheiro no caixa e fique sempre no verde', cols=2, nota=TAXA_PADRAO, itens=[
            ('Antecipação de cartão (à vista e parcelado)', '1,25% ao mês', '', 'Recebimento em até 2 dias úteis. Sujeito a análise de crédito', 'card'),
            ('Antecipação de boleto', 'A partir de 5,79% ao mês', '', 'Recebimento em até 3 dias úteis. Sujeito a análise de crédito', 'barcode'),
        ])),
        ('precos', dict(id='nota', titulo='Livre-se da papelada e reduza a burocracia', cols=1, nota=TAXA_PADRAO, itens=[('Nota fiscal eletrônica', 'R$ 0,49', '', 'por nota emitida', 'file')])),
        ('tabela', dict(id='saques', panel=True, titulo='Tenha liberdade para usar seu dinheiro como quiser', lead='Transferências via Pix e pagamentos grátis todo mês (pagamentos por QR Code dinâmico são gratuitos).', nota=TAXA_PADRAO, tabelas=[
            dict(cab=['Serviço', 'Pessoa física', 'Pessoa jurídica'], linhas=[
                ['Pix (pagamentos e transferências)', 'Grátis', 'Até 30 transferências grátis por mês e após R$ 2,00 por transação'],
                ['Pague contas', 'Grátis', 'Grátis'],
                ['Ted (transferências)', 'R$ 5,00', 'R$ 5,00'],
                ['Saques nacionais com Cartão Asaas', 'R$ 8,60', 'R$ 8,60'],
                ['Saques internacionais', 'R$ 10,00 + 3,5% de IOF', 'R$ 10,00 + 3,5% de IOF'],
            ])])),
        ('lista', dict(titulo='Ganhe escalabilidade nos processos financeiros', ic='code', ic_item='code', ok=False, lead='Temos uma API poderosa que vai transformar a experiência de pagamento dos seus clientes.',
            itens=['Infraestrutura BaaS', 'Checkout transparente', 'Split de pagamento', 'Tokenização de cartão'], cta=('Conhecer a API', 'solucoes/api-de-pagamentos/'))),
        ('cards', dict(panel=True, titulo='Todas as vantagens que seu negócio precisa em um único lugar', cols=4, itens=[
            ('barcode', 'Carnês e assinaturas por boleto', 'Crie cobranças parceladas ou recorrentes no boleto bancário e deixe que o Asaas envia a fatura para seu cliente todo mês.'),
            ('card', 'Vendas mais flexíveis no cartão', 'Parcele as cobranças em até 21 vezes no cartão de crédito, direto do seu celular, e receba o dinheiro de forma antecipada em até 2 dias úteis.'),
            ('send', 'Transferências grátis todo mês', 'Transfira seu dinheiro para outra conta sem pagar nada. Só no Asaas você tem 30 transferências gratuitas por mês, para qualquer banco.', 'ok'),
            ('bell', 'Redução da inadimplência', 'Envie lembretes antes e depois do vencimento, e receba confirmações quando o cliente fizer o pagamento.'),
        ])),
    ], app_titulo='Resolva tudo pelo celular', app_txt='Com o aplicativo do Asaas, você aumenta suas vendas e faz a gestão financeira do seu negócio de qualquer lugar.')

# ================================================================ SOBRE NÓS
SOBRE = dict(nome='Sobre nós', ic='heart', ic2='award', ic3='users', foto='empreendedora-atelie', ativo='sobre', slug='sobre', ref=None,
    titulo='Sobre o Asaas: conheça quem somos e nossa trajetória', desc=REF.get('sobre-nos', {}).get('descricao', ''),
    h1='A plataforma financeira e operacional para empresas mais completa do Brasil',
    lead='Asaas. Da gestão à evolução.',
    ctas=[('Conhecer nossa história', '#historia', 'btn-cta'), ('Criar conta grátis', 'criar-conta/', 'btn-ghost')],
    floats=[('users', 'ok', '+200 mil clientes', 'Empresas de todo o Brasil'), ('award', '', 'Desde 2010', 'Joinville · SC')],
    final_titulo='Cadastre-se agora!',
    secoes=[
        ('texto', dict(titulo='Quem somos', eyebrow=('Asaas', 'Da gestão à evolução'), foto='gestora-notas', alt='Empreendedora usando o Asaas no tablet',
            paragrafos=['O Asaas é uma das principais plataformas de gestão financeira e operacional para empresas do Brasil, responsável por centralizar e automatizar rotinas como cobranças, pagamentos, controle de fluxo de caixa, entre outros serviços que simplificam as operações dos negócios.',
                        'A companhia possui tecnologia robusta e integração via API, além de atuar como Instituição Financeira.'],
            blocos=[('O que fazemos', 'Desenvolvemos e oferecemos soluções para facilitar a gestão operacional e fortalecer a infraestrutura financeira das empresas.')],
            lista_titulo='Com o Asaas, você tem tudo em um só lugar:',
            lista=['Recebimentos por pix, boleto, cartão de crédito e débito', 'Conta digital PJ e ERP gratuitos', 'Asaas Tap (transforme seu celular em maquininha)', 'Cartão Asaas Mastercard', 'Antecipação de recebíveis', 'Régua de cobrança, emissão de nota fiscal e muito mais'])),
        ('valores', dict(panel=True, titulo='Movidos pelo seu desejo de ir mais longe', proposito='Acelerar a evolução dos negócios com inteligência, simplicidade e integração de tecnologias financeiras.',
            valores=[('heart', 'Respeito'), ('target', 'Comprometimento'), ('trend', 'Crescimento'), ('eye', 'Transparência'), ('users', 'Interesse genuíno pelo cliente'), ('award', 'Qualidade')])),
        ('texto', dict(titulo='Nossa história', inv=True, foto='cafe-cartao', alt='Empreendedor usando o Asaas no dia a dia',
            paragrafos=['O Asaas nasceu em 2010, na cidade de Joinville - SC. Fundado pelos irmãos Piero e Diego Contezini, a empresa foi fundada com o propósito de resolver uma dor que ambos já tinham lidado enquanto atuavam como sócios e fundadores de uma fábrica de software: a complexidade e ineficiência dos processos de cobrança, que eram totalmente manuais.',
                        'Impulsionados por uma veia empreendedora e atentos às transformações tecnológicas, Piero e Diego Contezini criaram o Asaas: uma solução automatizada, segura e escalável, capaz de transformar a rotina das empresas. O nome não foi escolhido por acaso, “Asaas” é um acrônimo de Automation for Software as a Service e sua pronúncia remete a “asas”, representando mais leveza e liberdade para a evolução dos negócios. O impacto foi imediato. Atividades que antes consumiam até 18 dias por mês passaram a ser realizadas em apenas cinco minutos por dia.'],
            blocos=[('Captações de investimentos', 'Em 2013, o Asaas captou sua primeira rodada de investimento Anjo e Semente. Esta seria a primeira de muitas outras captações expressivas na história da empresa, de entidades relevantes como Bradesco, Parallax e Vivo Ventures. Em 2024, conquistou a maior rodada de investimento da América Latina, com R$ 820M liderados pelo BOND Ventures.'),
                    ('Plataforma Completa', 'Desde 2021, o Asaas é autorizado como a 31ª Instituição de Pagamentos pelo Banco Central do Brasil. Visando ser uma plataforma cada vez mais completa, ao longo dos anos foram feitas aquisições para integrar outros serviços ao sistema, como Base ERP, Code Money e Mutuus Seguros. Hoje, mais que um facilitador para fluxos financeiros, o Asaas é uma tecnologia que existe para negócios evoluírem, integrando diversas soluções para o fluxo financeiro e operacional das empresas.')])),
        ('timeline', dict(panel=True, id='historia', titulo='Conheça os marcos da nossa trajetória', itens=[
            ('2010', 'Piero e Diego idealizam o projeto do Asaas, ainda dentro da Informant.'),
            ('2013', 'O projeto virou realidade: nascemos em Joinville-SC como empresa S/A, após uma rodada de captação Anjo e Semente.'),
            ('2019', 'Fomos eleitos uma das 100 startups mais inovadoras da América Latina pela Innovation Awards Latam Ranking. Conquistamos o Selo RA1000 e também o reconhecimento da Forbes.'),
            ('2020', 'Captamos R$ 37 milhões em investimento do Bradesco e Parallax. Ganhamos o Prêmio Reclame Aqui: empresa que mais evoluiu e aparecemos nas listas Latka (empresas que mais crescem) e 100 Startups to Watch (PEGN e Época Negócios).'),
            ('2021', 'Adquirimos o Base ERP e o Code Money. Fomos reconhecidos e autorizados pelo Bacen para atuar como a 31ª instituição de pagamento do Brasil.'),
            ('2022', 'Lançamos o cartão de crédito para PJ e criamos o boleto próprio, emitido pelo Asaas. Alcançamos a marca de 1 milhão de contas criadas, além de R$ 1 bilhão transacionados em apenas 1 mês.'),
            ('2023', 'Recebemos investimentos que totalizaram R$ 150 milhões. Atingimos 100 mil clientes. Ganhamos o selo de Great Place to Work e ainda realizamos nosso primeiro evento, o Asaas Connect, que reuniu 1.500 pessoas.'),
            ('2024', 'Atingimos a marca de R$ 1 bilhão em valor antecipado para os nossos clientes. Fizemos uma nova aquisição: a startup Nexinvoice. Captamos R$ 820 milhões, liderados pela BOND, para escalar a plataforma de automação financeira líder da América Latina.'),
            ('2025', 'Ultrapassamos a marca dos 200 mil clientes e adquirimos a empresa Mutuus, marcando nossa entrada no mercado de seguros.'),
            ('2026', 'Começamos a operar como Sociedade de Crédito, Financiamento e Investimento (SCFI) autorizada pelo Banco Central.'),
        ])),
        ('cards', dict(titulo='Seu dinheiro está seguro com o Asaas', cols=3, itens=[
            ('bank', 'Banco Central do Brasil', 'Somos uma instituição de pagamento e SCFI autorizada pelo Banco Central do Brasil.'),
            ('hash', 'Código 461', 'Nosso código bancário é o 461. Assim, você tem seus dados de agência e conta sem complicação.', 'ok'),
            ('lock', 'PCI-DSS', 'Seguimos o padrão PCI-DSS, garantindo mais segurança nas suas transações.', 'warn'),
        ])),
        ('midia', dict(panel=True, titulo='Asaas na mídia', itens=[
            'Fintech Asaas levanta R$ 820 milhões com BOND, Softbank e 23S', '15 anos de Asaas: a jornada da plataforma que está transformando a gestão das PMEs brasileiras',
            'Jovem Pan News entrevista fundador do Asaas', 'Fintech Asaas transforma licença de SCD em financeira',
            'Asaas, investida de BOND e SoftBank, acelera estratégia de M&A e entra no mercado de seguros', '4 estratégias que sustentaram o crescimento da Asaas até a rodada de R$ 820 milhões',
            'Vivo Ventures investe R$ 35 milhões em plataforma financeira para PMEs', 'Asaas capta R$ 100 milhões em novo FIDC e mira R$ 1 bilhão de receita em 2026',
        ])),
        ('faixa', dict(ic='users', eyebrow=('Carreiras', 'Tripulantes'), titulo='Quer mudar o mundo com a gente?', texto='Junte-se a centenas de tripulantes espalhados por todo o Brasil e vamos juntos transformar o jeito que as empresas fazem sua gestão financeira.', cta=('Ver vagas', '#'))),
        ('contatos', dict(titulo='Entre em contato com a gente')),
    ])
SOBRE['secoes'][6][1]['cta'] = ('Ver vagas', 'carreiras/')

# ================================================================ geração
geradas = []
for slug, p in P.items():
    geradas.append(pagina(f'solucoes/{slug}', p))
geradas.append(pagina('precos', PRECOS))
geradas.append(pagina('sobre-nos', SOBRE))

# ---------------------------------------------------------------- 2ª via
def segunda_via():
    R = '../'
    corpo = f'''<section class="hero" id="inicio" aria-labelledby="h1" style="padding-bottom:96px">
  <div class="blob a" data-speed="0.2"></div><div class="blob b" data-speed="-0.1"></div>
  <div class="wrap sv-wrap">
    <div class="hero-copy">
      <nav class="crumb" aria-label="Você está em"><a href="{R}">Início</a>{i("chevR",14)}<span aria-current="page">2ª Via</span></nav>
      <span class="sol-tag"><span class="tone">{i("receipt",18)}</span>2ª via de faturas</span>
      <h1 id="h1" style="font:800 clamp(34px,4.4vw,56px)/1.06 var(--font-family);letter-spacing:-.035em">Emitir 2ª via fatura Asaas</h1>
      <p class="lead">Perdeu o boleto ou a fatura venceu? Encontre sua cobrança com o CPF, CNPJ ou telefone e o valor da fatura.</p>
      <ul class="lista" style="opacity:0;animation:fadeUp .9s var(--ease-out) .9s forwards">
        <li><span class="tone ok">{i("search",18)}</span>Informe o documento ou telefone de quem vai pagar</li>
        <li><span class="tone ok">{i("cash",18)}</span>Digite o valor da fatura</li>
        <li><span class="tone ok">{i("pix",18)}</span>Pague por Pix, boleto ou baixe o PDF</li>
      </ul>
    </div>
    <div>
      <form class="sv-form rv" id="segundaVia" novalidate>
      <div class="sim-aviso form" role="note"><b>Simulação:</b> nada é enviado nem salvo. Não digite senha, CPF, CNPJ ou outros dados reais.</div>
        <h2>Emissão 2ª Via</h2>
        <div class="field"><label for="sv-doc">CPF, CNPJ ou Telefone</label><input id="sv-doc" name="doc" inputmode="numeric" placeholder="Informe um CPF, CNPJ ou Telefone" autocomplete="off" /><span class="msg">{i("alert",14)}Informe um CPF, CNPJ ou telefone válido.</span></div>
        <div class="field"><label for="sv-val">Valor da fatura</label><input id="sv-val" name="valor" inputmode="numeric" data-moeda placeholder="Informe o valor da fatura" /><span class="msg">{i("alert",14)}Informe o valor da fatura.</span></div>
        <button class="btn btn-cta" type="submit">{i("search",18)}Emissão 2ª Via</button>
        <div id="svResultado" aria-live="polite" hidden></div>
      </form>
    </div>
  </div>
</section>
<section class="sec" style="padding-top:24px">
  <div class="wrap">
    <div class="grid" style="--cols:3;margin-top:0">
      <article class="card rv"><span class="tone">{i("phone",22)}</span><h3 class="sm">Também pelo aplicativo</h3><p>Com o Asaas Money, além de gerar segunda via de boleto, você acessa fácil as faturas Asaas, parcela em até 12x e ainda libera lembretes de cobranças geradas, para evitar inadimplência.</p></article>
      <article class="card rv" style="--d:80ms"><span class="tone ok">{i("gift",22)}</span><h3 class="sm">5% de cashback</h3><p>No Asaas Money você ganha 5% de cashback no 1º pagamento. Disponível no Google Play e na App Store.</p></article>
      <article class="card rv" style="--d:160ms"><span class="tone warn">{i("shield",22)}</span><h3 class="sm">Pague com segurança</h3><p>Confira sempre o nome de quem está cobrando antes de pagar. Em caso de dúvida, use o <a href="#">Alerta de fraude</a>.</p></article>
    </div>
  </div>
</section>
'''
    out = head('Asaas - Emita a 2ª via de suas faturas', 'Emita a 2ª via de suas faturas Asaas com CPF, CNPJ ou telefone e o valor da fatura.') + \
          f'<body class="sub" data-root="{R}" data-pagina="2via">\n' + topo(R, '2via') + '<main>\n' + corpo + '</main>\n' + rodape(R)
    os.makedirs('segunda-via', exist_ok=True)
    open('segunda-via/index.html', 'w', encoding='utf-8').write(out)
    return 'segunda-via'
geradas.append(segunda_via())

# ---------------------------------------------------------------- criar conta
def criar_conta():
    R = '../'
    passos = ['Acesso', 'Tipo de conta', 'Seus dados', 'Endereço', 'Verificação']
    steps = ''.join(f'<li><span>{k + 1}</span><b>{E(t)}</b></li>' for k, t in enumerate(passos))
    nav = lambda volta=True, prox='Continuar': f'<div class="cc-nav">' + (f'<button type="button" class="btn btn-ghost" data-volta>{i("arrowL",18)}Voltar</button>' if volta else '') + f'<button type="button" class="btn btn-cta" data-prox>{E(prox)} {i("arrowR",18)}</button></div>'
    msg = lambda: f'<span class="msg">{i("alert",14)}<em style="font-style:normal"></em></span>'
    def campo(nome, rot, tipo='text', ph='', extra='', ac=''):
        return f'<div class="field"><label for="cc-{nome}">{E(rot)}</label><input id="cc-{nome}" name="{nome}" type="{tipo}" placeholder="{A(ph)}"{" autocomplete=" + chr(34) + ac + chr(34) if ac else ""} {extra} /><span class="msg">{i("alert",14)}</span></div>'
    p0 = f'''<div class="cc-passo" data-passo="0">
      <h2>Cadastre-se em menos de 5 minutos!</h2>
      <p class="lead">Abra sua conta e aproveite a solução mais completa e segura em emissão de cobranças e serviços financeiros.</p>
      {campo('email','Email','email','Informe seu e-mail','','email')}
      {campo('senha','Senha','password','Informe sua senha','minlength="8"','new-password')}
      {campo('senha2','Confirmar senha','password','Informe a senha novamente','','new-password')}
      <div class="field"><label class="chk"><input type="checkbox" name="termos" /> <span>Li e aceito os <a href="#">Termos e Condições de Uso</a> e o <a href="#">Regulamento de Promoções</a> do Asaas.</span></label><span class="msg">{i("alert",14)}</span></div>
      {nav(False, 'Criar conta')}
    </div>'''
    p1 = f'''<div class="cc-passo" data-passo="1" hidden>
      <h2>Como você vai usar o Asaas?</h2>
      <div class="field"><span class="lbl">Trabalho como</span><div class="radios"><label class="rad"><input type="radio" name="tipo" value="pj" checked /> Pessoa jurídica</label><label class="rad"><input type="radio" name="tipo" value="pf" /> Pessoa física</label></div></div>
      <div data-so="pj">{campo('cnpj','CNPJ','text','00.000.000/0000-00','inputmode="numeric" data-mask="cnpj"')}<p class="links-inline" style="margin-top:8px"><a href="#" data-tipo="pf">Ainda não tenho CNPJ</a></p></div>
      <div data-so="pf" hidden><div class="row2">{campo('cpf','CPF','text','000.000.000-00','inputmode="numeric" data-mask="cpf"')}{campo('nasc','Data de nascimento','text','00/00/0000','inputmode="numeric" data-mask="data"','bday')}</div><p class="links-inline" style="margin-top:8px"><a href="#" data-tipo="pj">Quero cadastrar com meu CNPJ</a></p></div>
      {nav()}
    </div>'''
    p2 = f'''<div class="cc-passo" data-passo="2" hidden>
      <h2>Seus dados</h2>
      {campo('nome','Nome completo (Igual ao documento)','text','Informe seu nome completo','','name')}
      <div data-so="pj">{campo('razao','Razão social da sua empresa','text','Informe o nome da sua empresa','','organization')}</div>
      <div data-so="pj"><div class="field"><label for="cc-empresa">Tipo de empresa</label><select id="cc-empresa" name="empresa"><option value="">Selecione o tipo da sua empresa</option><option>Firma Individual</option><option>Micro empreendedor individual</option><option>Empresa Limitada</option><option>Associação</option></select><span class="msg">{i("alert",14)}</span></div></div>
      {campo('celular','Celular','tel','(00) 00000-0000','inputmode="numeric" data-mask="cel"','tel-national')}
      {nav()}
    </div>'''
    p3 = f'''<div class="cc-passo" data-passo="3" hidden>
      <h2>Endereço</h2>
      <div class="row2">{campo('cep','CEP','text','00000-000','inputmode="numeric" data-mask="cep"','postal-code')}<div class="field" style="justify-content:flex-end"><p class="links-inline" style="min-height:52px;align-items:center"><a href="#" data-semcep>Não sei meu CEP</a></p></div></div>
      <div class="row3">{campo('cidade','Cidade','text','Cidade','','address-level2')}{campo('uf','UF','text','UF','maxlength="2"','address-level1')}{campo('numero','Número','text','00000','inputmode="numeric"')}</div>
      {campo('rua','Rua','text','Rua','','address-line1')}
      <div class="row2">{campo('bairro','Bairro','text','Bairro')}{campo('compl','Complemento (Opcional)','text','Ex: Apartamento 00','','address-line2')}</div>
      {nav(True, 'Enviar código')}
    </div>'''
    otp = ''.join(f'<input type="text" inputmode="numeric" maxlength="1" aria-label="Dígito {k + 1}" autocomplete="{"one-time-code" if k == 0 else "off"}" />' for k in range(6))
    p4 = f'''<div class="cc-passo" data-passo="4" hidden>
      <h2>Código de verificação</h2>
      <p class="lead">Enviamos um código de 6 dígitos para <b id="ccCel"></b>.</p>
      <div class="field"><span class="lbl">Código de verificação</span><div class="otp">{otp}</div><span class="msg">{i("alert",14)}Digite os 6 dígitos do código.</span></div>
      <p class="links-inline">Não recebeu o código? <a href="#" data-reenviar="Enviar código por SMS">Enviar código por SMS</a> <a href="#" data-reenviar="Enviar código por WhatsApp">Enviar código por WhatsApp</a></p>
      <p class="links-inline">Número incorreto? <a href="#" data-altera>Altere o número informado</a></p>
      {nav(True, 'Confirmar')}
    </div>'''
    p5 = f'''<div class="cc-passo ok-final" data-passo="5" hidden>
      <span class="tone ok">{i("check",34)}</span>
      <h2>Conta criada!</h2>
      <p class="lead">Agora é só acessar o Asaas e emitir sua primeira cobrança. A análise do cadastro leva até 2 dias úteis, mas você já pode emitir sua primeira cobrança antes mesmo desse período.</p>
      <a class="btn btn-cta" href="{R}painel/">Acessar minha conta {i("arrowR",18)}</a>
    </div>'''
    corpo = f'''<div class="cc-page">
  <aside class="cc-side" aria-label="Etapas do cadastro">
    <a href="{R}" class="logo" aria-label="Asaas, ir para o início">{logo(104,18,'#fff')}</a>
    <div style="display:flex;flex-direction:column;gap:10px"><h1>Abra sua conta Asaas</h1><p>Conta digital PJ completa e sem mensalidade. Cobre por Pix, boleto e cartão e gerencie tudo em um só lugar.</p></div>
    <ol class="cc-steps">{steps}</ol>
    <div class="mini-foto"><img src="/img/campanha-celular-cartao.webp" alt="" /><div class="float"><span class="tone ok">{i("shield",18)}</span><div><b>Banco 461</b><small>Autorizado pelo Banco Central</small></div></div></div>
  </aside>
  <main class="cc-main">
    <div class="cc-top"><a href="{R}" class="logo-m" aria-label="Asaas">{logo(96,16,'currentColor')}</a><span class="hide-m">Já tem conta?</span><a class="btn btn-ghost btn-sm" href="{R}painel/">Acessar minha conta</a><button class="icon-btn" type="button" id="themeBtn" aria-label="Usar tema escuro"></button></div>
    <div class="cc-body" id="criarConta">
      <form class="cc-card" novalidate onsubmit="return false">
        <div class="cc-barra" aria-hidden="true"><i></i></div>
        <p class="demo-note">{i("alert",16)}<span>Demonstração do conceito: nada é enviado nem salvo. Não use dados reais.</span></p>
        {p0}{p1}{p2}{p3}{p4}{p5}
      </form>
    </div>
  </main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite">{i("check",18)}<span></span></div>
<script type="module" src="/estilos/site.js"></script>
</body>
</html>
'''
    out = head('Asaas - Criar conta', 'Cadastre-se em menos de 5 minutos e abra sua conta digital Asaas.') + f'<body class="sub cc" data-root="{R}" data-pagina="criar-conta">\n' + '<div class="sim-aviso" role="note"><b>Conceito de design · simulação.</b> Não é o site do Asaas, sem relação oficial. Dados fictícios: não digite dados reais.</div>\n' + corpo
    os.makedirs('criar-conta', exist_ok=True)
    open('criar-conta/index.html', 'w', encoding='utf-8').write(out)
    return 'criar-conta'
geradas.append(criar_conta())

# ================================================================ BLOG (conteúdo de blog.asaas.com)
def blog():
    R = '../'
    cats = [('Recursos do Asaas','spark'),('Serviços Bancários','bank'),('Crédito Empresarial','trend'),('Finanças Empresariais','wallet'),('Meios de pagamento','cash'),('Rotinas fiscais','file'),('Gestão de Negócios','grid'),('Automação financeira','code')]
    icat = dict(cats)
    destaques = [('Recursos do Asaas','7 motivos para escolher o Asaas e alavancar seu negócio','Diego Contezini','29 de setembro de 2025','empreendedora-atelie'),
                 ('Recursos do Asaas','Quais são as taxas Asaas? Transparência total para o seu negócio','Diego Contezini','26 de setembro de 2025','campanha-celular-cartao'),
                 ('Recursos do Asaas','Quais são os tipos de contato Asaas? Conheça nosso atendimento humanizado','Diego Contezini','1 de setembro de 2025','freelancer-celular')]
    posts = [('Rotinas fiscais','Nova NFSe: Entenda emissão de nota fiscal pelo Portal Nacional','João Vitor Possamai','23 de outubro de 2026'),
             ('Meios de pagamento','O que é link de pagamento e como funciona na prática?','Eduardo Kruger','19 de outubro de 2026'),
             ('Automação financeira','Aprenda a escolher o gateway de pagamentos certo para seu negócio','Fernando Chagas','16 de outubro de 2026'),
             ('Meios de pagamento','O que é Pix Recorrente Agendado e como utilizá-lo na empresa?','Eduardo Kruger','16 de outubro de 2026'),
             ('Meios de pagamento','Como usar o Pix Agendado para otimizar sua rotina financeira?','Eduardo Kruger','15 de outubro de 2026'),
             ('Automação financeira','Como funciona e como escolher o sistema antifraude do seu negócio','Aline Steinwascher','14 de outubro de 2026'),
             ('Meios de pagamento','Como usar Pix no e-commerce para vender mais e receber rápido?','Eduardo Kruger','14 de outubro de 2026'),
             ('Meios de pagamento','Quais as formas de pagamento mais utilizadas e como escolher as melhores?','Jeferson Leandro Kortbein','14 de outubro de 2026'),
             ('Gestão de Negócios','Como melhorar sua taxa de conversão e diminuir o CAC?','Junior Beltrão','14 de outubro de 2026'),
             ('Meios de pagamento','Como gerar QR code Pix gratuito? Veja como usar','Eduardo Kruger','14 de outubro de 2026'),
             ('Meios de pagamento','Saiba tudo sobre como emitir boleto com QR code Pix gratuito','Eduardo Kruger','14 de outubro de 2026'),
             ('Crédito Empresarial','Como encontrar investidores ideais e adquirir capital com estratégia','Junior Beltrão','14 de outubro de 2026')]
    def card(c, t, a, d, foto=None, grande=False, k=0):
        capa = f'<img src="/img/{foto}.webp" alt="" loading="lazy" />' if foto else f'<span class="big-ic">{i(icat.get(c,"news"),32)}</span>'
        return f'<a class="post rv{" grande" if grande else ""}" href="#" data-cat="{A(c)}" data-titulo="{A(t.lower())}" style="--d:{(k % 3) * 70}ms"><div class="capa c{k % 4}">{capa}</div><div class="corpo"><span class="cat">{E(c)}</span><h3>{E(t)}</h3><span class="meta">por {E(a)} · {E(d)}</span></div></a>'
    filtros = '<button type="button" aria-pressed="true" data-filtro="">Todos</button>' + ''.join(f'<button type="button" aria-pressed="false" data-filtro="{A(c)}">{E(c)}</button>' for c, _ in cats)
    d0 = destaques[0]
    corpo = f"""<section class="hero" id="inicio" aria-labelledby="h1" style="padding-bottom:56px">
  <div class="blob a" data-speed="0.2"></div><div class="blob b" data-speed="-0.1"></div>
  <div class="wrap" style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:20px">
    <nav class="crumb" aria-label="Você está em"><a href="{R}">Início</a>{i("chevR",14)}<a href="{R}sobre-nos/">Sobre nós</a>{i("chevR",14)}<span aria-current="page">Blog</span></nav>
    <span class="sol-tag"><span class="tone">{i("news",18)}</span>Blog Asaas</span>
    <h1 id="h1" style="max-width:820px">Inteligência financeira e operacional para negócios</h1>
    <p class="lead" style="max-width:640px">Conteúdos exclusivos sobre gestão financeira, negócios, conta digital, cobrança, pagamento e muito mais.</p>
    <div style="width:100%;max-width:560px;text-align:left">
      <h2 class="sr">Asaas News: assine nossa newsletter e receba conteúdos exclusivos</h2>
      <form class="signup" novalidate data-news style="max-width:none">
        <div class="signup-row"><label><span class="sr">Seu e-mail</span><input type="email" name="email" placeholder="Seu e-mail para receber a Asaas News" autocomplete="email" /></label><button class="btn btn-cta" type="submit">Assinar</button></div>
        <p class="err" role="alert">{i("alert",16)}<span>Informe um e-mail válido para continuar.</span></p>
        <p class="note">Ao assinar a newsletter, declaro que conheço a <a href="#">Política de Privacidade</a> e autorizo a utilização das minhas informações pelo Asaas para o envio de novidades, ofertas e conteúdos personalizados, de acordo com os meus interesses.</p>
      </form>
    </div>
  </div>
</section>
<section class="sec" style="padding-top:24px">
  <div class="wrap">
    <div class="sec-head rv"><span class="eyebrow" style="align-self:flex-start"><b>Destaques</b> Recursos do Asaas</span><h2 class="h2">Comece por aqui</h2></div>
    <div class="destaques">
      {card(*d0[:4], foto=d0[4], grande=True)}
      <div class="lado">{card(*destaques[1][:4], foto=destaques[1][4], k=1)}</div>
    </div>
    <div class="destaques" style="grid-template-columns:1fr 1.4fr;margin-top:16px">{card(*destaques[2][:4], foto=destaques[2][4], k=2)}<div class="faixa rv" style="grid-template-columns:auto 1fr"><span class="tone">{i("download",28)}</span><div><span class="eyebrow"><b>Grátis</b> Materiais</span><h3>Baixe nossos materiais gratuitos</h3><p>Conteúdos exclusivos para ajudar sua empresa a crescer.</p></div></div></div>
  </div>
</section>
<section class="panel sec" aria-labelledby="h-mat">
  <div class="wrap">
    <div class="sec-head center rv"><span class="eyebrow"><b>Materiais</b> Planilhas e e-books</span><h2 class="h2" id="h-mat">Ferramentas prontas para usar</h2></div>
    <div class="materiais">
      <a class="rv" href="#"><span class="tone ok">{i("grid",18)}</span>Planilha de controle financeiro MEI</a>
      <a class="rv" href="#"><span class="tone ok">{i("box",18)}</span>Planilha de controle de estoque</a>
      <a class="rv" href="#"><span class="tone ok">{i("calc",18)}</span>Planilha modelo de orçamento</a>
      <a class="rv" href="#"><span class="tone ok">{i("trend",18)}</span>Planilha de fluxo de caixa</a>
      <a class="rv" href="#"><span class="tone">{i("file",18)}</span>E-book como regularizar a empresa</a>
      <a class="rv" href="#"><span class="tone">{i("cash",18)}</span>E-book aporte financeiro</a>
      <a class="rv" href="#"><span class="tone">{i("users",18)}</span>E-book de CEO para CEO</a>
      <a class="rv" href="#"><span class="tone">{i("arrowR",18)}</span>Ver todos os materiais</a>
    </div>
    <div class="checks-row rv" style="opacity:1;animation:none;justify-content:center;margin-top:24px"><span>{i("list",16)}Glossário</span><span>{i("award",16)}Cases</span><span>{i("news",16)}Notícias</span></div>
  </div>
</section>
<section class="sec" aria-labelledby="h-posts" id="artigos">
  <div class="wrap">
    <div class="sec-head center rv"><span class="eyebrow"><b>Artigos</b> Mais recentes</span><h2 class="h2" id="h-posts">Categorias</h2></div>
    <label class="busca rv"><span class="sr">Buscar artigos</span>{i("search",20)}<input type="search" id="buscaBlog" placeholder="Buscar artigos" /></label>
    <div class="filtros rv" role="group" aria-label="Filtrar por categoria">{filtros}</div>
    <div class="posts" id="posts">{''.join(card(*p, k=k) for k, p in enumerate(posts))}</div>
    <p class="vazio-busca" id="semPosts" hidden>Nenhum artigo encontrado. Tente outra busca ou categoria.</p>
  </div>
</section>
<section class="sec-sm" style="padding:24px 0 96px"><div class="wrap"><div class="faixa rv"><span class="tone">{i("wallet",28)}</span><div><h3>Asaas: conta digital completa para sua empresa</h3><p>Emita cobranças, faça transferências, pague contas e gerencie seu negócio em um único lugar.</p></div><a class="btn btn-white" href="{R}solucoes/conta-digital/">Conhecer o Asaas {i("arrowR",18)}</a></div></div></section>
"""
    out = head('Blog de Finanças, Tecnologia e Negócios | Blog Asaas', 'Conteúdos exclusivos sobre gestão financeira, negócios, conta digital, cobrança, pagamento e muito mais no blog de finanças do Asaas.') + \
          f'<body class="sub" data-root="{R}" data-pagina="blog">\n' + topo(R, 'blog') + '<main>\n' + corpo + '</main>\n' + rodape(R)
    os.makedirs('blog', exist_ok=True)
    open('blog/index.html', 'w', encoding='utf-8').write(out)
    return 'blog'

# ================================================================ CARREIRAS (conteúdo de carreiras.asaas.com)
def carreiras():
    R = '../'
    vagas = [('AI Product Manager - IAN','Remoto','Efetivo'),('Analista de Compensation Sênior (Foco em ILP e Design Organizacional)','Remoto','Efetivo'),
             ('Analista de Estratégia de Prevenção a Fraudes Sênior (Dados)','Remoto','Efetivo'),('Analista de Estratégia de Prevenção a Fraudes Sênior - Foco Cartão (Emissor)','Remoto','Efetivo'),
             ('Analista de Estratégia de Prevenção a Fraudes Sênior (Foco KYC/Onboarding)','Remoto','Efetivo'),('Analista de Estratégia de Prevenção a Fraudes Sênior - Transacional','Remoto','Efetivo'),
             ('Analista de IAM Senior','Híbrido · Joinville - SC','Efetivo'),('Analista de Operações Pleno','Remoto','Efetivo'),('Analista de Tesouraria Sênior - Backoffice Renda Fixa','Remoto','Efetivo'),
             ('Analista de Viagens Corporativas Júnior','Remoto','Efetivo'),('Analista Sênior de Tesouraria - Foco em Carteira Institucional e Gestão de Capital','Remoto','Efetivo'),
             ('Banco de Talentos - Pessoas com Deficiência','Remoto','Banco de talentos'),('Cientista de Dados Especialista (Modelagem de Crédito)','Remoto','Efetivo'),
             ('Cientista de Dados Especialista (Políticas de Crédito)','Remoto','Efetivo'),('Cientista de Dados Sênior (Políticas de Crédito)','Remoto','Efetivo'),
             ('Cloud Security Engineer Team Lead','Remoto','Efetivo'),('Engenheiro(a) de Software Full Stack Pleno [Seleção Contínua]','Remoto','Efetivo'),
             ('Engenheiro(a) de Software Full Stack Sênior [Seleção Contínua]','Remoto','Efetivo'),('Especialista Contábil','Remoto','Efetivo'),
             ('Product Designer Sênior - Marketplace (Flapp Store)','Remoto','Efetivo'),('Sênior Tax Compliance Analyst','Remoto','Efetivo'),
             ('Tech Lead de Analytics Engineer','Remoto','Efetivo'),('Tech Leader de Engenharia','Remoto','Efetivo')]
    lista = ''.join(f'<a class="vaga rv" href="#" data-titulo="{A(t.lower())}" data-modelo="{"hibrido" if "Híbrido" in m else "remoto"}"><span class="tone">{i("star" if "Talentos" in t else "users",20)}</span><span><b>{E(t)}</b><small>{E(tp)}</small></span><span class="tags"><span class="{"rem" if m == "Remoto" else ""}">{E(m)}</span></span></a>' for t, m, tp in vagas)
    beneficios = [('heart','Para saúde e bem-estar','Assistência médica e odontológica sem coparticipação, seguro de vida, auxílio para compra de medicamentos e para realizar atividades físicas. A Neon é nossa parceira para cuidar da saúde financeira do time e a Zenklub para a saúde física e mental (4 sessões mensais de terapia ou nutricionista gratuitas). Na sede, também temos quick massage.','ok'),
                  ('gift','Para alimentação e família','Benefício alimentação flexível, por meio de um cartão de crédito, bandeira Visa: o saldo pode ser usado como cada um desejar. Na sede, temos free food e, para as famílias, auxílio creche, programa de apoio parental e licença maternidade e paternidade estendida.',''),
                  ('award','Para educação e crescimento','Ambiente de desafios e muito desenvolvimento, plataforma de treinamentos in company e auxílio educação que subsidia 70% de mensalidades de graduações e idiomas, bem como a compra de cursos e livros.',''),
                  ('home','Para o trabalho remoto de qualidade','Auxílio Home Office, equipamentos de trabalho, auxílio mobília e parceria com a WOBA, para os nossos colaboradores usarem coworkings em todo o Brasil quando desejarem.',''),
                  ('spark','Extras, porque o Dream Team merece','Day Off no mês do aniversário, auxílio Happy Hour, bonificação por indicação de novos colaboradores, bonificação baseada em metas anuais, plano de Stock Options e um ambiente leve, no dress code!','warn')]
    valores = [('users','Interesse Genuíno Pelo Cliente','Nosso interesse pelo cliente é genuíno. Do cliente externo ao interno, parceiros e em todas as nossas relações, incentivamos o interesse genuíno pelas pessoas.'),
               ('target','Comprometimento','Fazemos tudo aquilo que está ao nosso alcance. Conciliamos a liberdade com a responsabilidade e temos autonomia.'),
               ('eye','Transparência','Assumimos nossos erros e temos integridade. Levantamos os aprendizados e buscamos oportunidades de melhoria.'),
               ('award','Qualidade','Temos paixão por excelência e inspiramos outras pessoas. Negociamos prazos, mas não negociamos qualidade.'),
               ('heart','Respeito','Nos comunicamos de forma precisa e com respeito pelos outros. Prezamos por um ambiente de respeito e empatia, no qual podemos ser nós mesmos.'),
               ('trend','Crescimento','Dedicamos tempo para aprender coisas novas e aprimorar o que já sabemos. Construímos um espaço no qual podemos ser melhores todos os dias.')]
    depo = [('Sem sombra de dúvidas essa foi a melhor experiência de trabalho de toda minha vida, tive espaço para crescimento, sempre pude opinar, concordar, discordar, dar ideias, receber ideias, ser ouvido e ser ouvinte. Ter essa sensação de pertencimento ao local onde estou trabalhando com certeza é super gratificante e faz a gente se sentir em casa.','Gean Farias','Tech Leader na Engenharia e Embaixador Asaas'),
            ('Eu amo toda a experiência que vivo aqui no Asaas! Esse amor existe por saber que os nossos valores estão na prática e não apenas na parede, que as nossas ideias são ouvidas e muitas vezes colocadas em prática, que existe reconhecimento profissional e oportunidade de desenvolvimento.','Débora Cardoso','Especialista em Gestão de Performance'),
            ('O que mais gosto na minha jornada no Asaas é o aprendizado contínuo que me ajuda a evoluir cada dia mais. Me sinto instigada a sempre fazer o melhor trabalho possível e vejo muito reconhecimento e valorização em todas as entregas.','Millena Dias','Tech Leader de Engenharia'),
            ('Trabalhar no Asaas é extraordinário! O cuidado com o colaborador é visível em todos os momentos da nossa jornada aqui dentro. A cultura da empresa é vista nos mínimos detalhes. Aqui temos autonomia para criarmos novas experiências e mudarmos a vida do empreendedor.','Caroline Godoi','Líder de Design de Produto e Embaixadora Asaas')]
    p = dict(nome='Carreiras', ic='star', ic2='users', ic3='heart', foto='dev-api', ativo='carreiras', slug='carreiras', ref=None,
        titulo='Carreiras no Asaas · Embarque no Asaas', desc='Vagas, benefícios e cultura do Asaas.',
        h1='Nós queremos mudar o mundo e começamos por aqui! Você vem com a gente?',
        lead='Somos uma Fintech, Instituição de Pagamento credenciada pelo Banco Central do Brasil e temos como propósito maximizar a produtividade das empresas através da tecnologia.',
        ctas=[('Ver vagas', '#vagas', 'btn-cta'), ('Banco de talentos', '#vagas', 'btn-ghost')],
        chips=['Remote first', 'Mais de 1.000 pessoas', 'Desde 2010 em Joinville/SC'],
        floats=[('users', 'ok', '23 vagas abertas', 'A maioria remota'), ('heart', '', 'Benefícios', 'Saúde, educação e família')],
        seguranca=False, app=False,
        secoes=[
            ('texto', dict(titulo='Embarque no Asaas', eyebrow=('Quem somos', 'Tripulantes'), foto='gestora-notas', alt='Profissional trabalhando com tablet',
                paragrafos=['Oferecemos uma solução completa para gestão de cobranças, pagamentos, antecipações de recebíveis e atendemos mais de 200 mil clientes divididos entre profissionais autônomos, microempreendedores individuais (MEI) e grandes empresas.',
                            'Nosso sonho começou em 2010, em Joinville/SC e acreditamos que o céu não é o limite para o nosso crescimento. Não é à toa que atualmente nosso time está em vários cantos do Brasil! Mais de 1.000 pessoas sonham junto com o Asaas, de forma colaborativa, inovadora, eficiente, com autonomia e liberdade para voar alto.'])),
            ('stats', dict(panel=True, titulo='Voos altos', lead='Voos altos exigem recursos para viver e trabalhar melhor, além de liberdade para administrá-los.', itens=[(1000, 0, '+', '', 'pessoas sonhando junto com o Asaas'), (200, 0, '+', ' mil', 'clientes atendidos'), (70, 0, '', '%', 'de subsídio do auxílio educação')])),
            ('cards', dict(titulo='Acolhemos e cuidamos do nosso time', lead='Benefícios que apoiam seu crescimento pessoal e profissional:', cols=3, itens=beneficios)),
        ])
    corpo = hero(R, p)
    for tipo, d in p['secoes']:
        corpo += BLOCOS[tipo](R, d)
    corpo += f"""<section class="panel sec alvo" id="vagas" aria-labelledby="h-vagas">
  <div class="wrap">
    <div class="sec-head rv"><span class="eyebrow" style="align-self:flex-start"><b>Vagas</b> Nossas oportunidades</span><h2 class="h2" id="h-vagas">Embarque no Asaas</h2></div>
    <div class="vagas-tools rv">
      <label class="busca"><span class="sr">Buscar vagas</span>{i("search",20)}<input type="search" id="buscaVaga" placeholder="Buscar vagas" /></label>
      <div class="filtros" role="group" aria-label="Modelo de trabalho" style="margin:0"><button type="button" aria-pressed="true" data-modelo="">Todas</button><button type="button" aria-pressed="false" data-modelo="remoto">Remoto</button><button type="button" aria-pressed="false" data-modelo="hibrido">Híbrido</button></div>
    </div>
    <p class="vagas-cont" id="contVagas" style="margin-top:16px">{len(vagas)} vagas encontradas</p>
    <div class="vagas" id="vagasLista">{lista}</div>
    <div class="faixa rv" style="margin-top:24px"><span class="tone">{i("star",28)}</span><div><h3>Não encontrou a vaga que procurava?</h3><p>Faça parte do nosso banco de talentos!</p></div><a class="btn btn-white" href="#">Entrar no banco de talentos {i("arrowR",18)}</a></div>
  </div>
</section>
"""
    corpo += b_cards(R, dict(titulo='Valores que norteiam nossos voos', lead='Nosso sonho é grande, assim como nossos desafios. Por isso, trabalhamos de forma colaborativa para tirar ideias do papel; temos autonomia para encontrar e apresentar soluções inovadoras; trocamos feedbacks, ouvimos sugestões e acreditamos nas pessoas.', cols=3, itens=valores))
    corpo += b_quotes(R, dict(panel=True, titulo='Liberdade, autonomia e flexibilidade', lead='São os pilares que sustentam nosso modelo de trabalho híbrido remote first. Nosso time está conectado, seja da home, do office, ou de onde cada um escolher trabalhar. O que dizem nossos tripulantes:', itens=depo))
    corpo += f"""<section class="sec"><div class="wrap" style="display:flex;flex-direction:column;align-items:center;gap:20px;text-align:center">
  <h2 class="h2 rv">Acompanhe o dia a dia a bordo</h2><p class="lead rv">Fique por dentro das novidades.</p>
  <div class="checks-row rv" style="opacity:1;animation:none;justify-content:center"><span>{i("globe",16)}Website</span><span>{i("users",16)}LinkedIn</span><span>{i("spark",16)}Instagram</span><span>{i("star",16)}Glassdoor</span></div>
</div></section>
"""
    out = head(p['titulo'], p['desc']) + f'<body class="sub" data-root="{R}" data-pagina="carreiras">\n' + topo(R, 'carreiras') + '<main>\n' + corpo + '</main>\n' + rodape(R)
    os.makedirs('carreiras', exist_ok=True)
    open('carreiras/index.html', 'w', encoding='utf-8').write(out)
    return 'carreiras'

geradas.append(blog())
geradas.append(carreiras())

print('Páginas geradas:')
for g in geradas:
    print(' -', g + '/index.html')
