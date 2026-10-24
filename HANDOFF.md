# Handoff · Redesenho do painel Asaas (conceito)

Redesenho visual, de organização e de jornada. **Nenhuma regra de negócio muda.** Dados fictícios. Idioma pt-BR. Valores em `R$ 1.234,56`. Data de referência do protótipo: **23/10/2026**.

---

## 1. Shell

### Layout
- Fundo `--color-bg-ground`. Padding de 16 px no desktop. Menu flutuante à esquerda (raio 28), conteúdo com `max-width: 1240px`.
- **Breakpoints:** ≥ 1100 desktop · 760–1099 tablet (menu recolhido por padrão, cards de resumo em 2 colunas, widgets de 1/3 viram 1/2) · < 760 mobile.

### Menu lateral (264 px; recolhido 84 px)
- Fundo `--color-nav-bg`, texto branco. Item ativo: fundo branco e texto `--color-nav-active-text`. Hover: `rgba(255,255,255,.16)`, com o ícone crescendo 8%.
- Topo: marca "Asaas · Conceito de redesenho" e botão de recolher/expandir (ícone). A largura anima em 260 ms.
- Grupos: (sem rótulo) Início · **Recebimentos** (Cobranças, Links de pagamento, Vendas físicas) · **Clientes** (Clientes, Consulta Serasa, Negativação) · **Dinheiro** (Meu dinheiro, Pix, Pague contas, Cartão Asaas, Antecipações) · **Fiscal** (Notas fiscais) · **Ferramentas** (Simulador de vendas, Open Finance, Seguros, Personalizar notificações) · **Mais** (Indicar amigo, Meus benefícios).
- Os submenus abrem com animação (altura + fade, itens em cascata de 30 ms, seta gira 180°). Lista completa em `NAV`.
- Badges: Cobranças "3" (aria: "3 cobranças vencidas") e Notas "1" (aria: "1 nota fiscal com erro"), só no cenário com movimento. Com o menu recolhido, o badge vira um balão absoluto no canto superior direito do ícone, com borda de 2 px da cor do menu, e não desloca o ícone. Recolhido, cada item mostra `title` no hover.
- Sem barra de rolagem visível (`scrollbar-width: none`).
- **Mobile:** o menu vira **bottom sheet**, sobe de baixo (`sheetUp`, 380 ms), largura total, até 86% da altura, raio só em cima, alça no topo e fundo escurecido. Fecha no X ou tocando no fundo. A barra inferior fixa tem Início, Cobranças, Pix, Extrato e Menu (56 px). O grupo "Mais" ganha o item "Personalizar início".

### Topo (desktop/tablet)
Busca global (placeholder "Buscar cobranças, clientes ou telas", atalho ⌘K) · espaço · **Notificações** · **Ajuda** · **Tema** (só ícone: lua no claro, sol no escuro) · **Conta** (avatar PA + "Paulo Augusto / Ateliê Souza"; no tablet só o avatar).

- **Popover de notificações** (400 px, `popIn`):
  - Cabeçalho "Notificações" + "Marcar todas como lidas".
  - Filtros "Todas" e "Não lidas (n)". Itens com ícone tonal, título, descrição e tempo; os não lidos têm fundo sutil e ponto azul.
  - Ao clicar, marca como lida, fecha e navega. Rodapé: "Ver todas" · "Preferências".
  - O badge do sino mostra o número de não lidas. Itens em `NTS`.
- **Popover da conta** (320 px):
  - E-mail e "Banco 461 · Agência 0001 · Conta 0000000-0 (fictícios)", com botão de copiar.
  - Itens: Minha conta, **Personalizar início**, Meus benefícios ("Novo"), Novidades, Planos, Taxas, Termos e contratos, Ajuda, Integrações e, após um separador, **Sair** em vermelho.
  - Notificações e conta são mutuamente exclusivos.

### Cabeçalho de página
Título (Início: "Olá, Paulo!\nO que vamos receber hoje?", 24 px), subtítulo e **um único CTA principal** (escuro, `--color-action-cta`). Por tela: Início e Cobranças "Criar cobrança" · Links "Criar link de pagamento" · Pix "Transferir via Pix" · Extrato "Transferir saldo" (secundários: Pagar contas, Exportar) · Notas "Emitir nota" (desabilitado sem configuração). No mobile, o CTA ocupa a largura toda.

### Controle de demonstração
Fica fora do produto: selo escuro no canto inferior, depois do menu, com "Demo do protótipo: Conta nova | Com movimento". Só no desktop/tablet. Alterna o cenário de dados.

---

## 2. Telas

### Início
- **Conta nova:**
  - Métricas zeradas com texto explicativo.
  - Card "Ative sua conta" (3 de 5 etapas, barra de progresso). A etapa atual "Criar a primeira cobrança" fica destacada; "Configurar notas fiscais" tem botão.
  - Card tracejado "Sua primeira cobrança em 3 passos".
- **Com movimento:** grade de **widgets** de 12 colunas (`grid-auto-flow: row dense`).
  - Padrão:
    - Resumo financeiro (12): Saldo R$ 12.480,35 · A receber R$ 2.180,00 · Vencidas R$ 1.340,00 (variante de risco, em vermelho) · Recebido em outubro R$ 4.900,00.
    - Precisa da sua atenção (8): 3 itens com ação.
    - Recebido por forma (4): anéis de Cartão 71%, Pix 25% e Boleto 4%.
    - Próximos vencimentos (8): faixa de 7 dias e lista.
    - Convite de antecipação (4): card azul dispensável.
  - **Personalizar** (pelo menu da conta):
    - Uma faixa tracejada no topo com "Adicionar widget", "Restaurar padrão" e "Concluir".
    - Cada widget ganha uma barra com alça, título, largura (1/3, 1/2, 2/3, Inteira; o Resumo tem mínimo de 1/2), mover antes/depois e ocultar.
    - Arrastar e soltar com HTML5 DnD. O alvo do drop ganha contorno tracejado azul e o item arrastado fica com 40% de opacidade.
    - O layout é salvo em `localStorage` (`asaas-inicio-layout`).
  - **Biblioteca de widgets:** painel com cards e "Adicionar ao Início" ou "Já está no Início".
    - Mostra os 5 atuais e 4 novos (selo "Novo"): Atalhos rápidos, Últimos lançamentos, Quem mais pagou e Links de pagamento.
  - O conteúdo dos widgets se adapta à largura: o resumo tem 4 colunas em 12, 2 colunas em ≤ 8 e no tablet; os atalhos têm 4 ou 2 colunas.

### Cobranças
- Banner dispensável de antecipação automática (1,15% a.m. à vista, 1,6% a.m. parcelado), só na aba Todas.
- Abas: Todas, Avulsas, Parcelamentos, Assinaturas, Grupos, Chargeback.
- Busca, chips de status com contagem (Todas, Aguardando, Vencidas, Recebidas, Chargeback, Canceladas) e botão "Filtros (n)", que abre um drawer com forma de pagamento e vencimento.
- **Desktop:** tabela com Cliente, Forma, Vencimento, Valor, Status e ações. **Mobile:** cards.
- **Drawer de detalhe** (480 px, entra pela direita com `drawerIn`):
  - Status, valor, cliente e alerta de risco (vencida ou chargeback), dados e histórico em linha do tempo.
  - Ações por status:
    - vencida/aguardando: Cancelar, Alterar vencimento, Reenviar;
    - recebida: Estornar, Baixar comprovante;
    - chargeback: Ver regras, Enviar defesa;
    - cancelada: Duplicar.
- **Cancelar/Estornar:** modal `alertdialog` com valor, cliente e "Esta ação não pode ser desfeita". Botão vermelho "Sim, cancelar cobrança".
- **Estados vazios:** sem cobranças · filtro sem resultado (com "Limpar filtros") · "Nenhum grupo de cobrança".

### Criar cobrança
- Tipo: Avulsa | Parcelada (número de parcelas) | Assinatura (periodicidade).
- **1 Cliente:** busca (combobox) com sugestões e "Cadastrar “X” como novo cliente", que abre o cadastro inline (nome, CPF/CNPJ, e-mail).
- **2 Valor e vencimento:** R$ com vírgula; o vencimento padrão é 30/10/2026.
- **3 Forma:** Pix (R$ 1,99), Boleto (R$ 1,99), Cartão (2,99% + R$ 0,49) ou Cliente escolhe. Taxas ilustrativas.
- **4 Descrição** (opcional).
- **Resumo lateral** (sticky): calcula o valor líquido em tempo real, com "Você recebe (estimado)".
- **Validação ao enviar:**
  - cliente obrigatório;
  - CPF com 11 dígitos ou CNPJ com 14 (cliente novo);
  - valor ≥ R$ 5,00;
  - vencimento ≥ 23/10/2026.
  - Mostra um resumo de erros no topo e a mensagem em cada campo (`aria-invalid`). O erro some ao editar.
- **Confirmação:**
  - QR Code ilustrativo, valor e cliente, "Aguardando pagamento", dados, link `https://pagar.exemplo.com.br/c/XXXXXX` com Copiar (toast), Enviar por e-mail, Baixar PDF e andamento em 3 etapas.
  - "Ver cobrança" abre a lista com o drawer daquela cobrança. "Criar outra" volta ao formulário.
  - A cobrança criada entra na lista.

### Links de pagamento
- **Lista:** cards com nome, valor (ou "Valor livre"), formas e pagamentos, badge Ativo e Copiar link. O estado vazio explica para que serve.
- **"Criar link de pagamento" abre MODAL** (880 px; tela cheia no mobile; `modalIn`; fecha no X, em Fechar ou no fundo).
  - Stepper de 3 etapas: as bolinhas ficam azuis ao concluir e a linha de conexão anima.
  1. Informações: Valor pré-definido | Cliente define o valor, valor, nome (obrigatório), descrição, switch de notificações e imagens (até 5, com remover).
  2. Formas: Pix, Boleto e Cartão (ao menos uma). Cartão pede parcelamento máximo; boleto pede dias para vencer.
  3. Resumo + **prévia de como o cliente vê**.
  4. Sucesso: link ativo com Copiar, "Criar outro link" e "Ver meus links".
  - Cada etapa entra com `stepIn`.

### Pix
- Abas: Transferências, Minhas chaves, Meus limites, Pix recorrentes, Pix Automático, Contestações Pix.
- Cards: Transferir · Pix Copia e Cola · Limite disponível hoje (barra).
- Lista de transferências. O estado vazio orienta o primeiro passo.
- **Drawer de transferência:**
  - Escolha entre Chave e Copia e Cola, valor e validações: chave obrigatória, valor > 0, ≤ saldo e ≤ limite.
  - "Revisar transferência" abre o **modal de confirmação** com destinatário, chave, instituição e saldo após. O texto diz que o Pix "não pode ser cancelado".
  - Ao confirmar, mostra um toast e a transferência entra na lista.

### Meu dinheiro › Extrato
- Cards: Saldo atual (azul) · Cobranças aguardando pagamento R$ 3.520,00 · Aguardando repasse R$ 3.394,86.
- Período: Hoje | 7 dias | 15 dias | Personalizado. Lançamentos agrupados por dia, com "Saldo ao fim do dia".
- "Exportar" abre um menu com PDF, Excel (.xlsx), CSV, OFX e CNAB 240.
- **Vazio:** "Nenhuma movimentação neste período", sem "tente novamente", com "Ver últimos 15 dias" quando fizer sentido.

### Notas fiscais
- **Sem configuração:**
  - Onboarding em 4 passos, com barra e stepper: Dados da empresa · Serviço e impostos · Acesso à prefeitura · Revisão.
  - Botões Voltar, **"Pular e emitir depois"** e Continuar/Concluir.
- **Pulou:** aviso "Configuração fiscal pendente… Você parou no passo X de 4" com "Retomar configuração". O estado vazio fica abaixo. "Emitir nota" fica desabilitado.
- **Com movimento:** lista com Erro (Corrigir), Emitida (Baixar PDF) e Agendada. Aba Configurações.

### Demais itens do menu
Tela "Área fora das telas prioritárias: função mantida".

---

## 3. Assistente proativo (canto inferior direito)
- Launcher: pílula azul "Pergunte ao assistente". Depois de 6 s encolhe para só o ícone (largura e opacidade animadas). No hover, o rótulo volta.
- **Proativo:** cerca de 1,4 s depois de entrar numa tela, **o painel abre sozinho** (desktop/tablet) com a sugestão daquela tela como primeira mensagem e botões de ação.
  - No mobile ele não abre sozinho: o launcher pulsa.
  - Fechar o painel dispensa a sugestão daquela tela.
  - Ao usar uma ação, o painel continua aberto e o assistente responde em seguida.
- **Sugestões por tela:**
  - Início com movimento: reenviar as 3 vencidas.
  - Início conta nova: criar a primeira cobrança.
  - Cobranças: montar a defesa do chargeback.
  - Criar cobrança: aplicar Pix, vencimento de 7 dias e lembrete.
  - Confirmação: ativar lembrete.
  - Pix: pedir aumento de limite.
  - Extrato: simular antecipação.
  - Notas: preencher o passo 1, ou corrigir e reemitir a NF 000125.
  - Links: criar link.
- **Painel** (384×600; no mobile 100% × 72vh):
  - Cabeçalho azul, mensagens com animação, indicador "digitando" (3 pontos) e respostas em ~1 s.
  - 9 perguntas sugeridas, ordenadas pela tela atual.
  - Campo livre com correspondência por palavras-chave (`matchKey`) e respostas com botões que navegam (`ACT`).
- Tudo é simulação, sem API.

---

## 4. Movimento
| Elemento | Animação |
|---|---|
| Submenu | `subIn` 260 ms + itens em cascata |
| Menu recolher | largura 260 ms |
| Drawer | `drawerIn` 380 ms (translateX) + corpo em cascata |
| Modal | `modalIn` 300 ms (escala 0,96 → 1 + subida) |
| Popovers | `popIn` 220 ms (origem no canto superior direito) |
| Bottom sheet mobile | `sheetUp` 380 ms |
| Assistente | `agentIn` 280 ms; `pulse` no launcher |
| Etapas | `stepIn` 300 ms |
| Hover de botões | brilho 93% + translateY(-1px); cards `lift` -3 px com sombra |

Todas respeitam `prefers-reduced-motion`.

## 5. Acessibilidade
- Contraste AA nos dois temas. Alvos ≥ 44 px. Só elementos nativos (button, a, input, select, table, label).
- Foco: anel de 3 px `#006FF0` com offset de 2 px (`:focus-visible`).
- Botões só com ícone têm `aria-label`. Badges têm texto acessível. Popovers usam `aria-expanded` e `aria-controls`.
- Modais/drawers usam `role="dialog"` ou `alertdialog`, `aria-modal` e fecham no X e no fundo. Devolva o foco ao gatilho e feche no Esc.
- O status nunca depende só da cor (ponto + texto).

## 6. Jornadas para testar
1. Início (com movimento) → o assistente abre sozinho → "Reenviar as 3" → toast e resposta do assistente.
2. Início → "Criar cobrança" → enviar vazio (ver erros) → buscar "Café" → selecionar → valor 1.200,00 → Pix → Criar → Confirmação → Copiar link → Ver cobrança (drawer aberto).
3. Cobranças → chip "Vencidas" → abrir Ana Beatriz Lima → Cancelar cobrança → confirmar → status "Cancelada".
4. Links → Criar link → validar etapa 1 → preencher → formas → resumo com prévia → Criar → copiar.
5. Pix → Transferir → chave + 780,00 → Revisar → Confirmar → item na lista.
6. Extrato → Hoje / 7 / 15 dias → Exportar → OFX.
7. Notas (conta nova) → passos 1 a 4 → Pular → aviso → Retomar.
8. Conta → Personalizar início → arrastar widget, mudar largura, ocultar → Adicionar widget "Atalhos rápidos" → Concluir → recarregar (layout mantido).
9. Sino → abrir uma notificação → badge diminui.
10. Alternar tema; alternar "Conta nova"; repetir em 834 px e 390 px (menu bottom sheet).
