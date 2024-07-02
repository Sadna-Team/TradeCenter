// components/Command.jsx

import React from 'react';

// Custom Command Components

export function Command({ children }) {
  return <div className="command">{children}</div>;
}

export function CommandInput({ placeholder, className, ...props }) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      className={`command-input ${className}`}
      {...props}
    />
  );
}

export function CommandList({ children }) {
  return <ul className="command-list">{children}</ul>;
}

export function CommandEmpty({ children }) {
  return <li className="command-empty">{children}</li>;
}

export function CommandGroup({ children }) {
  return <div className="command-group">{children}</div>;
}

export function CommandItem({ children, value, onSelect }) {
  return (
    <li className="command-item" onClick={() => onSelect(value)}>
      {children}
    </li>
  );
}
