// Grava (uma vez) o áudio de cada frase de scripts/frases-demo.json em public/voz/ e monta o índice.
// Precisa do servidor rodando (npm run dev) e da chave da ElevenLabs configurada. GASTA CRÉDITO só
// nas frases que ainda não têm arquivo; as já gravadas são puladas.
// Uso: node scripts/gerar-voz.mjs [--simular]   (--simular só mostra o que seria gravado)
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const simular = process.argv.includes('--simular');
const origem = process.env.TTS_URL || 'http://127.0.0.1:5173/api/tts';
const dir = fileURLToPath(new URL('../public/voz/', import.meta.url));
const frases = JSON.parse(fs.readFileSync(new URL('./frases-demo.json', import.meta.url), 'utf8'));
fs.mkdirSync(dir, { recursive: true });

const idxFile = path.join(dir, 'index.json');
const idx = fs.existsSync(idxFile) ? JSON.parse(fs.readFileSync(idxFile, 'utf8')) : {};
const nome = (t) => createHash('sha1').update(t).digest('hex').slice(0, 12) + '.mp3';

let novas = 0, puladas = 0, chars = 0, falhou = false;
for (const f of frases) {
  const arq = nome(f.falado);
  if (fs.existsSync(path.join(dir, arq))) { idx[f.falado] = arq; puladas++; continue; }
  if (simular) { novas++; chars += f.falado.length; continue; }
  const r = await fetch(origem, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: f.falado }) });
  if (!r.ok) {
    console.error('Parou: o servidor respondeu ' + r.status + ' em "' + f.falado.slice(0, 50) + '..."', (await r.text()).slice(0, 200));
    falhou = true;
    break;
  }
  fs.writeFileSync(path.join(dir, arq), Buffer.from(await r.arrayBuffer()));
  idx[f.falado] = arq;
  novas++;
  chars += f.falado.length;
  console.log('gravada', arq, f.falado.length + ' car.', '| cache do servidor:', r.headers.get('x-voz-cache'));
  fs.writeFileSync(idxFile, JSON.stringify(idx, null, 2) + '\n'); // salva a cada frase
}
if (!simular) fs.writeFileSync(idxFile, JSON.stringify(idx, null, 2) + '\n');
console.log((simular ? '[simulação] ' : '') + 'novas:', novas, '| já existiam:', puladas, '| caracteres das novas:', chars, falhou ? '| INCOMPLETO' : '');
process.exit(falhou ? 1 : 0);
