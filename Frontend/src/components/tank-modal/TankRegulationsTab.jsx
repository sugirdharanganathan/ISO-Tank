import React, { useState, useEffect } from 'react';
import { Plus, Trash2, AlertCircle } from 'lucide-react';
import { Button } from '../ui/Button';
import { FormSelect } from '../ui/FormSelect';
import { FormInput } from '../ui/FormInput';
import { 
  getMasterRegulations, 
  getTankRegulations, 
  addTankRegulation, 
  deleteTankRegulation 
} from '../../services/regulationService';

export default function TankRegulationsTab({ tankId }) {
  // Lists
  const [masterList, setMasterList] = useState([]);
  const [linkedRegulations, setLinkedRegulations] = useState([]);
  
  // Form State
  const [selectedRegId, setSelectedRegId] = useState('');
  const [approvalNo, setApprovalNo] = useState('');
  
  // NEW STATES FOR NEW FIELDS
  const [imoType, setImoType] = useState('');
  const [safetyStandard, setSafetyStandard] = useState('');
  const [countryRegistration, setCountryRegistration] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // If no tankId is present (New Tank mode not saved yet), show warning
  if (!tankId) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500 space-y-4">
        <AlertCircle className="w-12 h-12 text-orange-500" />
        <p className="text-lg font-medium">Please save the "Tank Basic Details" first.</p>
        <p className="text-sm">You need a created tank before you can link regulations to it.</p>
      </div>
    );
  }

  // Fetch Data
  const loadData = async () => {
    try {
      setLoading(true);
      const [masters, linked] = await Promise.all([
        getMasterRegulations(),
        getTankRegulations(tankId)
      ]);
      setMasterList(masters);
      setLinkedRegulations(linked);
    } catch (err) {
      setError('Failed to load regulations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tankId) {
      loadData();
    }
  }, [tankId]);

  // Handle Adding a Regulation
  const handleAdd = async () => {
    if (!selectedRegId) {
      alert('Please select a regulation.');
      return;
    }
    
    try {
      const payload = {
        tank_id: tankId,
        regulation_id: parseInt(selectedRegId),
        initial_approval_no: approvalNo.trim(), 
        imo_type: imoType.trim(), 
        safety_standard: safetyStandard.trim(), 
        country_registration: countryRegistration.trim(), 
        created_by: "Admin"
      };
      
      await addTankRegulation(payload);
      
      // Reset form and reload list
      setSelectedRegId('');
      setApprovalNo('');
      setImoType('');
      setSafetyStandard('');
      setCountryRegistration('');
      loadData();
    } catch (err) {
      alert('Failed to add regulation. It might already be linked or data is invalid. Check console for details.');
      console.error(err);
    }
  };

  // Handle Deleting a Regulation
  const handleDelete = async (id) => {
    if (confirm('Are you sure you want to remove this regulation?')) {
      try {
        await deleteTankRegulation(id);
        loadData();
      } catch (err) {
        alert('Failed to delete regulation.');
      }
    }
  };

  return (
    <div className="space-y-8">

      {/* --- Section 1: Add New Regulation Form --- */}
      <div className="p-4 space-y-4"> 
        
        {/* --- Top Row: Select Regulation, Approval No, IMO Type --- */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <FormSelect 
            label="Select Regulation" 
            id="reg_select" 
            value={selectedRegId} 
            onChange={(e) => setSelectedRegId(e.target.value)}
          >
            <option value="">-- Choose --</option>
            {masterList.map(reg => (
              <option key={reg.id} value={reg.id}>{reg.regulation_name}</option>
            ))}
          </FormSelect>

          <FormInput 
            label="Approval No (Optional)" 
            id="initial_approval_no" 
            value={approvalNo} 
            onChange={(e) => setApprovalNo(e.target.value)} 
            placeholder="e.g. AP-2025-001"
          />

          <FormInput 
            label="IMO Type" 
            id="imo_type" 
            value={imoType} 
            onChange={(e) => setImoType(e.target.value)} 
            placeholder="e.g. IMO-T11"
          />
        </div>

        {/* --- Bottom Row: Safety and Country & Add Button --- */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <FormInput 
            label="Safety Standard" 
            id="safety_standard" 
            value={safetyStandard} 
            onChange={(e) => setSafetyStandard(e.target.value)} 
            placeholder="e.g. EN 1443"
          />
          <FormInput 
            label="Country Registration" 
            id="country_registration" 
            value={countryRegistration} 
            onChange={(e) => setCountryRegistration(e.target.value)} 
            placeholder="e.g. US, DE, JP"
          />
          
          <div className="pb-1">
            <Button 
              onClick={handleAdd} 
              // Updated to match the exact style of the Save button (Slate Blue + Font Normal)
              className="bg-[#54737E] hover:bg-[#47656e] text-white w-full py-2.5 rounded-lg shadow-md flex items-center justify-center font-normal" 
              icon={Plus}
            >
              Add Regulation
            </Button>
          </div>
        </div>
        
      </div>

      {/* --- Section 2: List of Linked Regulations --- */}
      <div>
        <h4 className="text-lg font-semibold text-gray-800 mb-3">Regulations Linked</h4>
        
        {error && <p className="text-red-500">{error}</p>}
        
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full min-w-full divide-y divide-gray-200">
            {/* Updated Table Header to match the Modal Header Color (#54737E) */}
            <thead className="bg-[#54737E] text-white">
              <tr>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Regulation Name</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Approval No</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">IMO Type</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Safety Std</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Country</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Linked Date</th>
                <th className="px-3 py-3 text-left text-xs font-medium uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {linkedRegulations.length === 0 ? (
                <tr>
                  <td colSpan="7" className="px-6 py-4 text-center text-sm text-gray-500">
                    No regulations linked yet.
                  </td>
                </tr>
              ) : (
                linkedRegulations.map((item) => (
                  <tr key={item.id}>
                    <td className="px-3 py-4 text-sm font-medium text-gray-900">{item.regulation_name}</td>
                    <td className="px-3 py-4 text-sm text-gray-600">{item.initial_approval_no || '-'}</td>
                    <td className="px-3 py-4 text-sm text-gray-600">{item.imo_type || '-'}</td>
                    <td className="px-3 py-4 text-sm text-gray-600">{item.safety_standard || '-'}</td>
                    <td className="px-3 py-4 text-sm text-gray-600">{item.country_registration || '-'}</td>
                    <td className="px-3 py-4 text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-3 py-4 text-sm">
                      <Button 
                        onClick={() => handleDelete(item.id)} 
                        variant="danger" 
                        size="sm" 
                        icon={Trash2}
                      />
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}