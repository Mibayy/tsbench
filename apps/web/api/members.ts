import { apiClient } from '../lib/apiClient';
import { fetcher } from '../lib/fetcher';
import { DEFAULT_PAGE_SIZE } from '../lib/constants';

export interface MembersQuery {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}

const DEFAULT_QUERY: MembersQuery = {
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
  sortDir: 'asc',
};

export async function listMembers(params: MembersQuery = DEFAULT_QUERY) {
  const query = { ...DEFAULT_QUERY, ...params };
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${query.sortBy}:${query.sortDir ?? 'asc'}`);
  return apiClient(`/api/members?${search.toString()}`, {});
}

export async function getMembers(id: string) {
  if (!id) throw new Error('id required');
  return apiClient(`/api/members/${id}`, {});
}

export async function createMembers(payload: Record<string, unknown>) {
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/members', cleaned);
}

export async function updateMembers(id: string, payload: Record<string, unknown>) {
  return apiClient(`/api/members/${id}`, payload);
}

export async function deleteMembers(id: string) {
  return apiClient(`/api/members/${id}`, { _method: 'DELETE' });
}

export async function bulkMembers(ids: string[], action: 'archive' | 'delete' | 'restore') {
  return apiClient(`/api/members/bulk`, { ids, action });
}

export async function searchMembers(term: string) {
  return fetcher(`/api/members/search?q=${encodeURIComponent(term)}`);
}
