import { useState, useEffect, useCallback, useMemo } from 'react';

export interface useWebhooksState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetchCount: number;
}

export interface useWebhooksOptions {
  enabled?: boolean;
  refetchInterval?: number;
  staleTime?: number;
  onSuccess?: (data: unknown) => void;
  onError?: (error: Error) => void;
}

const DEFAULT_OPTIONS: useWebhooksOptions = {
  enabled: true,
  refetchInterval: 0,
  staleTime: 5000,
};

export function useWebhooks<T = unknown>(id: string, options: useWebhooksOptions = DEFAULT_OPTIONS) {
  const [state, setState] = useState<useWebhooksState<T>>({
    data: null,
    loading: false,
    error: null,
    refetchCount: 0,
  });

  const opts = useMemo(() => ({ ...DEFAULT_OPTIONS, ...options }), [options]);

  const fetchData = useCallback(async () => {
    if (!opts.enabled) return;
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const result = { id } as unknown as T;
      setState((s) => ({
        ...s,
        data: result,
        loading: false,
        refetchCount: s.refetchCount + 1,
      }));
      opts.onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setState((s) => ({ ...s, loading: false, error }));
      opts.onError?.(error);
    }
  }, [id, opts]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    if (!opts.refetchInterval) return;
    const t = setInterval(fetchData, opts.refetchInterval);
    return () => clearInterval(t);
  }, [fetchData, opts.refetchInterval]);

  const refetch = useCallback(() => fetchData(), [fetchData]);

  return { ...state, refetch };
}
