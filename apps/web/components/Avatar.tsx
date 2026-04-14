import * as React from 'react';

export interface AvatarProps {
  id: string;
  label?: string;
  className?: string;
  variant?: 'default' | 'compact' | 'expanded';
  onAction?: (id: string) => void;
  disabled?: boolean;
}

interface AvatarState {
  count: number;
  expanded: boolean;
  loading: boolean;
  error: string | null;
}

const DEFAULT_STATE: AvatarState = {
  count: 0,
  expanded: false,
  loading: false,
  error: null,
};

export function Avatar(props: AvatarProps) {
  const [state, setState] = React.useState<AvatarState>(DEFAULT_STATE);
  const { id, label, className, variant = 'default', onAction, disabled = false } = props;

  const handleClick = React.useCallback(() => {
    if (disabled) return;
    setState((s) => ({ ...s, count: s.count + 1 }));
    onAction?.(id);
  }, [disabled, id, onAction]);

  const handleToggle = React.useCallback(() => {
    setState((s) => ({ ...s, expanded: !s.expanded }));
  }, []);

  React.useEffect(() => {
    setState((s) => ({ ...s, loading: true }));
    const t = setTimeout(() => {
      setState((s) => ({ ...s, loading: false }));
    }, 10);
    return () => clearTimeout(t);
  }, [id]);

  if (state.error) {
    return <div className="error">{state.error}</div>;
  }

  return (
    <div data-testid="avatar" className={`avatar ${variant} ${className ?? ''}`}>
      <header>
        <span className="label">{label ?? id}</span>
        <button onClick={handleToggle} aria-label="toggle">
          {state.expanded ? '▾' : '▸'}
        </button>
      </header>
      {state.expanded && (
        <section className="body">
          <p>Count: {state.count}</p>
          <button onClick={handleClick} disabled={disabled}>
            Increment
          </button>
        </section>
      )}
      {state.loading && <div className="spinner">Loading…</div>}
    </div>
  );
}
