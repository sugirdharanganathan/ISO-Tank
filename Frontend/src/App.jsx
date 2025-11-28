import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import TankManagementPage from './pages/TankManagementPage';
import RegulationsMasterPage from './pages/RegulationsMasterPage'; // <-- Import this
import CargoMasterPage from './pages/CargoMasterPage';
import GeneratePPTPage from './pages/GeneratePPTPage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('TankManagement');

  const renderPage = () => {
    switch (currentPage) {
      case 'TankManagement':
        return <TankManagementPage />;
      case 'Dashboard':
        return <div>Dashboard Page Not Built Yet</div>;
      case 'GeneratePPT': // <-- This ID must match Sidebar NavItem
        return <GeneratePPTPage />;
      case 'CargoMaster':
        return <CargoMasterPage />;
      case 'RegulationsMaster':
        return <RegulationsMasterPage />; // <-- Use the component here
      case 'UserManagement':
        return <div>User Management Page Not Built Yet</div>;
      default:
        return <TankManagementPage />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <div className="flex-1 flex flex-col overflow-hidden">
        {renderPage()}
      </div>
    </div>
  );
} 