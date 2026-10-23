#!/usr/bin/env bash
# Publica a landing + o painel no GitHub Pages.
# Uso: ./publicar.sh [nome-do-repositorio]   (padrão: asaas-redesenho)
set -euo pipefail
cd "$(dirname "$0")"
REPO="${1:-asaas-redesenho}"

if ! command -v gh >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then brew install gh; else echo "Instale o GitHub CLI: https://cli.github.com"; exit 1; fi
fi
gh auth status >/dev/null 2>&1 || gh auth login --hostname github.com --web --git-protocol https
gh auth setup-git >/dev/null 2>&1 || true

OWNER="$(gh api user --jq .login)"

[ -d .git ] || git init -b main >/dev/null
git add -A
git commit -q -m "Asaas: landing page + painel (conceito de redesenho)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || true
git branch -M main

if ! git remote | grep -qx origin; then
  gh repo view "$OWNER/$REPO" >/dev/null 2>&1 || gh repo create "$REPO" --public --description "Conceito de redesenho do Asaas: landing page e painel"
  git remote add origin "https://github.com/$OWNER/$REPO.git"
fi

# Ativa o GitHub Pages publicando via GitHub Actions (antes do push, para o workflow já encontrar o Pages ligado)
gh api -X POST "repos/$OWNER/$REPO/pages" -f build_type=workflow >/dev/null 2>&1 \
  || gh api -X PUT "repos/$OWNER/$REPO/pages" -f build_type=workflow >/dev/null 2>&1 || true

git push -u origin main

echo
echo "Enviado. O deploy leva ~1 minuto: https://github.com/$OWNER/$REPO/actions"
echo "Site:   https://$OWNER.github.io/$REPO/"
echo "Painel: https://$OWNER.github.io/$REPO/painel/"
