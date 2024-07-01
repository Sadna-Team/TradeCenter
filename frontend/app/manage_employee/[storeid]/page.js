"use client";

import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import api from '@/lib/api'; // Import the configured axios instance
import Link from 'next/link';

const permissionsList = [
  { key: 'add_product', label: 'Add Product' },
  { key: 'change_purchase_policy', label: 'Change Purchase Policy' },
  { key: 'change_purchase_types', label: 'Change Purchase Types' },
  { key: 'change_discount_policy', label: 'Change Discount Policy' },
  { key: 'change_discount_types', label: 'Change Discount Types' },
  { key: 'add_manager', label: 'Add Manager' },
  { key: 'get_bid', label: 'Get Bid' },
];

export default function ManageEmployeePage() {
  const { storeid } = useParams();
  const [employees, setEmployees] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [updateFlag, setUpdateFlag] = useState(false); // State variable to trigger useEffect

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await api.post('/user/get_user_employees', {
          store_id: storeid,
        });
        const data = response.data.employees;
        const formattedEmployees = data.map((user) => ({
          id: user.user_id,
          name: user.username,
          role: user.role,
          isOwner: user.is_owner,
          permissions: {
            add_product: user.add_product,
            change_purchase_policy: user.change_purchase_policy,
            change_purchase_types: user.change_purchase_types,
            change_discount_policy: user.change_discount_policy,
            change_discount_types: user.change_discount_types,
            add_manager: user.add_manager,
            get_bid: user.get_bid,
          },
        }));
        setEmployees(formattedEmployees);
      } catch (error) {
        setErrorMessage('Error fetching employees');
        console.error('Error fetching employees:', error.response ? error.response.data : error.message);
      }
    };

    if (storeid) {
      fetchEmployees();
    }
  }, [storeid, updateFlag]); // Include updateFlag in the dependency array

  const handlePermissionChange = (employeeId, permission) => {
    setEmployees((prevEmployees) =>
      prevEmployees.map((employee) =>
        employee.id === employeeId
          ? {
              ...employee,
              permissions: {
                ...employee.permissions,
                [permission]: !employee.permissions[permission],
              },
            }
          : employee
      )
    );
  };

  const handleSaveChanges = async (employeeId) => {
    const employee = employees.find((emp) => emp.id === employeeId);
    const permissions = Object.keys(employee.permissions).filter((key) => employee.permissions[key]);

    try {
      const response = await api.post('/store/edit_manager_permissions', {
        store_id: storeid,
        manager_id: employeeId,
        permissions,
      });
      const data = response.data;
      setSuccessMessage(`Changes saved for employee ${employee.name}`);
      console.log(`Changes saved for employee ${employeeId}:`, data);

      // Clear the success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      setErrorMessage('Error saving changes');
      console.error('Error saving changes:', error.response ? error.response.data : error.message);
    }
  };

  const handleFireEmployee = async (username) => {
    try {
      const response = await api.post('/store/remove_store_role', {
        store_id: storeid,
        username,
      });
      const data = response.data;
      setSuccessMessage(`Employee ${username} fired successfully`);
      console.log(`Employee ${username} fired successfully:`, data);

      // Trigger useEffect to re-fetch employees
      setUpdateFlag((prevFlag) => !prevFlag);

      // Clear the success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      setErrorMessage('Error firing employee');
      console.error('Error firing employee:', error.response ? error.response.data : error.message);
    }
  };

  if (errorMessage) {
    return <div className="min-h-screen bg-gray-100 p-4">{errorMessage}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-4">Manage Employees</h1>
        <Link href={`/nominate-employees/${storeid}`}>
          <button className="bg-blue-500 text-white py-2 px-4 rounded mb-4">
            Add Employee
          </button>
        </Link>
        {successMessage && <p className="text-green-500 mb-4">{successMessage}</p>}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {employees.map((employee) => (
            <div key={employee.id} className="p-4 border rounded-lg bg-gray-50">
              <p className="text-lg font-bold mb-2">{employee.name}</p>
              <p className="text-sm text-gray-600 mb-2">Role: {employee.role}</p>
              {employee.isOwner ? (
                <p className="text-sm text-green-600 mb-2">Owner - Full Permissions</p>
              ) : (
                <div className="mb-4">
                  {permissionsList.map(({ key, label }) => (
                    <label key={key} className="block">
                      <input
                        type="checkbox"
                        checked={employee.permissions[key]}
                        onChange={() => handlePermissionChange(employee.id, key)}
                        className="mr-2"
                      />
                      {label}
                    </label>
                  ))}
                </div>
              )}
              <div className="flex items-center justify-between">
                {!employee.isOwner && (
                  <button
                    onClick={() => handleSaveChanges(employee.id)}
                    className="bg-green-500 text-white py-2 px-4 rounded"
                  >
                    Save Changes
                  </button>
                )}
                <button
                  onClick={() => handleFireEmployee(employee.name)}
                  className="bg-red-500 text-white py-2 px-4 rounded"
                >
                  Fire
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
