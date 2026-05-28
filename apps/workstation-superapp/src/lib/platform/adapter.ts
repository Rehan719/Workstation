export type Platform = 'web' | 'tauri' | 'capacitor';

export const getPlatform = (): Platform => {
  if (typeof window !== 'undefined' && (window as any).__TAURI__) return 'tauri';
  if (typeof window !== 'undefined' && (window as any).Capacitor) return 'capacitor';
  return 'web';
};

export const isNative = () => getPlatform() !== 'web';

export const getResponsiveTokens = (width: number) => {
  if (width < 768) {
    return {
      navType: 'bottom',
      avatarSize: 'sm',
      layout: 'mobile'
    };
  } else if (width < 1024) {
    return {
      navType: 'side',
      avatarSize: 'md',
      layout: 'tablet'
    };
  } else {
    return {
      navType: 'side',
      avatarSize: 'lg',
      layout: 'desktop'
    };
  }
};
