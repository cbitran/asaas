/* Asaas · comportamento compartilhado das páginas internas (soluções, preços, sobre nós, 2ª via, criar conta).
   Mesmo design system da landing e do painel: tokens/tokens.css + estilos/site.css. Tudo é demonstração: nada é enviado. */
(function(){
  'use strict';
  var ROOT = document.body.getAttribute('data-root') || './';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function(s,r){return (r||document).querySelector(s);};
  var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};

  /* ---------- ícones (mesmos paths do painel: stroke 1.8, viewBox 24) ---------- */
  var I = {
    home:'M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
    receipt:'M6 2h12v20l-3-2-3 2-3-2-3 2zM9 7h6M9 11h6M9 15h4',
    link:'M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1',
    pos:'M7 2h10a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zM9 5h6v4H9zM9 13h.01M12 13h.01M15 13h.01M9 17h.01M12 17h.01M15 17h.01',
    users:'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8',
    user:'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
    search:'M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3',
    shield:'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM12 8v4M12 16h.01',
    wallet:'M3 7a2 2 0 0 1 2-2h14v4M3 7v11a2 2 0 0 0 2 2h16V9H5a2 2 0 0 1-2-2zM17 14h.01',
    list:'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01',
    pix:'M12 2.5 21.5 12 12 21.5 2.5 12zM8.5 12 12 8.5l3.5 3.5-3.5 3.5z',
    barcode:'M3 5v14M7 5v14M10 5v14M14 5v14M17 5v14M21 5v14',
    card:'M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20M6 15h4',
    clock:'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2',
    file:'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5',
    bank:'M3 21h18M5 21V10M19 21V10M9 21V10M15 21V10M2 10 12 3l10 7z',
    bell:'M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0',
    chevD:'M6 9l6 6 6-6', chevR:'M9 6l6 6-6 6', chevL:'M15 6l-6 6 6 6',
    x:'M18 6 6 18M6 6l12 12', check:'M20 6 9 17l-5-5', plus:'M12 5v14M5 12h14',
    alert:'M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z',
    menu:'M4 6h16M4 12h16M4 18h16',
    sun:'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4',
    moon:'M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z',
    send:'M22 2 11 13M22 2l-7 20-4-9-9-4z', mail:'M3 5h18v14H3zM3 6l9 7 9-7',
    up:'M7 17 17 7M8 7h9v9',
    cash:'M2 6h20v12H2zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 12h.01M18 12h.01',
    code:'M16 18l6-6-6-6M8 6l-6 6 6 6M14 4l-4 16',
    grid:'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',
    spark:'M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z',
    volume:'M11 5 6 9H2v6h4l5 4zM15.5 8.5a5 5 0 0 1 0 7M19 5a9 9 0 0 1 0 14',
    arrowR:'M5 12h14M13 6l6 6-6 6', arrowL:'M19 12H5M11 6l-6 6 6 6',
    chat:'M21 12a8 8 0 0 1-11.8 7L3 21l2-6A8 8 0 1 1 21 12z',
    sms:'M4 4h16v12H8l-4 4zM8 9h8M8 12h5',
    trend:'M3 17l6-6 4 4 8-8M15 7h6v6',
    wifi:'M8.5 16.5a5 5 0 0 1 7 0M5 13a10 10 0 0 1 14 0M12 20h.01',
    hash:'M4 9h16M4 15h16M10 3 8 21M16 3l-2 18',
    lock:'M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4M12 15v2',
    split:'M6 3v6a6 6 0 0 0 6 6h0a6 6 0 0 1 6 6M18 3v6a6 6 0 0 1-6 6M3 6l3-3 3 3M15 6l3-3 3 3',
    hook:'M18 16.1A5 5 0 0 0 15.9 6L15 6a3 3 0 1 0-5.7 1.3L12 12M6 15a5 5 0 1 0 7 4.6V19h6M12 12l-3 5',
    phone:'M7 2h10a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zM11 18h2',
    play:'M6 3l14 9-14 9z',
    calc:'M5 2h14a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zM8 6h8v4H8zM8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01',
    box:'M21 8 12 3 3 8v8l9 5 9-5zM3 8l9 5 9-5M12 13v8',
    cart:'M3 3h2l2.4 12.2a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.6L21 7H6M9 21h.01M18 21h.01',
    heart:'M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z',
    award:'M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM8.2 13.9 7 22l5-3 5 3-1.2-8.1',
    globe:'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20',
    target:'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z',
    eye:'M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
    qr:'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h3v3h-3zM18 18h3v3h-3zM14 20h2M20 14v2',
    calendar:'M3 5h18v16H3zM3 10h18M8 3v4M16 3v4',
    copy:'M9 9h11v11H9zM5 15H4V4h11v1',
    news:'M4 4h13v16H6a2 2 0 0 1-2-2zM17 8h3v10a2 2 0 0 1-2 2M8 8h5M8 12h5M8 16h3',
    download:'M12 3v12M7 10l5 5 5-5M4 21h16',
    gift:'M20 12v10H4V12M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7z',
    star:'M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z'
  };
  function ic(n,s){s=s||20;return '<svg width="'+s+'" height="'+s+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+(I[n]||'')+'"/></svg>';}
  function paint(root){$$('i[data-i]',root).forEach(function(el){if(!el.firstChild)el.innerHTML=ic(el.getAttribute('data-i'),+el.getAttribute('data-s')||20);});}

  /* ---------- menu de soluções ---------- */
  var SOL = [
    ['pix','Pix','Receba em até 10 segundos','pix-asaas'],['barcode','Boleto bancário','Cobranças registradas','boleto-bancario'],['card','Cobrança por cartão','Crédito e débito','cobranca-cartao'],
    ['pos','Asaas Tap','Venda presencial','asaas-tap'],['link','Link de pagamento','Venda de qualquer lugar','link-pagamento'],['file','Nota fiscal','Emissão automática','nota-fiscal'],
    ['wallet','Conta digital','Banco 461, sem mensalidade','conta-digital'],['bell','Régua de Cobrança','Lembretes automáticos','regua-de-cobranca'],['trend','Antecipação de recebíveis','Mais liquidez','antecipacao-de-recebiveis'],
    ['grid','ERP','Sem limite de usuários','erp'],['code','API de pagamentos','REST, webhooks e split','api-de-pagamentos'],['cash','Meios de pagamento','5 em 1','meios-de-pagamento']
  ];
  var atual = document.body.getAttribute('data-pagina') || '';
  var mega = $('#mega');
  if (mega) mega.innerHTML = SOL.map(function(s){return '<a role="menuitem" href="'+ROOT+'solucoes/'+s[3]+'/"'+(s[3]===atual?' aria-current="page"':'')+'><span class="tone">'+ic(s[0],20)+'</span><span>'+s[1]+'<small>'+s[2]+'</small></span></a>';}).join('');
  var shSol = $('#sheetSol');
  if (shSol) shSol.innerHTML = SOL.map(function(s){return '<a href="'+ROOT+'solucoes/'+s[3]+'/">'+ic(s[0],20)+s[1]+'</a>';}).join('');
  var fSol = $('#fSol');
  if (fSol) fSol.innerHTML = SOL.map(function(s){return '<li><a href="'+ROOT+'solucoes/'+s[3]+'/">'+s[1]+'</a></li>';}).join('');
  paint();

  /* ---------- tema (mesma chave da landing) ---------- */
  var themeBtn = $('#themeBtn');
  function setTheme(t){document.documentElement.setAttribute('data-theme',t);if(themeBtn){themeBtn.innerHTML=ic(t==='dark'?'sun':'moon',20);themeBtn.setAttribute('aria-label',t==='dark'?'Usar tema claro':'Usar tema escuro');}try{localStorage.setItem('asaas-site-tema',t);}catch(e){}}
  var saved=null;try{saved=localStorage.getItem('asaas-site-tema');}catch(e){}
  setTheme(saved==='dark'?'dark':'light');
  if (themeBtn) themeBtn.addEventListener('click',function(){setTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');});

  /* ---------- sem áudio fora do painel ---------- */
  (function(){var bc=null;try{bc=new BroadcastChannel('asaas-voz');}catch(e){}
    function calar(){if(document.hidden)return;try{bc&&bc.postMessage('calar');}catch(e){}}
    calar();document.addEventListener('visibilitychange',calar);window.addEventListener('focus',calar);})();

  /* ---------- toast ---------- */
  var toastT;
  function toast(msg){var t=$('#toast');if(!t)return;$('span',t).textContent=msg;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('show');},3200);}

  /* ---------- cadastro rápido (e-mail) → página Criar conta ---------- */
  $$('[data-form]').forEach(function(f){
    var inp=$('input',f),row=$('.signup-row',f),err=$('.err',f);
    function bad(on){row.setAttribute('aria-invalid',on?'true':'false');inp.setAttribute('aria-invalid',on?'true':'false');err.classList.toggle('show',on);}
    inp.addEventListener('input',function(){bad(false);});
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(inp.value.trim())){bad(true);inp.focus();return;}
      try{sessionStorage.setItem('asaas-cadastro-email',inp.value.trim());}catch(e){}
      location.href=ROOT+'criar-conta/';
    });
  });

  /* ---------- menu Soluções e bottom sheet ---------- */
  var solBtn=$('#solBtn');
  function setMega(o){if(!mega)return;mega.classList.toggle('open',o);solBtn.setAttribute('aria-expanded',o);}
  if (solBtn) solBtn.addEventListener('click',function(e){e.stopPropagation();setMega(!mega.classList.contains('open'));});
  document.addEventListener('click',function(e){if(mega&&!mega.contains(e.target))setMega(false);});
  var sheet=$('#sheet'),ov=$('#overlay'),burger=$('#burger');
  function openSheet(){sheet.classList.add('show');ov.classList.add('show');burger.setAttribute('aria-expanded','true');$('#sheetClose').focus();}
  function closeSheet(){if(!sheet||!sheet.classList.contains('show'))return;sheet.classList.remove('show');ov.classList.remove('show');burger.setAttribute('aria-expanded','false');burger.focus();}
  if (burger){burger.addEventListener('click',openSheet);ov.addEventListener('click',closeSheet);$('#sheetClose').addEventListener('click',closeSheet);}
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){if(mega&&mega.classList.contains('open')){setMega(false);solBtn.focus();}closeSheet();}});


  /* ---------- dropdowns do topo (Sobre nós) ---------- */
  $$('[data-drop]').forEach(function(b){
    var m=document.getElementById(b.getAttribute('aria-controls'));
    function set(o){m.classList.toggle('open',o);b.setAttribute('aria-expanded',o);}
    b.addEventListener('click',function(e){e.stopPropagation();setMega&&setMega(false);set(!m.classList.contains('open'));});
    document.addEventListener('click',function(e){if(!m.contains(e.target))set(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.classList.contains('open')){set(false);b.focus();}});
  });
  if(solBtn)solBtn.addEventListener('click',function(){$$('.dd-menu.open').forEach(function(m){m.classList.remove('open');});});

  /* ---------- newsletter do blog ---------- */
  $$('[data-news]').forEach(function(f){var inp=$('input',f),err=$('.err',f),row=$('.signup-row',f);
    f.addEventListener('submit',function(e){e.preventDefault();var ok=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(inp.value.trim());err.classList.toggle('show',!ok);row.setAttribute('aria-invalid',!ok);
      if(ok){f.reset();toast('Pronto! Você vai receber a Asaas News.');}});
    inp.addEventListener('input',function(){err.classList.remove('show');row.setAttribute('aria-invalid','false');});});

  /* ---------- blog: busca + categorias ---------- */
  var postsBox=$('#posts');
  if(postsBox){var cat='',q='',bus=$('#buscaBlog');
    function filtra(){var n=0;$$('.post',postsBox).forEach(function(p){var ok=(!cat||p.getAttribute('data-cat')===cat)&&(!q||p.getAttribute('data-titulo').indexOf(q)>-1);p.hidden=!ok;if(ok){n++;p.classList.add('in');}});$('#semPosts').hidden=n>0;}
    $$('[data-filtro]').forEach(function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-filtro');$$('[data-filtro]').forEach(function(x){x.setAttribute('aria-pressed',x===b);});filtra();});});
    bus.addEventListener('input',function(){q=bus.value.trim().toLowerCase();filtra();});}

  /* ---------- carreiras: busca + modelo ---------- */
  var vagasBox=$('#vagasLista');
  if(vagasBox){var mod='',qv='',bv=$('#buscaVaga');
    function filtraV(){var n=0;$$('.vaga',vagasBox).forEach(function(v){var ok=(!mod||v.getAttribute('data-modelo')===mod)&&(!qv||v.getAttribute('data-titulo').indexOf(qv)>-1);v.hidden=!ok;if(ok){n++;v.classList.add('in');}});$('#contVagas').textContent=n+(n===1?' vaga encontrada':' vagas encontradas');}
    $$('[data-modelo]').forEach(function(b){if(b.tagName!=='BUTTON')return;b.addEventListener('click',function(){mod=b.getAttribute('data-modelo');$$('button[data-modelo]').forEach(function(x){x.setAttribute('aria-pressed',x===b);});filtraV();});});
    bv.addEventListener('input',function(){qv=bv.value.trim().toLowerCase();filtraV();});
    $$('.vaga',vagasBox).forEach(function(v){v.addEventListener('click',function(e){e.preventDefault();toast('Vaga de exemplo: as inscrições acontecem no portal de carreiras');});});}

  /* ---------- revelação + contadores ---------- */
  function fmtN(v,dec){return v.toLocaleString('pt-BR',{minimumFractionDigits:dec,maximumFractionDigits:dec});}
  function countUp(el){
    var to=parseFloat(el.getAttribute('data-count')),dec=+el.getAttribute('data-dec')||0,t0=null;
    if(reduce){el.textContent=fmtN(to,dec);return;}
    function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1600);el.textContent=fmtN(to*(1-Math.pow(1-p,4)),dec);if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  }
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;en.target.classList.add('in');$$('[data-count]',en.target).forEach(function(c){if(!c._done){c._done=1;countUp(c);}});io.unobserve(en.target);});},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  $$('.rv, .stat, .card').forEach(function(el){io.observe(el);});
  $$('.card').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');});});

  /* ---------- abas (segmented control do painel) ---------- */
  function movePill(seg){var on=$('[aria-selected=true]',seg),p=$('.pill',seg);if(!on||!p)return;p.style.width=on.offsetWidth+'px';p.style.transform='translateX('+(on.offsetLeft-5)+'px)';}
  $$('[data-tabs]').forEach(function(w){
    var seg=$('.seg',w),btns=$$('[role=tab]',seg),panels=$$('[role=tabpanel]',w);
    function sel(i){btns.forEach(function(b,k){b.setAttribute('aria-selected',k===i);b.tabIndex=k===i?0:-1;});panels.forEach(function(p,k){p.classList.toggle('on',k===i);p.hidden=k!==i;});movePill(seg);}
    btns.forEach(function(b,i){b.addEventListener('click',function(){sel(i);});b.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){var n=(i+(e.key==='ArrowRight'?1:-1)+btns.length)%btns.length;sel(n);btns[n].focus();}});});
    sel(0);w._move=function(){movePill(seg);};
  });
  function relayout(){$$('[data-tabs]').forEach(function(w){w._move&&w._move();});}
  window.addEventListener('resize',relayout);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(relayout);
  setTimeout(relayout,300);

  /* ---------- FAQ: uma dúvida aberta por vez ---------- */
  $$('.acc .qa button').forEach(function(b){b.addEventListener('click',function(){
    var qa=b.closest('.qa'),acc=b.closest('.acc'),open=!qa.classList.contains('open');
    $$('.qa.open',acc).forEach(function(o){if(o!==qa){o.classList.remove('open');$('button',o).setAttribute('aria-expanded','false');}});
    qa.classList.toggle('open',open);b.setAttribute('aria-expanded',open);
  });});

  /* ---------- simuladores (ilustrativos, com as taxas padrão publicadas no site) ---------- */
  var brl=function(v){return 'R$ '+fmtN(Math.max(0,v),2);};
  var num=function(s){var v=parseFloat(String(s||'').replace(/\./g,'').replace(/[^\d,]/g,'').replace(',','.'));return isNaN(v)?0:v;};
  $$('[data-moeda]').forEach(function(inp){inp.addEventListener('input',function(){var d=inp.value.replace(/\D/g,'');if(!d){inp.value='';return;}inp.value=fmtN(parseInt(d,10)/100,2);});});
  // cartão: [de, até, taxa padrão, taxa nos 3 primeiros meses] + R$ 0,49 · débito R$ 0,35 + 1,89%
  var FAIXAS=[[1,1,2.99,1.99],[2,6,3.49,2.49],[7,12,3.99,2.99],[13,21,4.29,3.29]];
  $$('[data-sim=cartao]').forEach(function(f){
    var v=$('[name=valor]',f),pa=$('[name=parcelas]',f),pr=$('[name=promo]',f),out=$('.sim-out',f);
    function calc(){
      var val=num(v.value),n=+pa.value,deb=n===0,promo=pr&&pr.checked,tx,fixa;
      if(deb){tx=1.89;fixa=0.35;}else{var fx=FAIXAS.filter(function(x){return n>=x[0]&&n<=x[1];})[0];tx=promo?fx[3]:fx[2];fixa=0.49;}
      var liq=val-(val*tx/100+fixa);
      $('[data-o=cliente]',out).textContent=deb?brl(val)+' no débito':(n===1?brl(val)+' à vista':n+'x de '+brl(val/n));
      $('[data-o=taxa]',out).textContent=(deb?'R$ 0,35 + 1,89%':'R$ 0,49 + '+fmtN(tx,2)+'%');
      $('[data-o=recebe]',out).textContent=brl(liq);
      $('[data-o=prazo]',out).textContent=deb?'Em até 3 dias úteis':(n===1?'32 dias após a confirmação':'1 parcela a cada 32 dias');
      out.classList.remove('pop');void out.offsetWidth;out.classList.add('pop');
    }
    [v,pa,pr].forEach(function(x){if(x){x.addEventListener('input',calc);x.addEventListener('change',calc);}});
    f.addEventListener('submit',function(e){e.preventDefault();calc();});calc();
  });
  // antecipação: boleto R$ 0,99 + 5,79% a.m. · cartão R$ 0,49 + 2,99% + 1,25% a.m. (1 mês antecipado)
  $$('[data-sim=antecipacao]').forEach(function(f){
    var v=$('[name=valor]',f),out=$('.sim-out',f);
    function calc(){
      var val=num(v.value),tipo=($('[name=tipo]:checked',f)||{}).value||'boleto',liq,info;
      if(tipo==='boleto'){liq=val-0.99-val*0.0579;info='Já incluso taxa de R$ 0,99 + taxa de antecipação de 5,79% ao mês';}
      else{liq=val-0.49-val*0.0299-val*0.0125;info='Já incluso taxa de R$ 0,49 + 2,99% + antecipação de 1,25% ao mês';}
      $('[data-o=recebe]',out).textContent=brl(liq);
      $('[data-o=tipo]',out).textContent=tipo==='boleto'?'no boleto bancário à vista':'no cartão de crédito à vista';
      $('[data-o=info]',out).textContent=info;
      $('[data-o=prazo]',out).textContent=tipo==='boleto'?'Receba em até 3 dias úteis':'Receba em até 2 dias úteis';
      out.classList.remove('pop');void out.offsetWidth;out.classList.add('pop');
    }
    $$('input',f).forEach(function(x){x.addEventListener('input',calc);x.addEventListener('change',calc);});
    f.addEventListener('submit',function(e){e.preventDefault();calc();});calc();
  });

  /* ---------- formulário de contato (API) ---------- */
  $$('[data-contato]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();
    var ok=true;$$('[required]',f).forEach(function(x){var g=x.closest('.field');var b=!x.value.trim();g&&g.classList.toggle('bad',b);if(b)ok=false;});
    if(!ok){toast('Preencha os campos obrigatórios');var b=$('.field.bad input,.field.bad select',f);b&&b.focus();return;}
    f.reset();toast('Recebemos seu contato. Um especialista vai falar com você.');});});

  /* ---------- terminal digitando (API) ---------- */
  var pre=$('#code');
  if(pre){
    var CODE=JSON.parse(pre.getAttribute('data-code')||'[]'),typed=false;
    var put=function(p){return p[0]?'<span class="'+p[0]+'">'+p[1]+'</span>':p[1];};
    var go=function(){if(typed)return;typed=true;
      if(reduce){pre.innerHTML=CODE.map(put).join('');$('#hook')&&$('#hook').classList.add('show');return;}
      var pi=0,ci=0,html='';(function tick(){if(pi>=CODE.length){pre.innerHTML=html+'<span class="caret"></span>';setTimeout(function(){$('#hook')&&$('#hook').classList.add('show');},400);return;}
        var p=CODE[pi];ci+=2;pre.innerHTML=html+put([p[0],p[1].slice(0,ci)])+'<span class="caret"></span>';if(ci>=p[1].length){html+=put(p);pi++;ci=0;}setTimeout(tick,20);})();};
    new IntersectionObserver(function(es,o){es.forEach(function(en){if(en.isIntersecting){o.disconnect();go();}});},{threshold:.4}).observe(pre);
  }

  /* ---------- parallax (scroll + mouse) e topo ---------- */
  var top=$('#top'),bar=$('.progress'),stage=$('#stage');
  var depthEls=$$('#stage [data-depth]'),speedEls=$$('[data-speed]');
  var mx=0,my=0,tx=0,ty=0;
  if(stage&&!reduce&&window.matchMedia('(pointer:fine)').matches){
    var hero=stage.closest('section');
    hero.addEventListener('pointermove',function(e){var r=stage.getBoundingClientRect();tx=(e.clientX-(r.left+r.width/2))/r.width;ty=(e.clientY-(r.top+r.height/2))/r.height;});
    hero.addEventListener('pointerleave',function(){tx=0;ty=0;});
  }
  function frame(){
    var y=window.scrollY,vh=window.innerHeight,h=document.documentElement.scrollHeight-vh;
    if(top)top.classList.toggle('scrolled',y>8);
    if(bar)bar.style.transform='scaleX('+(h>0?y/h:0)+')';
    if(!reduce){
      mx+=(tx-mx)*.08;my+=(ty-my)*.08;
      speedEls.forEach(function(el){
        var sp=parseFloat(el.getAttribute('data-speed'));
        if(window.innerWidth<760&&el.closest('.stage'))sp=0;
        var sy;
        if(el.closest('.hero'))sy=y*sp;else{var r=el.parentElement.getBoundingClientRect();sy=(r.top+r.height/2-vh/2)*sp;}
        var d=parseFloat(el.getAttribute('data-depth')||0);
        el.style.transform='translate3d('+(mx*d)+'px,'+(my*d+sy)+'px,0)';
      });
      depthEls.forEach(function(el){if(el.hasAttribute('data-speed'))return;var d=parseFloat(el.getAttribute('data-depth'));el.style.translate=(mx*d)+'px '+(my*d)+'px';});
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  /* ================= 2ª via (demonstração) ================= */
  var sv=$('#segundaVia');
  if(sv){
    var doc=$('[name=doc]',sv),val=$('[name=valor]',sv),res=$('#svResultado');
    doc.addEventListener('input',function(){var raw=doc.value,d=raw.replace(/\D/g,'').slice(0,14);
      if(/^\(/.test(raw)||(d.length===11&&d[2]==='9'&&/[()\s]/.test(raw))){doc.value=d.slice(0,11).replace(/(\d{2})(\d{5})(\d{0,4})/,'($1) $2-$3');return;}
      if(d.length<=11)doc.value=d.replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d{1,2})$/,'$1-$2');
      else doc.value=d.replace(/^(\d{2})(\d)/,'$1.$2').replace(/^(\d{2})\.(\d{3})(\d)/,'$1.$2.$3').replace(/\.(\d{3})(\d)/,'.$1/$2').replace(/(\d{4})(\d)/,'$1-$2');});
    $$('input',sv).forEach(function(x){x.addEventListener('input',function(){x.closest('.field').classList.remove('bad');});});
    sv.addEventListener('submit',function(e){e.preventDefault();
      var d=doc.value.replace(/\D/g,''),v=num(val.value);
      if(!(d.length===11||d.length===14||d.length===10)){doc.closest('.field').classList.add('bad');doc.focus();return;}
      if(v<=0){val.closest('.field').classList.add('bad');val.focus();return;}
      res.hidden=false;res.classList.remove('pop');void res.offsetWidth;res.classList.add('pop');
      if(v>=5000){res.innerHTML='<div class="sv-vazio">'+ic('search',28)+'<b>Nenhuma fatura encontrada</b><p>Por favor, faça uma nova pesquisa.</p></div>';return;}
      var venc=new Date(Date.now()+5*864e5),dd=('0'+venc.getDate()).slice(-2)+'/'+('0'+(venc.getMonth()+1)).slice(-2)+'/'+venc.getFullYear();
      res.innerHTML='<div class="sv-fatura">'+
        '<div class="sv-top"><span class="tone">'+ic('receipt',22)+'</span><div><small>Fatura de exemplo</small><b>Ateliê Souza</b></div><span class="badge warn">Aguardando pagamento</span></div>'+
        '<div class="sv-valor"><small>Valor</small><strong>'+brl(v)+'</strong><small>Novo vencimento: '+dd+'</small></div>'+
        '<div class="sv-acoes"><button type="button" class="btn btn-cta btn-sm" data-copiar>'+ic('pix',18)+'Copiar Pix copia e cola</button><button type="button" class="btn btn-ghost btn-sm" data-copiar>'+ic('barcode',18)+'Copiar linha digitável</button><button type="button" class="btn btn-ghost btn-sm" data-baixar>'+ic('download',18)+'Baixar PDF</button></div>'+
        '<p class="sv-aviso">'+ic('alert',16)+'Demonstração: esta fatura e os códigos são fictícios e não podem ser pagos.</p></div>';
      $$('[data-copiar]',res).forEach(function(b){b.addEventListener('click',function(){toast('Código de exemplo copiado');});});
      $$('[data-baixar]',res).forEach(function(b){b.addEventListener('click',function(){toast('PDF de exemplo indisponível nesta demonstração');});});
    });
  }

  /* ================= Criar conta (demonstração em 5 etapas) ================= */
  var cc=$('#criarConta');
  if(cc){
    var passos=$$('.cc-passo',cc),dots=$$('.cc-steps li'),barra=$('.cc-barra i'),atualP=0;
    var em=$('[name=email]',cc);try{var e0=sessionStorage.getItem('asaas-cadastro-email');if(e0&&em)em.value=e0;}catch(e){}
    var masks={
      cpf:function(d){return d.slice(0,11).replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d{1,2})$/,'$1-$2');},
      cnpj:function(d){return d.slice(0,14).replace(/^(\d{2})(\d)/,'$1.$2').replace(/^(\d{2})\.(\d{3})(\d)/,'$1.$2.$3').replace(/\.(\d{3})(\d)/,'.$1/$2').replace(/(\d{4})(\d)/,'$1-$2');},
      data:function(d){return d.slice(0,8).replace(/(\d{2})(\d)/,'$1/$2').replace(/(\d{2})(\d)/,'$1/$2');},
      cel:function(d){d=d.slice(0,11);return d.length>10?d.replace(/(\d{2})(\d{5})(\d{0,4})/,'($1) $2-$3'):d.replace(/(\d{2})(\d{4})(\d{0,4})/,'($1) $2-$3');},
      cep:function(d){return d.slice(0,8).replace(/(\d{5})(\d)/,'$1-$2');}
    };
    $$('[data-mask]',cc).forEach(function(i){i.addEventListener('input',function(){var d=i.value.replace(/\D/g,'');i.value=d?masks[i.getAttribute('data-mask')](d):'';});});
    var tipoPJ=true;
    function setTipo(pj){tipoPJ=pj;$$('[name=tipo]',cc).forEach(function(r){r.checked=(r.value==='pj')===pj;});$$('[data-so=pj]',cc).forEach(function(x){x.hidden=!pj;});$$('[data-so=pf]',cc).forEach(function(x){x.hidden=pj;});}
    $$('[name=tipo]',cc).forEach(function(r){r.addEventListener('change',function(){setTipo(r.value==='pj');});});
    $$('[data-tipo]',cc).forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();setTipo(a.getAttribute('data-tipo')==='pj');});});
    setTipo(true);
    function ir(i,rolar){atualP=i;passos.forEach(function(p,k){p.hidden=k!==i;if(k===i){p.classList.remove('step-in');void p.offsetWidth;p.classList.add('step-in');}});
      dots.forEach(function(d,k){d.classList.toggle('feito',k<i);d.classList.toggle('atual',k===i);if(k===i)d.setAttribute('aria-current','step');else d.removeAttribute('aria-current');});
      if(barra)barra.style.width=(Math.min(i,dots.length)/dots.length*100)+'%';
      var f=$('input:not([type=hidden]):not([type=checkbox]):not([type=radio]),select',passos[i]);if(f&&rolar!==false)f.focus({preventScroll:true});
      if(rolar!==false)cc.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});}
    function erro(campo,msg){var g=campo.closest('.field');if(!g)return false;g.classList.add('bad');var m=$('.msg',g);if(m)m.textContent=msg;return false;}
    $$('input,select',cc).forEach(function(x){x.addEventListener('input',function(){var g=x.closest('.field');g&&g.classList.remove('bad');});x.addEventListener('change',function(){var g=x.closest('.field');g&&g.classList.remove('bad');});});
    function valida(i){
      var p=passos[i],ok=true;$$('.field',p).forEach(function(g){g.classList.remove('bad');});
      var v=function(n){var x=$('[name='+n+']',p);return x?x.value.trim():'';};
      if(i===0){
        if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v('email')))ok=erro($('[name=email]',p),'Informe um e-mail válido.')&&ok;
        if(v('senha').length<8)ok=erro($('[name=senha]',p),'Use pelo menos 8 caracteres.')&&ok;
        if(!v('senha2')||v('senha2')!==v('senha'))ok=erro($('[name=senha2]',p),'As senhas não conferem.')&&ok;
        if(!$('[name=termos]',p).checked)ok=erro($('[name=termos]',p),'Aceite os termos para continuar.')&&ok;
      }
      if(i===1){
        if(tipoPJ){if(v('cnpj').replace(/\D/g,'').length!==14)ok=erro($('[name=cnpj]',p),'Informe um CNPJ com 14 dígitos.')&&ok;}
        else{if(v('cpf').replace(/\D/g,'').length!==11)ok=erro($('[name=cpf]',p),'Informe um CPF com 11 dígitos.')&&ok;
             if(v('nasc').replace(/\D/g,'').length!==8)ok=erro($('[name=nasc]',p),'Informe a data no formato dd/mm/aaaa.')&&ok;}
      }
      if(i===2){
        if(v('nome').split(' ').filter(Boolean).length<2)ok=erro($('[name=nome]',p),'Informe seu nome completo.')&&ok;
        if(tipoPJ&&!v('razao'))ok=erro($('[name=razao]',p),'Informe o nome da sua empresa.')&&ok;
        if(tipoPJ&&!v('empresa'))ok=erro($('[name=empresa]',p),'Selecione o tipo da sua empresa.')&&ok;
        if(v('celular').replace(/\D/g,'').length<10)ok=erro($('[name=celular]',p),'Informe um celular com DDD.')&&ok;
      }
      if(i===3){
        if(v('cep').replace(/\D/g,'').length!==8)ok=erro($('[name=cep]',p),'Informe um CEP com 8 dígitos.')&&ok;
        ['cidade','uf','rua','bairro','numero'].forEach(function(n){if(!v(n))ok=erro($('[name='+n+']',p),'Campo obrigatório.')&&ok;});
      }
      if(i===4){var c=$$('.otp input',p).map(function(x){return x.value;}).join('');if(c.length!==6){ok=false;$('.otp',p).closest('.field').classList.add('bad');}}
      if(!ok){var b=$('.field.bad input,.field.bad select',p);b&&b.focus();}
      return ok;
    }
    $$('[data-prox]',cc).forEach(function(b){b.addEventListener('click',function(){if(!valida(atualP))return;
      if(atualP===3){$('#ccCel').textContent=$('[name=celular]',cc).value;iniciaContagem();}
      ir(atualP+1);});});
    $$('[data-volta]',cc).forEach(function(b){b.addEventListener('click',function(){ir(Math.max(0,atualP-1));});});
    $$('[data-altera]',cc).forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();ir(2);});});
    var cepLink=$('[data-semcep]',cc);if(cepLink)cepLink.addEventListener('click',function(e){e.preventDefault();toast('Consulte seu CEP no site dos Correios');});
    var otp=$$('.otp input',cc);
    otp.forEach(function(x,k){x.addEventListener('input',function(){x.value=x.value.replace(/\D/g,'').slice(0,1);if(x.value&&otp[k+1])otp[k+1].focus();});
      x.addEventListener('keydown',function(e){if(e.key==='Backspace'&&!x.value&&otp[k-1])otp[k-1].focus();});
      x.addEventListener('paste',function(e){var t=(e.clipboardData||window.clipboardData).getData('text').replace(/\D/g,'').slice(0,6);if(t.length){e.preventDefault();otp.forEach(function(o,j){o.value=t[j]||'';});otp[Math.min(t.length,5)].focus();}});});
    var timer,seg=15;
    function iniciaContagem(){clearInterval(timer);seg=15;var links=$$('[data-reenviar]',cc);
      function upd(){links.forEach(function(a){var base=a.getAttribute('data-reenviar');a.textContent=seg>0?base+' em '+seg+'s':base;a.classList.toggle('off',seg>0);a.setAttribute('aria-disabled',seg>0);});}
      upd();timer=setInterval(function(){seg--;upd();if(seg<=0)clearInterval(timer);},1000);}
    $$('[data-reenviar]',cc).forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();if(seg>0)return;toast('Código reenviado (demonstração)');iniciaContagem();});});
    ir(0,false);
  }
})();
