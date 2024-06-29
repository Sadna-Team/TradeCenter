// components/Label.jsx

import React from 'react';

export function Label({ htmlFor, children, className }) {
  return (
    <label htmlFor={htmlFor} className={`label ${className}`}>
      {children}
    </label>
  );
}
