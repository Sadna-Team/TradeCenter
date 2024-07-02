import * as React from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/Accordion";

const AccordionDemo = ({ policy }) => {
  return (
    <Accordion type="single" collapsible className="w-full">
      <AccordionItem value={`item-${policy.purchase_policy_id}`}>
        <AccordionTrigger>{policy.policy_name}</AccordionTrigger>
        <AccordionContent>
          <div>
            <p><strong>Policy ID:</strong> {policy.purchase_policy_id}</p>
            <p><strong>Details:</strong> {policy.details}</p>
          </div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};

export default AccordionDemo;
