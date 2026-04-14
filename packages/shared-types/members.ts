export interface MembersId {
  kind: 'members';
  value: string;
}

export type MembersStatus = 'active' | 'archived';

export interface MembersMeta {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}
