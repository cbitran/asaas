# 6 · Design system

A versão visual, com amostras e alternância de tema, está em **`design-system/index.html`** (no site publicado: `/design-system/`). Esta página resume as regras. Todos os valores vêm de [`tokens/tokens.css`](../tokens/tokens.css), o mesmo arquivo usado pelo painel e pela landing, e [`tokens/tokens.json`](../tokens/tokens.json).

## Origem na marca

A base é a paleta enviada da marca: azul `#0038E5`, azul de apoio `#006FF0`, verde `#91C651`, vermelho `#B02A37` e neutros `#1D2125`, `#37474F`, `#F8F9FA`, `#EEEEEE`. Não criamos uma identidade nova. O sistema **organiza o uso** da marca em papéis (fundo, texto, ação, status) e adiciona o modo escuro.

Onde uma cor original não chega a 4,5:1 de contraste para texto (o verde `#91C651` e o cinza `#7A8696` do material original), o token de **texto** usa um tom mais escuro derivado dela, e a cor original fica para **gráficos e preenchimentos**.

## Tokens

| Grupo | Tokens principais |
|---|---|
| Cor (claro e escuro) | `bg-ground`, `bg-surface`, `bg-subtle`, `bg-sunken`, `border`, `text-primary/secondary/muted`, `brand-primary/support/tint/text`, `action-cta`, `nav-*`, `success/warning/danger/info` (texto e fundo), `focus`, `overlay` |
| Tipografia | Plus Jakarta Sans, pesos 400 a 800: `display` 40/48, `h1` 32/38, `h2` 18/24, `metric` 24/30, `body` 15/22, `label` 13/18, `caption` 12/16 |
| Espaçamento | Base 4: 4, 8, 12, 16, 24, 32, 48, 64 px |
| Raios | `sm` 10, `md` 14, `lg` 18, `card` 24, `panel` 28, `pill` 999 px |
| Sombras | `card`, `overlay`, `toast` |
| Movimento | `ease-out` cubic-bezier(.16, 1, .3, 1); 160 ms (rápido), 260 ms (base), 380 ms (drawer) |
| Layout | Menu de 264 px (84 px recolhido); conteúdo até 1240 px; alvo de toque mínimo de 44 px; pontos de quebra em 1100 px (tablet) e 760 px (celular) |

## Contraste calculado

Razões **calculadas** por `scripts/gerar-design-system.mjs`, pela fórmula de luminância relativa do WCAG 2.2. Meta: **4,5:1** para texto normal (critério 1.4.3, nível AA). Todos os 26 pares passaram.

| Uso | Claro | Escuro |
|---|---|---|
| Texto principal sobre cartão | 16,2:1 | 14,9:1 |
| Texto de apoio | 9,7:1 | 9,0:1 |
| Texto de legenda | 5,4:1 | 7,1:1 |
| Link e marca em texto | 9,3:1 | 7,8:1 |
| Botão principal | 16,2:1 | 5,5:1 |
| Status recebida | **4,8:1** (o menor do modo claro) | 8,1:1 |
| Status vencida e erro | 5,6:1 | 6,8:1 |
| Status chargeback | 5,7:1 | 7,7:1 |
| Status aguardando | 5,7:1 | 6,7:1 |
| Menu lateral, texto branco | 7,8:1 | 11,4:1 |

A tabela completa, com as cores de cada par, está na página visual. Para regenerar após mudar um token: `node scripts/gerar-design-system.mjs`.

*Limite:* verificamos **contraste de texto**. Não verificamos o contraste de componentes sem texto (bordas, ícones) nem o de imagens.

## Componentes e estados

Botões (padrão, hover, foco, selecionado, desabilitado, secundário, perigo) · campos e select (padrão, foco, erro) · card de métrica (inclusive variante de risco) · tabela com badges de status · lista de itens · estado vazio · banner dispensável · drawer · modal de confirmação · toast · menu lateral (aberto, recolhido e em gaveta no celular) · barra inferior do celular · assistente.

Regras de estado:

| Estado | Regra |
|---|---|
| Hover | Escurece 7% (filtro de brilho), botões sobem 1 px |
| Foco | Anel de 3 px em `--color-focus` com afastamento de 2 px, só pelo teclado |
| Selecionado | Fundo `brand-tint`, borda `brand-primary` e `aria-pressed` |
| Desabilitado | Opacidade de 45% e texto que explica o motivo |
| Erro | Borda `danger`, mensagem abaixo do campo e `aria-invalid` |
| Status | **Ponto + texto + cor**, nunca só cor |

## Acessibilidade

- **Alvo de toque de 44 por 44 px ou mais.** Esse tamanho corresponde ao critério 2.5.5 do WCAG, que está no nível **AAA** (não AA).
- Elementos nativos (`button`, `a`, `input`, `select`, `table`, `label`); rótulo em todos os campos; `aria-label` nos botões só com ícone.
- Modais com `role="dialog"` ou `alertdialog` e `aria-modal`; foco devolvido ao gatilho; Esc fecha.
- Animações desligadas quando a pessoa pede movimento reduzido.
- Tema claro e escuro em todas as telas.

*Limite:* essas regras foram **desenhadas e implementadas**. Não passaram por auditoria com leitor de tela nem por teste com pessoas com deficiência.

## Como usar

```css
@import url('tokens/tokens.css');
.botao { background: var(--color-action-cta); color: var(--color-action-on-cta); border-radius: var(--radius-md); min-height: var(--touch-min); }
```

Para o modo escuro, defina `data-theme="dark"` no elemento `<html>`. Use **apenas** tokens; não crie cores novas.
