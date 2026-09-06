# Panduan Lengkap Manajemen Google Analytics, SEO, GEO & AIO — Joy of Care

Dokumen ini adalah buku panduan operasional terpadu untuk mengelola **Google Analytics 4 (GA4)**, **Search Engine Optimization (SEO)**, **Generative Engine Optimization (GEO)**, dan **AI Overview (AIO)** untuk Joy of Care (`joyofcare.net`).

---

## 1. Google Analytics 4 (GA4) & Tracking Management

### 1.1 Arsitektur Tracking yang Telah Diimplementasikan
Situs `joyofcare-web` telah dilengkapi dengan komponen tracking kustom di [`src/components/GoogleAnalytics.astro`](file:///home/gobeam/Projects/joyofcare-web/src/components/GoogleAnalytics.astro) dan terhubung langsung di [`src/layouts/BaseLayout.astro`](file:///home/gobeam/Projects/joyofcare-web/src/layouts/BaseLayout.astro).

Komponen ini mendukung:
1. **Google Analytics 4 (`gtag.js`)** secara asynchronous tanpa membebani Core Web Vitals (LCP/INP).
2. **Auto-Tracking WhatsApp Click (`whatsapp_click`)**:
   - Menangkap setiap klik pada tombol / tautan WhatsApp (`wa.me` atau `whatsapp.com`).
   - Parameter yang dicatat: `event_label` (teks tombol), `link_url`, `page_location`, `page_title`.
   - Ini merupakan **Primary Key Conversion** utama Joy of Care.
3. **Auto-Tracking Phone Call (`phone_call_click`)**:
   - Menangkap klik nomor telepon `tel:+628811118911`.
4. **Auto-Tracking Scroll Depth (`scroll_depth`)**:
   - Mencatat milestone membaca artikel kesehatan (25%, 50%, 75%, 90%) untuk mengukur retensi dan engagement edukasi medis.

---

### 1.2 Cara Memasang ID Google Analytics & Search Console

Buka atau buat file `.env` di folder `joyofcare-web/` (sudah disediakan contoh di [`.env.example`](file:///home/gobeam/Projects/joyofcare-web/.env.example)):

```bash
# joyofcare-web/.env

# Masukkan ID Measurement GA4 Anda (format: G-XXXXXXXXXX)
PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# Masukkan kode verifikasi HTML Tag Google Search Console jika menggunakan metode meta tag
PUBLIC_GSC_VERIFICATION_ID=your-verification-code-here
```

> **Catatan:** Jika variabel di atas diisi, sistem Astro akan otomatis mengaktifkan tag GA4 dan meta tag Search Console saat proses `npm run build`.

---

### 1.3 Pengaturan Wajib di Google Analytics Console (Admin Steps)

Setelah properti GA4 dibuat di [analytics.google.com](https://analytics.google.com):

1. **Buat Data Stream Web:**
   - Masukkan URL: `https://joyofcare.net`
   - Beri nama: `Joy of Care Web`
   - Salin **Measurement ID** (`G-XXXXXXXXXX`) ke dalam `.env`.
2. **Aktifkan Enhanced Measurement:**
   - Di Data Stream, pastikan toggle aktif untuk: Page views, Outbound clicks, Site search, Scroll, Video engagement.
3. **Tandai `whatsapp_click` sebagai Key Event (Conversion):**
   - Masuk ke menu **Admin > Data display > Events**.
   - Cari event `whatsapp_click` (atau buat manual dengan nama `whatsapp_click` jika belum ada traffic).
   - Geser toggle **"Mark as key event"** (jadikan konversi utama).
4. **Tautkan dengan Google Search Console (GSC):**
   - Masuk ke **Admin > Product Links > Search Console Links**.
   - Klik **Link**, pilih properti Search Console `https://joyofcare.net/`, dan pilih Web Stream Anda.
   - *Manfaat:* Anda dapat melihat query pencarian organik Google langsung di dashboard GA4.

---

## 2. Search Engine Optimization (SEO)

### 2.1 Schema Markup (JSON-LD) Terpasang
Seluruh halaman web telah disematkan structured data Schema.org berstandar Google:
- **Homepage ([`BaseLayout.astro`](file:///home/gobeam/Projects/joyofcare-web/src/layouts/BaseLayout.astro)):**
  - `@type: MedicalBusiness`
  - Nama, logo, geokoordinat (`latitude: -6.3024, longitude: 106.6521`), alamat fisik BSD City.
  - `openingHoursSpecification`: 07:00 – 21:00 (tersedia on-call 24 jam).
  - `priceRange`: `$$`, `currenciesAccepted`: `IDR`.
  - `medicalSpecialty`: General Practice, Physical Therapy, Acupuncture, Nursing, Geriatrics.
  - `sameAs`: Akun media sosial resmi (Instagram, Facebook, Linktree).
  - `areaServed`: BSD City, Tangerang Selatan, Jakarta Barat/Selatan/Pusat/Timur/Utara, Depok, Bogor.
- **Halaman Layanan:**
  - `@type: MedicalProcedure` + `BreadcrumbList` + `FAQPage`.
- **Halaman Blog & Artikel:**
  - `@type: MedicalWebPage` + `BreadcrumbList` + `FAQPage` + referensi reviewer medis.

### 2.2 Verifikasi Google Search Console & Sitemap
1. Buka [Google Search Console](https://search.google.com/search-console).
2. Tambahkan Properti `https://joyofcare.net/` atau Domain `joyofcare.net` (DNS TXT record lebih disarankan).
3. Masuk ke menu **Sitemaps**, submit URL sitemap utama:
   ```
   https://joyofcare.net/sitemap-index.xml
   ```
4. Verifikasi status crawling robots.txt di:
   ```
   https://joyofcare.net/robots.txt
   ```

---

## 3. Generative Engine Optimization (GEO)

GEO bertujuan agar konten Joy of Care direferensikan dan dikutip oleh mesin pencari AI seperti **ChatGPT Search**, **Perplexity.ai**, **Claude**, **Bing Copilot**, dan **Gemini**.

### 3.1 Standar `llms.txt` & `llms-full.txt`
Joy of Care telah menerapkan protokol standar `llms.txt`:
1. **[`/public/llms.txt`](file:///home/gobeam/Projects/joyofcare-web/public/llms.txt)**: Ringkasan terstruktur untuk model LLM ber-token pendek:
   - Identitas entitas PT. Joyofcare Network Indonesia.
   - Daftar 8 layanan utama dengan URL rujukan resmi.
   - Standar keamanan (STR/SIP tenaga medis, cold-chain 2-8°C, alkes steril single-use).
   - Kontak langsung & pemesanan.
2. **[`/public/llms-full.txt`](file:///home/gobeam/Projects/joyofcare-web/public/llms-full.txt)**: Basis pengetahuan lengkap untuk query mendalam (kompetensi perawat, jenis vaksin Shingrix/Prevenar, paket lab HbA1c/profil lipid, cakupan area per kecamatan).

### 3.2 Izin Perayap AI di `robots.txt`
File [`robots.txt`](file:///home/gobeam/Projects/joyofcare-web/public/robots.txt) telah membuka akses eksplisit untuk bot AI:
- `GPTBot` (OpenAI training/model)
- `ChatGPT-User` (ChatGPT browsing)
- `OAI-SearchBot` (SearchGPT engine)
- `ClaudeBot` (Anthropic Claude search)
- `PerplexityBot` (Perplexity search engine)
- `Google-Extended` (Google Gemini training & multimodal)
- `Applebot-Extended` (Apple Intelligence)

---

## 4. AI Overview (AIO) Optimization (Google SGE)

Google AI Overview mengutamakan kutipan dari situs medis terverifikasi yang memenuhi prinsip **E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)**.

### 4.1 Format Jawaban Langsung (The 40-Word Rule)
- Setiap artikel blog dan halaman layanan dibuka dengan ringkasan padat 40–60 kata yang langsung menjawab pertanyaan utama pengguna.
- Hindari kalimat pembuka yang bertele-tele. Berikan definisi, angka biaya/rentang tarif, atau langkah tindakan klinis secara tegas.

### 4.2 Struktur Data Bertingkat & Tabel Perbandingan
- AI Overview sangat menyukai tag semantik `<table>`, `<ol>`, dan `<ul>`.
- Gunakan tabel perbandingan (misal: *Perbandingan Vaksin PCV13 vs PPSV23* atau *Joy of Care vs Rawat Mandiri*).

### 4.3 Sinyal Kredibilitas Medis (E-E-A-T Badges)
- Pastikan setiap artikel memuat:
  - Penulis (Author): Tim Edukasi Kesehatan Joy of Care.
  - Peninjau Medis (Medical Reviewer): Dokter ber-STR aktif.
  - Tanggal Pembaruan (Last Updated).
  - Rujukan Ilmiah (Kemenkes RI, WHO, CDC, Jurnal Kedokteran).

### 4.4 Sinkronisasi Google Business Profile (Local AIO Signal)
- AI Overview untuk kueri lokal (misal: *"fisioterapi stroke panggil ke rumah BSD"*) mencocokkan Name, Address, Phone (NAP) di website dengan profil Google Maps.
- Pastikan nama akun Google Business Profile sama persis: `Joy of Care - Layanan Kesehatan di Rumah BSD City`.
- Alamat dan nomor WhatsApp (`08811-118-911`) harus identik dengan Schema JSON-LD.

---

## 5. Checklist Monitoring Mingguan & Bulanan

| Periode | Task | Platform | Target / KPI |
|---|---|---|---|
| **Mingguan** | Pantau jumlah konversi `whatsapp_click` & rasio konversi per halaman | GA4 Dashboard | Conv Rate > 3.5% dari visitor unik |
| **Mingguan** | Cek error 404 & Coverage Index di GSC | Google Search Console | 0 error crawling sitemap |
| **Bulanan** | Analisis kata kunci pencarian baru & CTR halaman artikel | Google Search Console | Rata-rata posisi kata kunci naik |
| **Bulanan** | Uji query AI di ChatGPT, Perplexity & Google Search | ChatGPT / Perplexity | Joy of Care muncul sebagai opsi rekomendasi utama |
| **Bulanan** | Perbarui `llms-full.txt` bila ada penambahan layanan/tarif baru | `public/llms-full.txt` | Faktual & relevan |

---

## 6. Ringkasan File Terkait di Codebase

- [`joyofcare-web/src/components/GoogleAnalytics.astro`](file:///home/gobeam/Projects/joyofcare-web/src/components/GoogleAnalytics.astro) — Komponen tracking GA4 & custom events.
- [`joyofcare-web/src/consts.ts`](file:///home/gobeam/Projects/joyofcare-web/src/consts.ts) — Konfigurasi konstanta situs, ID GA4, ID GSC.
- [`joyofcare-web/src/layouts/BaseLayout.astro`](file:///home/gobeam/Projects/joyofcare-web/src/layouts/BaseLayout.astro) — Layout induk, meta tags, schema MedicalBusiness.
- [`joyofcare-web/public/robots.txt`](file:///home/gobeam/Projects/joyofcare-web/public/robots.txt) — Kebijakan crawler & AI search bot.
- [`joyofcare-web/public/llms.txt`](file:///home/gobeam/Projects/joyofcare-web/public/llms.txt) — Panduan singkat untuk mesin pencari AI.
- [`joyofcare-web/public/llms-full.txt`](file:///home/gobeam/Projects/joyofcare-web/public/llms-full.txt) — Dokumentasi pengetahuan komprehensif untuk AI.
