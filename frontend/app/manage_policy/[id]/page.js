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

const ManagePolicy = () => {
  const [errorMessage, setErrorMessage] = useState('');

  const searchParams = useSearchParams();
  const store_id = searchParams.get('id');

  // data required for the page
  const [policies, setPolicies] = useState([]);
  const [stores, setStores] = useState([]);
  const [products_to_store, setProductsToStore] = useState([]);
  const [categories, setCategories] = useState([]);

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
  const [expandedLeftPolicy, setExpandedLeftPolicy] = useState(null);
  const [expandedRightPolicy, setExpandedRightPolicy] = useState(null);
  const [expandedConstraint, setExpandedConstraint] = useState(null);

  // data required for adding constraints
  const [constraintDialogOpen, setConstraintDialogOpen] = useState(false);
  const [selectedConstraintType, setSelectedConstraintType] = useState('');
  const [constraintValues, setConstraintValues] = useState({});
  const [currentPolicyId, setCurrentPolicyId] = useState(null);

  //function for loading in all relevant data
  useEffect(() => {
    const fetchData = async () => {
      try {
        //load in all the policies of store
        const response = await api.get('/store/view_all_policies_of_store');
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
        
        setPolicies(data);        

      } catch (error) {
        console.error('Failed to fetch stores', error);
        setErrorMessage('Failed to fetch stores');
        setStores({});
      }
      //fetching all the stores for the constraints
      try {
        const response = await api.get('/store/store_ids_to_names');
        if(response.status !== 200){
          console.error('Failed to fetch stores', response);
          setErrorMessage('Failed to fetch stores');
          return;
        }
        console.log("the stores:", response.data.message)
        let data = response.data.message;

        if(data === null || data === undefined) {
          console.error('Failed to fetch stores', response);
          setErrorMessage('Failed to fetch stores');
          return;
        }

        setStores(data);
      } catch (error) {
        console.error('Failed to fetch stores', error);
        setErrorMessage('Failed to fetch stores');
      }

      //fetching all products of the store
      try {
        let data = [];
        for (let i = 0; i < stores.length; i++) {
          const response = await api.get(`/store/store_products?store_id=${stores[i].key}`);
          if(response.status !== 200){
            console.error('Failed to fetch products of store', response);
            setErrorMessage('Failed to fetch products');
            return;
          }
          console.log("the products of the store:", response.data.message)
          let data_of_store = response.data.message;

          if(data_of_store === null || data_of_store === undefined) {
            console.error('Failed to fetch products of store', response);
            setErrorMessage('Failed to fetch products of store');
            return;
          }
          data.push({ store_id: stores[i].key, products: data_of_store });
        }

        setProductsOfStore(data);
      } catch (error) {
        console.error('Failed to fetch products of store', error);
        setErrorMessage('Failed to fetch products of store');
      }

      //fetching all categories
      try {
        const response = await api.get('/store/category_ids_to_names');
        if(response.status !== 200){
          console.error('Failed to fetch categories', response);
          setErrorMessage('Failed to fetch categories');
          return;
        }
        console.log("the categories:", response.data.message)
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
    }

    fetchData();
  }, []);

  //function responsible for adding a new policy
  const handleSaveChanges = () => {
    if (!newPolicyName) {
      setErrorMessage('Please enter a policy name.');
      return;
    }
    let data;
    switch (dialogType) {
      case 'productSpecific':
        if (!selectedProduct) {
          setErrorMessage('Please select a product.');
          return;
        }
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
          "product_id": selectedProduct.product_id,
        };
        break;

      case 'categorySpecific':
        if (!selectedCategory) {
          setErrorMessage('Please select a category.');
          return;
        }
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
          "category_id": selectedCategory.category_id,
        };
        break;

      case 'basketSpecific':
        data = {
          "store_id": store_id,
          "policy_name": newPolicyName,
        };
        break;
      
        case 'andPolicies':
        case 'orPolicies':
        case 'conditionalPolicies':
          if (!selectedLeftPolicy || !selectedRightPolicy) {
            setErrorMessage('Please select both policies.');
            return;
          }
          let type_of_composite = 1;
          if (dialogType == 'orPolicies'){
            type_of_composite = 2;
          }else if(dialogType === 'conditionalPolicies'){
            type_of_composite = 3;
          }
          data = { 
            "store_id": store_id,
            "policy_name": newPolicyName,
            "left_policy_id": selectedLeftPolicy.policy_id,
            "right_policy_id": selectedRightPolicy.policy_id,
            "type_of_composite": type_of_composite
          };
          break;
      default:
        return;
    }

    let newPolicy;
    const savePolicy = async () => {
      try {
        console.log("the policy data:", data);
        //case of the simple policies
        if (dialogType === 'productSpecific' || dialogType === 'categorySpecific' || dialogType === 'basketSpecific') {
          const response = await api.post(`/store/add_purchase_policy`, data);
          if (response.status !== 200) {
            setErrorMessage('Failed to save policy data');
            return;
          }
          console.log("the response id of the new policy:", response.data.policy_id)
          newPolicy = {
            "policy_id": response.data.policy_id,
            ...data
          }

          console.log("the new policy:", newPolicy)
          // Add the new policy to the appropriate type
          setPolicies({ ...policies, [dialogType]: [...policies[dialogType], newPolicy] });

        } else {
          // case of the composite policies
          const response = await api.post(`/store/create_composite_policy`, data);
          if (response.status !== 200) {
            setErrorMessage('Failed to save policy data');
            return;
          }
          console.log("the response id of the new policy:", response.data.policy_id)
          newPolicy = {
            "policy_id": response.data.policy_id,
            "store_id": data.store_id,
            "policy_name": data.policy_name,
            "left_policy_id": selectedLeftPolicy,
            "right_policy_id": selectedRightPolicy,
            "type_of_composite": data.type_of_composite
          }
          console.log("the new policy:", newPolicy)

          // Add the new composite policy to the appropriate type
          const updatedPolicies = { ...policies };
          updatedPolicies[dialogType].push(newPolicy);
          setPolicies(updatedPolicies);

          // Remove the selected policies
          const removePolicy = (policyId) => {
            for (let type in updatedPolicies) {
              updatedPolicies[type] = updatedPolicies[type].filter(policy => policy.policy_id !== policyId);
            }
          };

          removePolicy(parseInt(selectedLeftPolicy.policy_id));
          removePolicy(parseInt(selectedRightPolicy.policy_id));
          setPolicies(updatedPolicies);
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
        setPolicies({
          ...policies,
          [type]: policies[type].filter(policy => policy.policy_id !== policyId)
        });
        setErrorMessage(null);
      } catch (error) {
        console.error('Error removing policy:', error);
        setErrorMessage('Failed to remove policy data');
      }
    };
    removePolicy();
  };

  //function responsible for toggling the expanded state of a policy
  const handleToggle = (policyId, type) => {
    setExpandedPolicies({
      ...expandedPolicies,
      [type]: expandedPolicies[type] === policyId ? null : policyId
    });
  };

  //function responsible for toggling the expanded sub policies of a composite policy
  const handleToggleLeftPolicy = (policyId) => {
    setExpandedLeftPolicy(expandedLeftPolicy === policyId ? null : policyId);
  };

  const handleToggleRightPolicy = (policyId) => {
    setExpandedRightPolicy(expandedRightPolicy === policyId ? null : policyId);
  };

  //function responsible for toggling the expanded constraint of a policy
  const handleToggleConstraint = (policyId) => {
    setExpandedConstraint(expandedConstraint === policyId ? null : policyId);
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

  //function responsible for adding a new constraint to a policy
  const handleSaveConstraint = () => {
    
    // Add other validation checks for different constraint types here...

    const updatedPolicies = { ...policies };
    const policyType = Object.keys(updatedPolicies).find(type => 
      updatedPolicies[type].some(policy => policy.policy_id === currentPolicyId)
    );

    const policyIndex = updatedPolicies[policyType].findIndex(policy => 
      policy.policy_id === currentPolicyId
    );

    updatedPolicies[policyType][policyIndex].constraints = [{
      type: selectedConstraintType,
      details: JSON.stringify(constraintValues)
    }];

    setPolicies(updatedPolicies);
    setConstraintDialogOpen(false);
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
              onChange={(e) => handleConstraintValueChange('age', e.target.value)}
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
                  {stores.map((store) => (
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
                  {stores.map((store) => (
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
                  {products_to_store.map((product_to_store) => (
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
          {categories.map((category) => (
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
          {stores.map((store) => (
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
          {stores.map((store) => (
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
          {products_to_store.map((product) => (
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
          {categories.map((category) => (
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
          {categories.map((category) => (
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
          {stores.map((store) => (
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
          {stores.map((store) => (
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
          {products.map((product) => (
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
        <p><strong>Store ID:</strong> {policy.store_id}</p>
        <p><strong>Policy Name:</strong> {policy.policy_name}</p>
        {type === 'productSpecific' && <p><strong>Product ID:</strong> {policy.product_id}</p>}
        {type === 'categorySpecific' && <p><strong>Category ID:</strong> {policy.category_id}</p>}
        {['andPolicies', 'orPolicies', 'conditionalPolicies'].includes(type) && (
          <>
            <div className="flex justify-between">
              <button onClick={() => handleToggleLeftPolicy(policy.policy_id)} className="mt-2">Show Left Policy</button>
              <button onClick={() => handleToggleRightPolicy(policy.policy_id)} className="mt-2">Show Right Policy</button>
            </div>
            {expandedLeftPolicy === policy.policy_id && (
              <div className="mt-2">
                {renderNestedPolicy(policy.left_policy_id)}
              </div>
            )}
            {expandedRightPolicy === policy.policy_id && (
              <div className="mt-2">
                {renderNestedPolicy(policy.right_policy_id)}
              </div>
            )}
          </>
        )}
        {['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) && (
          <button className="mt-2" onClick={() => handleToggleConstraint(policy.policy_id)}>Show Constraints</button>
        )}
        {expandedConstraint === policy.policy_id && (
          <div className="mt-2">
            {policy.constraints.map((constraint, index) => (
              <p key={index}>{constraint.type}: {constraint.details}</p>
            ))}
          </div>
        )}
        <div className={`flex ${['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) ? 'justify-between' : 'justify-center'} mt-4`}>
          {['productSpecific', 'categorySpecific', 'basketSpecific'].includes(type) && (
            <Button className="bg-blue-500 text-white py-1 px-3 rounded" onClick={() => handleOpenConstraintDialog(policy.policy_id)}>Add Constraint</Button>
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
                <AlertDialogAction onClick={() => handleRemovePolicy(type, policy.policy_id)}>Yes, remove policy</AlertDialogAction>
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
    policies[type].some(p => p.policy_id === policyId)
  );

  console.log('policyType found:', policyType); // Add log

  if (!policyType) {
    return <p>Policy not found</p>;
  }

  const nestedPolicy = policies[policyType].find(p => p.policy_id === policyId);

  console.log('nestedPolicy found:', nestedPolicy); // Add log

  if (!nestedPolicy) {
    return <p>Policy not found</p>;
  }

  return (
    <div className="ml-4">
      <p><strong>Policy ID:</strong> {nestedPolicy.policy_id}</p>
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
                  {products_to_store.map((product) => ( //here we need to do it so that only the products associated to our store are shown
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
                  {categories.map((category) => (
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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
                    <SelectItem key={policy.policy_id} value={policy.policy_id}>
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