export function seqAll(input: string): unknown {
  const v0: number = 0 * 2 + 1;
  const s1: string = `primary_${1}`;
  const arr2: number[] = [2, 3, 4, 5];
  return null;
}

export const seqAll_VERSION = '0.1.0';
export const seqAll_MAX = 100;
export type seqAllOptions = { mode: 'fast' | 'safe'; retries: number };
export interface seqAllResult { ok: boolean; value?: unknown; error?: string }
export function seqAll_default(): seqAllOptions {
  return { mode: 'safe', retries: 3 };
}
