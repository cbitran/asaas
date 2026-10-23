# Como ler os arquivos `.dc.html`

Os arquivos desta pasta vêm do canvas de design. Eles **não rodam fora do canvas** (dependem de um runtime próprio, `support.js`). Use-os como especificação exata de marcação, estilo, dados e comportamento, e reescreva em React.

## Estrutura
```
<x-dc>
  <helmet> … fonte, CSS global (hover, foco, keyframes) … </helmet>
  … marcação da tela com {{holes}} …
</x-dc>
<script type="text/x-dc" data-dc-script data-props='…'>
class Component extends DCLogic {
  renderVals() { … calcula tudo que a marcação usa … return { … }; }
}
</script>
```

## Equivalências para React
| No arquivo | Em React |
|---|---|
| `{{ a.b }}` | `{a.b}` (sempre um valor já calculado em `renderVals`) |
| `style="color: {{t.ink}}"` | `style={{ color: t.ink }}` ou variável CSS do token |
| `<sc-if value="{{x}}">…</sc-if>` | `{x && (…)}` |
| `<sc-for list="{{xs}}" as="x">…</sc-for>` | `{xs.map(x => …)}` |
| `onClick="{{fn}}"` | `onClick={fn}` |
| `this.state` / `this.setState` | `useReducer` / Context |
| `<dc-import name="Main" …>` | o mesmo componente com props |

## Onde está cada coisa em `Main.dc.html`
- **CSS global** (hover, foco, animações: `subIn`, `drawerIn`, `modalIn`, `popIn`, `sheetUp`, `agentIn`, `pulse`, `stepIn`): bloco `<helmet><style>` no topo.
- **Tokens em JS**: objetos `LIGHT` e `DARK` (equivalem a `tokens/tokens.css`).
- **Ícones**: objeto `I` (paths SVG).
- **Dados fictícios**: `BASE` (cobranças), `CLIENTES`, `EXT` (extrato), `pixBase`, `linksBase`, `NTS` (notificações), `NFS` (passos fiscais), `nf.items` (notas).
- **Menu**: `NAV` (grupos, itens, submenus, badges).
- **Layout responsivo**: objeto `L` (valores por desktop/tablet/mobile).
- **Cabeçalho por tela**: bloco `hdr` (título, subtítulo, CTA único da tela).
- **Início modular**: `WDEF`, `WT`, `LIBMETA`, `widgets`, `library`.
- **Formulário de cobrança**: `PRE`, `fx`, `submitForm` (validações).
- **Link de pagamento**: `LK0`, `lw` (3 etapas, validações).
- **Assistente**: `ACT`, `QS`, `matchKey`, `answer`, sugestões proativas por tela (`N`).
- **Overlays**: `ov`, `dc` (detalhe), `md` (modais de confirmação).
- **Notificações**: `NTS`, `nt`.

Os outros arquivos (`Sistema`, `Componentes`, `Arquitetura`, `Anotacoes`) são pranchas de documentação: tokens, estados de componentes, arquitetura do menu e comportamento dos estados.
