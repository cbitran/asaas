import React from 'react';
import { createRoot } from 'react-dom/client';
import { DCApp, parseDC } from './dc/runtime';
import { textoFalado } from './voz/normalizar.mjs';
import mainRaw from '../referencia/Main.dc.html?raw';

// Voz do assistente: áudios já gravados em public/voz (índice texto -> arquivo).
// Se uma frase não estiver no índice, o app tenta a voz ao vivo (/api/tts, só com chave configurada).
const base = import.meta.env.BASE_URL;
(window as any).asaasVoz = {
  textoFalado,
  base,
  idx: {} as Record<string, string>,
  pronto: fetch(base + 'voz/index.json')
    .then((r) => (r.ok ? r.json() : {}))
    .then((j) => { (window as any).asaasVoz.idx = j; })
    .catch(() => {})
};

const root = createRoot(document.getElementById('root')!);

try {
  const parsed = parseDC(mainRaw);
  root.render(<DCApp parsed={parsed} props={{}} />);
} catch (e: any) {
  root.render(<pre style={{ padding: 24, whiteSpace: 'pre-wrap', color: '#B02A37' }}>{String(e && e.message ? e.message : e)}</pre>);
}
