# Asaas · redesenho do painel (conceito)

> **Isto é uma simulação.** Landing, painel e páginas internas são um conceito de design. Todos os valores, nomes, datas, taxas, contatos e áudios são **fictícios**. Não é o site do Asaas e não tem relação oficial com a empresa. Não digite dados reais em nenhum formulário: nada é enviado nem salvo.

## Veja no ar

| O que | Endereço |
|---|---|
| Landing | https://cbitran.github.io/asaas/ |
| Painel (protótipo navegável) | https://cbitran.github.io/asaas/painel/ |
| Design system | https://cbitran.github.io/asaas/design-system/ |
| Defesa do estudo (slides) | https://cbitran.github.io/asaas/defesa/ |

O fluxo é um só: **landing → cadastro → painel → Conta › Sair → landing.** "Acessar minha conta" e o cadastro levam ao painel.

## Estudo de caso

Os documentos em [`docs/`](docs/README.md) mostram **como se chegou** ao redesenho: método e evidências, diagnóstico do painel original (heurísticas de Nielsen e leitura semiótica), comparação com concorrentes, voz do usuário, fluxogramas antes e depois, design system e visão de futuro. A apresentação em slides está em `/defesa/`.

## Rodar local

```bash
npm install
npm run dev     # landing em http://localhost:5173/ · painel em /painel/
npm run build   # gera dist/ (use BASE_PATH=/asaas/ para simular o GitHub Pages)
```

## O que tem aqui

- `index.html` e `painel/`: landing e painel (Vite + React + TypeScript). O painel renderiza `referencia/Main.dc.html`, o protótipo aprovado, com um interpretador próprio (`src/dc/`).
- `tokens/`: `tokens.css` (variáveis claro e escuro) e `tokens.json`. Fonte única das cores, tipografia e espaçamento.
- `docs/`, `defesa/`, `design-system/`: estudo de caso, apresentação e página do design system (gerada por `scripts/gerar-design-system.mjs`).
- `CLAUDE.md` e `HANDOFF.md`: especificação original do protótipo (telas, estados, fluxos, acessibilidade).
- `public/voz/`: 29 áudios gravados do assistente, com índice. O app toca esses arquivos e **não chama nenhum serviço de voz**.
- `scripts/`: geradores (`gerar-paginas.py`, `gerar-design-system.mjs`) e ferramentas de áudio (`coletar-frases.mjs`, `gerar-voz.mjs`, só para quem for gravar novas frases).

## Páginas internas (soluções, preços, sobre nós, blog, carreiras, 2ª via, criar conta)

- Geradas por `python3 scripts/gerar-paginas.py` a partir de `referencia/solucoes-original.json`.
- `estilos/site.css` é gerado do `<style>` da landing mais os estilos internos; `estilos/site.js` tem o comportamento compartilhado. Depois de mudar a landing ou o gerador, rode o script de novo.
- O gerador troca contatos e domínios reais do Asaas por equivalentes fictícios (`exemplo.com.br`, `0800 000 0000`) antes de gerar as páginas.

## Voz do assistente

O painel tem um assistente com ações propostas por tela. A fala usa áudios já gravados (`public/voz/`), tocados só no painel. Para gravar uma frase nova é preciso uma chave de TTS própria (veja `.env.example`); o app em si não precisa de chave.

## Publicação

O GitHub Pages publica sozinho a cada push na `main`, pelo workflow `.github/workflows/pages.yml` (`BASE_PATH` é o nome do repositório). O passo a passo e as conferências estão em [`HANDOFF-PUBLICAR.md`](HANDOFF-PUBLICAR.md). Não use `publicar.sh`: ele cria um repositório novo e fica só como legado.

## Avisos

- **Conteúdo de exemplo.** Os textos das páginas internas foram adaptados de páginas públicas do Asaas, apenas para um estudo de design. Preços, taxas e condições exibidos **não** são informação oficial.
- **Sem indexação.** As páginas que imitam o site (landing, internas e painel) usam `noindex`.
- **Áudio.** As vozes foram geradas com um serviço de síntese de voz; confira os termos do seu plano antes de redistribuir.
- **Origem das imagens.** A origem e a licença das imagens em `public/img/` **não foram verificadas**. Confirme antes de qualquer uso além deste estudo.
