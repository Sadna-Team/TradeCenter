"use client";
import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import User from '@/components/User'; // Ensure the path is correct

const Manage_Employee = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');

  // Mock data for demonstration purposes
  const storeData = {
    1: {
      title: 'Store One',
      employees: [
        {
          name: 'John Doe',
          username: 'johndoe',
          birthday: '1985-05-15',
          phone: '123-456-7890',
          isSuspended: false,
        },
        {
          name: 'Jane Smith',
          username: 'janesmith',
          birthday: '1990-10-25',
          phone: '098-765-4321',
          isSuspended: true,
        },
        // Add more employees as needed
      ],
    },
    2: {
      title: 'Store Two',
      employees: [
        {
          name: 'Alice Johnson',
          username: 'alicej',
          birthday: '1988-07-20',
          phone: '555-123-4567',
          isSuspended: false,
        },
        {
          name: 'Bob Brown',
          username: 'bobb',
          birthday: '1975-02-10',
          phone: '555-987-6543',
          isSuspended: false,
        },
        // Add more employees as needed
      ],
    },
    // Add more stores and employees as needed
  };

  const [store, setStore] = useState(null);

  useEffect(() => {
    if (id && storeData[id]) {
      setStore(storeData[id]);
    } else {
      setStore(null); // Handle case where store is not found
    }
  }, [id]);

  if (!store) {
    return <div className="min-h-screen bg-gray-100 p-4">Store not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">Employee Management of {store.title}</h1>
        
        {/* Employees List */}
        <div className="grid grid-cols-1 gap-6">
          {store.employees.map((employee, index) => (
            <User key={index} user={employee} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Manage_Employee;
