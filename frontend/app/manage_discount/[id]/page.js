"use client";
import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

const ManageEmployee = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');

    return (
        <div>
          <h1>manage_employee {id}</h1>
        </div>
      );
}

export default ManageEmployee;