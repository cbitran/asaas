# CLAUDE.md — Protótipo navegável do painel Asaas (conceito)

## Objetivo
Montar um app **local** (`npm run dev` → http://localhost:5173) para navegar pela jornada completa do redesenho do painel Asaas. É um **protótipo de UX**: dados fictícios em memória, sem backend, sem login, sem chamadas de rede (exceto Google Fonts).

## Fonte da verdade
1. `referencia/Main.dc.html` — o protótipo aprovado. Contém **toda** a marcação, estilos, estados, dados fictícios e regras de interação. Leia `referencia/COMO-LER.md` antes.
2. `HANDOFF.md` — especificação funcional: telas, estados, fluxos, validações, animações, breakpoints e acessibilidade.
3. `tokens/tokens.css` — tokens de cor (claro e escuro), tipografia, espaçamento, raios, sombras e movimento. **Use somente esses tokens**; não invente cores.

Em caso de dúvida entre HANDOFF e referência, **a referência vence** (valores exatos de padding, raio, tamanho de fonte e textos). Copie os textos em português exatamente como estão, com acentuação.

## Stack
- Vite + React 18 + TypeScript
- React Router (uma rota por tela, para o usuário poder navegar e usar o botão voltar)
- CSS com variáveis de `tokens/tokens.css` (CSS Modules ou um arquivo global, sem Tailwind)
- Estado global simples com Context + useReducer (tema, cenário de dados, cobranças criadas, links criados, layout do Início, notificações lidas)
- Sem bibliotecas de UI. Ícones: os paths SVG do objeto `I` em `Main.dc.html` (stroke 1.8, viewBox 24).
- Fonte: Plus Jakarta Sans (Google Fonts) 400–800.

## Rotas
| Rota | Tela |
|---|---|
| `/` | Início (modular) |
| `/cobrancas` | Lista de cobranças (`?status=vencida`, `?aba=Chargeback`) |
| `/cobrancas/nova` | Criar cobrança |
| `/cobrancas/:id/confirmacao` | Confirmação |
| `/links` | Links de pagamento (o "criar link" é **modal** sobre esta tela) |
| `/pix` | Pix (abas) |
| `/extrato` | Meu dinheiro › Extrato |
| `/notas` | Notas fiscais (onboarding em 4 passos ou lista) |
| `/area/:id` | Demais itens do menu (tela "função mantida") |

Drawers e modais (detalhe da cobrança, filtros, transferência Pix, confirmação Pix, cancelar/estornar, criar link) abrem por estado, sem trocar de rota.

## Ordem de implementação
1. Projeto Vite, tokens, fonte, tema claro/escuro (`data-theme` no `<html>`), layout shell (menu lateral + topo + conteúdo).
2. Menu agrupado com submenus animados, recolher para ícones, badges, menu mobile como bottom sheet e barra inferior.
3. Topo: busca, notificações (popover), ajuda, alternar tema (só ícone), menu da conta (popover).
4. Início com widgets (arrastar, largura, ocultar, biblioteca de widgets, persistência em localStorage).
5. Cobranças + drawer de detalhe + filtros + modais de cancelar/estornar.
6. Criar cobrança com validação e confirmação.
7. Links de pagamento + modal em 3 etapas.
8. Pix, Extrato e Notas fiscais.
9. Assistente proativo.
10. Controle "Demo do protótipo" (alterna conta nova × com movimento) no canto inferior.
11. Responsivo: desktop ≥ 1100, tablet 760–1099 (menu recolhido), mobile < 760.

## Critérios de aceite
- `npm install && npm run dev` sobe sem erros e sem warnings de console.
- Toda a jornada do HANDOFF (seção "Jornadas para testar") funciona clicando.
- Os dois cenários (conta nova e com movimento) e os dois temas funcionam em todas as telas.
- Em 1440, 834 e 390 px de largura não há scroll horizontal, nada corta e nada sobrepõe conteúdo.
- Alvos de toque ≥ 44 px, foco visível pelo teclado, labels em todos os campos e contraste AA.
- Valores sempre em `R$ 1.234,56` (vírgula decimal, ponto de milhar).

## Não fazer
- Não alterar regras de negócio, textos ou dados fictícios da referência.
- Não usar domínio real do Asaas em links (use `pagar.exemplo.com.br`).
- Não adicionar telas, métricas ou seções que não estejam na referência sem perguntar.

## Publicação (tarefa atual)
Para publicar no GitHub Pages, siga `HANDOFF-PUBLICAR.md`. Estrutura atual: landing em `index.html` (raiz) e painel em `painel/index.html`.
