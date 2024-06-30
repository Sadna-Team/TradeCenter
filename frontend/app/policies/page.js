
"use client";
import { useSearchParams } from 'next/navigation';
import { useState } from 'react';
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
      constraints: []
    },
    {
      purchase_policy_id: 2,
      store_id: 102,
      policy_name: "Product Policy 2",
      product_id: "product2",
      constraints: []
    }
  ],
  categorySpecific: [
    {
      purchase_policy_id: 3,
      store_id: 103,
      policy_name: "Category Policy 1",
      category_id: "category1",
      constraints: []
    }
  ],
  basketSpecific: [
    {
      purchase_policy_id: 4,
      store_id: 104,
      policy_name: "Basket Policy 1",
      constraints: []
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

// Mock data for categories
const mockCategories = [
  { value: 'category1', label: 'Category 1' },
  { value: 'category2', label: 'Category 2' },
  // Add more mock categories as needed
];

// Mock data for stores
const mockStores = [
  { value: 'store1', label: 'Store 1' },
  { value: 'store2', label: 'Store 2' },
  // Add more mock stores as needed
];

const constraintTypes = [
  { value: 'age', label: 'Age constraint' },
  { value: 'time', label: 'Time constraint' },
  { value: 'location', label: 'Location constraint' },
  { value: 'dayOfMonth', label: 'Day of month constraint' },
  { value: 'dayOfWeek', label: 'Day of week constraint' },
  { value: 'season', label: 'Season constraint' },
  { value: 'holiday', label: 'Holiday constraint' },
  { value: 'basketPrice', label: 'Basket price constraint' },
  { value: 'productPrice', label: 'Product price constraint' },
  { value: 'categoryPrice', label: 'Category price constraint' },
  { value: 'basketAmount', label: 'Basket amount constraint' },
  { value: 'productAmount', label: 'Product amount constraint' },
  { value: 'categoryAmount', label: 'Category amount constraint' },
  { value: 'categoryWeight', label: 'Category weight constraint' },
  { value: 'basketWeight', label: 'Basket weight constraint' },
  { value: 'productWeight', label: 'Product weight constraint' },
  { value: 'compositeConstraint', label: 'Composite Constraint' },

  // Add more constraint types as needed
];

const ManagePolicy = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');
  const [policies, setPolicies] = useState(mockPolicies);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedLeftPolicy, setSelectedLeftPolicy] = useState('');
  const [selectedRightPolicy, setSelectedRightPolicy] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [newPolicyName, setNewPolicyName] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [expandedPolicies, setExpandedPolicies] = useState({});
  const [expandedLeftPolicy, setExpandedLeftPolicy] = useState(null);
  const [expandedRightPolicy, setExpandedRightPolicy] = useState(null);
  const [expandedConstraint, setExpandedConstraint] = useState(null);
  const [constraintDialogOpen, setConstraintDialogOpen] = useState(false);
  const [selectedConstraintType, setSelectedConstraintType] = useState('');
  const [constraintValues, setConstraintValues] = useState({});
  const [currentPolicyId, setCurrentPolicyId] = useState(null);
  const [constraintError, setConstraintError] = useState('');

  const generateUniqueId = () => {
    // Generate a unique ID based on the current timestamp and a random number
    return Date.now() + Math.floor(Math.random() * 1000);
  };

  const handleSaveChanges = () => {
    if (!newPolicyName) {
      setErrorMessage('Please enter a policy name.');
      return;
    }
  
    let newPolicyId = generateUniqueId();
    let newPolicy;
    switch (dialogType) {
      case 'productSpecific':
        if (!selectedProduct) {
          setErrorMessage('Please select a product.');
          return;
        }
        newPolicy = {
          purchase_policy_id: newPolicyId,
          store_id: 100 + policies[dialogType].length + 1,
          policy_name: newPolicyName,
          product_id: selectedProduct,
          constraints: []
        };
        break;
      case 'categorySpecific':
        if (!selectedCategory) {
          setErrorMessage('Please select a category.');
          return;
        }
        newPolicy = {
          purchase_policy_id: newPolicyId,
          store_id: 100 + policies[dialogType].length + 1,
          policy_name: newPolicyName,
          category_id: selectedCategory,
          constraints: []
        };
        break;
      case 'basketSpecific':
        newPolicy = {
          purchase_policy_id: newPolicyId,
          store_id: 100 + policies[dialogType].length + 1,
          policy_name: newPolicyName,
          constraints: []
        };
        break;
      case 'andPolicies':
      case 'orPolicies':
      case 'conditionalPolicies':
        if (!selectedLeftPolicy || !selectedRightPolicy) {
          setErrorMessage('Please select both policies.');
          return;
        }
        newPolicy = {
          purchase_policy_id: newPolicyId,
          store_id: 100 + policies[dialogType].length + 1,
          policy_name: newPolicyName,
          left_policy_id: parseInt(selectedLeftPolicy),
          right_policy_id: parseInt(selectedRightPolicy)
        };
  
        // Add the new composite policy to the appropriate type
        const updatedPolicies = { ...policies };
        updatedPolicies[dialogType].push(newPolicy);
        setPolicies(updatedPolicies);
  
        // Remove the selected policies
        const removePolicy = (policyId) => {
          for (let type in updatedPolicies) {
            updatedPolicies[type] = updatedPolicies[type].filter(policy => policy.purchase_policy_id !== policyId);
          }
        };
  
        removePolicy(parseInt(selectedLeftPolicy));
        removePolicy(parseInt(selectedRightPolicy));
        setPolicies(updatedPolicies);
  
        break;
      default:
        return;
    }
  
    if (!['andPolicies', 'orPolicies', 'conditionalPolicies'].includes(dialogType)) {
      setPolicies({ ...policies, [dialogType]: [...policies[dialogType], newPolicy] });
    }
  
    setIsDialogOpen(false);
    setNewPolicyName('');
    setSelectedProduct('');
    setSelectedCategory('');
    setSelectedLeftPolicy('');
    setSelectedRightPolicy('');
    setErrorMessage('');
  };
  
  

  const handleRemovePolicy = (type, policyId) => {
    setPolicies({
      ...policies,
      [type]: policies[type].filter(policy => policy.purchase_policy_id !== policyId)
    });
  };

  const handleToggle = (policyId, type) => {
    setExpandedPolicies({
      ...expandedPolicies,
      [type]: expandedPolicies[type] === policyId ? null : policyId
    });
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

  const handleOpenDialog = (type) => {
    setDialogType(type);
    setIsDialogOpen(true);
  };

  const handleOpenConstraintDialog = (policyId) => {
    setCurrentPolicyId(policyId);
    setConstraintDialogOpen(true);
  };

  const handleConstraintTypeChange = (value) => {
    setSelectedConstraintType(value);
    setConstraintValues({});
  };

  const handleConstraintValueChange = (field, value) => {
    setConstraintValues({ ...constraintValues, [field]: value });
  };

  const handleSaveConstraint = () => {
    // Validation logic
    if (selectedConstraintType === 'age' && isNaN(constraintValues.ageLimit)) {
      setConstraintError('Age limit must be a number.');
      return;
    }
    
    // Add other validation checks for different constraint types here...

    const updatedPolicies = { ...policies };
    const policyType = Object.keys(updatedPolicies).find(type => 
      updatedPolicies[type].some(policy => policy.purchase_policy_id === currentPolicyId)
    );

    const policyIndex = updatedPolicies[policyType].findIndex(policy => 
      policy.purchase_policy_id === currentPolicyId
    );

    updatedPolicies[policyType][policyIndex].constraints = [{
      type: selectedConstraintType,
      details: JSON.stringify(constraintValues)
    }];

    setPolicies(updatedPolicies);
    setConstraintDialogOpen(false);
    setConstraintError('');
  };

  const renderConstraintFields = () => {
    switch (selectedConstraintType) {
      case 'age':
        return (
          <>
            <Input
              id="age-limit"
              placeholder="Enter age limit"
              value={constraintValues.ageLimit || ''}
              onChange={(e) => handleConstraintValueChange('ageLimit', e.target.value)}
              className="col-span-3 border border-black mt-2"
            />
             <div className="mt-8">
            {constraintValues.ageLimit && isNaN(constraintValues.ageLimit) && <p className="text-red-500">Not a number</p>}
          </div>
          </>
        );

      // Add other cases for different constraint types here...

      case 'time':
        return (
          <>
            <Select onValueChange={(value) => handleConstraintValueChange('startingHour', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Starting hour" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(24).keys()].map((hour) => (
                  <SelectItem key={hour} value={hour}>
                    {hour}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select onValueChange={(value) => handleConstraintValueChange('endingHour', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Ending hour" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(24).keys()].map((hour) => (
                  <SelectItem key={hour} value={hour}>
                    {hour}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select onValueChange={(value) => handleConstraintValueChange('startingMinute', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Starting minute" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(60).keys()].map((minute) => (
                  <SelectItem key={minute} value={minute}>
                    {minute}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select onValueChange={(value) => handleConstraintValueChange('endingMinute', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Ending minute" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(60).keys()].map((minute) => (
                  <SelectItem key={minute} value={minute}>
                    {minute}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </>
        );

      // Continue with other constraint types...
      case 'location':
        return (
          <>
            <Input
              id="address"
              placeholder="Address"
              value={constraintValues.address || ''}
              onChange={(e) => handleConstraintValueChange('address', e.target.value)}
              className="col-span-3 border border-black"
            />
            <Input
              id="city"
              placeholder="City"
              value={constraintValues.city || ''}
              onChange={(e) => handleConstraintValueChange('city', e.target.value)}
              className="col-span-3 border border-black"
            />
            <Input
              id="state"
              placeholder="State"
              value={constraintValues.state || ''}
              onChange={(e) => handleConstraintValueChange('state', e.target.value)}
              className="col-span-3 border border-black"
            />
            <Input
              id="country"
              placeholder="Country"
              value={constraintValues.country || ''}
              onChange={(e) => handleConstraintValueChange('country', e.target.value)}
              className="col-span-3 border border-black"
            />
            <Input
              id="zip-code"
              placeholder="Zip-code"
              value={constraintValues.zipCode || ''}
              onChange={(e) => handleConstraintValueChange('zipCode', e.target.value)}
              className="col-span-3 border border-black"
            />
            <div className="mt-2">
            {constraintValues.zipCode && isNaN(constraintValues.zipCode) && <p className="text-red-500">Not a number</p>}
          </div>
          </>
        );
      case 'dayOfMonth':
        return (
          <>
            <Select onValueChange={(value) => handleConstraintValueChange('startingDay', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Starting day" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(31).keys()].map((day) => (
                  <SelectItem key={day + 1} value={day + 1}>
                    {day + 1}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select onValueChange={(value) => handleConstraintValueChange('endingDay', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Ending day" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(31).keys()].map((day) => (
                  <SelectItem key={day + 1} value={day + 1}>
                    {day + 1}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </>
        );
      case 'dayOfWeek':
        return (
          <>
            <Select onValueChange={(value) => handleConstraintValueChange('startingDay', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Starting day" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(7).keys()].map((day) => (
                  <SelectItem key={day + 1} value={day + 1}>
                    {day + 1}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select onValueChange={(value) => handleConstraintValueChange('endingDay', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Ending day" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {[...Array(7).keys()].map((day) => (
                  <SelectItem key={day + 1} value={day + 1}>
                    {day + 1}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </>
        );
      case 'season':
        return (
          <>
            <Select onValueChange={(value) => handleConstraintValueChange('season', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Select season..." />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {['summer', 'winter', 'autumn', 'spring'].map((season) => (
                  <SelectItem key={season} value={season}>
                    {season}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </>
        );
      case 'holiday':
        return (
          <>
            <Select onValueChange={(value) => handleConstraintValueChange('countryCode', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Country code" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                <SelectItem value="IL">IL</SelectItem>
              </SelectContent>
            </Select>
          </>
        );


        case 'basketPrice':
          return (
            <>
              <Input
                id="min-price"
                placeholder="Min price (in dollars)"
                value={constraintValues.minPrice || ''}
                onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
                className="col-span-3 border border-black"
              />

              <div className="mt-2">
            {constraintValues.minPrice && isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          </div>
              <Input
                id="max-price"
                placeholder="Max price (in dollars)"
                value={constraintValues.maxPrice || ''}
                onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
                className="col-span-3 border border-black"
              />
              <div className="mt-2">
            {constraintValues.maxPrice && isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
           </div>
              <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Select store..." />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {mockStores.map((store) => (
                    <SelectItem key={store.value} value={store.value}>
                      {store.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </>
          );
        case 'productPrice':
          return (
            <>
              <Input
                id="min-price"
                placeholder="Min price (in dollars)"
                value={constraintValues.minPrice || ''}
                onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
                className="col-span-3 border border-black"
              />
              <div className="mt-2">
            {constraintValues.minPrice && isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
           </div>
              <Input
                id="max-price"
                placeholder="Max price (in dollars)"
                value={constraintValues.maxPrice || ''}
                onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
                className="col-span-3 border border-black"
              />
              <div className="mt-2">
            {constraintValues.maxPrice && isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
           </div>
              <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Select store..." />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {mockStores.map((store) => (
                    <SelectItem key={store.value} value={store.value}>
                      {store.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
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
            </>
          );

case 'categoryPrice':
  return (
    <>
      <Input
        id="min-price"
        placeholder="Min price (in dollars)"
        value={constraintValues.minPrice || ''}
        onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minPrice && isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
      </div>
      <Input
        id="max-price"
        placeholder="Max price (in dollars)"
        value={constraintValues.maxPrice || ''}
        onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.maxPrice && isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('category', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select category..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockCategories.map((category) => (
            <SelectItem key={category.value} value={category.value}>
              {category.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </>
  );
case 'basketAmount':
  return (
    <>
      <Input
        id="min-amount"
        placeholder="Min amount"
        value={constraintValues.minAmount || ''}
        onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minAmount && isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select store..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockStores.map((store) => (
            <SelectItem key={store.value} value={store.value}>
              {store.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </>
  );
case 'productAmount':
  return (
    <>
      <Input
        id="min-amount"
        placeholder="Min amount"
        value={constraintValues.minAmount || ''}
        onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minAmount && isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select store..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockStores.map((store) => (
            <SelectItem key={store.value} value={store.value}>
              {store.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
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
    </>
  );
case 'categoryAmount':
  return (
    <>
      <Input
        id="min-amount"
        placeholder="Min amount"
        value={constraintValues.minAmount || ''}
        onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minAmount && isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('category', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select category..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockCategories.map((category) => (
            <SelectItem key={category.value} value={category.value}>
              {category.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </>
  );
case 'categoryWeight':
  return (
    <>
      <Input
        id="min-weight"
        placeholder="Min weight (in kg)"
        value={constraintValues.minWeight || ''}
        onChange={(e) => handleConstraintValueChange('minWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minWeight && isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Input
        id="max-weight"
        placeholder="Max weight (in kg)"
        value={constraintValues.maxWeight || ''}
        onChange={(e) => handleConstraintValueChange('maxWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.maxWeight && isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('category', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select category..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockCategories.map((category) => (
            <SelectItem key={category.value} value={category.value}>
              {category.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </>
  );
case 'basketWeight':
  return (
    <>
      <Input
        id="min-weight"
        placeholder="Min weight (in kg)"
        value={constraintValues.minWeight || ''}
        onChange={(e) => handleConstraintValueChange('minWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minWeight && isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Input
        id="max-weight"
        placeholder="Max weight (in kg)"
        value={constraintValues.maxWeight || ''}
        onChange={(e) => handleConstraintValueChange('maxWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.maxWeight && isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select store..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockStores.map((store) => (
            <SelectItem key={store.value} value={store.value}>
              {store.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </>
  );
case 'productWeight':
  return (
    <>
      <Input
        id="min-weight"
        placeholder="Min weight (in kg)"
        value={constraintValues.minWeight || ''}
        onChange={(e) => handleConstraintValueChange('minWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.minWeight && isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Input
        id="max-weight"
        placeholder="Max weight (in kg)"
        value={constraintValues.maxWeight || ''}
        onChange={(e) => handleConstraintValueChange('maxWeight', e.target.value)}
        className="col-span-3 border border-black"
      />
      <div className="mt-2">
        {constraintValues.maxWeight && isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
      </div>
      <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
        <SelectTrigger className="col-span-3 border border-black bg-white">
          <SelectValue placeholder="Select store..." />
        </SelectTrigger>
        <SelectContent className="bg-white">
          {mockStores.map((store) => (
            <SelectItem key={store.value} value={store.value}>
              {store.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
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
    </>
  );
case 'compositeConstraint':
  return (
    <>
      <Input
        id="composite-constraint"
        placeholder="composite constraint: (and,(and (age 17), (or (time, 23, 00, 14, 00), (season, summer)))) "
        value={constraintValues.compositeConstraint || ''}
        onChange={(e) => handleConstraintValueChange('compositeConstraint', e.target.value)}
        className="col-span-3 border border-black"
      />
    </>
  );
default:
  return null;
}
};

const renderPolicy = (policy, type) => (
  <div 
    key={policy.purchase_policy_id} 
    className="mb-4 p-4 border-2 border-gray-300 rounded-md"
  >
    <button
      onClick={() => handleToggle(policy.purchase_policy_id, type)}
      className="text-left w-full"
    >
      {`Policy ID: ${policy.purchase_policy_id}`}
    </button>
    {expandedPolicies[type] === policy.purchase_policy_id && (
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
                {renderNestedPolicy(policy.left_policy_id)}
              </div>
            )}
            {expandedRightPolicy === policy.purchase_policy_id && (
              <div className="mt-2">
                {renderNestedPolicy(policy.right_policy_id)}
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
            <Button className="bg-blue-500 text-white py-1 px-3 rounded" onClick={() => handleOpenConstraintDialog(policy.purchase_policy_id)}>Add Constraint</Button>
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



const renderNestedPolicy = (policyId) => {
  
  console.log('renderNestedPolicy called with policyId:', policyId); // Add log
  const policyType = Object.keys(policies).find(type => 
    policies[type].some(p => p.purchase_policy_id === policyId)
  );

  console.log('policyType found:', policyType); // Add log

  if (!policyType) {
    return <p>Policy not found</p>;
  }

  const nestedPolicy = policies[policyType].find(p => p.purchase_policy_id === policyId);

  console.log('nestedPolicy found:', nestedPolicy); // Add log

  if (!nestedPolicy) {
    return <p>Policy not found</p>;
  }

  return (
    <div className="ml-4">
      <p><strong>Policy ID:</strong> {nestedPolicy.purchase_policy_id}</p>
      <p><strong>Store ID:</strong> {nestedPolicy.store_id}</p>
      <p><strong>Policy Name:</strong> {nestedPolicy.policy_name}</p>
      {policyType === 'productSpecific' && <p><strong>Product ID:</strong> {nestedPolicy.product_id}</p>}
      {policyType === 'categorySpecific' && <p><strong>Category ID:</strong> {nestedPolicy.category_id}</p>}
      {policyType === 'basketSpecific' && <p><strong>Constraints:</strong> {JSON.stringify(nestedPolicy.constraints)}</p>}
    </div>
  );
};


return (
  <div className="flex flex-wrap justify-center">
    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Product Specific Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.productSpecific.map((policy) => renderPolicy(policy, 'productSpecific'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'productSpecific'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('productSpecific')}>Add Product Policy</Button>
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
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="product" className="block mt-2">Choose Product</Label>
              <Select onValueChange={setSelectedProduct}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Choose Product" />
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
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Category Specific Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.categorySpecific.map((policy) => renderPolicy(policy, 'categorySpecific'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'categorySpecific'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('categorySpecific')}>Add Category Policy</Button>
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
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="category" className="block mt-2">Choose Category</Label>
              <Select onValueChange={setSelectedCategory}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Choose Category" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {mockCategories.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Basket Specific Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.basketSpecific.map((policy) => renderPolicy(policy, 'basketSpecific'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'basketSpecific'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('basketSpecific')}>Add Basket Policy</Button>
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
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">And Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.andPolicies.map((policy) => renderPolicy(policy, 'andPolicies'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'andPolicies'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('andPolicies')}>Add And Policy</Button>
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
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="left-policy" className="block mt-2">Policy 1</Label>
              <Select onValueChange={setSelectedLeftPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 1" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="right-policy" className="block mt-2">Policy 2</Label>
              <Select onValueChange={setSelectedRightPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 2" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Or Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.orPolicies.map((policy) => renderPolicy(policy, 'orPolicies'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'orPolicies'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('orPolicies')}>Add Or Policy</Button>
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
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="left-policy" className="block mt-2">Policy 1</Label>
              <Select onValueChange={setSelectedLeftPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 1" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="right-policy" className="block mt-2">Policy 2</Label>
              <Select onValueChange={setSelectedRightPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 2" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Conditional Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.conditionalPolicies.map((policy) => renderPolicy(policy, 'conditionalPolicies'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'conditionalPolicies'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('conditionalPolicies')}>Add Conditional Policy</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px] bg-white">
          <DialogHeader>
            <DialogTitle>Adding a Conditional policy</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            {errorMessage && (
              <div className="text-red-500 text-sm">{errorMessage}</div>
            )}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="policy-name" className="block mt-2">Policy Name</Label>
              <Input 
                id="policy-name" 
                placeholder="Policy Name"
                value={newPolicyName}
                onChange={(e) => setNewPolicyName(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="left-policy" className="block mt-2">Policy 1</Label>
              <Select onValueChange={setSelectedLeftPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 1" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="right-policy" className="block mt-2">Policy 2</Label>
              <Select onValueChange={setSelectedRightPolicy}>
                <SelectTrigger className="col-span-3 border border-black bg-white">
                  <SelectValue placeholder="Policy 2" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy.purchase_policy_id} value={policy.purchase_policy_id}>
                      {policy.policy_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <Dialog open={constraintDialogOpen} onOpenChange={setConstraintDialogOpen}>
      <DialogContent className="sm:max-w-[425px] bg-white">
        <DialogHeader>
          <DialogTitle>Adding a constraint</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {constraintError && (
            <div className="text-red-500 text-sm">{constraintError}</div>
          )}
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="constraint-type" className="block mt-2">Constraint Type</Label>
            <Select onValueChange={handleConstraintTypeChange}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Choose constraint type" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {constraintTypes.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          {renderConstraintFields()}
        </div>
        <DialogFooter>
          <Button type="button" onClick={handleSaveConstraint}>Save constraint</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
);

};

export default ManagePolicy;

