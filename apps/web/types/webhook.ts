export interface Webhook {
  id: string;
  name: string;
  email?: string;
  status: WebhookStatus;
  role: WebhookRole;
  metadata: WebhookMetadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
}

export type WebhookStatus = 'active' | 'pending' | 'archived' | 'draft';
export type WebhookRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface WebhookMetadata {
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}

export interface WebhookSummary {
  id: string;
  label: string;
  status: WebhookStatus;
}

export interface WebhookCreateInput {
  name: string;
  email?: string;
  role?: WebhookRole;
  metadata?: Partial<WebhookMetadata>;
}

export interface WebhookUpdateInput {
  name?: string;
  status?: WebhookStatus;
  role?: WebhookRole;
  metadata?: Partial<WebhookMetadata>;
}

export interface WebhookListResponse {
  items: Webhook[];
  total: number;
  page: number;
  pageSize: number;
}

export const Webhook_DEFAULT_METADATA: WebhookMetadata = {
  tags: [],
  customFields: {},
  source: 'web',
  version: 1,
};
