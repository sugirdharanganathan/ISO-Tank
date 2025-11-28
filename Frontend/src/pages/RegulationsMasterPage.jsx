import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { FormInput } from '../components/ui/FormInput';
import { 
  getMasterRegulations, 
  createMasterRegulation, 
  updateMasterRegulation, 
  deleteMasterRegulation 
} from '../services/regulationService';

export default function RegulationsMasterPage() {
  const [regulations, setRegulations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState('');
  
  // Edit State
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await getMasterRegulations();
      setRegulations(data);
    } catch (error) {
      alert('Failed to load regulations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAdd = async () => {
    if (!newName.trim()) return;
    try {
      await createMasterRegulation(newName);
      setNewName('');
      loadData();
    } catch (error) {
      alert('Failed to add regulation');
    }
  };

  const handleDelete = async (id) => {
    if (confirm('Are you sure? This might affect tanks linked to this regulation.')) {
      try {
        await deleteMasterRegulation(id);
        loadData();
      } catch (error) {
        alert('Failed to delete regulation');
      }
    }
  };

  const startEdit = (reg) => {
    setEditingId(reg.id);
    setEditName(reg.regulation_name);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditName('');
  };

  const saveEdit = async () => {
    try {
      await updateMasterRegulation(editingId, editName);
      setEditingId(null);
      loadData();
    } catch (error) {
      alert('Failed to update regulation');
    }
  };

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <header className="flex flex-wrap items-center justify-between gap-4 p-4 m-4 bg-white rounded-lg shadow-sm">
        <h1 className="text-3xl font-bold text-blue-700">Regulations Master</h1>
      </header>

      <main className="flex-grow p-4 pt-0">
        <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
          
          {/* --- Add New Section --- */}
          <div className="p-6 bg-gray-50 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Add New Regulation</h3>
            <div className="flex gap-4 items-end">
              <div className="flex-grow">
                <FormInput 
                  label="Regulation Name" 
                  id="new_reg" 
                  value={newName} 
                  onChange={(e) => setNewName(e.target.value)} 
                  placeholder="e.g. IMDG, ADR"
                />
              </div>
              <div className="pb-1">
                <Button onClick={handleAdd} variant="primary" icon={Plus}>Add</Button>
              </div>
            </div>
          </div>

          {/* --- List Section --- */}
          <div className="p-0">
            <table className="w-full divide-y divide-gray-200">
              <thead className="bg-teal-600 text-white">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase w-full">Regulation Name</th>
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {loading ? (
                  <tr><td colSpan="3" className="p-4 text-center">Loading...</td></tr>
                ) : regulations.map((reg) => (
                  <tr key={reg.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{reg.id}</td>
                    <td className="px-6 py-4 text-sm text-gray-900 font-medium">
                      {editingId === reg.id ? (
                        <input 
                          className="border rounded px-2 py-1 w-full"
                          value={editName}
                          onChange={(e) => setEditName(e.target.value)}
                        />
                      ) : (
                        reg.regulation_name
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end gap-2">
                        {editingId === reg.id ? (
                          <>
                            <Button onClick={saveEdit} variant="primary" size="sm" icon={Save} />
                            <Button onClick={cancelEdit} variant="secondary" size="sm" icon={X} />
                          </>
                        ) : (
                          <>
                            <Button onClick={() => startEdit(reg)} variant="outline" size="sm" icon={Edit} />
                            <Button onClick={() => handleDelete(reg.id)} variant="danger" size="sm" icon={Trash2} />
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}