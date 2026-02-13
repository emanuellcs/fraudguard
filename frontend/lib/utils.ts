import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function generateRandomTransaction() {
  // Generate random V1-V28 features (Standard Normal Distribution approx)
  const pca_features: Record<string, number> = {};
  for (let i = 1; i <= 28; i++) {
    // Box-Muller transform for normal distribution approximation
    const u = 1 - Math.random(); 
    const v = Math.random();
    const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    pca_features[`V${i}`] = parseFloat(z.toFixed(4));
  }

  return {
    time: Math.floor(Math.random() * 10000), // Random time offset
    amount: parseFloat((Math.random() * 500).toFixed(2)), // Random amount 0-500
    pca_features,
  };
}