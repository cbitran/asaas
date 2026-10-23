# 5 · Jornadas: antes e depois

Os fluxogramas abaixo usam Mermaid e aparecem desenhados no GitHub. O **"antes"** vem do que foi observado no painel original ou do que a Central de Ajuda do Asaas descreve (marcado em cada caso). O **"depois"** é o protótipo desta pasta.

## 1 · Navegação

**Antes (observado):** 17 itens no primeiro nível, sem agrupamento.

```mermaid
flowchart LR
  M["Menu lateral"] --> A["17 itens soltos<br/>Início · Meus Clientes · Cobranças (8 subitens)<br/>Vendas físicas · Pix (6 subitens) · Links de Pagamento<br/>Cartão Asaas · Consulta Serasa · Meu Dinheiro (3 subitens)<br/>Pague Contas · Antecipações (3 subitens) · Notas Fiscais (2 subitens)<br/>Open Finance · Negativação · Seguros<br/>Indicar Amigo · Meus benefícios"]
```

**Depois:** os mesmos recursos, organizados pela tarefa de quem usa. Os dois itens que estavam dentro de Cobranças e não eram cobranças (Simulador de vendas e Personalizar notificações) foram para Ferramentas.

```mermaid
flowchart LR
  M["Menu lateral"] --> D0["Início"]
  M --> G1["Recebimentos<br/>Cobranças (6 subitens)<br/>Links de pagamento<br/>Vendas físicas"]
  M --> G2["Clientes<br/>Clientes<br/>Consulta Serasa<br/>Negativação"]
  M --> G3["Dinheiro<br/>Meu dinheiro · Pix<br/>Pague contas · Cartão Asaas<br/>Antecipações"]
  M --> G4["Fiscal<br/>Notas fiscais"]
  M --> G5["Ferramentas<br/>Simulador de vendas · Open Finance<br/>Seguros · Personalizar notificações"]
  M --> G6["Mais<br/>Indicar amigo<br/>Meus benefícios"]
```

## 2 · Criar a primeira cobrança

**Antes** (Central de Ajuda do Asaas, resumo de busca; o botão "Criar cobrança" aparece em mais de um lugar, observado):

```mermaid
flowchart TD
  I["Início<br/>botão azul no menu<br/>e botão verde no cartão da conta"] --> C["Criar cobrança"]
  C --> E1["Etapa 1 · Dados da cobrança<br/>valor, descrição, formas de pagamento,<br/>antecipação, anexos"]
  E1 --> E2["Etapa 2 · Juros e multa<br/>opcional"]
  E2 --> E3["Etapa 3 · Dados do cliente<br/>forma de envio e cliente"]
  E3 --> E4["Etapa 4 · Resumo"]
  E4 -->|Voltar| E1
  E4 --> F["Finalizar"]
  F --> P["Página da cobrança"]
```

**Depois** (protótipo):

```mermaid
flowchart TD
  I["Início<br/>um botão principal: Criar cobrança"] --> F["Criar cobrança · uma tela<br/>1 Cliente · 2 Valor e vencimento<br/>3 Forma de pagamento · 4 Descrição<br/>resumo com valor líquido ao lado"]
  F -->|dados inválidos| ERR["Erro no campo<br/>e resumo de erros no topo"]
  ERR --> F
  F -->|dados válidos| CF["Confirmação<br/>link, QR Code, copiar, e-mail e PDF<br/>andamento em 3 etapas"]
  CF --> V["Ver cobrança<br/>detalhe em painel lateral"]
  CF --> O["Criar outra cobrança"]
  O --> F
```

| | Antes | Depois |
|---|---|---|
| Telas ou etapas até criar | Início + 4 etapas + página da cobrança | Início + 1 formulário + confirmação |
| Posição do cliente | 3ª etapa | 1º bloco, com busca e cadastro no campo |
| Campos obrigatórios | Não detalhados na fonte | 3 (cliente, valor e vencimento); +1 (CPF ou CNPJ) se o cliente é novo |
| Valor que a pessoa recebe | Não mencionado na fonte | Visível em tempo real no resumo |
| Botão principal | Mais de um, em cores diferentes | Um por tela |

*Contagem de etapas e telas. Não medimos tempo nem erros; isso depende do [teste com usuários](01-metodo-e-evidencias.md#validação-que-falta).*

## 3 · Ação irreversível (cancelar, estornar, enviar Pix)

O original não foi testado nesse ponto. No redesenho, o fluxo é este, por decisão de projeto (H3 e H5):

```mermaid
flowchart TD
  L["Lista de cobranças"] --> D["Detalhe da cobrança<br/>painel lateral"]
  D --> A["Ação: Cancelar ou Estornar"]
  A --> M["Confirmação em modal<br/>valor, cliente e forma<br/>'Esta ação não pode ser desfeita'<br/>foco inicial em Voltar"]
  M -->|Voltar ou Esc| D
  M -->|Sim, confirmar| R["Status atualizado<br/>e aviso na tela"]
```

## 4 · Notas fiscais

**Antes (observado):** bloco de cinco linhas e um botão. **Depois:** passos curtos, com saída.

```mermaid
flowchart TD
  subgraph ANTES["ANTES"]
    N0["Notas fiscais<br/>texto explicativo de 5 linhas"] --> N1["Iniciar a configuração"]
  end
  subgraph DEPOIS["DEPOIS"]
    P1["Passo 1 · Dados da empresa"] --> P2["Passo 2 · Serviço e impostos"]
    P2 --> P3["Passo 3 · Acesso à prefeitura"]
    P3 --> P4["Passo 4 · Revisão"]
    P4 --> OK["Configuração concluída<br/>Emitir nota liberado"]
    P1 -->|Pular e emitir depois| SK["Aviso: configuração pendente<br/>Retomar configuração"]
    P2 -->|Pular e emitir depois| SK
    P3 -->|Pular e emitir depois| SK
    SK --> P1
  end
```

## 5 · Estado vazio do Extrato

```mermaid
flowchart LR
  subgraph ANTES["ANTES (observado)"]
    V1["Sem transações no período"] --> V2["'Nenhuma transação encontrada.<br/>Por favor, tente novamente.'"]
    V2 --> V3["Parece erro; não há o que tentar de novo"]
  end
  subgraph DEPOIS["DEPOIS"]
    W1["Sem movimentação no período"] --> W2["'Nenhuma movimentação neste período'"]
    W2 --> W3["Atalho: Ver últimos 15 dias"]
  end
```

## 6 · Primeira tela, por prioridade

```mermaid
flowchart LR
  subgraph ANTES["ANTES (observado)"]
    B1["Saudação com número de documento"] --> B2["Carrossel de promoções"]
    B2 --> B3["Cartão 'Sua conta foi aprovada'<br/>5 de 5 etapas concluídas"]
    B3 --> B4["Situação das cobranças"]
  end
  subgraph DEPOIS["DEPOIS"]
    A1["Saudação pelo nome"] --> A2["Resumo: saldo, a receber,<br/>vencidas, recebido no mês"]
    A2 --> A3["Precisa da sua atenção<br/>com ação em cada item"]
    A3 --> A4["Próximos vencimentos"]
    A4 --> A5["Convite dispensável"]
  end
```
