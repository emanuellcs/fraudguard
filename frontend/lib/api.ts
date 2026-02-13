import axios from 'axios';

// When running inside Docker (Server Side), we might need the internal container URL.
// When running in Browser (Client Side), we need the public localhost URL.
// For this simple setup, we rely on the browser side mainly.
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface TransactionResponse {
  transaction_id: string;
  risk_score: number;
  is_fraud: boolean;
  status: string;
}