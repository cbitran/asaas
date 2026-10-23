// Prepara o texto para ser falado (valores, datas e abreviações por extenso).
// Usado pelo app (na hora de falar) e pelos scripts (na hora de gravar), para a chave do áudio ser a mesma.
const MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];

export function textoFalado(text) {
  return String(text)
    .replace(/R\$\s*([\d.]+)(?:,(\d{2}))?/g, (m, i, c) => {
      const n = i.replace(/\./g, '');
      if (n === '0' && c && c !== '00') return Number(c) + (Number(c) === 1 ? ' centavo' : ' centavos');
      return n + (n === '1' ? ' real' : ' reais') + (c && c !== '00' ? ' e ' + Number(c) + ' centavos' : '');
    })
    .replace(/\b(\d{1,2})\/(\d{1,2})\/(\d{4})\b/g, (m, d, mo, y) => Number(d) + ' de ' + (MESES[Number(mo) - 1] || mo) + ' de ' + y)
    .replace(/\b(\d{1,2})\/(\d{1,2})\b/g, (m, d, mo) => (Number(mo) >= 1 && Number(mo) <= 12 ? Number(d) + ' de ' + MESES[Number(mo) - 1] : m))
    .replace(/\bNF (\d+)/g, 'nota fiscal $1')
    .replace(/a\.m\./g, 'ao mês')
    .replace(/•/g, '')
    .replace(/›/g, ',')
    .replace(/\s·\s/g, ', ')
    .replace(/([.:;!?])[ \t]*\n+/g, '$1 ') // quebra depois de pontuação vira só um espaço
    .replace(/\n+/g, '. ')
    .replace(/\.{2,}/g, '.')
    .replace(/:\s*\./g, ':')
    .replace(/\s+/g, ' ')
    .trim();
}
