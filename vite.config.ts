import { defineConfig, loadEnv, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { readFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

/** Mesma origem de chave da ferramenta narrar.py: ~/.elevenlabs.env (linha ELEVENLABS_API_KEY=...). */
function chaveDoArquivoDoUsuario(): string {
  try {
    const txt = readFileSync(path.join(os.homedir(), '.elevenlabs.env'), 'utf8');
    for (const linha of txt.split(/\r?\n/)) {
      const l = linha.trim();
      if (l.startsWith('ELEVENLABS_API_KEY=')) return l.slice('ELEVENLABS_API_KEY='.length).trim().replace(/^['"]|['"]$/g, '');
    }
  } catch { /* arquivo não existe */ }
  return '';
}

/**
 * Proxy local de voz (ElevenLabs). A chave fica só no servidor (.env) e nunca vai ao navegador.
 * POST /api/tts  { text }  ->  audio/mpeg
 * Respostas já geradas ficam em .tts-cache para não gastar créditos repetindo a mesma frase.
 * Referência: POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}, cabeçalho xi-api-key.
 */
function ttsProxy(mode: string): Plugin {
  const cacheDir = path.resolve('.tts-cache');
  const json = (res: any, status: number, body: object) => {
    res.statusCode = status;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(body));
  };
  return {
    name: 'asaas-tts-proxy',
    configureServer(server) {
      server.middlewares.use('/api/tts', async (req, res) => {
        if (req.method !== 'POST') return json(res, 405, { error: 'metodo' });
        // relê o .env a cada pedido: dá para ajustar a voz sem reiniciar o servidor
        const env = loadEnv(mode, process.cwd(), '');
        const key = env.ELEVENLABS_API_KEY || process.env.ELEVENLABS_API_KEY || chaveDoArquivoDoUsuario();
        const voice = env.ELEVENLABS_VOICE_ID;
        if (!key || !voice) return json(res, 501, { error: 'sem_chave' });

        let raw = '';
        for await (const chunk of req) {
          raw += chunk;
          if (raw.length > 20000) return json(res, 413, { error: 'grande' });
        }
        let text = '';
        try { text = String(JSON.parse(raw).text || '').trim(); } catch { return json(res, 400, { error: 'json' }); }
        if (!text) return json(res, 400, { error: 'vazio' });
        if (text.length > 1200) return json(res, 413, { error: 'texto_longo' });

        const model = env.ELEVENLABS_MODEL || 'eleven_multilingual_v2';
        const settings = {
          stability: Number(env.ELEVENLABS_STABILITY || 0.45),
          similarity_boost: Number(env.ELEVENLABS_SIMILARITY || 0.75),
          style: Number(env.ELEVENLABS_STYLE || 0),
          speed: Number(env.ELEVENLABS_SPEED || 1),
          use_speaker_boost: true
        };
        const hash = createHash('sha1').update(JSON.stringify([voice, model, settings, text])).digest('hex');
        const file = path.join(cacheDir, hash + '.mp3');
        try {
          const cached = await readFile(file);
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('X-Voz-Cache', 'hit');
          return res.end(cached);
        } catch { /* sem cache */ }

        try {
          const r = await fetch(
            'https://api.elevenlabs.io/v1/text-to-speech/' + encodeURIComponent(voice) + '?output_format=mp3_44100_128',
            {
              method: 'POST',
              headers: { 'xi-api-key': key, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
              body: JSON.stringify({ text, model_id: model, voice_settings: settings })
            }
          );
          if (!r.ok) {
            const detail = (await r.text()).slice(0, 300);
            return json(res, r.status === 401 ? 401 : 502, { error: 'elevenlabs', status: r.status, detail });
          }
          const buf = Buffer.from(await r.arrayBuffer());
          await mkdir(cacheDir, { recursive: true });
          await writeFile(file, buf);
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('X-Voz-Cache', 'miss');
          return res.end(buf);
        } catch (e: any) {
          return json(res, 502, { error: 'rede', detail: String(e && e.message ? e.message : e).slice(0, 200) });
        }
      });
    }
  };
}

// GitHub Pages publica em /<repositório>/ — o workflow define BASE_PATH; localmente fica '/'.
export default defineConfig(({ mode }) => ({
  base: process.env.BASE_PATH || '/',
  plugins: [react(), ttsProxy(mode)],
  server: { port: 5173, host: '127.0.0.1' },
  build: {
    rollupOptions: {
      input: {
        site: path.resolve(__dirname, 'index.html'),
        painel: path.resolve(__dirname, 'painel/index.html'),
        designSystem: path.resolve(__dirname, 'design-system/index.html')
      }
    }
  }
}));
