import express from 'express';
import { lodgeComplaint } from '../controllers/complaintController.js';

const router = express.Router();

router.post('/', lodgeComplaint);  // POST route for lodging a complaint

export default router;
