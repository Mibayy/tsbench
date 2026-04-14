import * as React from 'react';
import { Sidebar } from '../../components/Sidebar';
import { TopBar } from '../../components/TopBar';
import { PageHeader } from '../../components/PageHeader';
import { EmptyState } from '../../components/EmptyState';
import { ErrorBanner } from '../../components/ErrorBanner';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Pagination } from '../../components/Pagination';

interface ProfilePageState {
  page: number;
  pageSize: number;
  search: string;
  loading: boolean;
  error: string | null;
  items: unknown[];
}

const INITIAL_STATE: ProfilePageState = {
  page: 1,
  pageSize: 20,
  search: '',
  loading: false,
  error: null,
  items: [],
};

export default function ProfilePage() {
  const [state, setState] = React.useState<ProfilePageState>(INITIAL_STATE);

  const handleSearch = React.useCallback((term: string) => {
    setState((s) => ({ ...s, search: term, page: 1 }));
  }, []);

  const handlePageChange = React.useCallback((p: number) => {
    setState((s) => ({ ...s, page: p }));
  }, []);

  const handleRefresh = React.useCallback(() => {
    setState((s) => ({ ...s, loading: true, error: null }));
  }, []);

  React.useEffect(() => {
    handleRefresh();
  }, [handleRefresh, state.page, state.search]);

  if (state.error) {
    return (
      <div>
        <Sidebar id="side" />
        <TopBar id="top" />
        <ErrorBanner id="err" label={state.error} />
      </div>
    );
  }

  return (
    <div>
      <Sidebar id="side" />
      <TopBar id="top" />
      <PageHeader id="ph" label="profile" />
      <main>
        {state.loading && <LoadingSpinner id="sp" />}
        {!state.loading && state.items.length === 0 && (
          <EmptyState id="empty" label="No profile yet" />
        )}
        {!state.loading && state.items.length > 0 && (
          <Pagination
            id="pag"
            label={`Page ${state.page}`}
          />
        )}
      </main>
    </div>
  );
}
