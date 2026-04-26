import { apiClient } from '../lib/apiClient';
import { fetcher } from '../lib/fetcher';
import { DEFAULT_PAGE_SIZE } from '../lib/constants';

export interface SessionsQuery {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}

const DEFAULT_QUERY: SessionsQuery = {
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
  sortDir: 'asc',
};

export async function listSessions(params: SessionsQuery = DEFAULT_QUERY) {
  const query = { ...DEFAULT_QUERY, ...params };
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${query.sortBy}:${query.sortDir ?? 'asc'}`);
  return apiClient(`/api/sessions?${search.toString()}`, {});
}

export async function getSessions(id: string) {
  if (!id) throw new Error('id required');
  return apiClient(`/api/sessions/${id}`, {});
}

export async function createSessions(payload: Record<string, unknown>) {
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/sessions', cleaned);
}

export async function updateSessions(id: string, payload: Record<string, unknown>) {
  return apiClient(`/api/sessions/${id}`, payload);
}

export async function deleteSessions(id: string) {
  return apiClient(`/api/sessions/${id}`, { _method: 'DELETE' });
}

export async function bulkSessions(ids: string[], action: 'archive' | 'delete' | 'restore') {
  return apiClient(`/api/sessions/bulk`, { ids, action });
}

export async function searchSessions(term: string) {
  return fetcher(`/api/sessions/search?q=${encodeURIComponent(term)}`);
}
