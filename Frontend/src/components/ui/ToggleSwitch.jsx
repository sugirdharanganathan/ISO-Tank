import React from 'react';

export const ToggleSwitch = ({ checked, onChange }) => {
  return (
    <div 
      className={`relative inline-flex h-6 w-11 items-center rounded-full cursor-pointer transition-colors duration-200 ease-in-out ${
        // State: Red (Checked/Right) for Inactive, Green (Unchecked/Left) for Active
        checked ? 'bg-red-500' : 'bg-green-500' 
      }`}
      // Toggle logic reverses the status (Active -> Inactive, Inactive -> Active)
      onClick={() => onChange(!checked)}
    >
      <span className="sr-only">Toggle Status</span>
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition duration-200 ease-in-out ${
          checked ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </div>
  );
};