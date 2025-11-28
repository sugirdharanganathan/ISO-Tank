import axios from 'axios';

export const handleGeneratePPT = async (tankId) => {
  try {
    console.log(`Triggering Server-Side PPT Generation for ID: ${tankId}...`);

    const response = await axios.post(
      `http://127.0.0.1:8000/api/ppt/generate`, 
      { tank_id: tankId }
      // NOTE: Removed "responseType: 'blob'" because we expect JSON now
    );

    // Check for success message from backend
    if (response.status === 200 && response.data.file_path) {
        alert(`Success! File saved at:\n${response.data.file_path}`);
        return true;
    }

  } catch (error) {
    console.error("PPT Generation Error:", error);
    
    // Optional: Extract specific error message from backend if available
    let msg = "Failed to generate report.";
    if (error.response && error.response.data && error.response.data.detail) {
        msg += ` Server says: ${error.response.data.detail}`;
    }
    
    alert(msg);
    return false;
  }
};