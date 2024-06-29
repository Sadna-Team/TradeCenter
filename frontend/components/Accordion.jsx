import * as React from "react";

export const Accordion = ({ children, type, collapsible, className }) => {
  return (
    <div className={`accordion ${className}`} data-type={type} data-collapsible={collapsible}>
      {children}
    </div>
  );
};

export const AccordionItem = ({ children, value }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`accordion-item ${isOpen ? 'open' : ''}`} data-value={value}>
      <div onClick={toggleAccordion} className="accordion-trigger">
        {children[0]}
      </div>
      <div className={`accordion-content ${isOpen ? 'block' : 'hidden'}`}>
        {children[1]}
      </div>
    </div>
  );
};

export const AccordionTrigger = ({ children }) => {
  return (
    <div className="accordion-trigger">
      {children}
    </div>
  );
};

export const AccordionContent = ({ children }) => {
  return (
    <div className="accordion-content">
      {children}
    </div>
  );
};
