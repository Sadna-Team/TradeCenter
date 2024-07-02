"use client";

import * as React from "react";
import { DayPicker } from "react-day-picker";

const Calendar = React.forwardRef(
  ({ className, ...props }, ref) => (
    <DayPicker
      ref={ref}
      className={`rounded-md border p-4 ${className}`}
      {...props}
    />
  )
);
Calendar.displayName = "Calendar";

export { Calendar };
