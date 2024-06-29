import * as React from "react";
import ScrollArea from "@/components/ScrollArea";
import Separator from "@/components/Separator";
import AccordionDemo from "@/components/AccordionDemo";

const ScrollAreaDemo = ({ policies }) => {
  return (
    <ScrollArea className="h-72 w-96 rounded-md border">
      <div className="p-4">
        <h4 className="mb-4 text-sm font-medium leading-none">Policies</h4>
        {policies.map(policy => (
          <div key={policy.purchase_policy_id}>
            <AccordionDemo policy={policy} />
            <Separator className="my-2" />
          </div>
        ))}
      </div>
    </ScrollArea>
  );
};

export default ScrollAreaDemo;
