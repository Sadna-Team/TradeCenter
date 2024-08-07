"use client";
import api from '@/lib/api';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { ScrollArea } from '@/components/ScrollArea';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/Dialog";
import { format } from 'date-fns';
import { Input } from "@/components/Input";
import { Label } from "@/components/Label";
import Button from "@/components/Button";
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

const constraintTypes = [
  { value: 'age', label: 'Age constraint' },
  { value: 'location', label: 'Location constraint' },
  { value: 'time', label: 'Time constraint' },
  { value: 'day_of_month', label: 'Day of month constraint' },
  { value: 'day_of_week', label: 'Day of week constraint' },
  { value: 'season', label: 'Season constraint' },
  { value: 'holidays_of_country', label: 'Holiday constraint' },
  { value: 'price_basket', label: 'Basket price constraint' },
  { value: 'price_product', label: 'Product price constraint' },
  { value: 'price_category', label: 'Category price constraint' },
  { value: 'weight_basket', label: 'Basket weight constraint' },
  { value: 'weight_product', label: 'Product weight constraint' },
  { value: 'weight_category', label: 'Category weight constraint' },
  { value: 'amount_basket', label: 'Basket amount constraint' },
  { value: 'amount_product', label: 'Product amount constraint' },
  { value: 'amount_category', label: 'Category amount constraint' },
  { value: 'compositeConstraint', label: 'Composite Constraint' },
];

const ManageDiscount = () => {
  const [errorMessage, setErrorMessage] = useState('');

  const searchParams = useSearchParams();
  const store_id = searchParams.get('id');

  //data required for our page
  const [discounts, setDiscounts] = useState([]);
  const [stores, setStores] = useState({});
  const [products_to_store, setProductsToStore] = useState([]);
  const [categories, setCategories] = useState({});

  // states for our dialog
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState('');
  

  // data for adding new discount
  const [newDiscountDescription, setNewDiscountDescription] = useState('');
  const [newDiscountStartingDate, setNewDiscountStartingDate] = useState('');
  const [newDiscountEndingDate, setNewDiscountEndingDate] = useState('');
  const [newDiscountPercentage, setNewDiscountPercentage] = useState(null);
  const [newIsSubApplied, setNewIsSubApplied] = useState(false);
  
  //data for composite discounts
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedLeftDiscount, setSelectedLeftDiscount] = useState('');
  const [selectedRightDiscount, setSelectedRightDiscount] = useState('');
  const [selectedMultipleDiscounts, setSelectedMultipleDiscounts] = useState([]);

  const [expandedDiscounts, setExpandedDiscounts] = useState({});
  const [expandedLeftDiscounts, setExpandedLeftDiscounts] = useState({});
  const [expandedRightDiscounts, setExpandedRightDiscounts] = useState({});
  const [expandedConstraints, setExpandedConstraints] = useState({});
  const [expandedMultipleDiscounts, setExpandedMultipleDiscounts] = useState({});

  const [constraintDialogOpen, setConstraintDialogOpen] = useState(false);
  const [selectedConstraintType, setSelectedConstraintType] = useState('');
  const [constraintValues, setConstraintValues] = useState({});
  const [currentDiscountId, setCurrentDiscountId] = useState(null);

  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editDiscountDescription, setEditDiscountDescription] = useState('');
  const [editDiscountPercentage, setEditDiscountPercentage] = useState('');
  const [editDiscountType, setEditDiscountType] = useState('');


  useEffect(() => {
    fetchDiscounts();
    fetchStores();
    fetchCategories();
  }, []);


  const fetchDiscounts = async () => {
    try {
      const response = await api.post('/store/view_discounts_info',{'store_id': store_id});
      if(response.status !== 200){
        console.error('Failed to fetch discounts', response);
        setErrorMessage('Failed to fetch discounts');
        return;
      }
      console.log("the discounts of the system:", response.data.message)
      let data = response.data.message;
  
      if(data === null || data === undefined) {
        console.error('Failed to fetch policies of store', response);
        setErrorMessage('Failed to fetch policies of store');
        return;
      }

      let storeDiscount = [];
      let categoryDiscount = [];
      let productDiscount = [];
      let andDiscount = [];
      let orDiscount = [];
      let xorDiscount = [];
      let additiveDiscount = [];
      let maxDiscount = [];
    
      for(let i = 0; i < data.length; i++){
        console.log("the current discount is:", data[i]);
        if(data[i].discount_type === 'storeDiscount'){
          storeDiscount.push(data[i]);
        }else if(data[i].discount_type === 'categoryDiscount'){
          categoryDiscount.push(data[i]);
        }else if(data[i].discount_type === 'productDiscount'){
          productDiscount.push(data[i]);
        }else if(data[i].discount_type === 'andDiscount'){
          andDiscount.push(data[i]);
        }else if(data[i].discount_type === 'orDiscount'){
          orDiscount.push(data[i]);
        }else if(data[i].discount_type === 'xorDiscount'){
          xorDiscount.push(data[i]);
        }else if(data[i].discount_type === 'additiveDiscount'){
          additiveDiscount.push(data[i]);
        }else if(data[i].discount_type === 'maxDiscount'){
          maxDiscount.push(data[i]);
        }else{
          console.error('Unknown discount type:', data[i].discount_type);
          setErrorMessage('Unknown discount type');
        }
      }

      let discounts = {
        storeDiscount: storeDiscount,
        categoryDiscount: categoryDiscount,
        productDiscount: productDiscount,
        andDiscount: andDiscount,
        orDiscount: orDiscount,
        xorDiscount: xorDiscount,
        additiveDiscount: additiveDiscount,
        maxDiscount: maxDiscount
      }

      setDiscounts(discounts);
    } catch (error) {
      console.error('Failed to fetch discounts', error);
      setErrorMessage('Failed to fetch discounts');
    }
  };

  const fetchStores = async () => {
    try {
      const response = await api.get('/store/store_ids_to_names');
      if(response.status !== 200){
        console.error('Failed to fetch stores', response);
        setErrorMessage('Failed to fetch stores');
        return;
      }
      console.log("the stores:", response.data.message);
      let data = response.data.message;
  
      if(data === null || data === undefined) {
        console.error('Failed to fetch stores', response);
        setErrorMessage('Failed to fetch stores');
        return;
      }
  
      setStores(data);

      //fetching the products of each store
      let products_data = [];
      console.log("Trying to add the products of each store");
      for(let key of Object.keys(data)){
        console.log("Adding products of store:", key)
        const product_response = await api.post(`/store/store_products`, { 'store_id': key });
        if(product_response.status !== 200){
          console.error('Failed to fetch products of store', product_response);
          setErrorMessage('Failed to fetch products');
          return;
        }
        console.log("the products of the store:", product_response.data.message);
        let product_data = product_response.data.message;

        if(product_data === null || product_data === undefined) {
          console.error('Failed to fetch products of store', product_response);
          setErrorMessage('Failed to fetch products of store');
          return;
        }
        products_data.push({ store_id: key, products: product_data });
      }

      setProductsToStore(products_data);

    } catch (error) {
      console.error('Failed to fetch stores', error);
      setErrorMessage('Failed to fetch stores');
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/store/category_ids_to_names');
      if(response.status !== 200){
        console.error('Failed to fetch categories', response);
        setErrorMessage('Failed to fetch categories');
        return;
      }
      console.log("the categories:", response.data.message);
      let data = response.data.message;
  
      if(data === null || data === undefined) {
        console.error('Failed to fetch categories', response);
        setErrorMessage('Failed to fetch categories');
        return;
      }
  
      setCategories(data);
    } catch (error) {
      console.error('Failed to fetch categories', error);
      setErrorMessage('Failed to fetch categories');
    }
  };


  // Function responsible for adding a new discount
  const handleSaveChanges = () => {
    if (!newDiscountStartingDate || !newDiscountEndingDate) {
      setErrorMessage('Please select both starting and ending dates.');
      return;
    }

    let percentage;
    if (dialogType === 'productDiscount' || dialogType === 'categoryDiscount' || dialogType === 'storeDiscount') {
      if (newDiscountPercentage === '' || isNaN(parseFloat(newDiscountPercentage))) {
        setErrorMessage('Please enter a percentage.');
        return;
      }
      percentage = parseFloat(newDiscountPercentage);
      if(percentage < 0 || percentage > 100){
        setErrorMessage('Please enter a percentage between 0 and 100.');
        return;
      }

      percentage = percentage/100;
    }
    

    const starting_date = format(newDiscountStartingDate, "yyyy-MM-dd");
    const ending_date = format(newDiscountEndingDate, "yyyy-MM-dd");

    if (!newDiscountDescription) {
      setErrorMessage('Please enter a description.');
      return;
    }

    let data;
    console.log("the dialog type is:", dialogType);
    switch (dialogType) {
      case 'storeDiscount':
        data = {
          description: newDiscountDescription,
          start_date: starting_date,
          end_date: ending_date,
          percentage: percentage,
          store_id: store_id,
        };
        break;
      case 'categoryDiscount':
        if (selectedCategory === null || selectedCategory === '' || selectedCategory === undefined) {
          setErrorMessage('Please select a category.');
          return;
        }

        data = {
          description: newDiscountDescription,
          start_date: starting_date,
          end_date: ending_date,
          percentage: percentage,
          category_id: selectedCategory,
          applied_to_sub: newIsSubApplied,
          store_id: store_id,
        };
        break;
      case 'productDiscount':
        if (selectedProduct === null || selectedProduct === '' || selectedProduct === undefined) {
          setErrorMessage('Please select a product.');
          return;
        }

        data = {
          description: newDiscountDescription,
          start_date: starting_date,
          end_date: ending_date,
          percentage: percentage,
          product_id: selectedProduct,
          store_id: store_id,
        };
        break;
      case 'andDiscount':
      case 'orDiscount':
      case 'xorDiscount':
        if (selectedLeftDiscount === '' || !selectedRightDiscount === '') {
          setErrorMessage('Please select both discounts.');
          return;
        }
        let type_of_discount = 1;
        if(dialogType === 'orDiscount'){
          type_of_discount = 2;
        }else if(dialogType === 'xorDiscount'){
          type_of_discount = 3;
        }
        data = {
          description: newDiscountDescription,
          start_date: starting_date,
          end_date: ending_date,
          discount_id1: parseInt(selectedLeftDiscount),
          discount_id2: parseInt(selectedRightDiscount),
          type_of_composite: type_of_discount,
          store_id: store_id,
        };
        break;


      case 'additiveDiscount':
      case 'maxDiscount':
        if (selectedMultipleDiscounts.length === 0) {
          setErrorMessage('Please select at least one discount.');
          return;
        }
        let type_of_composite =1;
        if(dialogType === 'additiveDiscount'){
          type_of_composite = 2;
        }

        console.log("the selected multiple discounts:", selectedMultipleDiscounts);
        data = {
          description: newDiscountDescription,
          start_date: starting_date,
          end_date: ending_date,
          discount_ids: selectedMultipleDiscounts.map((value) => parseInt(value.value)),
          type_of_composite: type_of_composite,
          store_id: store_id,
        };
        break;
      default:
        return;
    }

    const saveDiscount = async () => {
      try {
        console.log("the discount data: ", data)
        if(dialogType === 'storeDiscount' || dialogType === 'categoryDiscount' || dialogType === 'productDiscount'){
          const response = await api.post('/store/add_discount', data);
          if(response.status !== 200){
            console.error('Failed to add discount', response);
            setErrorMessage('Failed to add discount');
            return;
          }
          console.log("the response of adding discount:", response.data.message);
        }else if(dialogType === 'andDiscount' || dialogType === 'orDiscount' || dialogType === 'xorDiscount'){
          const response = await api.post('/store/create_logical_composite', data);
          if(response.status !== 200){
            console.error('Failed to add discount', response);
            setErrorMessage('Failed to add discount');
            return;
          }
          console.log("the response of adding discount:", response.data.message);
        } else if(dialogType === 'additiveDiscount' || dialogType === 'maxDiscount'){
          const response = await api.post('/store/create_numerical_composite', data);
          if(response.status !== 200){
            console.error('Failed to add discount', response);
            setErrorMessage('Failed to add discount');
            return;
          }
          console.log("the response of adding discount:", response.data.message);
        }
      }
      catch (error) {
        console.error('Failed to add discount', error);
        setErrorMessage('Failed to add discount');
      }
    };

    saveDiscount();
    setIsDialogOpen(false);
    setNewDiscountDescription('');
    setNewDiscountPercentage('');
    setNewDiscountStartingDate('');
    setNewDiscountEndingDate('');
    setNewIsSubApplied(false);
    setSelectedProduct('');
    setSelectedCategory('');
    setSelectedLeftDiscount('');
    setSelectedRightDiscount('');
    setSelectedMultipleDiscounts([]);
    setErrorMessage('');
    fetchDiscounts();
  };

  //function responsible for editing a discount
  const handleEditSaveChanges = () => {
    const editDiscount = async () => {
      let data;
      if (editDiscountDescription !== ''){
        data = {
          discount_id: currentDiscountId,
          description: editDiscountDescription,
          store_id: store_id,
        }

        try {
          const response = await api.post('/store/change_discount_description', data);
          if(response.status !== 200){
            console.error('Failed to edit discount', response);
            setErrorMessage('Failed to edit discount');
            return;
          }
          console.log("the response of editing discount:", response.data.message);
          fetchDiscounts();
          setErrorMessage('');
        }
        catch (error) {
          console.error('Failed to edit discount', error);
          setErrorMessage('Failed to edit discount');
        }
      }

      if (editDiscountPercentage !== ''){
        let percentage = parseFloat(editDiscountPercentage);
        if(percentage < 0 || percentage > 100){
          setErrorMessage('Please enter a percentage between 0 and 100.');
          return;
        }

        percentage = percentage/100;
        data = {
          discount_id: currentDiscountId,
          percentage: percentage,
          store_id: store_id,
        }

        try {
          const response = await api.post('/store/change_discount_percentage', data);
          if(response.status !== 200){
            console.error('Failed to edit discount', response);
            setErrorMessage('Failed to edit discount');
            return;
          }
          console.log("the response of editing discount:", response.data.message);
          fetchDiscounts();
          setErrorMessage('');
        }
        catch (error) {
          console.error('Failed to edit discount', error);
          setErrorMessage('Failed to edit discount');
        }
      }
    }
    
    editDiscount();
    setIsEditDialogOpen(false);
    setEditDiscountDescription('');
    setEditDiscountPercentage('');
    setErrorMessage('');
    fetchDiscounts();
  };


  const handleRemoveDiscount = (type, discountId) => {
    const removeDiscount = async () => {
      try {
        const response = await api.post('/store/remove_discount', { discount_id: discountId, store_id: store_id});
        if(response.status !== 200){
          console.error('Failed to remove discount', response);
          setErrorMessage('Failed to remove discount');
          return;
        }
        console.log("the response of removing discount:", response.data.message);
        fetchDiscounts();
        setErrorMessage('');
      } catch (error) {
        console.error('Failed to remove discount', error);
        setErrorMessage('Failed to remove discount');
      }
    };

    removeDiscount();
  };

  
  const handleOpenDialog = (type) => {
    setDialogType(type);
    setIsDialogOpen(true);
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
    // Check if the value is a valid number
    const numberValue = Number(value);
    if (!isNaN(numberValue)) {
      setConstraintValues({ ...constraintValues, [field]: numberValue });
    } else {
      // Handle non-numeric values if necessary
      setConstraintValues({ ...constraintValues, [field]: value });
    } 
  };

 // Function responsible for adding a new constraint to a discount
 const handleSaveConstraint = async () => {
  const parseConstraintString = (constraintStr) => {
    const splitRegex = /[\s,]+/;
  
    const convertToNumber = (s) => {
      if (!isNaN(parseInt(s))) {
        return parseInt(s);
      }
      if (!isNaN(parseFloat(s))) {
        return parseFloat(s);
      }
      return s;
    };
  
    const parse = (s) => {
      const tokens = s.replace(/[()]/g, '').trim().split(splitRegex);
      return tokens.map((token) => convertToNumber(token));
    };
  
    const cleanStr = constraintStr.replace(/\s+/g, ' ').trim();
    return parse(cleanStr);
  };
  
  
  const simpleComponents = ['age', 'time', 'location', 'day_of_month', 'day_of_week', 'season', 'holidays_of_country', 'price_basket', 'price_product', 'price_category', 'amount_basket', 'amount_product', 'amount_category', 'weight_category', 'weight_basket', 'weight_product'];
  const compositeComponents = ['and', 'or', 'xor', 'implies'];
  
  const buildNestedArray = (parsedComposite, index) => {
    let properties = [];
    let constraintType = '';
    for (let i = index; i < parsedComposite.length; i++) {
      if (compositeComponents.includes(parsedComposite[i])) {
        let left, right, newIndex;
        [left, newIndex] = buildNestedArray(parsedComposite, i + 1);
        [right, newIndex] = buildNestedArray(parsedComposite, newIndex + 1);
        return [[parsedComposite[i], left, right], newIndex];
      } else if (simpleComponents.includes(parsedComposite[i])) {
        if (constraintType === '') {
          constraintType = parsedComposite[i];
        } else {
          return [[constraintType, ...properties], i - 1];
        }
      } else {
        properties.push(parsedComposite[i]);
      }
    }
    return [[constraintType, ...properties], parsedComposite.length];
  };
  
  let data;
  switch(selectedConstraintType){
    case 'compositeConstraint':
      const parsedComposite = parseConstraintString(`(${constraintValues.compositeConstraint})`);
  
      const [finalComposite] = buildNestedArray(parsedComposite, 0);
      console.log("the final composite constraint:", finalComposite);
    
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: finalComposite,
      };

      console.log("the first variable of the predicate_builder is " + data.predicate_builder[0])
      break;

    case 'age': 
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['age']],
      };
      break;
    
    case 'time':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['startingHour'], constraintValues['startingMinute'], constraintValues['endingHour'], constraintValues['endingMinute']],
      };
      break;

    case 'location':
      let location = {'address': constraintValues['address'], 'city': constraintValues['city'], 'state': constraintValues['state'], 'country': constraintValues['country'], 'zip_code': constraintValues['zipCode']}
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, location],
      };
      break;

    case 'day_of_month':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['startingDay'], constraintValues['endingDay']],
      };
      break;

    case 'day_of_week':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['startingDay'], constraintValues['endingDay']],
      };
      break;

    case 'season':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['season']],
      };
      break;

    case 'holidays_of_country':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['countryCode']],
      };
      break;

    case 'price_basket':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['store']],
      };
      break;

    case 'price_product':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['product'], constraintValues['store']],
      };
      break;

    case 'price_category':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['category']],
      };
      break;

    case 'amount_basket':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['store']],
      };
      break;

    case 'amount_product':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['product'], constraintValues['store']],
      };
      break;

    case 'amount_category':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['category']],
      };
      break;

    case 'weight_category':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['category']],
      };
      break;

    case 'weight_basket':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['store']],
      };
      break;

    case 'weight_product':
      data = {
        discount_id: currentDiscountId,
        store_id: store_id,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['product'], constraintValues['store']],
      };
      break;

    default:
      return;
  }
    
  console.log(`predicate builder of current constraint of type ${selectedConstraintType} we are trying to add is: ${data.predicate_builder}`);

  try {
    const response = await api.post('/store/assign_predicate_to_discount', data);
    if (response.status !== 200) {
      setErrorMessage('Failed to save constraint');
      return;
    }
    fetchDiscounts();
    setConstraintDialogOpen(false);
    setSelectedConstraintType('');
    setConstraintValues({});
  } catch (error) {
    console.error('Error saving constraint:', error);
    setErrorMessage('Failed to save constraint');
  }
};

const renderConstraintFields = () => {
  switch (selectedConstraintType) {
    case 'age':
      return (
        <>
          <Input
            id="age-limit"
            placeholder="Enter age limit"
            value={constraintValues.age || ''}
            onChange={(e) => handleConstraintValueChange('age', e.target.value)}
            className="col-span-3 border border-black mt-2"
          />
          {isNaN(constraintValues.age) && <p className="text-red-500">Not a number</p>}
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
          {isNaN(constraintValues.zipCode) && <p className="text-red-500">Not a number</p>}
        </>
      );

    case 'day_of_month':
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

    case 'day_of_week':
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

    case 'holidays_of_country':
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

    case 'price_basket':
      return (
        <>
          <Input
            id="min-price"
            placeholder="Min price (in dollars)"
            value={constraintValues.minPrice || ''}
            onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'price_product':
      return (
        <>
          <Input
            id="min-price"
            placeholder="Min price (in dollars)"
            value={constraintValues.minPrice || ''}
            onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {(constraintValues.store !== null || constraintValues.store !== '' || constraintValues.store !== undefined) && (
            <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Select product..." />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {products_to_store
                  .filter((store) => parseInt(store.store_id) === constraintValues.store)
                  .flatMap((store) => store.products)
                  .map((product) => (
                    <SelectItem key={product.product_id} value={product.product_id}>
                      {product.name}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          )}
        </>
      );

    case 'price_category':
      return (
        <>
          <Input
            id="min-price"
            placeholder="Min price (in dollars)"
            value={constraintValues.minPrice || ''}
            onChange={(e) => handleConstraintValueChange('minPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('category', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select category..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.values(categories).map((category) => (
                <SelectItem key={category.category_id} value={category.category_id}>
                  {category.category_name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'amount_basket':
      return (
        <>
          <Input
            id="min-amount"
            placeholder="Min amount"
            value={constraintValues.minAmount || ''}
            onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          { isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxAmount) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'amount_product':
      return (
        <>
          <Input
            id="min-amount"
            placeholder="Min amount"
            value={constraintValues.minAmount || ''}
            onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="Max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxAmount) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {(constraintValues.store !== null || constraintValues.store !== '' || constraintValues.store !== undefined ) && (
            <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Select product..." />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {products_to_store
                  .filter((store) => parseInt(store.store_id) === constraintValues.store)
                  .flatMap((store) => store.products)
                  .map((product) => (
                    <SelectItem key={product.product_id} value={product.product_id}>
                      {product.name}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          )}
        </>
      );

    case 'amount_category':
      return (
        <>
          <Input
            id="min-amount"
            placeholder="Min amount"
            value={constraintValues.minAmount || ''}
            onChange={(e) => handleConstraintValueChange('minAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="Max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxAmount) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('category', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select category..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.values(categories).map((category) => (
                <SelectItem key={category.category_id} value={category.category_id}>
                  {category.category_name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'weight_category':
      return (
        <>
          <Input
            id="min-weight"
            placeholder="Min weight (in kg)"
            value={constraintValues.minWeight || ''}
            onChange={(e) => handleConstraintValueChange('minWeight', (e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', (e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('category', (value))}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select category..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
            {Object.values(categories).map((category) => (
                  <SelectItem key={category.category_id} value={category.category_id}>
                    {category.category_name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'weight_basket':
      return (
        <>
          <Input
            id="min-weight"
            placeholder="Min weight (in kg)"
            value={constraintValues.minWeight || ''}
            onChange={(e) => handleConstraintValueChange('minWeight', (e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', (e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', (value))}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </>
      );

    case 'weight_product':
      return (
        <>
          <Input
            id="min-weight"
            placeholder="Min weight (in kg)"
            value={constraintValues.minWeight || ''}
            onChange={(e) => handleConstraintValueChange('minWeight', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', e.target.value)}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', value)}>
            <SelectTrigger className="col-span-3 border border-black bg-white">
              <SelectValue placeholder="Select store..." />
            </SelectTrigger>
            <SelectContent className="bg-white">
              {Object.keys(stores).map((key) => (
                <SelectItem key={key} value={key}>
                  {stores[key]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {(constraintValues.store !== null || constraintValues.store !== '' || constraintValues.store !== undefined)&& (
            <Select onValueChange={(value) => handleConstraintValueChange('product', value)}>
              <SelectTrigger className="col-span-3 border border-black bg-white">
                <SelectValue placeholder="Select product..." />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {products_to_store
                  .filter((store) => parseInt(store.store_id) === constraintValues.store)
                  .flatMap((store) => store.products)
                  .map((product) => (
                    <SelectItem key={product.product_id} value={product.product_id}>
                      {product.name}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          )}
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



const handleToggle = (discountId, type) => {
  setExpandedDiscounts(prevState => ({
    ...prevState,
    [type]: prevState[type] === discountId ? null : discountId
  }));
};


const handleToggleLeftDiscount = (discountId) => {
  setExpandedLeftDiscounts(prevState => ({
    ...prevState,
    [discountId]: !prevState[discountId]
  }));
};

const handleToggleRightDiscount = (discountId) => {
  setExpandedRightDiscounts(prevState => ({
    ...prevState,
    [discountId]: !prevState[discountId]
  }));
};

const handleToggleMultipleDiscounts = (discountId) => {
  setExpandedMultipleDiscounts(prevState => ({
    ...prevState,
    [discountId]: !prevState[discountId]
  }));
};

const handleToggleConstraint = (discountId) => {
  setExpandedConstraints(prevState => ({
    ...prevState,
    [discountId]: !prevState[discountId]
  }));
};

const renderNestedDiscount = (discount) => {
  if (!discount) return null;

  return (
    <div className="ml-4">
      <p><strong>Discount ID:</strong> {discount.discount_id}</p>
      <p><strong>Store ID:</strong> {discount.store_id}</p>
      <p><strong>Description:</strong> {discount.description}</p>
      <p><strong>Start Date:</strong> {discount.start_date}</p>
      <p><strong>End Date:</strong> {discount.end_date}</p>
      {(discount.discount_type === 'productDiscount' || discount.discount_type === 'storeDiscount' || discount.discount_type === "categoryDiscount") &&  <p><strong>Percentage:</strong> {discount.percentage*100}%</p>}
      {discount.discount_type === 'productDiscount' && <p><strong>Product ID:</strong> {discount.product_id}</p>}
      {discount.discount_type === 'categoryDiscount' && <p><strong>Category ID:</strong> {discount.category_id}</p>}
      {discount.discount_type === 'categoryDiscount' && <p><strong>Is Applied To Sub</strong> {discount.applied_to_subcategories}</p>}
      {['andDiscount', 'orDiscount', 'xorDiscount'].includes(discount.discount_type) && (
        <>
          <div className="flex justify-between">
            <button onClick={() => handleToggleLeftDiscount(discount.discount_id)} className="mt-2">
              {expandedLeftDiscounts[discount.discount_id] ? 'Hide Left Discount' : 'Show Left Discount'}
            </button>
            <button onClick={() => handleToggleRightDiscount(discount.discount_id)} className="mt-2">
              {expandedRightDiscounts[discount.discount_id] ? 'Hide Right Discount' : 'Show Right Discount'}
            </button>
          </div>
          {expandedLeftDiscounts[discount.discount_id] && discount.discount_id1 && (
            <div className="mt-2 ml-4">
              {renderNestedDiscount(discount.discount_id1)}
            </div>
          )}
          {expandedRightDiscounts[discount.discount_id] && discount.discount_id2 && (
            <div className="mt-2 ml-4">
              {renderNestedDiscount(discount.discount_id2)}
            </div>
          )}
        </>
      )}
      {['maxDiscount', 'additiveDiscount'].includes(discount.discount_type) && (
        <>
          <button onClick={() => handleToggleMultipleDiscounts(discount.discount_id)} className="mt-2">
            {expandedMultipleDiscounts[discount.discount_id] ? 'Hide Discounts' : 'Show Discounts'}
          </button>
          {expandedMultipleDiscounts[discount.discount_id] && discount.discounts_info && (
            <div className="mt-2 ml-4">
              {Object.values(discount.discounts_info).map((discount) => renderNestedDiscount(discount))}
            </div>
          )}
        </>
      )}
      {['productDiscount', 'storeDiscount', 'categoryDiscount'].includes(discount.discount_type) && discount.predicate && (
        <>
          <button onClick={() => handleToggleConstraint(discount.discount_id)} className="text-gray-500 mt-2">
            {expandedConstraints[discount.discount_id] ? 'Hide Constraint' : 'Show Constraint'}
          </button>
          {expandedConstraints[discount.discount_id] && (
            <div className="mt-2">
              <p>{discount.predicate}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};


// Function for rendering a Discount
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
        <p><strong>Discount ID:</strong> {discount.discount_id}</p>
        <p><strong>Store ID:</strong> {discount.store_id}</p>
        <p><strong>Description:</strong> {discount.description}</p>
        <p><strong>Start Date:</strong> {discount.start_date}</p>
        <p><strong>End Date:</strong> {discount.end_date}</p>
        {(discount.discount_type === 'productDiscount' || discount.discount_type === 'storeDiscount' || discount.discount_type === "categoryDiscount") &&  <p><strong>Percentage:</strong> {discount.percentage*100}%</p>}
        {discount.discount_type === 'productDiscount' && <p><strong>Product ID:</strong> {discount.product_id}</p>}
        {discount.discount_type === 'categoryDiscount' && <p><strong>Category ID:</strong> {discount.category_id}</p>}
        {discount.discount_type === 'categoryDiscount' && <p><strong>Is Applied To Sub</strong> {discount.applied_to_subcategories}</p>}
        {['andDiscount', 'orDiscount', 'xorDiscount'].includes(type) && (
          <>
            <div className="flex justify-between">
              <button onClick={() => handleToggleLeftDiscount(discount.discount_id)} className="mt-2">
                {expandedLeftDiscounts[discount.discount_id] ? 'Hide Left Discount' : 'Show Left Discount'}
              </button>
              <button onClick={() => handleToggleRightDiscount(discount.discount_id)} className="mt-2">
                {expandedRightDiscounts[discount.discount_id] ? 'Hide Right Discount' : 'Show Right Discount'}
              </button>
            </div>
            {expandedLeftDiscounts[discount.discount_id] && discount.discount_id1 && (
              <div className="mt-2 ml-4">
                {renderNestedDiscount(discount.discount_id1)}
              </div>
            )}
            {expandedRightDiscounts[discount.discount_id] && discount.discount_id2 && (
              <div className="mt-2 ml-4">
                {renderNestedDiscount(discount.discount_id2)}
              </div>
            )}
          </>
        )}
        {['maxDiscount', 'additiveDiscount'].includes(type) && (
          <>
            <button onClick={() => handleToggleMultipleDiscounts(discount.discount_id)} className="mt-2">
              {expandedMultipleDiscounts[discount.discount_id] ? 'Hide Discounts' : 'Show Discounts'}
            </button>
            {expandedMultipleDiscounts[discount.discount_id] && discount.discounts_info && (
              <div className="mt-2 ml-4">
                {Object.values(discount.discounts_info).map((discount) => renderNestedDiscount(discount))}
              </div>
            )}
          </>
        )}
        {['productDiscount', 'storeDiscount', 'categoryDiscount'].includes(type) && (
          <>
            <button onClick={() => handleToggleConstraint(discount.discount_id)} className="text-gray-500 mt-2">
              {expandedConstraints[discount.discount_id] ? 'Hide Constraint' : 'Show Constraint'}
            </button>
            {expandedConstraints[discount.discount_id] && discount.predicate && (
              <div className="mt-2">
                <p>{discount.predicate}</p>
              </div>
            )}
          </>
        )}
        <div className={`flex ${['productDiscount', 'storeDiscount', 'categoryDiscount'].includes(type) ? 'justify-between' : 'justify-center'} mt-4`}>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button className="bg-red-500 text-white py-1 px-3 rounded mr-2">Remove Discount</Button>
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
                <AlertDialogAction onClick={() => handleRemoveDiscount(type, discount.discount_id)}>Yes, remove discount </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
          <Button className="bg-green-500 text-white py-1 px-3 rounded" onClick={() => handleOpenEditDialog(discount.discount_id, type)}>Edit Discount</Button>
          {['productDiscount', 'storeDiscount', 'categoryDiscount'].includes(type) && (
            <Button onClick={() => handleOpenConstraintDialog(discount.discount_id)} className="ml-2">
              Add Constraint
            </Button>
          )}
        </div>
      </div>
    )}
  </div>
);

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
              {['storeDiscount', 'categoryDiscount', 'productDiscount'].includes(type) && (
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
              {type === 'categoryDiscount' && (
                <>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="category-id" className="block mt-2">Category ID</Label>
                    <Select onValueChange={setSelectedCategory}>
                      <SelectTrigger className="col-span-3 border border-black bg-white">
                        <SelectValue placeholder="Category ID" />
                      </SelectTrigger>
                      <SelectContent className="bg-white">
                        {Object.values(categories).map((category) => (
                          <SelectItem key={category.category_id} value={category.category_id}>
                            {category.category_name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="apply-sub-categories" className="block mt-2">Apply to Sub Categories</Label>
                    <Select onValueChange={(value) => setNewIsSubApplied(value === 'yes')}>
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
              {type === 'productDiscount' && (
                <>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="product-id" className="block mt-2">Product ID</Label>
                    <Select onValueChange={setSelectedProduct}>
                      <SelectTrigger className="col-span-3 border border-black bg-white">
                        <SelectValue placeholder="Product ID" />
                      </SelectTrigger>
                      <SelectContent className="bg-white">
                        {products_to_store
                          .filter((store) => store.store_id === store_id)
                          .flatMap((store) => store.products)
                          .map((product) => (
                            <SelectItem key={product.product_id} value={product.product_id}>
                              {product.name}
                            </SelectItem>
                          ))}
                      </SelectContent>
                    </Select>
                  </div>
                </>
              )}
              {['andDiscount', 'orDiscount', 'xorDiscount'].includes(type) && (
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
              {['additiveDiscount', 'maxDiscount'].includes(type) && (
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
          {['storeDiscount', 'categoryDiscount', 'productDiscount'].includes(editDiscountType) && (
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
      <DialogHeader className="text-center">
        <DialogTitle>Adding a constraint</DialogTitle>
      </DialogHeader>
      <div className="grid gap-4 py-4">
        <div className="flex items-center">
          <Label htmlFor="constraint-type" className="mr-2 whitespace-nowrap">Constraint Type</Label>
          <Select onValueChange={handleConstraintTypeChange} className="flex-grow ml-2">
            <SelectTrigger className="border border-black bg-white w-full">
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
      <DialogFooter className="flex justify-between items-center">
        <div className="text-red-500 text-sm text-left flex-grow">{errorMessage}</div>
        <Button type="button" onClick={handleSaveConstraint} className="ml-2 px-6">Save constraint</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</div>);
};

export default ManageDiscount;