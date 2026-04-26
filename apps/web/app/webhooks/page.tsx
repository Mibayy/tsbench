import * as React from 'react';
import { Sidebar } from '../../components/Sidebar';
import { TopBar } from '../../components/TopBar';
import { PageHeader } from '../../components/PageHeader';
import { EmptyState } from '../../components/EmptyState';
import { ErrorBanner } from '../../components/ErrorBanner';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Pagination } from '../../components/Pagination';
import { DEFAULT_PAGE_SIZE } from '../../lib/constants';

interface WebhooksPageState {
  page: number;
  pageSize: number;
  search: string;
  loading: boolean;
  error: string | null;
  items: unknown[];
}

const INITIAL_STATE: WebhooksPageState = {
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
  search: '',
  loading: false,
  error: null,
  items: [],
};

export default function WebhooksPage() {
  const [state, setState] = React.useState<WebhooksPageState>(INITIAL_STATE);

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
      <PageHeader id="ph" label="webhooks" />
      <main>
        {state.loading && <LoadingSpinner id="sp" />}
        {!state.loading && state.items.length === 0 && (
          <EmptyState id="empty" label="No webhooks yet" />
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
