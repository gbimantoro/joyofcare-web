/** Canonical site URL — single source of truth (DECIDED 2026-09-06). */
export const SITE_URL = 'https://joyofcare.net';

export const SITE_NAME = 'Joy of Care';
export const WHATSAPP = '628811118911';
export const WHATSAPP_URL = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(
  'Hi, saya tahu dari web. Mau tanya layanan Joy of Care'
)}`;

/** Google Analytics 4 Measurement ID (override via PUBLIC_GA_MEASUREMENT_ID env var) */
export const GA_MEASUREMENT_ID = import.meta.env.PUBLIC_GA_MEASUREMENT_ID || '';

/** Google Search Console verification code (override via PUBLIC_GSC_VERIFICATION_ID env var) */
export const GSC_VERIFICATION_ID = import.meta.env.PUBLIC_GSC_VERIFICATION_ID || '';