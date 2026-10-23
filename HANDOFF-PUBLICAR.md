# Handoff · Publicar no GitHub Pages (para o Claude Code)

## Objetivo
Publicar este projeto (landing page + painel do conceito Asaas) no **GitHub Pages** da conta do Bitran, num repositório **público** chamado `asaas-redesenho`, com deploy automático a cada push na `main`.

Resultado esperado:
- Site (landing): `https://<usuario>.github.io/asaas-redesenho/`
- Painel: `https://<usuario>.github.io/asaas-redesenho/painel/`

## O que já está pronto (não refazer)
- **Estrutura multipágina (Vite):** `index.html` = landing · `painel/index.html` = painel. Entradas em `vite.config.ts` (`build.rollupOptions.input`).
- **Base path:** `vite.config.ts` usa `base: process.env.BASE_PATH || '/'`. O workflow define `BASE_PATH=/<nome-do-repo>/`.
- **Workflow:** `.github/workflows/pages.yml` (Node 20 → `npm ci` → `npm run build` → `upload-pages-artifact` → `deploy-pages`).
- **Script:** `publicar.sh` faz tudo (cria repo, liga o Pages, faz push). `Publicar no GitHub.command` só chama o script.
- **Build já validado** com `BASE_PATH=/asaas-redesenho/`: sem 404, imagens em `/asaas-redesenho/img/…`, voz em `/asaas-redesenho/voz/…`.
- `.gitignore`: `node_modules`, `dist`, `.env`, `.tts-cache`, `.DS_Store`.

## Passos
1. `cd "/Volumes/SSD Dock/Projetos Claude/Asaas/asaas-redesenho"`
2. Conferir o GitHub CLI: `gh auth status`. Se não estiver logado, pedir ao Bitran para rodar `gh auth login --web` (não digitar tokens).
3. Validar o build local antes de publicar:
   ```bash
   npm ci && BASE_PATH=/asaas-redesenho/ npm run build
   ```
   Deve gerar `dist/index.html`, `dist/painel/index.html`, `dist/img/*.webp`, `dist/voz/*.mp3`.
4. Publicar: `./publicar.sh` (ou `./publicar.sh outro-nome` se `asaas-redesenho` já existir com outro conteúdo).
   O script, nesta ordem:
   - `git init -b main` (se preciso) → `git add -A` → commit;
   - `gh repo create asaas-redesenho --public` (se não existir) e `origin`;
   - liga o Pages em modo Actions: `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow`;
   - `git push -u origin main`.
5. Acompanhar o deploy: `gh run watch` (ou `gh run list --workflow pages.yml`). Leva ~1 min.
6. Verificar no navegador:
   - Landing abre com fotos, órbitas animadas e FAQ (uma dúvida aberta por vez).
   - "Acessar minha conta" e "Criar conta grátis" (com e-mail válido) levam a `/painel/`.
   - No painel: Paulo Souza › **Sair** volta para a landing.
   - A voz do assistente toca só no painel (não na landing).
7. Responder ao Bitran com os dois links finais.

## Antes do commit, confira
- `git status` **não** pode listar `.env` nem `.tts-cache/` (a chave da ElevenLabs fica só local).
- A pasta vazia `site/` e o arquivo `../asaas-src.tgz` (fora do projeto) são sobras de teste: podem ser apagados.

## Se algo falhar
| Sintoma | Causa provável | Correção |
|---|---|---|
| Workflow falha em `configure-pages`/`deploy-pages` com "Pages not enabled" | Pages não ligado em modo Actions | `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow` (ou PUT se já existir) e `gh workflow run pages.yml` |
| Site abre sem CSS / 404 em `/assets` | `BASE_PATH` errado | Nome do repo diferente de `asaas-redesenho`: o workflow já usa o nome real; conferir se o build rodou pelo Actions |
| `npm ci` falha no Actions | `package-lock.json` fora de sincronia | `npm install` local, commit do lock, push |
| Push recusado (repo já existe com histórico) | Repositório com outro conteúdo | Publicar com outro nome: `./publicar.sh asaas-redesenho-conceito` |

## Não fazer
- Não commitar `.env`, `.tts-cache`, `dist` ou `node_modules`.
- Não alterar textos, layout ou regras do protótipo; esta tarefa é só publicação.
- Não usar domínio real do Asaas em links (já está assim).
