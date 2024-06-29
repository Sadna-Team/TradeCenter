// @/components/Input.jsx
import * as React from "react";

export function Input({ id, value, onChange, className }) {
  return (
    <input
      id={id}
      value={value}
      onChange={onChange}
      className={`w-full p-2 border rounded ${className}`}
    />
  );
}
