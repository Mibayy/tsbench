export interface SessionsId {
  kind: 'sessions';
  value: string;
}

export type SessionsStatus = 'active' | 'pending' | 'archived';

export interface SessionsMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
