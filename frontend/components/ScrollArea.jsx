import * as React from "react";

const ScrollArea = ({ children, className }) => {
  return (
    <div className={`overflow-auto ${className}`}>
      {children}
    </div>
  );
};

export default ScrollArea;
