import axios from 'axios';

const API_URL = 'http://localhost:8000/api/tank-drawings/';

export const getTankDrawings = async (tankId) => {
  try {
    const response = await axios.get(`${API_URL}tank/${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching drawings for tank ${tankId}:`, error);
    throw error;
  }
};

export const uploadDrawing = async (formData) => {
  try {
    // FIX: Removed manual 'Content-Type' header. 
    // Axios automatically sets the correct multipart boundary when it receives a FormData object.
    const response = await axios.post(API_URL, formData);
    return response.data;
  } catch (error) {
    console.error('Error uploading drawing:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteDrawing = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting drawing ${id}:`, error);
    throw error;
  }
};