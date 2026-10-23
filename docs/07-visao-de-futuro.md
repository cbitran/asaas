# 7 · Visão de futuro

O que o Asaas oferece hoje, o que o mercado oferece e onde ainda há espaço. Tudo o que está na seção 3 em diante são **hipóteses para discutir**, cada uma ligada a uma evidência. Nada aqui é promessa de entrega nem decisão do Asaas. Consulta em 23/10/2026.

**Legenda das fontes:** *(observado)* = visto no painel original · *(aberta)* = página oficial lida por inteiro · *(resumo de busca)* = a página apareceu numa busca, mas não foi aberta; o dado **não está confirmado na página**.

## 1 · O que o Asaas oferece hoje

**No painel original** *(observado, menu e telas)*: cobranças avulsas, parceladas e por assinatura, grupos e chargeback; links de pagamento; vendas físicas; Pix (transferências, chaves, limites, recorrentes, Pix Automático e contestações); cartão; consulta Serasa e negativação; extrato, transferências e registro de recebíveis; pagamento de contas; antecipação (inclusive automática); notas fiscais de serviço; Open Finance; seguros; programa de indicação e benefícios. A tela de login anuncia o assistente **"Ian", a IA do Asaas, pelo WhatsApp**. A página inicial divulga o **Asaas Tap** (receber por aproximação no celular).

**Nas páginas e na documentação oficiais** *(resumo de busca, exceto onde indicado)*: conta digital PJ apresentada como gratuita, com cobrança por uso; API com Pix, boleto, cartão, TED, assinaturas, split, subcontas e webhooks; emissão de NFS-e imediata ou agendada para cobranças recorrentes; Pix Automático com reagendamento de tentativas. A documentação de cobranças lista os campos `customer`, `billingType`, `value` e `dueDate` *(aberta)*.

## 2 · O que o mercado oferece

Concorrentes escolhidos como em [Concorrentes](03-concorrentes.md): Mercado Pago, Stone e Efí Bank (apontados pelo Reclame Aqui) mais Cora, Inter Empresas e iugu.

**✔** consta em página oficial lida · **⚠** consta só em resumo de busca, ou as fontes se contradizem · **—** não consta nas páginas consultadas (**não prova que não exista**; vários recursos não foram pesquisados em todos).

| Capacidade | Asaas | Cora | Inter | Mercado Pago | Stone | Efí | iugu |
|---|---|---|---|---|---|---|---|
| Cobrança por boleto e Pix | ✔ | ✔ | ✔ | ⚠ | ⚠ | ⚠ | ⚠ |
| Link de pagamento | ✔ | ✔ | — | ⚠ | ⚠ | ⚠ | — |
| Cobrança recorrente ou assinatura | ✔ | ✔ | ⚠ | — | ⚠ | ⚠ | ⚠ |
| Pix Automático | ✔ item de menu | — | ⚠ | — | — | ⚠ | ⚠ (fontes divergem) |
| Nota fiscal de serviço integrada | ✔ | ✔ | — | — | — | — | — |
| Antecipação de recebíveis | ✔ | ⚠ citada, sem detalhe | — | ⚠ receber no mesmo dia, com custo | — | — | — |
| Maquininha ou celular como maquininha | ✔ Asaas Tap | — | ⚠ | ⚠ Point | ⚠ | — | — |
| API para integração | ✔ | ⚠ só um link de rodapé | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ |
| Split e subcontas | ⚠ | — | — | — | — | ⚠ split | ⚠ split |
| Régua de cobrança por vários canais | ✔ e-mail, SMS e voz | ✔ e-mail, SMS e WhatsApp | — | — | — | — | ⚠ e-mail e SMS |
| Fluxo de caixa ou gestão financeira | — não observado (conta vazia) | ✔ | — | ⚠ | ⚠ | — | — |
| Acesso para contador | — | ✔ | — | — | — | — | — |
| Crédito ou capital de giro | — | ⚠ citado | ⚠ | ⚠ | ⚠ | — | — |
| Cartão PJ | ✔ débito | ✔ crédito | ⚠ | ⚠ | — | ⚠ | — |
| Open Finance | ✔ item de menu | — | ⚠ (fontes divergem) | — | — | ⚠ | — |
| Assistente de IA | ✔ Ian, pelo WhatsApp | — | — | — | — | — | — |
| Atendimento humano 24 h | — | — | — | — | ⚠ | — | — |

**Como ler:** o Asaas aparece forte em **cobrança, notas fiscais, antecipação e API**, e é o único da lista em que vimos um assistente de IA anunciado. As colunas dos outros têm mais "—" porque cada um foi pesquisado só nos recursos de cobrança e gestão. Para decidir roadmap, é preciso uma pesquisa de recurso por recurso, com acesso às contas.

## 3 · O que ainda pode evoluir e o que podemos oferecer

Cada oportunidade tem a evidência, uma hipótese de valor e uma forma de validar. O **horizonte** (Agora, Próximo, Depois) é uma **proposta** de ordem, feita por evidência e risco de bloqueio da pessoa; não considera esforço de engenharia, que não avaliamos.

| # | Oportunidade | Evidência | Hipótese de valor | Como validar | Horizonte |
|---|---|---|---|---|---|
| 1 | **Recuperação de acesso** (login, senha, troca de número) | Reclame Aqui: "Login-Senha", 230 relatos; uma avaliação no Google Play cita perda de acesso após perder o número *(resumo de busca)* | Quem fica sem acesso fica sem receber. Um caminho claro, com alternativas, evita o bloqueio | Teste com 5 pessoas simulando perda de celular | Agora |
| 2 | **Transparência de valores em todas as ações financeiras** (Pix, antecipação, estorno), não só ao criar cobrança | Reclame Aqui: divergência de valores (41), estorno (539); a criação de cobrança do protótipo já mostra o valor líquido | Simular antes de confirmar reduz a surpresa. Efeito sobre reclamações **não medido** | Medir, no teste, se a pessoa acerta quanto vai receber | Agora |
| 3 | **Abertura de conta guiada, com status da análise** | Reclame Aqui: "Dificuldade de cadastro" (145); a landing só simula o cadastro | Mostrar em que etapa a análise está reduz a ansiedade e o abandono | Teste de abertura de conta de ponta a ponta | Próximo |
| 4 | **Cancelar ou mudar de plano com caminho claro** | Reclame Aqui: "Não consigo cancelar" (125) | Um caminho visível dentro de "Conta › Planos". Decisão de retenção é do negócio | Perguntar onde a pessoa procura o cancelamento | Próximo |
| 5 | **Previsão de caixa no Início** (entradas dos próximos dias e semanas) | Cora oferece fluxo de caixa com lançamentos futuros *(aberta)*; o Início do protótipo já mostra os próximos vencimentos | Quem cobra decide melhor sabendo o que entra | Entrevista: "o que você precisa saber ao abrir o painel?" | Próximo |
| 6 | **Régua de cobrança visual, com canais e status de entrega** | Cora envia por e-mail, SMS e WhatsApp *(aberta)*; o painel original menciona e-mail, SMS e voz *(observado)*; "Não recebi os boletos" (29). Uso de WhatsApp na régua do Asaas **não foi verificado** | Ver e editar a régua e saber se a mensagem chegou tira dúvida. Efeito sobre inadimplência **não medido** | Teste de tarefa: "reenvie e confira se o cliente recebeu" | Próximo |
| 7 | **Pix Automático com tela de autorizações** (quem autorizou, tentativas, falhas) | Inter, Efí e iugu oferecem por API *(resumo de busca)*; o Asaas tem o item de menu *(observado)*; o blog cita reagendamento de tentativas *(resumo de busca)* | Uma tela própria torna a recorrência compreensível. Seguir as regras do Banco Central | Revisar com o time de produto o que já existe | Próximo |
| 8 | **Assistente único (painel e WhatsApp), com ações confirmáveis** | O Asaas já tem o "Ian" no WhatsApp *(observado)*; o protótipo tem um assistente simulado, com ação proativa por tela e voz gravada | Mesma base e mesmas permissões nos dois canais. **Risco:** IA que age com dinheiro precisa de confirmação e trilha de auditoria | Teste de compreensão: a pessoa entende o que o assistente fará antes de confirmar | Depois |
| 9 | **Acesso para contador e equipe** | Cora tem acesso para contador *(aberta)*; multiusuário **não consta** na página da Cora; no Asaas **não verificamos** | Quem tem contador precisa compartilhar sem passar a senha | Entrevistar usuários que têm contador | Depois |
| 10 | **Exportação agendada para a contabilidade** | O Extrato original exporta em PDF, Excel, CSV, OFX e CNAB 240 *(observado)* | Enviar ao contador sem lembrar de exportar | Perguntar com que frequência exportam | Depois |
| 11 | **Rascunho de cobrança e link reutilizável** | iugu oferece rascunho *(resumo de busca)*; Mercado Pago oferece link fixo *(resumo de busca)* | Ideias de baixo risco para quem cobra com frequência | Perguntar se usariam | Depois |
| 12 | **Paridade entre app e web** | Relato na App Store de que a web funciona melhor que o app e de que o Asaas Tap não funciona no iPhone *(aberta, relatos isolados)* | Mesma experiência em qualquer tela | Comparar tarefas no app e na web | Depois |

## 4 · Riscos e limites

- **IA e dinheiro:** nenhuma ação irreversível sem confirmação explícita, com valor e destinatário repetidos. O protótipo já segue essa regra nas ações manuais.
- **Regras do Banco Central** (Pix, Pix Automático, Open Finance) definem o que é permitido e devem ser conferidas na norma, não nesta análise.
- **Cópia:** aprender com o mercado não é copiar. Marcas, textos e artes de concorrentes não entram no produto.
- **Dados e privacidade:** qualquer recurso novo com dados pessoais (por exemplo, acesso do contador) precisa de consentimento e registro de quem acessou.
- **Evidência frágil:** parte das fontes é resumo de busca ou marketing da própria empresa. Antes de decidir, confirme nas páginas e, melhor, com usuários.

## 5 · Perguntas abertas

1. Os recursos marcados "—" no Asaas (fluxo de caixa, acesso para contador, crédito) realmente não existem, ou não foram vistos numa conta vazia?
2. Qual parcela das reclamações de "cobrança indevida" vem de pagadores, e não de quem usa o painel?
3. Quais dessas oportunidades uma pessoa que cobra clientes pagaria para ter, e quais ela espera de graça?
