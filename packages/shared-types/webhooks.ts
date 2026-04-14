export interface WebhooksId {
  kind: 'webhooks';
  value: string;
}

export type WebhooksStatus = 'active' | 'pending' | 'archived';

export interface WebhooksMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
