// @/components/Input.jsx
import * as React from "react";

export function Input({ id, value, onChange, className, placeholder }) {
  return (
    <input
      id={id}
      value={value}
      onChange={onChange}
      placeholder={placeholder} // Added placeholder prop
      className={`w-full p-2 border rounded ${className}`}
    />
  );
}
