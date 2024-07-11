"use client";
import api from '@/lib/api';
import { useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react';
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

const ManagePolicy = () => {
  const [errorMessage, setErrorMessage] = useState('');

  const searchParams = useSearchParams();
  const store_id = searchParams.get('id');

  // data required for the page
  const [policies, setPolicies] = useState([]);
  const [stores, setStores] = useState({});
  const [products_to_store, setProductsToStore] = useState([]);
  const [categories, setCategories] = useState({});

  // states for our dialog
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState('');
  
  const [newPolicyName, setNewPolicyName] = useState('');

  // data for adding new composite policies
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedLeftPolicy, setSelectedLeftPolicy] = useState('');
  const [selectedRightPolicy, setSelectedRightPolicy] = useState('');

  // data for viewing policy data
  const [expandedPolicies, setExpandedPolicies] = useState({});
  const [expandedLeftPolicies, setExpandedLeftPolicies] = useState({});
  const [expandedRightPolicies, setExpandedRightPolicies] = useState({});
  const [expandedConstraints, setExpandedConstraints] = useState({});
  

  // data required for adding constraints
  const [constraintDialogOpen, setConstraintDialogOpen] = useState(false);
  const [selectedConstraintType, setSelectedConstraintType] = useState('');
  const [constraintValues, setConstraintValues] = useState({});
  const [currentPolicyId, setCurrentPolicyId] = useState(null);

  //function for loading in all relevant data
  useEffect(() => {
    fetchPolicies();
    fetchStores();
    fetchCategories();
  }, []);

  const fetchPolicies = async () => {
    try {
      const response = await api.post('/store/view_all_policies_of_store', { 'store_id': store_id });
      if(response.status !== 200){
        console.error('Failed to fetch policies of store', response);
        setErrorMessage('Failed to fetch policies');
        return;
      }
      console.log("the policies of the store:", response.data.message)
      let data = response.data.message;
  
      if(data === null || data === undefined) {
        console.error('Failed to fetch policies of store', response);
        setErrorMessage('Failed to fetch policies of store');
        return;
      }
  
      let productSpecificPolicies = [];
      let categorySpecificPolicies = [];
      let basketSpecificPolicies = [];
      let andPolicies = [];
      let orPolicies = [];
      let conditionalPolicies = [];

      
  
      for(let i = 0; i < data.length; i++){
        console.log("the current policy:", data[i])
        if(data[i].policy_type === "productSpecificPolicy"){
          productSpecificPolicies.push(data[i]);
        } else if(data[i].policy_type === "categorySpecificPolicy"){
          categorySpecificPolicies.push(data[i]);
        } else if(data[i].policy_type === "basketSpecificPolicy"){
          basketSpecificPolicies.push(data[i]);
        } else if(data[i].policy_type === "andPolicy"){
          andPolicies.push(data[i]);
        } else if(data[i].policy_type === "orPolicy"){
          orPolicies.push(data[i]);
        } else if(data[i].policy_type === "conditionalPolicy"){
          conditionalPolicies.push(data[i]);
        } else {
          console.error('Failed to fetch policies of store', response);
          setErrorMessage('Failed to fetch policies of store');
          return;
        }
      }
  
      let policies = {
        productSpecificPolicy: productSpecificPolicies, 
        categorySpecificPolicy: categorySpecificPolicies, 
        basketSpecificPolicy: basketSpecificPolicies, 
        andPolicy: andPolicies, 
        orPolicy: orPolicies, 
        conditionalPolicy: conditionalPolicies
      };
  
      setPolicies(policies);        
  
    } catch (error) {
      console.error('Failed to fetch policies', error);
      setErrorMessage('Failed to fetch policies');
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
  
  


  //function responsible for adding a new policy
  const handleSaveChanges = () => {
    if (!newPolicyName) {
      setErrorMessage('Please enter a policy name.');
      return;
    }
    let data;
    console.log("the dialog type:", dialogType)
    switch (dialogType) {
      case 'productSpecificPolicy':
        if (selectedProduct === null || selectedProduct === undefined || selectedProduct === "") {
          setErrorMessage('Please select a product.');
          return;
        }
        console.log("the selected product:", selectedProduct)
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
          "product_id": selectedProduct,
        };
        break;

      case 'categorySpecificPolicy':
        if (selectedCategory === null || selectedCategory === undefined || selectedCategory === "") {
          setErrorMessage('Please select a category.');
          return;
        }
        console.log("the selected category:", selectedCategory)
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
          "category_id": selectedCategory,
        };
        break;

      case 'basketSpecificPolicy':
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
        };
        break;
      
        case 'andPolicy':
        case 'orPolicy':
        case 'conditionalPolicy':
          if (selectedLeftPolicy === '' || selectedRightPolicy === '') {
            setErrorMessage('Please select both policies.');
            return;
          }
          let type_of_composite = 1;
          if (dialogType == 'orPolicy'){
            type_of_composite = 2;
          }else if(dialogType === 'conditionalPolicy'){
            type_of_composite = 3;
          }
          data = { 
            "store_id": store_id,
            "policy_name": newPolicyName,
            "policy_id1": selectedLeftPolicy,
            "policy_id2": selectedRightPolicy,
            "type_of_composite": type_of_composite
          };
          break;
      default:
        return;
    }

    let newPolicy;
    const savePolicy = async () => {
      console.log("the data of the new policy:", data)
      try {
        console.log("the policy data:", data);
        //case of the simple policies
        if (dialogType === 'productSpecificPolicy' || dialogType === 'categorySpecificPolicy' || dialogType === 'basketSpecificPolicy') {
          const response = await api.post(`/store/add_purchase_policy`, data);
          if (response.status !== 200) {
            setErrorMessage('Failed to save policy data');
            return;
          }
          console.log("the response id of the new policy:", response.data.policy_id)
        } else {
          // case of the composite policies
          const response = await api.post(`/store/create_composite_purchase_policy`, data);
          if (response.status !== 200) {
            setErrorMessage('Failed to save policy data');
            return;
          }
          console.log("the response id of the new policy:", response.data.policy_id)
        }
        setErrorMessage(null);
      } catch (error) {
        console.error('Error adding store:', error);
        setErrorMessage('Failed to save policy data');
      }
    };

    savePolicy();
    setIsDialogOpen(false);
    setNewPolicyName('');
    setSelectedProduct('');
    setSelectedCategory('');
    setSelectedLeftPolicy('');
    setSelectedRightPolicy('');
    setErrorMessage('');
    fetchPolicies();
  };
  
  
  //function responsible for removing a policy
  const handleRemovePolicy = (type, policyId) => {
    const removePolicy = async () => {
      console.log("the policy id to remove:", policyId)
      try {
        const response = await api.post(`/store/remove_purchase_policy`, { "store_id": store_id, "policy_id": policyId });
        if (response.status !== 200) {
          setErrorMessage('Failed to remove policy data');
          return;
        }
        fetchPolicies();
        setErrorMessage(null);
      } catch (error) {
        console.error('Error removing policy:', error);
        setErrorMessage('Failed to remove policy data');
      }
    };
    removePolicy();
  };

  //function responsible for opening the dialog for adding a new policy
  const handleOpenDialog = (type) => {
    setDialogType(type);
    setIsDialogOpen(true);
  };

  //function responsible for opening the dialog for adding a new constraint
  const handleOpenConstraintDialog = (policyId) => {
    setCurrentPolicyId(policyId);
    setConstraintDialogOpen(true);
  };

  //function responsible for changing the view for the adding a constraint type
  const handleConstraintTypeChange = (value) => {
    setSelectedConstraintType(value);
    setConstraintValues({});
  };

  //function responsible for changing the values for the constraint we are adding
  const handleConstraintValueChange = (field, value) => {
    setConstraintValues({ ...constraintValues, [field]: value });
  };

 // Function responsible for adding a new constraint to a policy
const handleSaveConstraint = () => {
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
  let store_id_int = parseInt(store_id);
  switch(selectedConstraintType){
    case 'compositeConstraint':
      const parsedComposite = parseConstraintString(`(${constraintValues.compositeConstraint})`);
  
      const [finalComposite] = buildNestedArray(parsedComposite, 0);
      console.log("the final composite constraint:", finalComposite);
    
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: finalComposite,
      };

      console.log("the first variable of the predicate_builder is " + data.predicate_builder[0])
      break;

    case 'age': 
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['age']],
      };
      break;
    
    case 'time':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['startingHour'], constraintValues['startingMinute'], constraintValues['endingHour'], constraintValues['endingMinute']],
      };
      break;

    case 'location':
      let location = {'address': constraintValues['address'], 'city': constraintValues['city'], 'state': constraintValues['state'], 'country': constraintValues['country'], 'zip_code': constraintValues['zipCode']}
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, location],
      };
      break;

    case 'day_of_month':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['startingDay'], constraintValues['endingDay']],
      };
      break;

    case 'day_of_week':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['startingDay'], constraintValues['endingDay']],
      };
      break;

    case 'season':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['season']],
      };
      break;

    case 'holidays_of_country':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['countryCode']],
      };
      break;

    case 'price_basket':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['store']],
      };
      break;

    case 'price_product':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['product'], constraintValues['store']],
      };
      break;

    case 'price_category':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minPrice'], constraintValues['maxPrice'], constraintValues['category']],
      };
      break;

    case 'amount_basket':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['store']],
      };
      break;

    case 'amount_product':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['product'], constraintValues['store']],
      };
      break;

    case 'amount_category':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minAmount'], constraintValues['maxAmount'], constraintValues['category']],
      };
      break;

    case 'weight_category':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['category']],
      };
      break;

    case 'weight_basket':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['store']],
      };
      break;

    case 'weight_product':
      data = {
        store_id: store_id_int,
        policy_id: currentPolicyId,
        predicate_builder: [selectedConstraintType, constraintValues['minWeight'], constraintValues['maxWeight'], constraintValues['product'], constraintValues['store']],
      };
      break;

    default:
      return;
  }
    
  console.log(`predicate builder of current constraint of type ${selectedConstraintType} we are trying to add is: ${data.predicate_builder}`);

  const saveConstraint = async () => {
    try {
      const response = await api.post(`/store/assign_predicate_to_purchase_policy`, data);
      if (response.status !== 200) {
        setErrorMessage('Failed to save constraint');
        return;
      }
      fetchPolicies();
      setConstraintDialogOpen(false);
      setSelectedConstraintType('');
      setConstraintValues({});
    } catch (error) {
      console.error('Error saving constraint:', error);
      setErrorMessage('Failed to save constraint');
    }
  }

  saveConstraint();
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
            onChange={(e) => handleConstraintValueChange('age', parseInt(e.target.value))}
            className="col-span-3 border border-black mt-2"
          />
          {constraintValues.age && isNaN(constraintValues.age) && <p className="text-red-500">Not a number</p>}
        </>
      );

    case 'time':
      return (
        <>
          <Select onValueChange={(value) => handleConstraintValueChange('startingHour', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('startingMinute', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('endingHour', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('endingMinute', parseInt(value))}>
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
          {constraintValues.zipCode && isNaN(constraintValues.zipCode) && <p className="text-red-500">Not a number</p>}
        </>
      );

    case 'day_of_month':
      return (
        <>
          <Select onValueChange={(value) => handleConstraintValueChange('startingDay', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('endingDay', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('startingDay', parseInt(value))}>
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
          <Select onValueChange={(value) => handleConstraintValueChange('endingDay', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            <Select onValueChange={(value) => handleConstraintValueChange('product', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minPrice) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-price"
            placeholder="Max price (in dollars)"
            value={constraintValues.maxPrice || ''}
            onChange={(e) => handleConstraintValueChange('maxPrice', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxPrice) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('category', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minAmount', parseInt(e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="Max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', parseInt(e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxAmount) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minAmount', parseInt(e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="Max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', parseInt(e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxAmount) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            <Select onValueChange={(value) => handleConstraintValueChange('product', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minAmount', parseInt(e.target.value))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minAmount) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-amount"
            placeholder="Max amount"
            value={constraintValues.maxAmount || ''}
            onChange={(e) => handleConstraintValueChange('maxAmount', parseInt(e.target.value))}
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
            onChange={(e) => handleConstraintValueChange('minWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('category', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            onChange={(e) => handleConstraintValueChange('minWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.minWeight) && <p className="text-red-500">Not a number</p>}
          <Input
            id="max-weight"
            placeholder="Max weight (in kg)"
            value={constraintValues.maxWeight || ''}
            onChange={(e) => handleConstraintValueChange('maxWeight', parseFloat(parseFloat(e.target.value).toFixed(1)))}
            className="col-span-3 border border-black"
          />
          {isNaN(constraintValues.maxWeight) && <p className="text-red-500">Not a number</p>}
          <Select onValueChange={(value) => handleConstraintValueChange('store', parseInt(value))}>
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
            <Select onValueChange={(value) => handleConstraintValueChange('product', parseInt(value))}>
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


const handleToggle = (policyId, type) => {
  setExpandedPolicies(prevState => ({
    ...prevState,
    [type]: prevState[type] === policyId ? null : policyId
  }));
};

const handleToggleLeftPolicy = (policyId) => {
  setExpandedLeftPolicies(prevState => ({
    ...prevState,
    [policyId]: !prevState[policyId]
  }));
};

const handleToggleRightPolicy = (policyId) => {
  setExpandedRightPolicies(prevState => ({
    ...prevState,
    [policyId]: !prevState[policyId]
  }));
};

const handleToggleConstraint = (policyId) => {
  setExpandedConstraints(prevState => ({
    ...prevState,
    [policyId]: !prevState[policyId]
  }));
};

const renderNestedPolicy = (policy) => {
  if (!policy) return null;

  return (
    <div className="ml-4">
      <p><strong>Policy ID:</strong> {policy.policy_id}</p>
      <p><strong>Store ID:</strong> {policy.store_id}</p>
      <p><strong>Policy Name:</strong> {policy.policy_name}</p>
      {policy.policy_type === 'productSpecificPolicy' && <p><strong>Product ID:</strong> {policy.product_id}</p>}
      {policy.policy_type === 'categorySpecificPolicy' && <p><strong>Category ID:</strong> {policy.category_id}</p>}
      {['andPolicy', 'orPolicy', 'conditionalPolicy'].includes(policy.policy_type) && (
        <>
          <div className="flex justify-between">
            <button onClick={() => handleToggleLeftPolicy(policy.policy_id)} className="mt-2">
              {expandedLeftPolicies[policy.policy_id] ? 'Hide Left Policy' : 'Show Left Policy'}
            </button>
            <button onClick={() => handleToggleRightPolicy(policy.policy_id)} className="mt-2">
              {expandedRightPolicies[policy.policy_id] ? 'Hide Right Policy' : 'Show Right Policy'}
            </button>
          </div>
          {expandedLeftPolicies[policy.policy_id] && policy.policy_left && (
            <div className="mt-2 ml-4">
              {renderNestedPolicy(policy.policy_left)}
            </div>
          )}
          {expandedRightPolicies[policy.policy_id] && policy.policy_right && (
            <div className="mt-2 ml-4">
              {renderNestedPolicy(policy.policy_right)}
            </div>
          )}
        </>
      )}
      {['productSpecificPolicy', 'categorySpecificPolicy', 'basketSpecificPolicy'].includes(policy.policy_type) && policy.predicate && (
        <>
          <button onClick={() => handleToggleConstraint(policy.policy_id)} className="text-gray-500 mt-2">
            {expandedConstraints[policy.policy_id] ? 'Hide Constraint' : 'Show Constraint'}
          </button>
          {expandedConstraints[policy.policy_id] && (
            <div className="mt-2">
              <p>{policy.predicate}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};


// Function for rendering a policy
const renderPolicy = (policy, type) => (
  <div 
    key={policy.policy_id} 
    className="mb-4 p-4 border-2 border-gray-300 rounded-md"
  >
    <button
      onClick={() => handleToggle(policy.policy_id, type)}
      className="text-left w-full"
    >
      {`Policy ID: ${policy.policy_id}`}
    </button>
    {expandedPolicies[type] === policy.policy_id && (
      <div className="mt-2">
        <p><strong>Policy Name:</strong> {policy.policy_name}</p>
        <p><strong>Store ID:</strong> {policy.store_id}</p>
        {type === 'productSpecificPolicy' && <p><strong>Product ID:</strong> {policy.product_id}</p>}
        {type === 'categorySpecificPolicy' && <p><strong>Category ID:</strong> {policy.category_id}</p>}
        {['andPolicy', 'orPolicy', 'conditionalPolicy'].includes(type) && (
          <>
            <div className="flex justify-between">
              <button onClick={() => handleToggleLeftPolicy(policy.policy_id)} className="mt-2">
                {expandedLeftPolicies[policy.policy_id] ? 'Hide Left Policy' : 'Show Left Policy'}
              </button>
              <button onClick={() => handleToggleRightPolicy(policy.policy_id)} className="mt-2">
                {expandedRightPolicies[policy.policy_id] ? 'Hide Right Policy' : 'Show Right Policy'}
              </button>
            </div>
            {expandedLeftPolicies[policy.policy_id] && policy.policy_left && (
              <div className="mt-2 ml-4">
                {renderNestedPolicy(policy.policy_left)}
              </div>
            )}
            {expandedRightPolicies[policy.policy_id] && policy.policy_right && (
              <div className="mt-2 ml-4">
                {renderNestedPolicy(policy.policy_right)}
              </div>
            )}
          </>
        )}
        {['productSpecificPolicy', 'categorySpecificPolicy', 'basketSpecificPolicy'].includes(type) && (
          <>
            <button onClick={() => handleToggleConstraint(policy.policy_id)} className="text-gray-500 mt-2">
              {expandedConstraints[policy.policy_id] ? 'Hide Constraint' : 'Show Constraint'}
            </button>
            {expandedConstraints[policy.policy_id] && policy.predicate && (
              <div className="mt-2">
                <p>{policy.predicate}</p>
              </div>
            )}
          </>
        )}
        <div className={`flex ${['productSpecificPolicy', 'categorySpecificPolicy', 'basketSpecificPolicy'].includes(type) ? 'justify-between' : 'justify-center'} mt-4`}>
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
                <AlertDialogAction onClick={() => handleRemovePolicy(type, policy.policy_id)}>Yes, remove policy</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
          {['productSpecificPolicy', 'categorySpecificPolicy', 'basketSpecificPolicy'].includes(type) && (
            <Button onClick={() => handleOpenConstraintDialog(policy.policy_id)} className="ml-2">
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
    <div className="w-full max-w-md p-4">
      <h2 className="text-center font-bold mb-4">Product Specific Policies</h2>
      <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
        {policies.productSpecificPolicy && policies.productSpecificPolicy.map((policy) => renderPolicy(policy, 'productSpecificPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'productSpecificPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('productSpecificPolicy')}>Add Product Policy</Button>
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
                {products_to_store.filter(store => parseInt(store.store_id) === parseInt(store_id)).flatMap(store => store.products).map(product => (
                  <SelectItem key={product.product_id} value={product.product_id}>
                    {product.name}
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
        {policies.categorySpecificPolicy && policies.categorySpecificPolicy.map((policy) => renderPolicy(policy, 'categorySpecificPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'categorySpecificPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('categorySpecificPolicy')}>Add Category Policy</Button>
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
                <SelectValue placeholder="Please select a category" />
              </SelectTrigger>
              <SelectContent className="bg-white">
                <SelectItem value="" disabled>Please select a category</SelectItem>
                {Object.values(categories).map((category) => (
                  <SelectItem key={category.category_id} value={category.category_id}>
                    {category.category_name}
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
        {policies.basketSpecificPolicy && policies.basketSpecificPolicy.map((policy) => renderPolicy(policy, 'basketSpecificPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'basketSpecificPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('basketSpecificPolicy')}>Add Basket Policy</Button>
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
        {policies.andPolicy && policies.andPolicy.map((policy) => renderPolicy(policy, 'andPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'andPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('andPolicy')}>Add And Policy</Button>
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
                  <SelectValue placeholder="Select the first policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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
                  <SelectValue placeholder="Select the second policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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
        {policies.orPolicy && policies.orPolicy.map((policy) => renderPolicy(policy, 'orPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'orPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('orPolicy')}>Add Or Policy</Button>
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
                  <SelectValue placeholder="Select the first policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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
                  <SelectValue placeholder="Select the second policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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
        {policies.conditionalPolicy && policies.conditionalPolicy.map((policy) => renderPolicy(policy, 'conditionalPolicy'))}
      </ScrollArea>
      <Dialog open={isDialogOpen && dialogType === 'conditionalPolicy'} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="w-full mt-2" onClick={() => handleOpenDialog('conditionalPolicy')}>Add Conditional Policy</Button>
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
                  <SelectValue placeholder="Select the first policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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
                  <SelectValue placeholder="Select the second policy" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {Object.values(policies).flat().map((policy) => (
                    <SelectItem key={policy} value={policy.policy_id}>
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

  </div>
  );
};


export default ManagePolicy;