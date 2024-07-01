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
import { format } from 'date-fns';

import { MultiSelect } from 'react-multi-select-component';
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
import { DatePickerDemo } from "@/components/DatePickerDemo";



// Mock data for discounts
const mockDiscounts = {
  storeDiscounts: [
    {
      discount_id: 1,
      description: "Store Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      percentage: 10,
      store_id: "store1",
      constraints: []
    }
  ],
  categoryDiscounts: [
    {
      discount_id: 2,
      description: "Category Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      percentage: 15,
      category_id: "category1",
      apply_to_sub_categories: true,
      constraints: []
    }
  ],
  productDiscounts: [
    {
      discount_id: 3,
      description: "Product Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      percentage: 20,
      product_id: "product1",
      store_id: "store1",
      constraints: []
    }
  ],
  andDiscounts: [
    {
      discount_id: 4,
      description: "And Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      left_discount_id: 1,
      right_discount_id: 2
    }
  ],
  orDiscounts: [
    {
      discount_id: 5,
      description: "Or Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      left_discount_id: 2,
      right_discount_id: 3
    }
  ],
  xorDiscounts: [
    {
      discount_id: 6,
      description: "Xor Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      left_discount_id: 3,
      right_discount_id: 1
    }
  ],
  additiveDiscounts: [
    {
      discount_id: 7,
      description: "Additive Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      discounts: [1, 2, 3]
    }
  ],
  maxDiscounts: [
    {
      discount_id: 8,
      description: "Max Discount 1",
      starting_date: "2024-01-01",
      ending_date: "2024-12-31",
      discounts: [2, 3, 4]
    }
  ]
};

// Mock data for products
const mockProducts = [
  { value: 'product1', label: 'Product 1' },
  { value: 'product2', label: 'Product 2' },
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
];

const ManageDiscount = () => {
    const searchParams = useSearchParams();
    const id = searchParams.get('id');
    const [discounts, setDiscounts] = useState(mockDiscounts);
    const [selectedProduct, setSelectedProduct] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedLeftDiscount, setSelectedLeftDiscount] = useState('');
    const [selectedRightDiscount, setSelectedRightDiscount] = useState('');
    const [selectedMultipleDiscounts, setSelectedMultipleDiscounts] = useState([]);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [dialogType, setDialogType] = useState('');
    const [newDiscountDescription, setNewDiscountDescription] = useState('');
    const [newDiscountStartingDate, setNewDiscountStartingDate] = useState(null);
    const [newDiscountEndingDate, setNewDiscountEndingDate] = useState(null);
    const [newDiscountPercentage, setNewDiscountPercentage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [expandedDiscounts, setExpandedDiscounts] = useState({});
    const [expandedLeftDiscount, setExpandedLeftDiscount] = useState(null);
    const [expandedRightDiscount, setExpandedRightDiscount] = useState(null);
    const [expandedConstraint, setExpandedConstraint] = useState(null);
    const [constraintDialogOpen, setConstraintDialogOpen] = useState(false);
    const [selectedConstraintType, setSelectedConstraintType] = useState('');
    const [constraintValues, setConstraintValues] = useState({});
    const [currentDiscountId, setCurrentDiscountId] = useState(null);
    const [constraintError, setConstraintError] = useState('');
    const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
    const [editDiscountDescription, setEditDiscountDescription] = useState('');
    const [editDiscountPercentage, setEditDiscountPercentage] = useState('');
    const [editDiscountType, setEditDiscountType] = useState('');
  

  const generateUniqueId = () => {
    // Generate a unique ID based on the current timestamp and a random number
    return Date.now() + Math.floor(Math.random() * 1000);
  };

  const handleSaveChanges = () => {
    if (!newDiscountDescription) {
      setErrorMessage('Please enter a description.');
      return;
    }

    if (!newDiscountStartingDate || !newDiscountEndingDate) {
      setErrorMessage('Please select both starting and ending dates.');
      return;
    }

    const starting_date = format(newDiscountStartingDate, "yyyy-MM-dd");
    const ending_date = format(newDiscountEndingDate, "yyyy-MM-dd");

    let newDiscountId = generateUniqueId();
    let newDiscount;
    switch (dialogType) {
      case 'storeDiscounts':
        newDiscount = {
          discount_id: newDiscountId,
          description: newDiscountDescription,
          starting_date,
          ending_date,
          percentage: parseInt(newDiscountPercentage),
          store_id: selectedProduct,
          constraints: []
        };
        break;
      case 'categoryDiscounts':
        newDiscount = {
          discount_id: newDiscountId,
          description: newDiscountDescription,
          starting_date,
          ending_date,
          percentage: parseInt(newDiscountPercentage),
          category_id: selectedCategory,
          apply_to_sub_categories: selectedLeftDiscount === 'yes',
          constraints: []
        };
        break;
      case 'productDiscounts':
        newDiscount = {
          discount_id: newDiscountId,
          description: newDiscountDescription,
          starting_date,
          ending_date,
          percentage: parseInt(newDiscountPercentage),
          product_id: selectedProduct,
          store_id: selectedRightDiscount,
          constraints: []
        };
        break;
      case 'andDiscounts':
      case 'orDiscounts':
      case 'xorDiscounts':
        if (!selectedLeftDiscount || !selectedRightDiscount) {
          setErrorMessage('Please select both discounts.');
          return;
        }
        newDiscount = {
          discount_id: newDiscountId,
          description: newDiscountDescription,
          starting_date,
          ending_date,
          left_discount_id: parseInt(selectedLeftDiscount),
          right_discount_id: parseInt(selectedRightDiscount)
        };

        // Remove the selected discounts
        setDiscounts((prevDiscounts) => {
          const updatedDiscounts = { ...prevDiscounts };
          Object.keys(updatedDiscounts).forEach((type) => {
            updatedDiscounts[type] = updatedDiscounts[type].filter(
              (discount) =>
                discount.discount_id !== parseInt(selectedLeftDiscount) &&
                discount.discount_id !== parseInt(selectedRightDiscount)
            );
          });
          return updatedDiscounts;
        });
        break;
      case 'additiveDiscounts':
      case 'maxDiscounts':
        if (selectedMultipleDiscounts.length === 0) {
          setErrorMessage('Please select at least one discount.');
          return;
        }
        newDiscount = {
          discount_id: newDiscountId,
          description: newDiscountDescription,
          starting_date,
          ending_date,
          discounts: selectedMultipleDiscounts.map((value) => parseInt(value))
        };

        // Remove the selected discounts
        setDiscounts((prevDiscounts) => {
          const updatedDiscounts = { ...prevDiscounts };
          selectedMultipleDiscounts.forEach((selectedDiscountId) => {
            Object.keys(updatedDiscounts).forEach((type) => {
              updatedDiscounts[type] = updatedDiscounts[type].filter(
                (discount) => discount.discount_id !== parseInt(selectedDiscountId)
              );
            });
          });
          return updatedDiscounts;
        });
        break;
      default:
        return;
    }

    if (!['andDiscounts', 'orDiscounts', 'xorDiscounts', 'additiveDiscounts', 'maxDiscounts'].includes(dialogType)) {
      setDiscounts((prevDiscounts) => ({
        ...prevDiscounts,
        [dialogType]: [...prevDiscounts[dialogType], newDiscount],
      }));
    } else {
      setDiscounts((prevDiscounts) => ({
        ...prevDiscounts,
        [dialogType]: [...prevDiscounts[dialogType], newDiscount],
      }));
    }

    setIsDialogOpen(false);
    setNewDiscountDescription('');
    setNewDiscountPercentage('');
    setNewDiscountStartingDate(null);
    setNewDiscountEndingDate(null);
    setSelectedProduct('');
    setSelectedCategory('');
    setSelectedLeftDiscount('');
    setSelectedRightDiscount('');
    setSelectedMultipleDiscounts([]);
    setErrorMessage('');
  };

  const handleEditSaveChanges = () => {
    if (!editDiscountDescription) {
      setErrorMessage('Please enter a description.');
      return;
    }

    const updatedDiscounts = { ...discounts };
    const discountIndex = updatedDiscounts[editDiscountType].findIndex(
      (discount) => discount.discount_id === currentDiscountId
    );

    if (discountIndex !== -1) {
      updatedDiscounts[editDiscountType][discountIndex].description = editDiscountDescription;
      if (editDiscountType === 'storeDiscounts' || editDiscountType === 'categoryDiscounts' || editDiscountType === 'productDiscounts') {
        updatedDiscounts[editDiscountType][discountIndex].percentage = parseInt(editDiscountPercentage);
      }
    }

    setDiscounts(updatedDiscounts);
    setIsEditDialogOpen(false);
    setEditDiscountDescription('');
    setEditDiscountPercentage('');
  };

  const handleRemoveDiscount = (type, discountId) => {
    setDiscounts({
      ...discounts,
      [type]: discounts[type].filter(discount => discount.discount_id !== discountId)
    });
  };

  const handleToggle = (discountId, type) => {
    setExpandedDiscounts({
      ...expandedDiscounts,
      [type]: expandedDiscounts[type] === discountId ? null : discountId
    });
  };

  const handleToggleLeftDiscount = (discountId) => {
    setExpandedLeftDiscount(expandedLeftDiscount === discountId ? null : discountId);
  };

  const handleToggleRightDiscount = (discountId) => {
    setExpandedRightDiscount(expandedRightDiscount === discountId ? null : discountId);
  };

  const handleToggleConstraint = (discountId) => {
    setExpandedConstraint(expandedConstraint === discountId ? null : discountId);
  };



  const handleOpenDialog = (type) => {
    setDialogType(type);
    setIsDialogOpen(true);
    setNewDiscountDescription('');
    setNewDiscountStartingDate(null);
    setNewDiscountEndingDate(null);
    setNewDiscountPercentage('');
    setSelectedProduct('');
    setSelectedCategory('');
    setSelectedLeftDiscount('');
    setSelectedRightDiscount('');
    setSelectedMultipleDiscounts([]);
    setErrorMessage('');
  };

  const handleOpenEditDialog = (discountId, type) => {
    const discount = discounts[type].find((discount) => discount.discount_id === discountId);
    if (discount) {
      setCurrentDiscountId(discountId);
      setEditDiscountType(type);
      setEditDiscountDescription(discount.description);
      setEditDiscountPercentage(discount.percentage?.toString() || '');
      setIsEditDialogOpen(true);
    }
  };

  const handleOpenConstraintDialog = (discountId) => {
    setCurrentDiscountId(discountId);
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

    const updatedDiscounts = { ...discounts };
    const discountType = Object.keys(updatedDiscounts).find(type => 
      updatedDiscounts[type].some(discount => discount.discount_id === currentDiscountId)
    );

    const discountIndex = updatedDiscounts[discountType].findIndex(discount => 
      discount.discount_id === currentDiscountId
    );

    updatedDiscounts[discountType][discountIndex].constraints = [{
      type: selectedConstraintType,
      details: JSON.stringify(constraintValues)
    }];

    setDiscounts(updatedDiscounts);
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
  placeholder="Composite constraint: (and, (age, 17), (or, (time, 23, 00, 14, 00), (season, summer)))"
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

const renderDiscount = (discount, type) => (
<div 
key={discount.discount_id} 
className="mb-4 p-4 border-2 border-gray-300 rounded-md"
>
<button
onClick={() => handleToggle(discount.discount_id, type)}
className="text-left w-full"
>
{`Discount ID: ${discount.discount_id}`}
</button>
{expandedDiscounts[type] === discount.discount_id && (
<div className="mt-2">
<p><strong>Description:</strong> {discount.description}</p>
<p><strong>Starting Date:</strong> {discount.starting_date}</p>
<p><strong>Ending Date:</strong> {discount.ending_date}</p>
{discount.percentage && <p><strong>Percentage:</strong> {discount.percentage}%</p>}
{type === 'storeDiscounts' && <p><strong>Store ID:</strong> {discount.store_id}</p>}
{type === 'categoryDiscounts' && <p><strong>Category ID:</strong> {discount.category_id}</p>}
{type === 'productDiscounts' && (
<>
  <p><strong>Product ID:</strong> {discount.product_id}</p>
  <p><strong>Store ID:</strong> {discount.store_id}</p>
</>
)}
{['andDiscounts', 'orDiscounts', 'xorDiscounts'].includes(type) && (
<>
  <div className="flex justify-between">
    <button onClick={() => handleToggleLeftDiscount(discount.discount_id)} className="mt-2">Show Left Discount</button>
    <button onClick={() => handleToggleRightDiscount(discount.discount_id)} className="mt-2">Show Right Discount</button>
  </div>
  {expandedLeftDiscount === discount.discount_id && (
    <div className="mt-2">
      {renderNestedDiscount(discount.left_discount_id)}
    </div>
  )}
  {expandedRightDiscount === discount.discount_id && (
    <div className="mt-2">
      {renderNestedDiscount(discount.right_discount_id)}
    </div>
  )}
</>
)}
{['additiveDiscounts', 'maxDiscounts'].includes(type) && (
<button className="mt-2" onClick={() => handleToggleConstraint(discount.discount_id)}>Show Discounts</button>
)}
{expandedConstraint === discount.discount_id && discount.discounts && (
<div className="mt-2">
  {discount.discounts.map((id) => renderNestedDiscount(id))}
</div>
)}
{['storeDiscounts', 'categoryDiscounts', 'productDiscounts'].includes(type) && (
<button className="mt-2" onClick={() => handleToggleConstraint(discount.discount_id)}>Show Constraints</button>
)}
{expandedConstraint === discount.discount_id && discount.constraints && (
<div className="mt-2">
  {discount.constraints.map((constraint, index) => (
    <p key={index}>{constraint.type}: {constraint.details}</p>
  ))}
</div>
)}
<div className="flex justify-between mt-4">
{['storeDiscounts', 'categoryDiscounts', 'productDiscounts'].includes(type) && (
  <Button className="bg-blue-500 text-white py-1 px-3 rounded" onClick={() => handleOpenConstraintDialog(discount.discount_id)}>Add Constraint</Button>
)}
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button className="bg-red-500 text-white py-1 px-3 rounded">Remove Discount</Button>
  </AlertDialogTrigger>
  <AlertDialogContent className="bg-white">
    <AlertDialogHeader>
      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. This will permanently delete the discount.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={() => handleRemoveDiscount(type, discount.discount_id)}>Yes, remove discount</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
<Button className="bg-green-500 text-white py-1 px-3 rounded" onClick={() => handleOpenEditDialog(discount.discount_id, type)}>Edit Discount</Button>
</div>
</div>
)}
</div>
);

const renderNestedDiscount = (discountId) => {
const discountType = Object.keys(discounts).find(type => 
discounts[type].some(d => d.discount_id === discountId)
);

if (!discountType) {
return <p>Discount not found</p>;
}

const nestedDiscount = discounts[discountType].find(d => d.discount_id === discountId);

if (!nestedDiscount) {
return <p>Discount not found</p>;
}

return (
<div className="ml-4">
<p><strong>Discount ID:</strong> {nestedDiscount.discount_id}</p>
<p><strong>Description:</strong> {nestedDiscount.description}</p>
<p><strong>Starting Date:</strong> {nestedDiscount.starting_date}</p>
<p><strong>Ending Date:</strong> {nestedDiscount.ending_date}</p>
{nestedDiscount.percentage && <p><strong>Percentage:</strong> {nestedDiscount.percentage}%</p>}
{discountType === 'storeDiscounts' && <p><strong>Store ID:</strong> {nestedDiscount.store_id}</p>}
{discountType === 'categoryDiscounts' && <p><strong>Category ID:</strong> {nestedDiscount.category_id}</p>}
{discountType === 'productDiscounts' && (
<>
<p><strong>Product ID:</strong> {nestedDiscount.product_id}</p>
<p><strong>Store ID:</strong> {nestedDiscount.store_id}</p>
</>
)}
</div>
);
};

return (
    <div className="flex flex-wrap justify-center">
      {/* Render all discount types here */}
      {Object.keys(discounts).map((type) => (
        <div key={type} className="w-full max-w-md p-4">
          <h2 className="text-center font-bold mb-4">{type.replace(/([A-Z])/g, ' $1').trim()} Discounts</h2>
          <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
            {discounts[type].map((discount) => renderDiscount(discount, type))}
          </ScrollArea>
          <Dialog open={isDialogOpen && dialogType === type} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog(type)}>Add {type.replace(/([A-Z])/g, ' $1').trim()} Discount</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px] bg-white">
              <DialogHeader>
                <DialogTitle>Adding a {type.replace(/([A-Z])/g, ' $1').trim()} discount</DialogTitle>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                {errorMessage && (
                  <div className="text-red-500 text-sm">{errorMessage}</div>
                )}
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="block mt-2">Description</Label>
                  <Input
                    id="description"
                    placeholder="Description"
                    value={newDiscountDescription}
                    onChange={(e) => setNewDiscountDescription(e.target.value)}
                    className="col-span-3 border border-black"
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="starting-date" className="block mt-2">Starting Date</Label>
                  <DatePickerDemo
                    selectedDate={newDiscountStartingDate}
                    onDateChange={setNewDiscountStartingDate}
                    className="col-span-3 wider-date-picker"
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="ending-date" className="block mt-2">Ending Date</Label>
                  <DatePickerDemo
                    selectedDate={newDiscountEndingDate}
                    onDateChange={setNewDiscountEndingDate}
                    className="col-span-3 wider-date-picker"
                  />
                </div>
                {['storeDiscounts', 'categoryDiscounts', 'productDiscounts'].includes(type) && (
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="percentage" className="block mt-2">Percentage</Label>
                    <Input
                      id="percentage"
                      placeholder="Percentage"
                      value={newDiscountPercentage}
                      onChange={(e) => setNewDiscountPercentage(e.target.value)}
                      className="col-span-3 border border-black"
                    />
                  </div>
                )}
                {type === 'storeDiscounts' && (
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="store-id" className="block mt-2">Store ID</Label>
                    <Select onValueChange={setSelectedProduct}>
                      <SelectTrigger className="col-span-3 border border-black bg-white">
                        <SelectValue placeholder="Store ID" />
                      </SelectTrigger>
                      <SelectContent className="bg-white">
                        {mockStores.map((store) => (
                          <SelectItem key={store.value} value={store.value}>
                            {store.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
                {type === 'categoryDiscounts' && (
                  <>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="category-id" className="block mt-2">Category ID</Label>
                      <Select onValueChange={setSelectedCategory}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Category ID" />
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
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="apply-sub-categories" className="block mt-2">Apply to Sub Categories</Label>
                      <Select onValueChange={setSelectedLeftDiscount}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Apply to Sub Categories" />
                        </SelectTrigger>
                        <SelectContent className="bg-white">
                          <SelectItem value="yes">YES</SelectItem>
                          <SelectItem value="no">NO</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </>
                )}
                {type === 'productDiscounts' && (
                  <>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="store-id" className="block mt-2">Store ID</Label>
                      <Select onValueChange={setSelectedProduct}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Store ID" />
                        </SelectTrigger>
                        <SelectContent className="bg-white">
                          {mockStores.map((store) => (
                            <SelectItem key={store.value} value={store.value}>
                              {store.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="product-id" className="block mt-2">Product ID</Label>
                      <Select onValueChange={setSelectedRightDiscount}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Product ID" />
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
                  </>
                )}
                {['andDiscounts', 'orDiscounts', 'xorDiscounts'].includes(type) && (
                  <>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="left-discount-id" className="block mt-2">Discount 1</Label>
                      <Select onValueChange={setSelectedLeftDiscount}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Select Discount 1" />
                        </SelectTrigger>
                        <SelectContent className="bg-white">
                          {Object.values(discounts).flat().map((discount) => (
                            <SelectItem key={discount.discount_id} value={discount.discount_id}>
                              {discount.description}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="right-discount-id" className="block mt-2">Discount 2</Label>
                      <Select onValueChange={setSelectedRightDiscount}>
                        <SelectTrigger className="col-span-3 border border-black bg-white">
                          <SelectValue placeholder="Select Discount 2" />
                        </SelectTrigger>
                        <SelectContent className="bg-white">
                          {Object.values(discounts).flat().map((discount) => (
                            <SelectItem key={discount.discount_id} value={discount.discount_id}>
                              {discount.description}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </>
                )}
                {['additiveDiscounts', 'maxDiscounts'].includes(type) && (
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="discounts" className="block mt-2">Discounts</Label>
                    <MultiSelect
                      options={Object.values(discounts).flat().map((discount) => ({
                        label: discount.description,
                        value: discount.discount_id.toString()
                      }))}
                      value={selectedMultipleDiscounts}
                      onChange={setSelectedMultipleDiscounts}
                      labelledBy="Select Discounts"
                      className="wider-select"
                    />
                  </div>
                )}
              </div>
              <DialogFooter>
                <Button type="button" onClick={handleSaveChanges}>Save changes</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      ))}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[425px] bg-white">
          <DialogHeader>
            <DialogTitle>Editing a discount</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            {errorMessage && (
              <div className="text-red-500 text-sm">{errorMessage}</div>
            )}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="edit-description" className="block mt-2">Change Description</Label>
              <Input
                id="edit-description"
                placeholder="Change Description"
                value={editDiscountDescription}
                onChange={(e) => setEditDiscountDescription(e.target.value)}
                className="col-span-3 border border-black"
              />
            </div>
            {['storeDiscounts', 'categoryDiscounts', 'productDiscounts'].includes(editDiscountType) && (
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-percentage" className="block mt-2">Change Percentage</Label>
                <Input
                  id="edit-percentage"
                  placeholder="Change Percentage"
                  value={editDiscountPercentage}
                  onChange={(e) => setEditDiscountPercentage(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
            )}
          </div>
          <DialogFooter>
            <Button type="button" onClick={handleEditSaveChanges}>Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
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
  
  export default ManageDiscount;
  
