import axios from 'axios';

const MASTER_URL = 'http://localhost:8000/api/cargo-master/';
const LINK_URL = 'http://localhost:8000/api/cargo-tank/';

// --- MASTER LIST FUNCTIONS ---

export const getMasterCargos = async () => {
  try {
    const response = await axios.get(MASTER_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching master cargo:', error.response?.data || error.message);
    throw error;
  }
};

export const createMasterCargo = async (name) => {
  try {
    const response = await axios.post(MASTER_URL, { cargo_reference: name });
    return response.data;
  } catch (error) {
    console.error('Error creating cargo:', error.response?.data || error.message);
    throw error;
  }
};

export const updateMasterCargo = async (id, name) => {
  try {
    const response = await axios.put(`${MASTER_URL}${id}`, { cargo_reference: name });
    return response.data;
  } catch (error) {
    console.error('Error updating cargo:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteMasterCargo = async (id) => {
  try {
    const response = await axios.delete(`${MASTER_URL}${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting cargo:', error.response?.data || error.message);
    throw error;
  }
};

// --- TANK LINK FUNCTIONS ---

export const getTankCargos = async (tankId) => {
  try {
    const response = await axios.get(`${LINK_URL}tank/${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching cargo for tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};

export const addTankCargo = async (payload) => {
  try {
    // payload: { tank_id: 1, cargo_master_id: 5 }
    // Note: Your backend expects "cargo_master_id" but maps it to "cargo_reference" column
    const response = await axios.post(LINK_URL, payload);
    return response.data;
  } catch (error) {
    console.error('Error adding tank cargo:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteTankCargo = async (txnId) => {
  try {
    const response = await axios.delete(`${LINK_URL}${txnId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting cargo link ${txnId}:`, error.response?.data || error.message);
    throw error;
  }
};