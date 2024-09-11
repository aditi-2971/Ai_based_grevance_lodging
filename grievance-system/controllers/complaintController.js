import axios from 'axios';

export const lodgeComplaint = async (req, res) => {
  try {
    const { complaintText } = req.body;

    // Call the Python service to classify the complaint
    const response = await axios.post('http://localhost:5001/classify', { complaintText });
const data = response.data;
    const { department } = response.data;

    res.json({ department, complaint: complaintText, data});
  } catch (error) {
    res.status(500).json({ message: 'Error processing the complaint' });
  }
};
