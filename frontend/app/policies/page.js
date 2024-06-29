"use client";
import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { ScrollArea } from '@/components/ScrollArea';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/Dialog";
import { Input } from "@/components/Input";
import { Label } from "@/components/Label";
import Button from "@/components/Button";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/Select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/AlertDialog";

// Mock data for policies
const mockPolicies = {
  productSpecific: [
    {
      purchase_policy_id: 1,
      store_id: 101,
      policy_name: "Product Policy 1",
      product_id: "product1",
      constraints: [
        { type: "Age", details: "Must be 18+" },
        { type: "Time", details: "Not allowed after 10 PM" }
      ]
    },
    {
      purchase_policy_id: 2,
      store_id: 102,
      policy_name: "Product Policy 2",
      product_id: "product2",
      constraints: [
        { type: "Age", details: "Must be 21+" }
      ]
    }
  ],
  categorySpecific: [
    {
      purchase_policy_id: 3,
      store_id: 103,
      policy_name: "Category Policy 1",
      category_id: "category1",
      constraints: [
        { type: "Age", details: "Must be 18+" }
      ]
    }
  ],
  basketSpecific: [
    {
      purchase_policy_id: 4,
      store_id: 104,
      policy_name: "Basket Policy 1",
      constraints: [
        { type: "Time", details: "Not allowed after 9 PM" }
      ]
    }
  ],
  andPolicies: [
    {
      purchase_policy_id: 5,
      store_id: 105,
      policy_name: "And Policy 1",
      left_policy: { id: 1, details: "Left policy details" },
      right_policy: { id: 2, details: "Right policy details" }
    }
  ],
  orPolicies: [
    {
      purchase_policy_id: 6,
      store_id: 106,
      policy_name: "Or Policy 1",
      left_policy: { id: 3, details: "Left policy details" },
      right_policy: { id: 4, details: "Right policy details" }
    }
  ],
  conditionalPolicies: [
    {
      purchase_policy_id: 7,
      store_id: 107,
      policy_name: "Conditional Policy 1",
      left_policy: { id: 5, details: "Left policy details" },
      right_policy: { id: 6, details: "Right policy details" }
    }
  ]
};

// Mock data for products
const mockProducts = [
  { value: 'product1', label: 'Product 1' },
  { value: 'product2', label: 'Product 2' },
  { value: 'product3', label: 'Product 3' },
  { value: 'product4', label: 'Product 4' },
  { value: 'product5', label: 'Product 5' },
  { value: 'product6', label: 'Product 6' },
  { value: 'product7', label: 'Product 7' },
  { value: 'product8', label: 'Product 8' },
  { value: 'product9', label: 'Product 9' },
  { value: 'product10', label: 'Product 10' },
  // Add more mock products as needed
];

const ManagePolicy = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');
  const [policies, setPolicies] = useState(mockPolicies);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newPolicyName, setNewPolicyName] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [expandedPolicy, setExpandedPolicy] = useState(null);
  const [expandedLeftPolicy, setExpandedLeftPolicy] = useState(null);
  const [expandedRightPolicy, setExpandedRightPolicy] = useState(null);
  const [expandedConstraint, setExpandedConstraint] = useState(null);

  const handleSaveChanges = (type) => {
    if (!selectedProduct) {
      setErrorMessage('Please select a product.');
      return;
    }

    const newPolicy = {
      purchase_policy_id: policies[type].length + 1,
      store_id: 100 + policies[type].length + 1,
      policy_name: newPolicyName,
      product_id: selectedProduct,
      constraints: []
    };
    setPolicies({ ...policies, [type]: [...policies[type], newPolicy] });
    setIsDialogOpen(false);
    setNewPolicyName('');
    setSelectedProduct('');
    setErrorMessage('');
  };

  const handleRemovePolicy = (type, policyId) => {
    setPolicies({
      ...policies,
      [type]: policies[type].filter(policy => policy.purchase_policy_id !== policyId)
    });
  };

  const handleToggle = (policyId) => {
    setExpandedPolicy(expandedPolicy === policyId ? null : policyId);
  };

  const handleToggleLeftPolicy = (policyId) => {
    setExpandedLeftPolicy(expandedLeftPolicy === policyId ? null : policyId);
  };

  const handleToggleRightPolicy = (policyId) => {
    setExpandedRightPolicy(expandedRightPolicy === policyId ? null : policyId);
  };

  const handleToggleConstraint = (policyId) => {
    setExpandedConstraint(expandedConstraint === policyId ? null : policyId);
  };

  const renderPolicy = (policy, type) => (
    <div 
      key={policy.purchase_policy_id} 
      className="mb-4 p-4 border-2 border-gray-300 rounded-md"
    >
      <button
        onClick={() => handleToggle(policy.purchase_policy_id)}
        className="text-left w-full"
      >
        {`Policy ID: ${policy.purchase_policy_id}`}
      </button>
      {expandedPolicy === policy.purchase_policy_id && (
        <div className="mt-2">
          <p><strong>Store ID:</strong> {policy.store_id}</p>
          <p><strong>Policy Name:</strong> {policy.policy_name}</p>
          {type === 'productSpecific' && <p><strong>Product ID:</strong> {policy.product_id}</p>}
          {type === 'categorySpecific' && <p><strong>Category ID:</strong> {policy.category_id}</p>}
          {['andPolicies', 'orPolicies', 'conditionalPolicies'].includes(type) && (
            <>
              <div className="flex justify-between">
                <button onClick={() => handleToggleLeftPolicy(policy.purchase_policy_id)} className="mt-2">Show Left Policy</button>
                <button onClick={() => handleToggleRightPolicy(policy.purchase_policy_id)} className="mt-2">Show Right Policy</button>
              </div>
              {expandedLeftPolicy === policy.purchase_policy_id && (
                <div className="mt-2">
                  <p><strong>Left Policy ID:</strong> {policy.left_policy.id}</p>
                  <p><strong>Left Policy Details:</strong> {policy.left_policy.details}</p>
                </div>
              )}
              {expandedRightPolicy === policy.purchase_policy_id && (
                <div className="mt-2">
                  <p><strong>Right Policy ID:</strong> {policy.right_policy.id}</p>
                  <p><strong>Right Policy Details:</strong> {policy.right_policy.details}</p>
                </div>
              )}
            </>
          )}
          {['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) && (
            <button className="mt-2" onClick={() => handleToggleConstraint(policy.purchase_policy_id)}>Show Constraints</button>
          )}
          {expandedConstraint === policy.purchase_policy_id && (
            <div className="mt-2">
              {policy.constraints.map((constraint, index) => (
                <p key={index}>{constraint.type}: {constraint.details}</p>
              ))}
            </div>
          )}
          <div className={`flex ${['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) ? 'justify-between' : 'justify-center'} mt-4`}>
            {['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) && (
              <Button className="bg-blue-500 text-white py-1 px-3 rounded" onClick={() => alert('Add constraint clicked')}>Add Constraint</Button>
            )}
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button className="bg-red-500 text-white py-1 px-3 rounded">Remove Policy</Button>
              </AlertDialogTrigger>
              <AlertDialogContent className="bg-white">
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete the policy.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={() => handleRemovePolicy(type, policy.purchase_policy_id)}>Yes, remove policy</AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="flex flex-wrap justify-center">
      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Product Specific Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.productSpecific.map((policy) => renderPolicy(policy, 'productSpecific'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add Product Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding a product specific policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('productSpecific')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Category Specific Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.categorySpecific.map((policy) => renderPolicy(policy, 'categorySpecific'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add Category Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding a category specific policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('categorySpecific')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Basket Specific Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.basketSpecific.map((policy) => renderPolicy(policy, 'basketSpecific'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add Basket Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding a basket specific policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('basketSpecific')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">And Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.andPolicies.map((policy) => renderPolicy(policy, 'andPolicies'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add And Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding an And policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('andPolicies')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Or Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.orPolicies.map((policy) => renderPolicy(policy, 'orPolicies'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add Or Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding an Or policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('orPolicies')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Conditional Policies</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {policies.conditionalPolicies.map((policy) => renderPolicy(policy, 'conditionalPolicies'))}
        </ScrollArea>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full mt-2">Add Conditional Policy</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Adding a conditional policy</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policy-name" className="text-right">
                  Policy Name
                </Label>
                <Input 
                  id="policy-name" 
                  value={newPolicyName}
                  onChange={(e) => setNewPolicyName(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="product" className="text-right">
                  Choose Product
                </Label>
                <Select onValueChange={setSelectedProduct}>
                  <SelectTrigger className="col-span-3 border border-black bg-white">
                    <SelectValue placeholder="Select product..." />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    {mockProducts.map((product) => (
                      <SelectItem key={product.value} value={product.value}>
                        {product.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={() => handleSaveChanges('conditionalPolicies')}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default ManagePolicy;
