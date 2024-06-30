// SidePanel.jsx
"use client";

import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";

const SidePanel = DialogPrimitive.Root;
const SidePanelTrigger = DialogPrimitive.Trigger;
const SidePanelPortal = DialogPrimitive.Portal;
const SidePanelClose = DialogPrimitive.Close;

const SidePanelOverlay = React.forwardRef(
  ({ className, ...props }, ref) => (
    <DialogPrimitive.Overlay
      ref={ref}
      className={`fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 ${className}`}
      {...props}
    />
  )
);
SidePanelOverlay.displayName = DialogPrimitive.Overlay.displayName;

const SidePanelContent = React.forwardRef(
  ({ className, children, ...props }, ref) => (
    <SidePanelPortal>
      <SidePanelOverlay />
      <DialogPrimitive.Content
        ref={ref}
        className={`fixed right-0 top-0 z-50 h-full w-[300px] max-w-full translate-x-[100%] bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-right-full sm:rounded-l-lg ${className}`}
        {...props}
      >
        {children}
        <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
          <span className="sr-only">Close</span>
        </DialogPrimitive.Close>
      </DialogPrimitive.Content>
    </SidePanelPortal>
  )
);
SidePanelContent.displayName = DialogPrimitive.Content.displayName;

const SidePanelHeader = ({ className, ...props }) => (
  <div className={`flex flex-col space-y-1.5 text-center sm:text-left ${className}`} {...props} />
);
SidePanelHeader.displayName = "SidePanelHeader";

const SidePanelFooter = ({ className, ...props }) => (
  <div className={`flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 ${className}`} {...props} />
);
SidePanelFooter.displayName = "SidePanelFooter";

const SidePanelTitle = React.forwardRef(
  ({ className, ...props }, ref) => (
    <DialogPrimitive.Title
      ref={ref}
      className={`text-lg font-semibold leading-none tracking-tight ${className}`}
      {...props}
    />
  )
);
SidePanelTitle.displayName = DialogPrimitive.Title.displayName;

const SidePanelDescription = React.forwardRef(
  ({ className, ...props }, ref) => (
    <DialogPrimitive.Description
      ref={ref}
      className={`text-sm text-muted-foreground ${className}`}
      {...props}
    />
  )
);
SidePanelDescription.displayName = DialogPrimitive.Description.displayName;

export {
  SidePanel,
  SidePanelTrigger,
  SidePanelPortal,
  SidePanelOverlay,
  SidePanelContent,
  SidePanelHeader,
  SidePanelFooter,
  SidePanelTitle,
  SidePanelDescription,
};
