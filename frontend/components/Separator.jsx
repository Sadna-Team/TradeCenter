import * as React from "react";

const Separator = ({ orientation = "horizontal", className = "" }) => {
  const separatorClass = orientation === "vertical" ? "w-px h-full" : "h-px w-full";
  return (
    <div className={`${separatorClass} bg-gray-200 ${className}`} />
  );
};

export default Separator;
