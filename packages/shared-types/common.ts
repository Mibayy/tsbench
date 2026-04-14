export interface CommonId {
  kind: 'common';
  value: string;
}

export type CommonStatus = 'active' | 'pending' | 'archived';

export interface CommonMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
