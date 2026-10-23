# Handoff · Publicar no GitHub Pages (para o Claude Code)

> **Atualizado em 23/10/2026.** A primeira versão deste arquivo mandava criar o repositório `asaas-redesenho`. **Isso já foi feito de outra forma:** o site está publicado em `cbitran/asaas`. Não crie outro repositório.

## Estado atual (já publicado)

| Item | Valor |
|---|---|
| Repositório | https://github.com/cbitran/asaas (público), branch `main` |
| Pages | Ligado em modo **GitHub Actions** (`.github/workflows/pages.yml`) |
| Landing | https://cbitran.github.io/asaas/ |
| Painel (protótipo) | https://cbitran.github.io/asaas/painel/ |
| Design system | https://cbitran.github.io/asaas/design-system/ |
| Defesa (slides do estudo) | https://cbitran.github.io/asaas/defesa/ |
| Documentos do estudo | `docs/` (visíveis no GitHub) |
| Remoto | `origin` já aponta para `https://github.com/cbitran/asaas.git` |
| Identidade do git (local) | E-mail "noreply" do GitHub; não mude |

O workflow roda a cada push na `main`: `npm ci` → `npm run build` com `BASE_PATH=/<nome-do-repositório>/` → publica `dist`. Como o repositório se chama `asaas`, o caminho base é `/asaas/` e **não precisa de ajuste manual**.

**Não use** `publicar.sh` nem `Publicar no GitHub.command`: eles servem para publicar do zero e criariam o repositório `asaas-redesenho`. Ficam no projeto só como legado.

## Tarefa atual: unir e subir o que está pendente

Há trabalho de outra sessão que ainda **não foi commitado** (17 itens): `README.md`, `index.html` e `vite.config.ts` modificados; pastas novas `blog/`, `carreiras/`, `criar-conta/`, `precos/`, `segunda-via/`, `sobre-nos/`, `solucoes/`, `estilos/`; 4 imagens em `public/img/`; `referencia/solucoes-original.json`; `scripts/gerar-paginas.py`. Este arquivo também aparece como modificado.

1. `cd "/Volumes/SSD Dock/Projetos Claude/Asaas/asaas-redesenho"` e `git status`.
2. Confirme que **`.env` e `.tts-cache/` não aparecem** (estão no `.gitignore`) e que nenhum arquivo traz chave de API.
3. Valide o build como o GitHub fará:
   ```bash
   npm ci && BASE_PATH=/asaas/ npm run build
   ```
   Deve gerar `dist/index.html`, `dist/painel/`, `dist/design-system/`, `dist/defesa/`, `dist/voz/*.mp3` (29 áudios) e as páginas novas. O `vite.config.ts` da árvore de trabalho já lista `design-system` e `defesa`.
4. Commit em português com esses arquivos e `git push origin main`.
5. Acompanhe: `gh run watch` (ou `gh run list --workflow pages.yml`). Leva cerca de 1 minuto.
6. Confira com `curl -s -o /dev/null -w '%{http_code}'` que respondem **200**: `/asaas/`, `/asaas/painel/`, `/asaas/design-system/`, `/asaas/defesa/` e as páginas novas.
7. No navegador: a landing abre com as imagens; o cadastro com e-mail válido leva a `/painel/`; no painel, Conta › **Sair** volta para a landing; a voz do assistente toca só no painel.
8. Responda com os links finais.

## Se algo falhar

| Sintoma | Causa provável | Correção |
|---|---|---|
| Workflow falha com "Pages not enabled" | Pages desligado | `gh api -X PUT repos/cbitran/asaas/pages -f build_type=workflow` e `gh workflow run pages.yml` |
| Site sem CSS ou 404 em `/assets` | `BASE_PATH` errado | O workflow já usa o nome real do repositório; confirme que o build rodou pelo Actions |
| `npm ci` falha no Actions | `package-lock.json` fora de sincronia | `npm install` local, commit do lock e novo push |
| Página nova dá 404 | Pasta não listada nas entradas do `vite.config.ts` | Incluir a pasta na lista de páginas e refazer o build |
| Push recusado | Alguém empurrou antes | `git pull --rebase origin main`, resolver, novo push |

## Não fazer

- **Não criar outro repositório** (`asaas-redesenho` ou qualquer outro) nem rodar `publicar.sh`.
- Não commitar `.env`, `.tts-cache`, `dist` nem `node_modules`.
- Não alterar textos, layout ou regras do protótipo: esta tarefa é só publicação.
- Não apagar a pasta `site/` (vazia) nem o arquivo `../asaas-src.tgz` sem perguntar.
- Não versionar a pasta `../demo-reel/` (vídeo em produção; fica fora do repositório).
- Não usar domínio real do Asaas em links.
- O protótipo é **simulação**: valores, nomes e datas são fictícios.
