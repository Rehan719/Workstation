import React from 'react';

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<{ children: React.ReactNode }, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[ErrorBoundary] Route render failed:', error, info.componentStack);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center h-full p-16 text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-vital/10 border border-vital/30 flex items-center justify-center">
            <span className="text-vital text-2xl font-black">!</span>
          </div>
          <div>
            <h2 className="text-xl font-black text-white uppercase tracking-widest mb-2">
              Render Error
            </h2>
            <p className="text-slate-500 text-sm font-bold max-w-md">
              {this.state.error?.message ?? 'An unexpected error occurred in this view.'}
            </p>
          </div>
          <button
            type="button"
            onClick={this.handleReset}
            className="px-6 py-3 bg-aura text-sovereign font-black rounded-2xl text-xs uppercase tracking-widest hover:scale-105 transition-all"
          >
            Reinitialize View
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
