import React from 'react';
import { Droplet, LayoutList, FileText, File } from 'lucide-react';

// A reusable helper for the sidebar links
const NavItem = ({ icon: Icon, text, active, onClick }) => (
  <button
    onClick={onClick}
    className={`
      flex items-center w-full px-4 py-3 mb-2 rounded-lg transition-all duration-200
      text-sm font-medium
      ${
        active
          ? 'bg-white/20 text-white shadow-sm' // Active: Semi-transparent white box
          : 'text-gray-100 hover:bg-white/10'  // Inactive: Hover effect only
      }
    `}
  >
    <Icon className="w-5 h-5 mr-3" />
    <span>{text}</span>
  </button>
);

export default function Sidebar({ currentPage, setCurrentPage }) {
  return (
    // Main Sidebar Container - using the specific Slate/Blue-Grey color
    <div className="flex flex-col w-64 h-full text-white bg-[#546E7A] shadow-xl font-sans">
      
      {/* 1. Logo Section */}
      <div className="flex items-center px-6 py-8 mb-2">
        <Droplet className="w-6 h-6 mr-2 fill-white text-white" />
        <span className="text-xl font-bold tracking-wide">ISO Tank</span>
      </div>

      {/* 2. Navigation Links */}
      <nav className="flex-1 px-4 overflow-y-auto">
        <NavItem
          icon={LayoutList} // Matches the "list" icon style
          text="Tank Master"
          active={currentPage === 'TankManagement'}
          onClick={() => setCurrentPage('TankManagement')}
        />
        
        <NavItem
          icon={FileText}
          text="Generate PPT"
          active={currentPage === 'GeneratePPT'}
          onClick={() => setCurrentPage('GeneratePPT')}
        />
        
        <NavItem
          icon={File}
          text="View PPTs"
          active={currentPage === 'ViewPPTs'}
          onClick={() => setCurrentPage('ViewPPTs')}
        />
      </nav>

      {/* 3. Footer Section */}
      <div className="p-6 text-xs text-center text-gray-300 border-t border-white/10">
        v1.0 • © Techspire Solutions
      </div>
    </div>
  );
}