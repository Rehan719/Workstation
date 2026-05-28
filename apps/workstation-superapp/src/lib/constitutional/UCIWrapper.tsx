import React from 'react';

interface UCIWrapperProps {
  children: React.ReactNode;
  actionId: string;
}

export const UCIWrapper: React.FC<UCIWrapperProps> = ({ children, actionId }) => {
  // OMNISYNTHESIS: Universal Constitutional Interceptor
  console.log(`UCI Intercept: ${actionId}`);
  return <>{children}</>;
};
