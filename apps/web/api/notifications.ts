import { apiClient } from '../lib/apiClient';
import { fetcher } from '../lib/fetcher';

export interface NotificationsQuery {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}

const DEFAULT_QUERY: NotificationsQuery = {
  page: 1,
  pageSize: 20,
  sortDir: 'asc',
};

export async function listNotifications(params: NotificationsQuery = DEFAULT_QUERY) {
  const query = { ...DEFAULT_QUERY, ...params };
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${query.sortBy}:${query.sortDir ?? 'asc'}`);
  return apiClient(`/api/notifications?${search.toString()}`, {});
}

export async function getNotifications(id: string) {
  if (!id) throw new Error('id required');
  return apiClient(`/api/notifications/${id}`, {});
}

export async function createNotifications(payload: Record<string, unknown>) {
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/notifications', cleaned);
}

export async function updateNotifications(id: string, payload: Record<string, unknown>) {
  return apiClient(`/api/notifications/${id}`, payload);
}

export async function deleteNotifications(id: string) {
  return apiClient(`/api/notifications/${id}`, { _method: 'DELETE' });
}

export async function bulkNotifications(ids: string[], action: 'archive' | 'delete' | 'restore') {
  return apiClient(`/api/notifications/bulk`, { ids, action });
}

export async function searchNotifications(term: string) {
  return fetcher(`/api/notifications/search?q=${encodeURIComponent(term)}`);
}
