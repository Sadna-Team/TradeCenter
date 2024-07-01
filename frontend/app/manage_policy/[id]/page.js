"use client";
import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

const ManagePolicy = () => {

  const searchParams = useSearchParams();
  const id = searchParams.get('id');

    return (
        <div>
          <h1>manage_policy {id}</h1>
          
        </div>
      );
}

export default ManagePolicy;