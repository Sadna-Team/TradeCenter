"use client";

import * as React from "react";

const ScrollAreaDemo = ({ policies }) => {
  return (
    <div className="scroll-area">
      {policies.map((policy) => (
        <div key={policy.purchase_policy_id} className="policy-item">
          <h2>{policy.policy_name}</h2>
          <p>{policy.details}</p>
        </div>
      ))}
    </div>
  );
};

export default ScrollAreaDemo;
