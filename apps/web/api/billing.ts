import { apiClient } from '../lib/apiClient';
import { fetcher } from '../lib/fetcher';

export interface BillingQuery {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}

const DEFAULT_QUERY: BillingQuery = {
  page: 1,
  pageSize: 20,
  sortDir: 'asc',
};

export async function listBilling(params: BillingQuery = DEFAULT_QUERY) {
  const query = { ...DEFAULT_QUERY, ...params };
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${query.sortBy}:${query.sortDir ?? 'asc'}`);
  return apiClient(`/api/billing?${search.toString()}`, {});
}

export async function getBilling(id: string) {
  if (!id) throw new Error('id required');
  return apiClient(`/api/billing/${id}`, {});
}

export async function createBilling(payload: Record<string, unknown>) {
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/billing', cleaned);
}

export async function updateBilling(id: string, payload: Record<string, unknown>) {
  return apiClient(`/api/billing/${id}`, payload);
}

export async function deleteBilling(id: string) {
  return apiClient(`/api/billing/${id}`, { _method: 'DELETE' });
}

export async function bulkBilling(ids: string[], action: 'archive' | 'delete' | 'restore') {
  return apiClient(`/api/billing/bulk`, { ids, action });
}

export async function searchBilling(term: string) {
  return fetcher(`/api/billing/search?q=${encodeURIComponent(term)}`);
}
