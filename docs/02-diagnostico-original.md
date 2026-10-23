# 2 · Diagnóstico do painel original

Cada linha liga **o que foi observado** a **um critério** e a **uma decisão de redesenho**. Observações feitas em 23/10/2026, em modo leitura, numa conta recém-aberta e sem movimentação. A numeração das heurísticas (H1 a H10) segue a lista de Jakob Nielsen (Nielsen Norman Group), resumida ao final.

## Achados e decisões

| # | Observado no original | Critério | Decisão no redesenho | Onde ver no protótipo |
|---|---|---|---|---|
| 1 | **17 itens no primeiro nível** do menu, sem agrupamento. O submenu de Cobranças tem 8 itens, e dois deles (Simulador de vendas e Personalizar notificações) não são cobranças | H6 reconhecer em vez de lembrar, H4 consistência | Menu em grupos por tarefa (Recebimentos, Clientes, Dinheiro, Fiscal, Ferramentas) e rodapé "Mais". Os dois itens foram para Ferramentas; Cobranças ficou com 6 subitens. **Nenhuma função foi removida** | Menu lateral |
| 2 | **Botão "Criar cobrança" repetido na mesma tela**, em cores diferentes: azul no menu e verde no cartão de conta aprovada. Aparece também no estado vazio de Cobranças | H4 consistência e padrões | Um botão principal por tela, no cabeçalho da página, sempre no mesmo estilo, e que muda conforme o contexto (Criar cobrança, Transferir via Pix etc.) | Cabeçalho de cada tela |
| 3 | **Início abre com promoção e checklist já concluído**: carrossel de ofertas (cartão) no topo e um cartão "Sua conta foi aprovada" com todas as 5 etapas marcadas, antes de qualquer pendência | H8 design minimalista, H1 visibilidade do status | Início por prioridade: o que precisa de atenção, saldo, vencimentos. O checklist só aparece enquanto há etapa pendente. O convite de antecipação é um cartão dispensável | Início |
| 4 | **Número de documento antes do nome** na saudação ("Olá, [número] [nome]") | H2 linguagem do usuário | Saudação humana: "Olá, Paulo!" | Início |
| 5 | **Indicadores vermelhos em vários itens do menu** (Cobranças, Pix, Pague Contas, Antecipações, Seguros, Meus benefícios) sem dizer o motivo | H1 visibilidade do status, H6 | Indicador só onde há pendência real, com texto acessível ("3 cobranças vencidas"). O card "Precisa da sua atenção" explica cada pendência e leva à lista já filtrada | Menu e Início |
| 6 | **Estado vazio com tom de erro** no Extrato: "Nenhuma transação encontrada. Por favor, tente novamente." Não houve falha; apenas não há movimento | H9 reconhecer e se recuperar de erros, H1 | "Nenhuma movimentação neste período", sem pedir nova tentativa, com o atalho "Ver últimos 15 dias" quando faz sentido | Meu dinheiro, Extrato |
| 7 | **Faixa promocional repetida em telas de trabalho**: antecipação automática em Cobranças > Todas, cartão no Início | H8 | Promoção como cartão dispensável e contextual, que não ocupa o lugar da tarefa | Cobranças, Início |
| 8 | **Notas fiscais** abre com um texto de cinco linhas antes do botão "Iniciar a configuração" | H8, H10 ajuda e documentação | Configuração em 4 passos com barra de progresso e a opção "Pular e emitir depois" | Notas fiscais |
| 9 | **Janelas sobre o conteúdo**: pesquisa de satisfação ("O quão fácil foi criar sua conta?") e balão de chat flutuante | H8 | Um único assistente, em lugar fixo e dispensável. *Troca consciente:* ele abre sozinho ao entrar e pode cobrir parte do conteúdo no desktop; foi mantido por decisão do produto | Canto inferior direito |
| 10 | **Pix > Transferências** com estado vazio que explica o benefício ("Transfira e pague mais rápido") mas não indica o primeiro passo | H10, H6 | Estado vazio que orienta a primeira ação; ação que move dinheiro exige confirmação | Pix |
| 11 | **Criar cobrança em 4 etapas em sequência** (Dados da cobrança, Juros e multa, Dados do cliente, Resumo), com o cliente na terceira etapa. *Fonte: Central de Ajuda do Asaas (resumo de busca; página não aberta).* | H7 eficiência, H1, H5 prevenção de erros | Um formulário único: cliente primeiro (busca ou cadastro no próprio campo), valor e vencimento, forma de pagamento, descrição. Resumo ao lado com **valor líquido** em tempo real. Erros no campo e resumo de erros no topo | Criar cobrança |

## Ações irreversíveis (decisão de projeto)

O original não foi testado nesse ponto (não movimentamos dinheiro nem cancelamos nada). No redesenho, **cancelar, estornar e enviar Pix** passam por uma confirmação que repete o valor e o destinatário, diz que a ação não pode ser desfeita, começa com o foco em "Voltar" e fecha com Esc. Critérios: H3 controle e liberdade, H5 prevenção de erros.

## O que o original já fazia bem

- Estados vazios ilustrados, com texto que explica a tela e um botão claro.
- "Criar cobrança" como rótulo direto, sem jargão.
- Assistente de IA pelo WhatsApp ("Ian"), anunciado na tela de login.
- Pix disponível no link da fatura, segundo o blog do Asaas.

Mantivemos esses pontos. O redesenho **organiza e prioriza**; não substitui o que funcionava.

## Leitura semiótica (Peirce)

Referência: a entrada "Peirce's Theory of Signs" (Stanford Encyclopedia of Philosophy) distingue o **ícone**, que significa por semelhança; o **índice**, que significa por conexão real com o que indica (a fumaça indica fogo); e o **símbolo**, que significa por convenção. Esta é uma **leitura analítica da equipe**, não um dado medido.

| Tipo de signo | Exemplo no produto | Problema no original | Escolha no redesenho |
|---|---|---|---|
| Índice | Número em círculo vermelho no menu: indica que **existe** algo pendente | Indica a existência, mas não o objeto ("o quê?") | O índice vem acompanhado do texto que o nomeia ("3 cobranças vencidas") e leva ao item |
| Símbolo | Vermelho = alerta, verde = sucesso (convenção cultural) | Cor sozinha pode ser lida de formas diferentes e não funciona para quem não distingue cores | Status sempre com **ponto + texto + cor**. A cor reforça, não carrega sozinha o significado |
| Ícone | Documento para nota fiscal, relógio para "a receber", carteira para saldo | Sem rótulo, o ícone isolado pode ser ambíguo | No menu recolhido, cada ícone mantém `title` e `aria-label` com o nome |
| Símbolo | Botão escuro de destaque = ação principal | Na tela original, o mesmo comando aparece em azul e em verde, o que enfraquece a convenção | Uma única cor e um único lugar para a ação principal |

## As 10 heurísticas de Nielsen (resumo)

H1 visibilidade do status do sistema · H2 correspondência entre o sistema e o mundo real · H3 controle e liberdade do usuário · H4 consistência e padrões · H5 prevenção de erros · H6 reconhecer em vez de lembrar · H7 flexibilidade e eficiência de uso · H8 design estético e minimalista · H9 ajudar a reconhecer, diagnosticar e corrigir erros · H10 ajuda e documentação.

Fonte: Nielsen Norman Group, <https://www.nngroup.com/articles/ten-usability-heuristics/> (publicado em 24/04/1994, revisado em 30/01/2024). Nomes traduzidos e definições resumidas por nós.

## Cobertura das heurísticas no redesenho

| Heurística | Como foi atendida | Evidência |
|---|---|---|
| H1 | Saldo, pendências e status sempre visíveis; toast confirma ações; progresso nos passos fiscais | Início, toasts, Notas |
| H2 | Linguagem do dia a dia ("Você recebe (estimado)", "Precisa da sua atenção") | Textos do protótipo |
| H3 | "Voltar", "Agora não", fechar com Esc, "Pular e emitir depois" | Modais, drawers, Notas |
| H4 | Tokens únicos, um botão principal por tela, componentes reutilizados | [Design system](06-design-system.md) |
| H5 | Confirmação em ação irreversível, validação antes de enviar, valor líquido visível | Criar cobrança, Pix |
| H6 | Menu agrupado, chips e filtros visíveis, cliente com busca e sugestões | Menu, Cobranças |
| H7 | Busca global (⌘K), Início personalizável, assistente com atalhos | Topo, Início |
| H8 | Início por prioridade, promoções dispensáveis, estados vazios curtos | Início |
| H9 | Erro no campo, resumo de erros no topo, mensagem diz o que corrigir | Criar cobrança |
| H10 | Assistente contextual por tela e textos de ajuda no ponto de uso | Assistente |

*Limite:* "atendida" significa **desenhada e implementada no protótipo**. Que isso melhore a tarefa para quem usa depende do teste com usuários.
