import axios from 'axios';

const API_URL = 'http://localhost:8000/api/tanks/'; 

/**
 * Fetches all tanks.
 */
export const getTanks = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching tanks:', error.response?.data || error.message);
    throw error;
  }
};

// --- ADD THIS FUNCTION ---
/**
 * Fetches a single tank by its primary ID.
 * Corresponds to: GET /api/tanks/{tank_id}
 */
export const getTankById = async (tankId) => {
  try {
    const response = await axios.get(`${API_URL}${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};
// --- END OF NEW FUNCTION ---

/**
 * Creates a new tank (header and details).
 */
export const createTank = async (tankData) => {
  try {
    const dataToSend = {
      ...tankData,
      lease: tankData.lease ? 1 : 0
    };
    const response = await axios.post(API_URL, dataToSend);
    return response.data;
  } catch (error) {
    console.error('Error creating tank:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Updates an existing tank.
 * Corresponds to: PUT /api/tanks/{tank_id}
 */
export const updateTank = async (tankId, tankData) => {
  try {
    const dataToSend = {
      ...tankData,
      lease: tankData.lease ? 1 : 0
    };
    const response = await axios.put(`${API_URL}${tankId}`, dataToSend);
    return response.data;
  } catch (error) {
    console.error(`Error updating tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};

/**
 * Deletes a tank by its primary ID.
 */
export const deleteTank = async (tankId) => {
  try {
    const response = await axios.delete(`${API_URL}${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};