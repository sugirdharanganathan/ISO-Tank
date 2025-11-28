import React, { useState, useEffect } from 'react';
import { Save, AlertCircle, Trash2, FileText } from 'lucide-react';
import { Button } from '../ui/Button';
import { FormInput } from '../ui/FormInput';
import { FormSelect } from '../ui/FormSelect';
import { createCertificate, getTankCertificates, deleteCertificate } from '../../services/tankCertificateService'; 
import { getTankById } from '../../services/tankService';

// Inspection Agency Options
const INSPECTION_AGENCIES = ['BV', 'LR', 'DNV', 'RNA'];

export default function TankCertificateTab({ tankId, onClose }) {
  // State for the list of certificates
  const [certificatesList, setCertificatesList] = useState([]);
  const [tankDetails, setTankDetails] = useState({ date_mfg: '' });
  
  // Form State
  const [inspectionAgency, setInspectionAgency] = useState('');
  const [formData, setFormData] = useState({
    insp_2_5y_date: '',
    next_insp_date: '',
    tank_certificate: '', 
  });
  const [certificateFile, setCertificateFile] = useState(null);
  
  // UI State
  const [loading, setLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  // --- Data Fetching ---
  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch Tank Details (for Year of MFG)
      const details = await getTankById(tankId); 
      setTankDetails(details);

      // Fetch List of Certificates
      const certificates = await getTankCertificates(tankId); 
      setCertificatesList(certificates);

    } catch (err) {
      console.error(err);
      setError('Failed to load certificate data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tankId) {
      loadData();
    }
  }, [tankId]);

  // Show warning if tank isn't saved
  if (!tankId) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500 space-y-4">
        <AlertCircle className="w-12 h-12 text-orange-500" />
        <p className="text-lg font-medium">Please save the "Tank Basic Details" first.</p>
      </div>
    );
  }

  // --- Handlers ---
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleFileChange = (e) => {
    setCertificateFile(e.target.files[0]);
  };
  
  const handleSave = async () => {
    // Basic validation
    if (!formData.tank_certificate) {
        alert("Certificate No. is required.");
        return;
    }

    try {
      setIsSaving(true);
      
      const uploadData = new FormData();
      
      // 1. Append File
      if (certificateFile) {
        uploadData.append('certificate_file', certificateFile);
      }
      
      // 2. Append form data
      uploadData.append('tank_id', tankId);
      uploadData.append('certificate_number', formData.tank_certificate);
      uploadData.append('insp_2_5y_date', formData.insp_2_5y_date || '');
      uploadData.append('next_insp_date', formData.next_insp_date || '');
      uploadData.append('inspection_agency', inspectionAgency || ''); 
      uploadData.append('created_by', 'User');
      
      // Create new certificate
      await createCertificate(uploadData);

      alert('Certificate added successfully!');
      
      // Clear Form
      setFormData({
        insp_2_5y_date: '',
        next_insp_date: '',
        tank_certificate: '', 
      });
      setInspectionAgency('');
      setCertificateFile(null);
      
      // Refresh List
      loadData(); 
    } catch (err) {
      console.error(err);
      setError('Failed to save certificate. ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (confirm('Are you sure you want to delete this certificate?')) {
        try {
            await deleteCertificate(id);
            loadData(); // Refresh list
        } catch (err) {
            alert("Failed to delete certificate.");
        }
    }
  };

  const handleCancel = () => {
      // Clear form
      setFormData({
        insp_2_5y_date: '',
        next_insp_date: '',
        tank_certificate: '', 
      });
      setInspectionAgency('');
      setCertificateFile(null);
      onClose();
  };

  return (
    <div className="space-y-8">

      {error && <div className="p-3 text-red-800 bg-red-100 border border-red-300 rounded-md">{error}</div>}

      {/* --- Form Section --- */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Row 1 */}
            <FormInput 
                label="Year of MFG" 
                id="date_mfg" 
                value={tankDetails.date_mfg ? new Date(tankDetails.date_mfg).getFullYear() : 'N/A'}
                disabled={true} 
            />
            <FormInput 
                label="Inspection Date" 
                id="insp_2_5y_date" 
                type="date" 
                value={formData.insp_2_5y_date} 
                onChange={handleChange}
            />
            <FormInput 
                label="Next Inspection" 
                id="next_insp_date" 
                type="date" 
                value={formData.next_insp_date} 
                onChange={handleChange}
            />
            
            {/* Row 2 */}
            <FormInput 
                label="Certificate No." 
                id="tank_certificate" 
                value={formData.tank_certificate} 
                onChange={handleChange}
                placeholder="Enter certificate number"
            />
            
            <FormSelect
                label="Inspection Agency"
                id="inspection_agency"
                value={inspectionAgency}
                onChange={(e) => setInspectionAgency(e.target.value)}
            >
                <option value="">-- Select Agency --</option>
                {INSPECTION_AGENCIES.map(agency => (
                    <option key={agency} value={agency}>{agency}</option>
                ))}
            </FormSelect>

            {/* File Upload */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Upload Certificate
                </label>
                <div className="flex items-center space-x-2">
                    <input 
                        type="file" 
                        id="cert_file_upload"
                        className="hidden"
                        accept=".pdf, image/jpeg, image/jpg"
                        onChange={handleFileChange} 
                    />
                    {/* UPDATED: Choose File Button with Light Grey Background for Visibility */}
                    <Button
                        type="button"
                        onClick={() => document.getElementById('cert_file_upload').click()}
                        className="bg-gray-200 text-gray-800 hover:bg-gray-300 rounded-md px-4 py-2 text-sm font-medium transition-colors"
                    >
                        Choose file
                    </Button>
                    <span className="text-sm text-gray-600 truncate max-w-[150px]">
                        {certificateFile?.name || 'No file chosen'}
                    </span>
                </div>
            </div>
        </div>
        
        {/* Action Buttons */}
        <div className="flex justify-end pt-2 space-x-3">
            {/* UPDATED: Cancel Button matched to Grey style */}
            <Button 
                onClick={handleCancel} 
                className="bg-[#6B7280] text-white hover:bg-[#4B5563] rounded-lg px-6 py-2.5 font-normal shadow-md"
            >
                Cancel
            </Button>
            {/* Save Button matched to Slate Blue style */}
            <Button 
                onClick={handleSave} 
                className="bg-[#54737E] text-white hover:bg-[#47656e] rounded-lg px-6 py-2.5 font-normal shadow-md flex items-center"
                icon={Save}
                disabled={isSaving}
            >
                {isSaving ? 'Saving...' : 'Save'}
            </Button>
        </div>
      </div>

      {/* --- Linked Certificates List (Table) --- */}
      <div>
        <h4 className="text-lg font-semibold text-gray-800 mb-3">Linked Certificates</h4>
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full min-w-full divide-y divide-gray-200">
            {/* UPDATED: Table Header matched to Slate Blue style */}
            <thead className="bg-[#54737E] text-white">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Cert No.</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Agency</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Insp. Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Next Due</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">File</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                 <tr><td colSpan="6" className="px-4 py-4 text-center text-sm text-gray-500">Loading...</td></tr>
              ) : certificatesList.length === 0 ? (
                <tr><td colSpan="6" className="px-4 py-4 text-center text-sm text-gray-500">No certificates linked.</td></tr>
              ) : (
                certificatesList.map((item) => (
                  <tr key={item.id}>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{item.certificate_number}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{item.inspection_agency || '-'}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{item.insp_2_5y_date || '-'}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{item.next_insp_date || '-'}</td>
                    <td className="px-4 py-3 text-sm text-blue-600 truncate max-w-[150px]">
                        {item.certificate_file ? (
                            <span className="flex items-center" title={item.certificate_file}>
                                <FileText className="w-4 h-4 mr-1" />
                                File
                            </span>
                        ) : '-'}
                    </td>
                    <td className="px-4 py-3 text-sm">
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