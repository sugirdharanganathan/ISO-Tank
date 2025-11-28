import React, { useState, useEffect } from 'react';
import { Save, Upload, AlertCircle, Trash2, FileText } from 'lucide-react';
import { Button } from '../ui/Button';
import { FormSelect } from '../ui/FormSelect';
import { FormInput } from '../ui/FormInput';
import { uploadDrawing, getTankDrawings, deleteDrawing } from '../../services/tankDrawingService';

const drawingTypes = [
  "P&ID (Piping & Instrumentation Diagram)",
  "PFD (Process Flow Diagram)",
  "GA Drawing (General Arrangement)",
  "Isometric (Iso) Drawing",
  "Fabrication Drawing",
  "Electrical Drawing",
  "Instrumentation Drawing",
  "Safety / Fire Fighting Drawing",
];

export default function TankDrawingsTab({ tankId }) {
  const [drawingType, setDrawingType] = useState('');
  const [description, setDescription] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState('No file chosen');
  
  // List State
  const [drawingsList, setDrawingsList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  // --- Load Data ---
  const loadDrawings = async () => {
    try {
      setLoading(true);
      const data = await getTankDrawings(tankId);
      setDrawingsList(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load drawings.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tankId) loadDrawings();
  }, [tankId]);

  // --- Handlers ---
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileName(file.name);
    } else {
      setSelectedFile(null);
      setFileName('No file chosen');
    }
  };

  const handleSave = async () => {
    if (!drawingType || !selectedFile) {
      alert('Please select a Drawing Type and upload a file.');
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('tank_id', tankId);
      formData.append('drawing_type', drawingType);
      formData.append('description', description);
      formData.append('file', selectedFile);
      formData.append('created_by', 'Admin'); // Hardcoded for now

      await uploadDrawing(formData);
      
      // Reset form
      setDrawingType('');
      setDescription('');
      setSelectedFile(null);
      setFileName('No file chosen');
      
      // Refresh list
      loadDrawings();
      alert("Drawing uploaded successfully!");
    } catch (err) {
      setError("Failed to upload drawing.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (confirm("Are you sure you want to delete this drawing?")) {
      try {
        await deleteDrawing(id);
        loadDrawings();
      } catch (err) {
        alert("Failed to delete drawing.");
      }
    }
  };

  const handleCancel = () => {
    setDrawingType('');
    setDescription('');
    setSelectedFile(null);
    setFileName('No file chosen');
    setError(null);
  };

  if (!tankId) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500 space-y-4">
        <AlertCircle className="w-12 h-12 text-orange-500" />
        <p className="text-lg font-medium">Please save the "Tank Basic Details" first.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {error && <div className="p-3 text-red-800 bg-red-100 border border-red-300 rounded-md">{error}</div>}

      {/* --- Upload Form --- */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <FormSelect
            label="Drawing Type"
            id="drawing_type"
            value={drawingType}
            onChange={(e) => setDrawingType(e.target.value)}
            required
          >
            <option value="">-- Select Drawing Type --</option>
            {drawingTypes.map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </FormSelect>

          <FormInput
            label="Description"
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g. As-Built P&ID"
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Upload Drawing</label>
            <div className="flex items-center space-x-2">
                <input
                    type="file"
                    id="file_upload"
                    className="hidden"
                    onChange={handleFileChange}
                    accept=".pdf, .dwg, .dxf, .jpg, .png"
                />
                {/* UPDATED: Light Grey Background for Choose File Button */}
                <Button
                    type="button"
                    onClick={() => document.getElementById('file_upload').click()}
                    className="bg-gray-200 text-gray-800 hover:bg-gray-300 rounded-md px-4 py-2 text-sm font-medium transition-colors"
                    icon={Upload}
                >
                    Choose file
                </Button>
                <span className="text-sm text-gray-600 truncate max-w-[150px]" title={fileName}>{fileName}</span>
            </div>
          </div>
        </div>

        <div className="flex justify-end space-x-3 pt-2">
            {/* UPDATED: Cancel Button to Grey */}
            <Button 
                onClick={handleCancel} 
                className="bg-[#6B7280] text-white hover:bg-[#4B5563] rounded-lg px-6 py-2.5 font-normal shadow-md"
            >
                Cancel
            </Button>
            
            {/* UPDATED: Save Button to Slate Blue */}
            <Button 
                onClick={handleSave} 
                className="bg-[#54737E] text-white hover:bg-[#47656e] rounded-lg px-6 py-2.5 font-normal shadow-md flex items-center"
                icon={Save} 
                disabled={isSaving}
            >
                {isSaving ? 'Uploading...' : 'Save'}
            </Button>
        </div>
      </div>

      {/* --- Drawings List Table --- */}
      <div>
        <h4 className="text-lg font-semibold text-gray-800 mb-3">Linked Drawings</h4>
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full min-w-full divide-y divide-gray-200">
            {/* UPDATED: Table Header to Slate Blue */}
            <thead className="bg-[#54737E] text-white">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Type</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Description</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">File Name</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Uploaded Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                 <tr><td colSpan="5" className="px-4 py-4 text-center text-sm text-gray-500">Loading...</td></tr>
              ) : drawingsList.length === 0 ? (
                <tr><td colSpan="5" className="px-4 py-4 text-center text-sm text-gray-500">No drawings uploaded yet.</td></tr>
              ) : (
                drawingsList.map((item) => (
                  <tr key={item.id}>
                    <td className="px-4 py-3 text-sm text-gray-900 font-medium">{item.drawing_type}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{item.description || '-'}</td>
                    <td className="px-4 py-3 text-sm text-blue-600 truncate max-w-xs flex items-center">
                        <FileText className="w-4 h-4 mr-1" />
                        {item.original_filename}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">{new Date(item.created_at).toLocaleDateString()}</td>
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