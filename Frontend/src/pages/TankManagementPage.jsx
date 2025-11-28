import React, { useState, useEffect } from 'react';
import { Plus, Edit, FileSpreadsheet, Search, X } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { ToggleSwitch } from '../components/ui/ToggleSwitch';
import { getTanks, updateTank } from '../services/tankService';
import AddTankModal from '../components/tank-modal/AddTankModal';

export default function TankManagementPage() {
  const [tanks, setTanks] = useState([]);
  const [filteredTanks, setFilteredTanks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingTankId, setEditingTankId] = useState(null);

  // Search State
  const [searchField, setSearchField] = useState('tank_number'); 
  const [searchText, setSearchText] = useState('');

  // --- Data Loading ---
  const loadTanks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getTanks();
      setTanks(data);
      setFilteredTanks(data);
    } catch (err) {
      setError('Failed to load tanks.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadTanks(); }, []);

  // --- Handlers ---
  const handleSaveSuccess = () => { loadTanks(); };

  const handleStatusToggle = async (tank) => {
    const newStatus = tank.status === 'active' ? 'inactive' : 'active';
    
    // Optimistic update
    const updatedTanks = tanks.map(t => 
      t.id === tank.id ? { ...t, status: newStatus } : t
    );
    setTanks(updatedTanks);
    setFilteredTanks(updatedTanks); 

    try {
      await updateTank(tank.id, { status: newStatus });
    } catch (err) {
      alert("Failed to update status.");
      loadTanks();
    }
  };

  const handleEditClick = (tankId) => { setEditingTankId(tankId); setShowModal(true); };
  const handleAddClick = () => { setEditingTankId(null); setShowModal(true); };
  const handleCloseModal = () => { setShowModal(false); setEditingTankId(null); loadTanks(); };
  const handleExport = () => window.open('http://localhost:8000/api/tanks/export-to-excel', '_blank');
  
  const handleSearch = () => {
    if (!searchText.trim()) { setFilteredTanks(tanks); return; }
    const lowerText = searchText.toLowerCase();
    const filtered = tanks.filter(tank => {
      const value = String(tank[searchField] || '').toLowerCase();
      return value.includes(lowerText);
    });
    setFilteredTanks(filtered);
  };

  const handleCancelSearch = () => {
    setSearchText('');
    setFilteredTanks(tanks);
  };
  
  return (
    <>
      <AddTankModal 
        show={showModal} 
        onClose={handleCloseModal}
        onSaveSuccess={handleSaveSuccess}
        tankId={editingTankId}
      />

      <div className="flex flex-col h-full bg-gray-50 font-sans">
        {/* --- 1. Top Header --- */}
        <header className="flex items-center justify-between px-8 py-6 bg-white border-b border-gray-200">
          <h1 className="text-2xl font-bold text-[#546E7A]">Tank Master</h1>
          <div className="flex gap-3">
            {/* Export to Excel Button - Muted Teal/Green */}
            <Button 
              variant="primary" 
              icon={FileSpreadsheet}
              className="bg-[#529085] hover:bg-[#437a70] text-white font-medium px-4 py-2 rounded shadow-sm border border-transparent"
              onClick={handleExport}
            >
              Export to Excel
            </Button>
            
            {/* Add Tank Button - Matching the uploaded image (Teal/Blue-Grey) */}
            <Button 
              variant="primary" 
              icon={Plus}
              className="bg-[#546E7A] hover:bg-[#455A64] text-white font-medium px-4 py-2 rounded shadow-sm border border-transparent"
              onClick={handleAddClick}
            >
              Add Tank
            </Button>
          </div>
        </header>

        {/* --- 2. Search Section --- */}
        <div className="px-8 py-6">
          <div className="flex flex-col md:flex-row gap-4 items-end">
            <div className="w-full md:w-64">
              <label className="block text-sm font-medium text-gray-600 mb-2">Search by</label>
              <div className="relative">
                <select 
                  value={searchField}
                  onChange={(e) => setSearchField(e.target.value)}
                  className="w-full pl-3 pr-10 py-2 bg-white border border-gray-300 rounded text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 appearance-none"
                >
                  <option value="tank_number">Tank Name</option>
                  <option value="mfgr">MFGR</option>
                  <option value="status">Status</option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
                  <svg className="h-4 w-4 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/></svg>
                </div>
              </div>
            </div>
            
            <div className="flex-grow">
               <label className="block text-sm font-medium text-gray-600 mb-1 invisible">Search</label>
               <input 
                type="text"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder="Enter search text"
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="flex gap-3 pb-[1px]">
              {/* Search Button - EXACT Match to Image 1 (Dark Slate/Blue-Grey) */}
              <Button 
                onClick={handleSearch}
                className="bg-[#546E7A] hover:bg-[#455A64] text-white px-6 py-2 rounded shadow-sm font-normal text-base"
                icon={Search}
              >
                Search
              </Button>
              
              {/* Cancel Button - EXACT Match to Image 2 (White with Grey Border) */}
              <Button 
                onClick={handleCancelSearch}
                variant="secondary"
                className="bg-white border border-[#546E7A] text-[#546E7A] hover:bg-gray-50 px-6 py-2 rounded shadow-sm font-normal text-base flex items-center gap-2"
              >
                <X className="w-4 h-4" />
                Cancel
              </Button>
            </div>
          </div>
        </div>
        
        {/* --- 3. Table Section --- */}
        <main className="flex-grow px-8 pb-8 overflow-hidden flex flex-col">
          {error && <div className="p-4 mb-4 text-red-600 bg-red-50 border-l-4 border-red-500">{error}</div>}

          {/* Outer Border Container */}
          <div className="w-full bg-white rounded-lg border-2 border-[#546E7A] overflow-hidden flex flex-col h-full shadow-md">
            
            <div className="flex-grow overflow-auto">
              <table className="w-full min-w-full">
                {/* Header matching the image: specific Slate/Blue-Grey color */}
                <thead className="bg-[#546E7A] sticky top-0 z-10">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider w-16 border-r border-[#607D8B]">S.No</th>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Tank Number</th>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">MFGR</th>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Capacity (L)</th>
                    
                    {/* --- NEW COLUMNS --- */}
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Lease</th>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Frame Type</th>
                    <th className="px-6 py-3 text-left text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Body/Frame Colour</th>

                    <th className="px-6 py-3 text-center text-sm font-bold text-white uppercase tracking-wider border-r border-[#607D8B]">Status</th>
                    <th className="px-6 py-3 text-center text-sm font-bold text-white uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                
                <tbody className="bg-white divide-y divide-gray-200">
                  {loading ? (
                    <tr><td colSpan="9" className="p-8 text-center text-gray-500">Loading data...</td></tr>
                  ) : filteredTanks.length === 0 ? (
                    <tr><td colSpan="9" className="p-8 text-center text-gray-500">No tanks found.</td></tr>
                  ) : (
                    filteredTanks.map((tank, index) => (
                      <tr key={tank.id} className="hover:bg-gray-50 border-b border-gray-200">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{index + 1}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{tank.tank_number}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{tank.mfgr}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{tank.capacity_l}</td>
                        
                        {/* --- NEW DATA CELLS --- */}
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                          {tank.lease ? 'Yes' : 'No'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                          {tank.frame_type || '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                          {tank.color_body_frame || '-'}
                        </td>
                        
                        {/* Status Column - Active is Solid Green */}
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          <span className={`px-3 py-1 inline-flex text-xs leading-4 font-bold rounded-md ${
                            tank.status === 'active' 
                              ? 'bg-[#48BB78] text-white' 
                              : 'bg-red-500 text-white'
                          }`}>
                            {tank.status === 'active' ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        
                        {/* Action Column */}
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          <div className="flex items-center justify-center gap-4">
                            {/* Blue Edit Icon */}
                            <button 
                              onClick={() => handleEditClick(tank.id)}
                              className="text-blue-600 hover:text-blue-800 transition-colors"
                              title="Edit Details"
                            >
                              <Edit className="w-5 h-5" />
                            </button>
                            
                            {/* Toggle Switch (Red for Active/On per image) */}
                            <ToggleSwitch 
                              checked={tank.status === 'active'} 
                              onChange={() => handleStatusToggle(tank)}
                            />
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}