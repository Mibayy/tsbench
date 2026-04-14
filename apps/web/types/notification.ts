export interface Notification {
  id: string;
  name: string;
  email?: string;
  status: NotificationStatus;
  role: NotificationRole;
  metadata: NotificationMetadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
}

export type NotificationStatus = 'active' | 'pending' | 'archived' | 'draft';
export type NotificationRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface NotificationMetadata {
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}

export interface NotificationSummary {
  id: string;
  label: string;
  status: NotificationStatus;
}

export interface NotificationCreateInput {
  name: string;
  email?: string;
  role?: NotificationRole;
  metadata?: Partial<NotificationMetadata>;
}

export interface NotificationUpdateInput {
  name?: string;
  status?: NotificationStatus;
  role?: NotificationRole;
  metadata?: Partial<NotificationMetadata>;
}

export interface NotificationListResponse {
  items: Notification[];
  total: number;
  page: number;
  pageSize: number;
}

export const Notification_DEFAULT_METADATA: NotificationMetadata = {
  tags: [],
  customFields: {},
  source: 'web',
  version: 1,
};
