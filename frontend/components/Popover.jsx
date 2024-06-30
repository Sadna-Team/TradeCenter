// components/Popover.jsx

import React, { useState } from 'react';

export function Popover({ children }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="popover">
      {React.Children.map(children, child => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, { isOpen, handleToggle });
        }
        return child;
      })}
    </div>
  );
}

export function PopoverTrigger({ children, handleToggle }) {
  return (
    <div className="popover-trigger" onClick={handleToggle}>
      {children}
    </div>
  );
}

export function PopoverContent({ children, isOpen }) {
  if (!isOpen) return null;
  return <div className="popover-content">{children}</div>;
}
