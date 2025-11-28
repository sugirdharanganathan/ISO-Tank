import React, { useState, useEffect } from 'react';
import { Save } from 'lucide-react';
import { Button } from '../ui/Button';
import { FormInput } from '../ui/FormInput';
import { Checkbox } from '../ui/Checkbox';
import { FormSelect } from '../ui/FormSelect'; 
import { createTank, updateTank, getTankById } from '../../services/tankService';

// Initial state for the form
const initialState = {
  tank_number: '',
  lease: false,
  mfgr: '',
  date_mfg: '',
  pv_code: '',
  un_iso_code: '',
  capacity_l: '',
  mawp: '',
  design_temperature: '',
  tare_weight_kg: '',
  mgw_kg: '',
  mpl_kg: '',
  size: '',
  pump_type: '',
  vesmat: '',
  gross_kg: '',
  net_kg: '',
  color_body_frame: '',
  working_pressure: '',
  cabinet_type: '',
  frame_type: '',
  remark: '',
  created_by: 'Admin'
};

export default function TankDetailsTab({ onClose, onSaveSuccess, tankId }) {
  const [formData, setFormData] = useState(initialState);
  const [isSaving, setIsSaving] = useState(false);
  const [errors, setErrors] = useState({});

  const isEditMode = tankId !== null;

  useEffect(() => {
    if (isEditMode) {
      const fetchTankData = async (id) => {
        try {
          const data = await getTankById(id);
          setFormData({
            tank_number: data.tank_number || '',
            lease: Boolean(data.lease) || false,
            mfgr: data.mfgr || '',
            date_mfg: data.date_mfg || '',
            pv_code: data.pv_code || '',
            un_iso_code: data.un_iso_code || '',
            capacity_l: data.capacity_l || '',
            mawp: data.mawp || '',
            design_temperature: data.design_temperature || '',
            tare_weight_kg: data.tare_weight_kg || '',
            mgw_kg: data.mgw_kg || '',
            mpl_kg: data.mpl_kg || '',
            size: data.size || '',
            pump_type: data.pump_type || '',
            vesmat: data.vesmat || '',
            gross_kg: data.gross_kg || '',
            net_kg: data.net_kg || '',
            color_body_frame: data.color_body_frame || '',
            working_pressure: data.working_pressure || '',
            cabinet_type: data.cabinet_type || '',
            frame_type: data.frame_type || '',
            remark: data.remark || '',
            created_by: data.created_by || 'Admin'
          });
        } catch (err) {
          console.error(err);
          setErrors({ form: 'Failed to load tank data. Please close and try again.' });
        }
      };
      fetchTankData(tankId);
    } else {
      setFormData(initialState);
    }
  }, [tankId, isEditMode]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    let newValue = value;
    
    // AUTOFILL LOGIC FOR ISO SIZE
    if (name === 'size' && /^\d+$/.test(value)) {
        newValue = value + "'";
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : newValue
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    const data = formData;

    const requiredFields = [
      "tank_number", "mfgr", "pv_code", "un_iso_code", "capacity_l", "mawp", 
      "design_temperature", "tare_weight_kg", "mgw_kg", "mpl_kg", "size", 
      "pump_type", "vesmat", "gross_kg", "net_kg", "color_body_frame"
    ];
    requiredFields.forEach(field => {
      if (!data[field]) {
        newErrors[field] = `${field} is required.`;
      }
    });

    const tankNumberPattern = /^[A-Z]{4}\s\d{7}$/;
    if (data.tank_number && !tankNumberPattern.test(data.tank_number)) {
      newErrors.tank_number = "Format must be 4 uppercase letters + space + 7 digits (e.g., IGEU 8899860).";
    }

    const mfgrPattern = /^[a-zA-Z0-9\s]{1,20}$/;
    if (data.mfgr && !mfgrPattern.test(data.mfgr)) {
      newErrors.mfgr = "Max 20 characters. Letters, numbers, and spaces only.";
    }

    const pvCodePattern = /^[A-Z0-9]+\s\/\s[A-Z0-9]+$/i;
    if (data.pv_code && !pvCodePattern.test(data.pv_code)) {
      newErrors.pv_code = "Format must be ALPHANUMERIC / ALPHANUMERIC (e.g., GB150 / IMDG).";
    }
    
    const isoCodePattern = /^([A-Z0-9-]+|\d{4}[A-Z0-9])(\s\/\s([A-Z0-9-]+|\d{4}[A-Z0-9]))?$/i;
    if (data.un_iso_code && !isoCodePattern.test(data.un_iso_code)) {
      newErrors.un_iso_code = "Format must be XXXXX / YYYYY (e.g., T-75 / 22K7).";
    }

    const capacity = Number(data.capacity_l);
    if (data.capacity_l && (!Number.isInteger(capacity) || capacity <= 0)) {
      newErrors.capacity_l = "Must be a whole number greater than zero.";
    }

    const mawp = Number(data.mawp);
    if (data.mawp && (isNaN(mawp) || mawp <= 0)) {
      newErrors.mawp = "Must be a positive number (e.g., 21.0).";
    }

    const designTempPattern = /^(SS|[-]?\d+°C\s?to\s?[-]?\d+°C)$/i;
    if (data.design_temperature && !designTempPattern.test(data.design_temperature)) {
      newErrors.design_temperature = "Format must be 'SS' or 'Min°C to Max°C' (e.g., -196°C to 50°C).";
    }
    
    const sizePattern = /^\d+'$/;
    if (data.size && !sizePattern.test(data.size.trim())) {
        newErrors.size = "Format must be a number followed by a single quote (e.g., 20').";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validate()) return;
    
    setIsSaving(true);
    try {
      if (isEditMode) {
        await updateTank(tankId, formData);
        alert('Tank updated successfully!');
      } else {
        await createTank(formData);
        alert('Tank created successfully!');
      }
      onSaveSuccess();
    } catch (err) {
      console.error(err);
      setErrors({ form: 'Failed to save tank. Please check fields and try again.' });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {errors.form && <div className="p-3 mb-4 text-red-800 bg-red-100 border border-red-300 rounded-md">{errors.form}</div>}
      
      {/* Main Form Body - Uniform Grid with consistent spacing */}
      <div className="flex-grow overflow-y-auto pr-2">
        <div className="grid grid-cols-2 gap-x-12 gap-y-5">
          {/* --- Column 1 (Left side) --- */}
          <div className="space-y-5">
            <FormInput label="Tank Number" id="tank_number" name="tank_number" value={formData.tank_number} onChange={handleChange} required error={errors.tank_number} />
            <Checkbox label="Lease" id="lease" name="lease" checked={formData.lease} onChange={handleChange} />
            <FormInput label="Manufacturer" id="mfgr" name="mfgr" value={formData.mfgr} onChange={handleChange} required error={errors.mfgr} />
            <FormInput label="Date MFG" id="date_mfg" name="date_mfg" type="date" value={formData.date_mfg || ''} onChange={handleChange} error={errors.date_mfg} />
            <FormInput label="PV Code" id="pv_code" name="pv_code" value={formData.pv_code} onChange={handleChange} required error={errors.pv_code} />
            <FormInput label="UN/ISO Code" id="un_iso_code" name="un_iso_code" value={formData.un_iso_code} onChange={handleChange} required error={errors.un_iso_code} />
            <FormInput label="Capacity (L)" id="capacity_l" name="capacity_l" value={formData.capacity_l} onChange={handleChange} required error={errors.capacity_l} />
            <FormInput label="Working Pressure" id="working_pressure" name="working_pressure" value={formData.working_pressure} onChange={handleChange} error={errors.working_pressure} />
            <FormInput label="Cabinet Type" id="cabinet_type" name="cabinet_type" value={formData.cabinet_type} onChange={handleChange} error={errors.cabinet_type} />
            <FormInput label="Frame Type" id="frame_type" name="frame_type" value={formData.frame_type} onChange={handleChange} error={errors.frame_type} />
            <FormInput label="Created By" id="created_by" name="created_by" value={formData.created_by} onChange={handleChange} error={errors.created_by} />
            <FormInput label="Remarks" id="remark" name="remark" value={formData.remark} onChange={handleChange} />
          </div>
          
          {/* --- Column 2 (Right side) --- */}
          <div className="space-y-5">
            <FormInput label="MAWP (bar)" id="mawp" name="mawp" value={formData.mawp} onChange={handleChange} required error={errors.mawp} />
            <FormInput label="Design Temp (°C)" id="design_temperature" name="design_temperature" value={formData.design_temperature} onChange={handleChange} required error={errors.design_temperature} />
            <FormInput label="Tare Weight (kg)" id="tare_weight_kg" name="tare_weight_kg" value={formData.tare_weight_kg} onChange={handleChange} required error={errors.tare_weight_kg} />
            <FormInput label="MGW (kg)" id="mgw_kg" name="mgw_kg" value={formData.mgw_kg} onChange={handleChange} required error={errors.mgw_kg} />
            <FormInput label="MPL (kg)" id="mpl_kg" name="mpl_kg" value={formData.mpl_kg} onChange={handleChange} required error={errors.mpl_kg} />
            <FormInput label="ISO Size" id="size" name="size" value={formData.size} onChange={handleChange} required error={errors.size} placeholder="e.g. 20" />
            
            <FormSelect label="Pump" id="pump_type" name="pump_type" value={formData.pump_type} onChange={handleChange} required error={errors.pump_type}>
              <option value="">-- Select Status --</option>
              <option value="Yes">Yes</option>
              <option value="Nil">Nil</option>
            </FormSelect>
            
            <FormInput label="Vessel Material" id="vesmat" name="vesmat" value={formData.vesmat} onChange={handleChange} required error={errors.vesmat} />
            <FormInput label="Gross Weight (kg)" id="gross_kg" name="gross_kg" value={formData.gross_kg} onChange={handleChange} required error={errors.gross_kg} />
            <FormInput label="Net Weight (kg)" id="net_kg" name="net_kg" value={formData.net_kg} onChange={handleChange} required error={errors.net_kg} />
            <FormInput label="Body/Frame Color" id="color_body_frame" name="color_body_frame" value={formData.color_body_frame} onChange={handleChange} required error={errors.color_body_frame} />
        
          </div>
        </div>
      </div>
      
      {/* Footer Buttons */}
      <div className="flex justify-end pt-6 mt-6 border-t space-x-3">
        {/* Cancel Button - Grey */}
        <Button 
            onClick={onClose} 
            className="bg-[#6B7280] text-white hover:bg-[#4B5563] rounded-lg px-6 py-2.5 font-normal shadow-md"
        >
          Cancel
        </Button>
        
        {/* Save Button - Slate Blue */}
        <Button 
            onClick={handleSave} 
            className="bg-[#54737E] text-white hover:bg-[#47656e] rounded-lg px-6 py-2.5 font-normal shadow-md flex items-center"
            disabled={isSaving}
        >
          <Save className="w-4 h-4 mr-2" />
          {isSaving ? 'Saving...' : 'Save'}
        </Button>
      </div>
    </div>
  );
}