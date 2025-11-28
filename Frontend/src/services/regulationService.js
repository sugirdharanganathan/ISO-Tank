import axios from 'axios';

const MASTER_URL = 'http://localhost:8000/api/regulations-master/';
const LINK_URL = 'http://localhost:8000/api/tank-regulations/';

// --- MASTER LIST FUNCTIONS ---

export const getMasterRegulations = async () => {
  try {
    const response = await axios.get(MASTER_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching master regulations:', error.response?.data || error.message);
    throw error;
  }
};

// --- FIX: This function MUST use 'export const' ---
export const createMasterRegulation = async (name) => {
  try {
    const response = await axios.post(MASTER_URL, { regulation_name: name });
    return response.data;
  } catch (error) {
    console.error('Error creating regulation:', error.response?.data || error.message);
    throw error;
  }
};

export const updateMasterRegulation = async (id, name) => {
  try {
    const response = await axios.put(`${MASTER_URL}${id}`, { regulation_name: name });
    return response.data;
  } catch (error) {
    console.error('Error updating regulation:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteMasterRegulation = async (id) => {
  try {
    const response = await axios.delete(`${MASTER_URL}${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting regulation:', error.response?.data || error.message);
    throw error;
  }
};

// --- TANK LINK FUNCTIONS (Keep these) ---

export const getTankRegulations = async (tankId) => {
  try {
    const response = await axios.get(`${LINK_URL}tank/${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching regulations for tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};

export const addTankRegulation = async (payload) => {
  try {
    const response = await axios.post(LINK_URL, payload);
    return response.data;
  } catch (error) {
    console.error('Error adding tank regulation:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteTankRegulation = async (regId) => {
  try {
    const response = await axios.delete(`${LINK_URL}${regId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting regulation ${regId}:`, error.response?.data || error.message);
    throw error;
  }
};