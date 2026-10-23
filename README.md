# Asaas · redesenho do painel — pacote para o Claude Code

## Como usar
1. Descompacte esta pasta onde quiser (ex.: `~/Projetos/asaas-redesenho`).
2. No Terminal:
   ```
   cd ~/Projetos/asaas-redesenho
   claude
   ```
3. Cole este pedido:
   > Leia CLAUDE.md, HANDOFF.md e referencia/COMO-LER.md. Monte o protótipo navegável em Vite + React + TypeScript seguindo a ordem de implementação do CLAUDE.md, usando referencia/Main.dc.html como fonte exata de layout, textos, dados e interações. No final, rode `npm install` e `npm run dev` e me passe a URL do localhost.
4. Abra http://localhost:5173 no navegador.

## O que tem aqui
- `CLAUDE.md`: instruções para o Claude Code (stack, rotas, ordem, critérios de aceite)
- `HANDOFF.md`: especificação de telas, estados, fluxos, animações, responsivo e acessibilidade
- `tokens/`: `tokens.css` (variáveis claro/escuro) e `tokens.json`
- `referencia/`: arquivos do protótipo aprovado no canvas, mais `COMO-LER.md`

Os dados são fictícios.

## Landing page + painel
- `npm run dev` → landing em http://localhost:5173/ e painel em http://localhost:5173/painel/
- A landing usa `tokens/tokens.css` do painel. "Acessar minha conta" e o cadastro levam ao painel; Conta › Sair volta para a landing.
- A voz do assistente só toca no painel: cala quando a aba fica oculta ou quando a landing está aberta (BroadcastChannel `asaas-voz`).

## Publicar no GitHub Pages
- `./publicar.sh` (opcional: nome do repositório; padrão `asaas-redesenho`).
- Cria o repositório público, liga o Pages e envia. A cada push na `main`, `.github/workflows/pages.yml` gera o build e publica.
