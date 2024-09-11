import express from 'express';
import dotenv from 'dotenv';
import bodyParser from 'body-parser';
import complaintRoutes from './routes/complaintRoutes.js';

dotenv.config();

const app = express();

// Middleware
app.use(bodyParser.json());

// Routes
app.use('/api/complaints', complaintRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(3000, () => {
  console.log(`Server is running on port ${PORT}`);
});
