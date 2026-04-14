export interface Billing {
  id: string;
  name: string;
  email?: string;
  status: BillingStatus;
  role: BillingRole;
  metadata: BillingMetadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
}

export type BillingStatus = 'active' | 'pending' | 'archived' | 'draft';
export type BillingRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface BillingMetadata {
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}

export interface BillingSummary {
  id: string;
  label: string;
  status: BillingStatus;
}

export interface BillingCreateInput {
  name: string;
  email?: string;
  role?: BillingRole;
  metadata?: Partial<BillingMetadata>;
}

export interface BillingUpdateInput {
  name?: string;
  status?: BillingStatus;
  role?: BillingRole;
  metadata?: Partial<BillingMetadata>;
}

export interface BillingListResponse {
  items: Billing[];
  total: number;
  page: number;
  pageSize: number;
}

export const Billing_DEFAULT_METADATA: BillingMetadata = {
  tags: [],
  customFields: {},
  source: 'web',
  version: 1,
};
