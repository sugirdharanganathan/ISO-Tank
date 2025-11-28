import axios from 'axios';

const API_URL = 'http://localhost:8000/api/valve-test-reports/';

export const getValveTestReport = async (tankId) => {
  try {
    // Backend returns a list of reports for the tank
    const response = await axios.get(`${API_URL}tank/${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching valve reports for tank ${tankId}:`, error);
    throw error;
  }
};

export const saveValveTestReport = async (formData) => {
  try {
    // Axios automatically handles Content-Type for FormData
    const response = await axios.post(API_URL, formData);
    return response.data;
  } catch (error) {
    console.error('Error creating valve report:', error.response?.data || error.message);
    throw error;
  }
};

export const updateValveTestReport = async (reportId, formData) => {
  try {
    const response = await axios.put(`${API_URL}${reportId}`, formData);
    return response.data;
  } catch (error) {
    console.error(`Error updating valve report ${reportId}:`, error.response?.data || error.message);
    throw error;
  }
};

export const deleteValveTestReport = async (reportId) => {
  try {
    const response = await axios.delete(`${API_URL}${reportId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting valve report ${reportId}:`, error.response?.data || error.message);
    throw error;
  }
};