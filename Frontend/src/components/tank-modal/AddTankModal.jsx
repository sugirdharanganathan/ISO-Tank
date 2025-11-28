import React, { useState } from 'react';
import { X } from 'lucide-react';
import TankFormTabs from './TankFormTabs';
import TankDetailsTab from './TankDetailsTab';
import TankRegulationsTab from './TankRegulationsTab';
import TankCargoTab from './TankCargoTab';
import TankCertificateTab from './TankCertificateTab'; 
import TankDrawingsTab from './TankDrawingsTab';
import TankValveTestReportTab from './TankValveTestReportTab'; 

export default function AddTankModal({ show, onClose, onSaveSuccess, tankId }) {
    const [activeTab, setActiveTab] = useState('tank'); 

    if (!show) return null;

    const isEditMode = tankId !== null;
    const title = isEditMode ? 'Edit Tank' : 'Add New Tank';

    return (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-50 p-6">
            {/* Modal Body - Full screen with small margins */}
            <div className="bg-white rounded-lg shadow-xl w-full h-full flex flex-col">
                
                {/* 1. Header - Updated to match the Save button color (#54737E) */}
                <div className="flex items-center justify-between px-6 py-4 bg-[#54737E] text-white rounded-t-lg">
                    <h3 className="text-xl font-semibold">
                        {title}
                    </h3>
                    <button onClick={onClose} className="text-gray-300 hover:text-white">
                        <X className="w-6 h-6" />
                    </button>
                </div>
                
                {/* 2. Tab Bar Placement */}
                <div className="px-6 pt-5 pb-3">
                    <TankFormTabs activeTab={activeTab} setActiveTab={setActiveTab} />
                </div>
                
                {/* 3. Tab Content Area - Increased padding for better spacing */}
                <div className="flex-grow px-8 pb-6 overflow-y-auto">
                    {/* Tank Details Tab (Has its own Save/Cancel logic) */}
                    {activeTab === 'tank' && (
                        <TankDetailsTab 
                            onClose={onClose} 
                            onSaveSuccess={onSaveSuccess} 
                            tankId={tankId} 
                        />
                    )}
                    
                    {/* Regulations Tab */}
                    {activeTab === 'regulations' && (
                        <TankRegulationsTab onClose={onClose} tankId={tankId} />
                    )}

                    {/* Cargo Tab */}
                    {activeTab === 'cargo' && (
                        <TankCargoTab onClose={onClose} tankId={tankId} /> 
                    )}
                    
                    {/* Certificate Tab */}
                    {activeTab === 'certificate' && (
                        <TankCertificateTab onClose={onClose} tankId={tankId} />
                    )}
                    
                    {/* Drawings Tab */}
                    {activeTab === 'drawing' && (
                        <TankDrawingsTab onClose={onClose} tankId={tankId} />
                    )}
                    
                    {/* Valve Test Report Tab */}
                    {activeTab === 'valve' && (
                        <TankValveTestReportTab onClose={onClose} tankId={tankId} />
                    )}
                </div>
            </div>
        </div>
    );
}