import siteSettings from './content/settings/site.json';

/** Canonical site URL — single source of truth (DECIDED 2026-09-06). */
export const SITE_URL = siteSettings.siteUrl || 'https://joyofcare.net';

export const SITE_NAME = siteSettings.siteName || 'Joy of Care';
export const WHATSAPP = siteSettings.whatsappNumber || '628811118911';
export const WHATSAPP_URL = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(
  'Hi, saya tahu dari web. Mau tanya layanan Joy of Care'
)}`;

/** Google Analytics 4 Measurement ID (CMS siteSettings.json -> env var -> fallback G-K4XR1K77PK) */
export const GA_MEASUREMENT_ID =
  import.meta.env.PUBLIC_GA_MEASUREMENT_ID ||
  siteSettings.gaMeasurementId ||
  'G-K4XR1K77PK';

/** Google Search Console verification code (override via PUBLIC_GSC_VERIFICATION_ID env var) */
export const GSC_VERIFICATION_ID = import.meta.env.PUBLIC_GSC_VERIFICATION_ID || '';