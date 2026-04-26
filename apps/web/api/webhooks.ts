import { apiClient } from '../lib/apiClient';
import { fetcher } from '../lib/fetcher';
import { DEFAULT_PAGE_SIZE } from '../lib/constants';

export interface WebhooksQuery {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}

const DEFAULT_QUERY: WebhooksQuery = {
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
  sortDir: 'asc',
};

export async function listWebhooks(params: WebhooksQuery = DEFAULT_QUERY) {
  const query = { ...DEFAULT_QUERY, ...params };
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${query.sortBy}:${query.sortDir ?? 'asc'}`);
  return apiClient(`/api/webhooks?${search.toString()}`, {});
}

export async function getWebhooks(id: string) {
  if (!id) throw new Error('id required');
  return apiClient(`/api/webhooks/${id}`, {});
}

export async function createWebhooks(payload: Record<string, unknown>) {
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/webhooks', cleaned);
}

export async function updateWebhooks(id: string, payload: Record<string, unknown>) {
  return apiClient(`/api/webhooks/${id}`, payload);
}

export async function deleteWebhooks(id: string) {
  return apiClient(`/api/webhooks/${id}`, { _method: 'DELETE' });
}

export async function bulkWebhooks(ids: string[], action: 'archive' | 'delete' | 'restore') {
  return apiClient(`/api/webhooks/bulk`, { ids, action });
}

export async function searchWebhooks(term: string) {
  return fetcher(`/api/webhooks/search?q=${encodeURIComponent(term)}`);
}
