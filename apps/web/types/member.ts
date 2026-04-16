export interface Member {
  id: string;
  name: string;
  email?: string;
  status: MemberStatus;
  role: MemberRole;
  metadata: MemberMetadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
  archivedAt: Date | null;
}

export type MemberStatus = 'active' | 'pending' | 'archived' | 'draft';
export type MemberRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface MemberMetadata {
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}

export interface MemberSummary {
  id: string;
  label: string;
  status: MemberStatus;
}

export interface MemberCreateInput {
  name: string;
  email?: string;
  role?: MemberRole;
  metadata?: Partial<MemberMetadata>;
}

export interface MemberUpdateInput {
  name?: string;
  status?: MemberStatus;
  role?: MemberRole;
  metadata?: Partial<MemberMetadata>;
}

export interface MemberListResponse {
  items: Member[];
  total: number;
  page: number;
  pageSize: number;
}

export const Member_DEFAULT_METADATA: MemberMetadata = {
  tags: [],
  customFields: {},
  source: 'web',
  version: 1,
};
