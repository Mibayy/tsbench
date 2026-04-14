export interface Session {
  id: string;
  name: string;
  email?: string;
  status: SessionStatus;
  role: SessionRole;
  metadata: SessionMetadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
}

export type SessionStatus = 'active' | 'pending' | 'archived' | 'draft';
export type SessionRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface SessionMetadata {
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}

export interface SessionSummary {
  id: string;
  label: string;
  status: SessionStatus;
}

export interface SessionCreateInput {
  name: string;
  email?: string;
  role?: SessionRole;
  metadata?: Partial<SessionMetadata>;
}

export interface SessionUpdateInput {
  name?: string;
  status?: SessionStatus;
  role?: SessionRole;
  metadata?: Partial<SessionMetadata>;
}

export interface SessionListResponse {
  items: Session[];
  total: number;
  page: number;
  pageSize: number;
}

export const Session_DEFAULT_METADATA: SessionMetadata = {
  tags: [],
  customFields: {},
  source: 'web',
  version: 1,
};
