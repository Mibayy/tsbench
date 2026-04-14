export interface BillingId {
  kind: 'billing';
  value: string;
}

export type BillingStatus = 'active' | 'pending' | 'archived';

export interface BillingMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
