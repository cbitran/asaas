# 1 · Método e evidências

Data das consultas: **23/10/2026**. Tudo o que está nos demais documentos tem origem em uma das categorias abaixo.

## Classificação das evidências

| Categoria | Significado | Onde aparece |
|---|---|---|
| **Observado** | Visto diretamente no painel original, em modo leitura (nada foi criado, enviado ou movimentado) | [Diagnóstico](02-diagnostico-original.md) |
| **Fonte aberta e lida** | Página oficial aberta e lida na íntegra nesta consulta | [Concorrentes](03-concorrentes.md), [Voz do usuário](04-voz-do-usuario.md) |
| **Resumo de busca** | A página oficial apareceu numa busca, mas não pôde ser aberta (erro 403). O dado vem do resumo e **não foi confirmado na página** | Marcado como "(resumo de busca)" |
| **Calculado** | Número obtido por cálculo reproduzível neste repositório | [Design system](06-design-system.md) |
| **Interpretação** | Leitura analítica da equipe, apresentada como tal | Marcado como "leitura" |

## Etapas

1. **Observação direta do painel original.** Telas vistas: Início, Cobranças, Clientes, Pix (Transferências), Meu Dinheiro (Extrato), Antecipações e Notas Fiscais, mais a barra lateral expandida. A sessão expirou antes de abrirmos o formulário de criação de cobrança; por isso o fluxo "antes" dessa tarefa vem da Central de Ajuda do Asaas, e não de observação.
2. **Diagnóstico** pelas 10 heurísticas de usabilidade de Jakob Nielsen e por uma leitura semiótica (ver fontes teóricas abaixo).
3. **Comparação com concorrentes** pelos fluxos oficiais de ajuda de Cora, Inter Empresas, iugu e Mercado Pago.
4. **Voz do usuário** em fontes públicas: Reclame Aqui, App Store e Google Play.
5. **Princípios e decisões**, registrados nos documentos 2 e 5.
6. **Protótipo** navegável (landing e painel) e **design system** com tokens.
7. **Apoio de modelo de julgamento (Jev).** Avaliou a análise (completude entre "parcial" e "boa", 1,67 de 3) e apontou a navegação longa como o maior risco de usabilidade. É um apoio, **não uma decisão**: parte das respostas veio com confiança baixa e foi revista pela equipe.

## Fontes teóricas (conferidas na fonte)

| Tema | Fonte | O que usamos |
|---|---|---|
| Heurísticas | J. Nielsen, "10 Usability Heuristics for User Interface Design", Nielsen Norman Group, publicado em 24/04/1994, revisado em 30/01/2024. <https://www.nngroup.com/articles/ten-usability-heuristics/> | As 10 heurísticas como critério de diagnóstico |
| Semiótica | A. Atkin, "Peirce's Theory of Signs", Stanford Encyclopedia of Philosophy, publicado em 13/10/2006, revisão substantiva em 04/08/2022. <https://plato.stanford.edu/entries/peirce-semiotics/> | Distinção entre ícone, índice e símbolo |
| Contraste | W3C, WCAG 2.2, critério 1.4.3 (nível AA): 4,5:1 para texto normal e 3:1 para texto grande. <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html> | Meta de contraste de texto |
| Alvo de toque | W3C, WCAG 2.2, critério 2.5.5 (nível **AAA**): alvos de 44 por 44 pixels CSS. <https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html> | Tamanho mínimo dos controles |

## Limites conhecidos

- **O protótipo é uma simulação.** Valores em reais, nomes de clientes, datas, taxas, contagens e estatísticas da landing e do painel são inventados para o desenho. Nenhuma análise deste estudo trata esses números como reais; eles só ilustram como a interface se comporta.
- **Sem teste com usuários.** Nenhum ganho de tempo ou de taxa de acerto foi medido. Onde dizemos "menos etapas", é contagem de etapas, não de segundos.
- **Conta vazia.** O original foi visto sem dados. Não sabemos como suas listas, filtros e detalhes se comportam com movimento.
- **Concorrentes por documentação.** Não usamos as contas internas deles. A comparação trata do fluxo **descrito na ajuda oficial**, não da qualidade geral do produto.
- **Fontes bloqueadas.** Três páginas de ajuda (Asaas, iugu e Mercado Pago) responderam 403 à leitura direta. Esses pontos estão marcados.
- **Reclamações** são relatos de pessoas, com taxonomia escolhida por quem registra. Não provam defeito, e várias não têm relação com a interface (ver [Voz do usuário](04-voz-do-usuario.md)).
- **Telas com dados do redesenho** foram desenhadas sem validação em conta real; valores são fictícios.

## Validação que falta

Roteiro mínimo para testar o redesenho contra o original, com 5 a 8 pessoas do público (empreendedores que cobram clientes):

1. **Tarefa 1:** criar a primeira cobrança de R$ 1.200,00 para um cliente novo, por Pix.
2. **Tarefa 2:** descobrir quantas cobranças estão vencidas e reenviar uma.
3. **Tarefa 3:** cancelar uma cobrança.
4. **Tarefa 4:** transferir R$ 780,00 por Pix.

**Medir:** conclusão sem ajuda (sim/não), tempo até concluir, número de erros e de voltas ao menu, e uma pergunta de facilidade percebida (escala de 1 a 7) ao fim de cada tarefa. Comparar duas versões com o mesmo roteiro.
