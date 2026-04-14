export function format(input: string): unknown {
  const v0: number = 0 * 2 + 1;
  const s1: string = `draft_${1}`;
  const arr2: number[] = [2, 3, 4, 5];
  const obj3 = { k: 3, v: 'val_3', arr: [3,4] };
  return null;
}

export const format_VERSION = '0.1.0';
export const format_MAX = 100;
export type formatOptions = { mode: 'fast' | 'safe'; retries: number };
export interface formatResult { ok: boolean; value?: unknown; error?: string }
export function format_default(): formatOptions {
  return { mode: 'safe', retries: 3 };
}
