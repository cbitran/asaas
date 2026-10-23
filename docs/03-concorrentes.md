# 3 · Comparação com concorrentes

**Escopo.** Comparamos o **fluxo de criar uma cobrança**, como as páginas oficiais de ajuda o descrevem. Não usamos as contas internas dos concorrentes. Isto não avalia a qualidade geral de nenhum produto.

**Como escolhemos os concorrentes.** Pelo próprio Reclame Aqui, que na página do Asaas lista "pessoas que acessaram Asaas também acessaram": Mercado Pago, Stone e Efí Bank. Somamos Cora, Inter Empresas e iugu, que cobrem conta PJ com cobrança e cobrança recorrente. Consulta em 23/10/2026.

**Legenda das fontes:** *(aberta)* = página oficial lida por inteiro · *(resumo de busca)* = a página apareceu numa busca, mas não abriu (erro 403); o dado **não foi confirmado na página**.

## Criar uma cobrança, lado a lado

| | Asaas (original) | Cora | Inter Empresas | iugu | Mercado Pago |
|---|---|---|---|---|---|
| **Fonte** | Central de Ajuda *(resumo de busca)* e observação direta | Central de Ajuda *(aberta)* | Central de Ajuda *(aberta)* | Suporte iugu *(resumo de busca)* | Blog oficial *(resumo de busca)*; não há página de ajuda oficial confirmada |
| **Como começa** | Botão "Criar Cobrança", no topo da página inicial | Menu superior "Cobrar" (app) | Internet Banking: "Cobrar ou Receber" › "Nova cobrança" › "Gestão de cobrança" | Painel: Recebimento › Faturas › Nova | App: "Cobrar"; web: "Ferramentas para vender" › "Link de pagamento" |
| **Estrutura** | 4 etapas em sequência: Dados da cobrança, Juros e multa (opcional), Dados do cliente, Resumo; botões Voltar e Finalizar | **14 passos** no fluxo com QR Code Pix e **15** no boleto tradicional | 5 passos de caminho; os campos não são detalhados na página | Itens com descrição, quantidade e preço; opção de rascunho | Título, valor, foto e descrição; parcelamento e expiração |
| **Cliente** | Escolhido ou cadastrado na **3ª** etapa | Contato novo ou salvo logo no início, mais nome, tipo de pessoa e documento | Selecionar pagadores ou cadastrar | **Cadastrado antes**, em outra área (Cadastro › Cliente › Novo) | Link sem cliente cadastrado |
| **Pix na cobrança** | Opção "Boleto/Pix"; o Pix aparece no link da fatura | Boleto com QR Code Pix num fluxo único | Boleto sai com QR Code Pix se a conta tem chave Pix | Boleto, cartão ou Pix, restringível a um só | Link com Pix e cartão |
| **Campos obrigatórios** | Não detalhados na fonte | **8**: contato, à vista ou parcelada, nome, tipo de pessoa, documento, valor, vencimento e nome da cobrança | Não detalhados; valor de R$ 2,50 a R$ 1.000.000,00 | CPF/CNPJ e endereço para boleto registrado | Não detalhados |
| **Observação** | Resumo antes de finalizar | Descrição só do fluxo no **app** | Recorrente exige habilitar a função antes *(resumo de busca)* | Orientada a faturas e a API | Opções avançadas só na web *(resumo de busca)* |

## O que cada um faz bem e onde há limite (no fluxo documentado)

| | Faz bem | Limite documentado |
|---|---|---|
| **Asaas (original)** | Pix no link da fatura; cadastro de cliente na própria cobrança; tela de resumo e botão Voltar antes de finalizar | O fluxo é dividido em 4 etapas, com "Juros e multa" como etapa própria; o botão de criar aparece em mais de um lugar e em cores diferentes |
| **Cora** | Boleto com QR Code Pix num único fluxo; emissão gratuita, segundo a própria Cora; régua de cobrança por e-mail, SMS e WhatsApp | 14 a 15 passos; 8 campos obrigatórios, entre eles tipo de pessoa e nome da cobrança; o artigo de ajuda descreve só o app |
| **Inter Empresas** | Caminho curto; QR Code Pix automático quando há chave Pix; limites de valor explícitos | Dois rótulos em sequência para o mesmo caminho ("Nova cobrança" e depois "Gestão de cobrança"); a página não detalha os campos |
| **iugu** | Itens detalhados na fatura; rascunho; escolha dos meios de pagamento | Exige cadastrar o cliente antes, em outra área *(resumo de busca)* |
| **Mercado Pago** | Link de pagamento rápido, com parcelamento e prazo de validade; link fixo reutilizável ("Seu link") | Fontes são blog, não ajuda; os passos não foram confirmados em página oficial |

## O que o redesenho resolve

| Limite encontrado | Como resolvemos | Quem demonstra o problema |
|---|---|---|
| Etapas demais antes de ver o resultado | **Um formulário** com os quatro blocos visíveis ao mesmo tempo | Asaas original (4 etapas), Cora (14 a 15 passos) |
| Cliente fora do fluxo ou só no fim | **Cliente primeiro**, com busca e cadastro no próprio campo | iugu (cadastro prévio), Asaas original (3ª etapa) |
| Muitos campos obrigatórios | **3 campos obrigatórios** (cliente, valor, vencimento); forma de pagamento já vem em Pix; descrição opcional. Se o cliente é novo, pede também CPF ou CNPJ | Cora (8 campos) |
| Não saber o que vai receber | **Valor líquido** em tempo real no resumo | Nenhuma das páginas consultadas menciona o valor líquido na etapa de revisão (isso não prova que o produto não mostre) |
| Depois de criar, o que fazer? | **Tela de confirmação** com link, QR Code, copiar, e-mail e PDF, e andamento em três etapas | As páginas descrevem o fim como "concluir" ou "finalizar" e, no caso da Cora, "compartilhar"; não detalham o que vem depois |
| Botão principal duplicado e inconsistente | **Um botão principal por tela** | Asaas original |

## O que aprendemos com cada um

- **Cora:** boleto e Pix num fluxo só. No redesenho, o **Pix é a forma padrão** do formulário.
- **Inter:** limites de valor explícitos. No redesenho, o valor mínimo (R$ 5,00, fictício) aparece na mensagem de erro do campo.
- **iugu:** rascunho de cobrança. **Não adotamos** nesta versão; fica como ideia para o futuro ([visão de futuro](07-visao-de-futuro.md)).
- **Mercado Pago:** link fixo reutilizável. O redesenho já tem Links de pagamento; o link reutilizável é uma ideia para o futuro.

## Limites desta comparação

- Contagem de "passos" **não é comparável diretamente**: a Cora conta cada campo como um passo, enquanto o Asaas descreve seções. Por isso comparamos também campos obrigatórios e posição do cliente.
- Duas das cinco fontes do fluxo são resumos de busca. Antes de usar estes números em decisão, confira as páginas.
- Preços e tarifas citados pelas fontes mudam; não os usamos como argumento de design.

## Fontes

- Asaas, Central de Ajuda: <https://central.ajuda.asaas.com/hc/pt-br/articles/31408702720283-Como-criar-uma-cobran%C3%A7a> *(resumo de busca; leitura direta bloqueada)*; blog oficial: <https://blog.asaas.com/asaas-boleto/> *(aberta)*
- Cora: <https://www.cora.com.br/ajuda/artigo/como-faco-para-emitir-um-boleto-de-cobranca/> *(aberta)*
- Inter: <https://ajuda.inter.co/conta-digital-pessoa-juridica/como-emitir-um-boleto-de-cobranca-na-minha-conta-pj> *(aberta)*
- iugu: <https://support.iugu.com/hc/pt-br/articles/360056468051-Como-emitir-uma-fatura> *(resumo de busca)*
- Mercado Pago: <https://www.mercadopago.com.br/blog/criar-compartilhar-link-pagamento-mercado-pago> *(resumo de busca)*
- Reclame Aqui, lista "também acessaram": <https://www.reclameaqui.com.br/empresa/asaas-gestao-financeira/> *(aberta)*
