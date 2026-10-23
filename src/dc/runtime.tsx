import React, { useEffect, useReducer, useRef } from 'react';

/**
 * Interpretador do formato `.dc.html` do canvas de design.
 * Lê a marcação ({{holes}}, <sc-if>, <sc-for>) e a classe Component (renderVals + estado)
 * do arquivo de referência e renderiza em React, sem reescrever as telas.
 */

export class DCLogic {
  props: Record<string, any> = {};
  state: Record<string, any> = {};
  _update: (() => void) | null = null;
  setState(patch: any) {
    const next = typeof patch === 'function' ? patch(this.state) : patch;
    this.state = Object.assign({}, this.state, next);
    if (this._update) this._update();
  }
}

type Scope = Record<string, any>;

const VOID = new Set(['input', 'br', 'img', 'hr', 'meta', 'link']);
const NO_WS = new Set(['table', 'thead', 'tbody', 'tfoot', 'tr', 'colgroup']);
const BOOLS = new Set(['readonly', 'novalidate', 'disabled', 'checked', 'selected', 'required', 'multiple']);
const ATTR_MAP: Record<string, string> = {
  class: 'className', for: 'htmlFor', tabindex: 'tabIndex', readonly: 'readOnly', novalidate: 'noValidate',
  autocomplete: 'autoComplete', inputmode: 'inputMode', maxlength: 'maxLength', colspan: 'colSpan', rowspan: 'rowSpan'
};

const has = (o: any, k: string) => Object.prototype.hasOwnProperty.call(o, k);

function lookup(expr: string, vals: any, scope: Scope): any {
  const e = expr.trim();
  if (e === 'true') return true;
  if (e === 'false') return false;
  if (e === 'null') return null;
  if (e === 'undefined') return undefined;
  if (/^-?\d+(\.\d+)?$/.test(e)) return Number(e);
  const parts = e.split('.');
  let cur: any = has(scope, parts[0]) ? scope[parts[0]] : vals[parts[0]];
  for (let i = 1; i < parts.length; i++) {
    if (cur == null) return undefined;
    cur = cur[parts[i]];
  }
  return cur;
}

function interp(s: string, vals: any, scope: Scope): string {
  return s.replace(/\{\{([^}]+)\}\}/g, (_m, e) => {
    const v = lookup(e, vals, scope);
    return v == null ? '' : String(v);
  });
}

function resolveAttr(raw: string, vals: any, scope: Scope): any {
  const whole = /^\{\{([^}]+)\}\}$/.exec(raw.trim());
  if (whole) return lookup(whole[1], vals, scope);
  return raw.indexOf('{{') >= 0 ? interp(raw, vals, scope) : raw;
}

function parseStyle(css: string): Record<string, string> {
  const out: Record<string, string> = {};
  css.split(';').forEach((decl) => {
    const i = decl.indexOf(':');
    if (i < 0) return;
    const k = decl.slice(0, i).trim();
    const v = decl.slice(i + 1).trim();
    if (!k || !v) return;
    let key = k;
    if (!k.startsWith('--')) {
      key = k.replace(/^-(webkit|moz|ms)-/, (_m, p) => (p === 'ms' ? 'ms-' : p[0].toUpperCase() + p.slice(1) + '-'));
      key = key.replace(/-([a-z])/g, (_m, c) => c.toUpperCase());
    }
    out[key] = v;
  });
  return out;
}

function reactAttrName(name: string): string {
  if (has(ATTR_MAP, name)) return ATTR_MAP[name];
  if (name.startsWith('aria-') || name.startsWith('data-')) return name;
  if (name.indexOf('-') >= 0) return name.replace(/-([a-z])/g, (_m, c) => c.toUpperCase());
  return name;
}

function renderChildren(node: Node, vals: any, scope: Scope, kp: string): React.ReactNode[] {
  const out: React.ReactNode[] = [];
  // <sc-if>/<sc-for> não existem no DOM final: o pai real é o primeiro ancestral que não é sc-*.
  let real: Node | null = node;
  while (real && (real as Element).localName && (real as Element).localName.startsWith('sc-')) real = real.parentNode;
  const parentTag = real ? (real as Element).localName : '';
  node.childNodes.forEach((child, i) => {
    const r = renderNode(child, vals, scope, kp + '.' + i, parentTag);
    if (r !== null && r !== undefined) out.push(r);
  });
  return out;
}

function renderNode(node: Node, vals: any, scope: Scope, key: string, parentTag: string): React.ReactNode {
  if (node.nodeType === 3) {
    const text = node.nodeValue || '';
    if (!text.trim()) return NO_WS.has(parentTag) ? null : ' ';
    return interp(text, vals, scope);
  }
  if (node.nodeType !== 1) return null;
  const el = node as Element;
  const tag = el.localName;

  if (tag === 'helmet') return null;
  if (tag === 'sc-if') {
    const v = resolveAttr(el.getAttribute('value') || '', vals, scope);
    return v ? <React.Fragment key={key}>{renderChildren(el, vals, scope, key)}</React.Fragment> : null;
  }
  if (tag === 'sc-for') {
    const list = resolveAttr(el.getAttribute('list') || '', vals, scope);
    const as = el.getAttribute('as') || 'item';
    if (!Array.isArray(list)) return null;
    return (
      <React.Fragment key={key}>
        {list.map((item, i) => (
          <React.Fragment key={i}>
            {renderChildren(el, vals, Object.assign({}, scope, { [as]: item }), key + '.' + i)}
          </React.Fragment>
        ))}
      </React.Fragment>
    );
  }

  const props: Record<string, any> = { key };
  Array.from(el.attributes).forEach((a) => {
    const name = a.name;
    if (name.startsWith('hint-') || name === 'xmlns') return;
    if (name === 'style') {
      props.style = parseStyle(interp(a.value, vals, scope));
      return;
    }
    let val = resolveAttr(a.value, vals, scope);
    if (/^on[A-Z]/.test(name)) {
      if (typeof val === 'function') props[name] = val;
      return;
    }
    if (BOOLS.has(name) && a.value === '') val = true;
    const rn = reactAttrName(name);
    if (rn.startsWith('aria-')) {
      if (val === undefined || val === null) return;
      props[rn] = typeof val === 'boolean' ? String(val) : val;
      return;
    }
    if (val === undefined || val === null || val === false) return;
    props[rn] = val;
  });

  if ((tag === 'input' || tag === 'textarea' || tag === 'select') && has(props, 'value') && !props.onChange) {
    props.defaultValue = props.value;
    delete props.value;
  }
  if (tag === 'input' && has(props, 'checked') && !props.onChange) {
    props.defaultChecked = props.checked;
    delete props.checked;
  }

  if (VOID.has(tag) || tag === 'textarea') return React.createElement(tag, props);
  return React.createElement(tag, props, ...renderChildren(el, vals, scope, key));
}

export interface ParsedDC {
  css: string;
  root: Element;
  Component: new () => DCLogic & Record<string, any>;
}

export function parseDC(raw: string): ParsedDC {
  const m = /<x-dc>([\s\S]*?)<\/x-dc>/.exec(raw);
  if (!m) throw new Error('Arquivo .dc.html sem bloco <x-dc>.');
  let inner = m[1];
  const helmet = /<helmet>([\s\S]*?)<\/helmet>/.exec(inner);
  const styleM = helmet ? /<style>([\s\S]*?)<\/style>/.exec(helmet[1]) : null;
  const css = styleM ? styleM[1] : '';
  inner = inner.replace(/<helmet>[\s\S]*?<\/helmet>/, '');
  inner = inner.replace(/<(input|br|img|hr|meta|link)\b([^>]*?)(\/?)>/g, (all, t, rest, sl) => (sl ? all : '<' + t + rest + '/>'));
  const doc = new DOMParser().parseFromString('<root xmlns="http://www.w3.org/1999/xhtml">' + inner + '</root>', 'application/xhtml+xml');
  const err = doc.getElementsByTagName('parsererror')[0];
  if (err) throw new Error('Erro ao ler a marcação: ' + (err.textContent || '').slice(0, 400));

  const sm = /<script type="text\/x-dc" data-dc-script[^>]*>([\s\S]*?)<\/script>/.exec(raw);
  if (!sm) throw new Error('Arquivo .dc.html sem bloco de script.');
  // eslint-disable-next-line no-new-func
  const Component = new Function('DCLogic', sm[1] + '\nreturn Component;')(DCLogic);
  return { css, root: doc.documentElement, Component };
}

export function DCApp({ parsed, props }: { parsed: ParsedDC; props?: Record<string, any> }) {
  const [, force] = useReducer((x: number) => x + 1, 0);
  const ref = useRef<any>(null);
  if (!ref.current) {
    const inst = new parsed.Component();
    inst.props = props || {};
    inst._update = force as any;
    ref.current = inst;
  }
  const inst = ref.current;

  useEffect(() => {
    if (inst.componentDidMount) inst.componentDidMount();
    return () => {
      if (inst.componentWillUnmount) inst.componentWillUnmount();
      inst._update = null;
    };
  }, []);
  useEffect(() => {
    if (inst.componentDidUpdate) inst.componentDidUpdate();
  });

  const vals = inst.renderVals();
  return (
    <>
      <style>{parsed.css}</style>
      {renderChildren(parsed.root, vals, {}, 'r')}
    </>
  );
}
