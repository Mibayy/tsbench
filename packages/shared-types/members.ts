export interface MembersId {
  kind: 'members';
  value: string;
}

export type MembersStatus = 'active' | 'pending' | 'archived';

export interface MembersMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
