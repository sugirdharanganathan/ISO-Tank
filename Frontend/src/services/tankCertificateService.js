import axios from 'axios';

// Assuming your backend router for certificates is at this path
const API_URL = 'http://localhost:8000/api/tank-certificates/'; 

/**
 * Gets certificate records for the given tank ID.
 */
export const getTankCertificates = async (tankId) => {
  try {
    const response = await axios.get(`${API_URL}tank/${tankId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching certificates for tank ${tankId}:`, error.response?.data || error.message);
    throw error;
  }
};

/**
 * Creates a new certificate record. Handles multipart if FormData is present.
 * Corresponds to: POST /api/tank-certificates/
 */
export const createCertificate = async (formDataOrPayload) => {
  try {
    const isFormData = formDataOrPayload instanceof FormData;
    
    const response = await axios.post(API_URL, formDataOrPayload, {
        headers: {
            'Content-Type': isFormData ? 'multipart/form-data' : 'application/json',
        },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating certificate:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Updates an existing certificate record. Handles multipart if FormData is present.
 * Corresponds to: PUT /api/tank-certificates/{id}
 */
export const updateCertificate = async (id, formDataOrPayload) => {
  try {
    const isFormData = formDataOrPayload instanceof FormData;
    
    const response = await axios.put(`${API_URL}${id}`, formDataOrPayload, {
        headers: {
            'Content-Type': isFormData ? 'multipart/form-data' : 'application/json',
        },
    });
    return response.data;
  } catch (error) {
    console.error(`Error updating certificate ${id}:`, error.response?.data || error.message);
    throw error;
  }
};

/**
 * Deletes a certificate record.
 * Corresponds to: DELETE /api/tank-certificates/{id}
 */
export const deleteCertificate = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting certificate ${id}:`, error.response?.data || error.message);
    throw error;
  }
};