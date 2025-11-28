import axios from 'axios';

const API_URL = 'http://localhost:8000/api/tank-inspection/';

/**
 * Gets all inspection records for the given tank ID.
 * Corresponds to: GET /api/tank-inspection?tank_id={id} (we assume a filter)
 */
export const getTankInspections = async (tankId) => {
  try {
    // Note: Router only has GET / and GET /{id}, so we assume /tank/{tank_id} or filter by tankId
    // Since the backend GET / returns all, we filter manually here for safety:
    const response = await axios.get(API_URL);
    // Since the backend GET / returns all, we filter manually here for safety:
    return response.data.filter(record => record.tank_id === tankId);
  } catch (error) {
    console.error(`Error fetching inspections for tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};

/**
 * Creates a new inspection record.
 * Corresponds to: POST /
 */
export const createInspection = async (payload) => {
  try {
    const response = await axios.post(API_URL, payload);
    return response.data;
  } catch (error) {
    console.error('Error creating inspection:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Updates an existing inspection record.
 * Corresponds to: PUT /{id}
 */
export const updateInspection = async (id, payload) => {
  try {
    const response = await axios.put(`${API_URL}${id}`, payload);
    return response.data;
  } catch (error) {
    console.error(`Error updating inspection ${id}:`, error.response?.data || error.message);
    throw error;
  }
};