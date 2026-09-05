# Joy of Care — Panduan Alur Kerja Publikasi & Standar Konten Web
**Standard Operating Procedure (SOP) & Technical Publishing Workflow**

* **Versi Dokumen:** 1.0 (Final)  
* **Tanggal Rilis:** 5 September 2026  
* **Penanggung Jawab:** JoC Publisher  
* **Target Repositori:** `joyofcare-net` & `joyofcare-web`  
* **Status:** Aktif & Terverifikasi

---

## 1. Ikhtisar & Arsitektur Publishing

Sistem publikasi Joy of Care dirancang untuk mendukung performa tinggi, kecepatan muat instan (Core Web Vitals), kepatuhan E-E-A-T medis yang ketat, serta optimalisasi mesin pencari berbasis AI (Generative Engine Optimization / GEO dan AI Overviews / AIO).

### Struktur Direktori Kunci
```text
joyofcare-web/
├── pages/
│   ├── blog/
│   │   ├── index.html                   # Blog Hub (semua artikel)
│   │   ├── feed.xml                     # Live RSS 2.0 & Atom feed
│   │   ├── index.json                   # Metadata indeks artikel JSON
│   │   ├── healthy-aging/               # Kategori: Lansia Sehat & Geriatri
│   │   ├── pengalaman/                  # Kategori: Pengalaman Pasien
│   │   ├── studi-luar-negeri/           # Kategori: Studi di Luar Negeri
│   │   └── vaksinasi/                   # Kategori: Vaksinasi di Rumah
│   ├── templates/
│   │   ├── article-template.html        # Template HTML artikel produksi
│   │   ├── article-template.mdx         # Template MDX untuk CMS/SSG (Astro/Next.js)
│   │   ├── rss-template.xml             # Template struktur RSS channel
│   │   └── generate_sitemap.py          # Script otomatisasi Sitemap & RSS
│   ├── css/
│   │   ├── style.css                    # Design system utama Joy of Care
│   │   └── blog.css                     # Komponen visual khusus blog & artikel
│   ├── sitemap.xml                      # Main Sitemap
│   └── sitemap-articles.xml             # Article Sitemap
```

---

## 2. Cara Menambahkan Artikel Baru (Step-by-Step)

### Langkah 1: Riset Kata Kunci & Format Topik
1. Pilih kata kunci primer dan sekunder dari dokumen [keyword-research-top20.md](file:///home/gobeam/Projects/joyofcare-net/keyword-research-top20.md).
2. Tentukan kategori artikel yang sesuai:
   * `healthy-aging`: Geriatri, mobilitas lansia, Parkinson, demensia, osteoartritis, nutrisi tulang.
   * `pengalaman`: Kisah nyata pemulihan pasien homecare.
   * `studi-luar-negeri`: Vaksinasi pelajar, medical check up visa Australia/Inggris.
   * `vaksinasi`: Imunisasi dewasa, vaksin influenza, pneumonia lansia.

### Langkah 2: Penyusunan Konten Berbasis GEO/AIO
Setiap artikel wajib mengikuti struktur formula 5 bagian:
1. **Hook & Lead:** Paragraf pembuka 2-3 kalimat yang langsung menjawab inti pertanyaan pasien / pencari.
2. **Ringkasan Medis (Key Takeaways):** Kotak rangkuman 3-4 poin fakta medis penting dengan bullet centang. Format ini sangat diprioritaskan oleh AI Search (ChatGPT, Perplexity, Google AI Overviews).
3. **Isi Utama Terstruktur:** H2 dan H3 dengan poin-poin bernomor atau bullet list, mencakup langkah praktis, tanda bahaya, dan solusi.
4. **Call-to-Action (CTA) WhatsApp:** Komponen ajakan konsultasi dengan nomor `08811-118-911` dan pesan otomatis yang relevan.
5. **FAQ Medis (3-5 Pertanyaan):** Format tanya jawab ringkas untuk injeksi `FAQPage` schema.

### Langkah 3: Review Medis (E-E-A-T)
Sebelum artikel dirilis ke publik:
- Cantumkan **Penulis** (misal: *Tim Redaksi Medis Joy of Care*).
- Cantumkan **Reviewer Medis Berlisensi** beserta gelar, nomor STR, dan spesialisasi (contoh: *dr. Hendra Wijaya, Sp.KFR*).
- Sertakan catatan penafian (*Medical Disclaimer*) standar di akhir konten.

### Langkah 4: Pembuatan File HTML / MDX
1. Duplikasi file template:
   * Untuk HTML statis: [/home/gobeam/Projects/joyofcare-web/pages/templates/article-template.html](file:///home/gobeam/Projects/joyofcare-web/pages/templates/article-template.html).
   * Untuk Astro / Keystatic / MDX: [/home/gobeam/Projects/joyofcare-web/pages/templates/article-template.mdx](file:///home/gobeam/Projects/joyofcare-web/pages/templates/article-template.mdx).
2. Ganti seluruh placeholder variabel:
   * `{{ARTICLE_TITLE}}`: Judul artikel 50-60 karakter.
   * `{{META_DESCRIPTION}}`: Deskripsi ringkas 150-160 karakter + CTA.
   * `{{CATEGORY_SLUG}}` & `{{CATEGORY_NAME}}`: Kategori slug & label.
   * `{{ARTICLE_SLUG}}`: URL slug bersih (contoh: `panduan-fisioterapi-lansia`).
   * `{{DATE_PUBLISHED}}` & `{{DATE_MODIFIED}}`: Format ISO 8601 (misal: `2026-09-05T08:00:00+07:00`).
   * `{{KEY_TAKEAWAYS_LIST_ITEMS}}`: `<li>Poin ringkasan...</li>`.
   * `{{FAQ_JSON_ITEMS}}` & `{{FAQ_HTML_ACCORDION_ITEMS}}`: Schema JSON-LD & HTML accordion.
3. Simpan file HTML pada direktori kategori:
   * `/home/gobeam/Projects/joyofcare-web/pages/blog/{category-slug}/{article-slug}.html`

### Langkah 5: Registrasi ke Index & Update Otomatis
1. Tambahkan data artikel baru ke file [/home/gobeam/Projects/joyofcare-web/pages/blog/index.json](file:///home/gobeam/Projects/joyofcare-web/pages/blog/index.json):
   ```json
   {
     "slug": "panduan-fisioterapi-lansia",
     "title": "Panduan Lengkap Fisioterapi Lansia di Rumah",
     "url": "http://www.joyofcare.net/blog/healthy-aging/panduan-fisioterapi-lansia",
     "category": "healthy-aging-3",
     "word_count": 950
   }
   ```
2. Jalankan script regenerasi sitemap & RSS:
   ```bash
   python3 /home/gobeam/Projects/joyofcare-web/pages/templates/generate_sitemap.py
   ```

---

## 3. Cara Memperbarui Artikel yang Sudah Ada (Update Workflow)

Peremajaan artikel (*content refresh*) diwajibkan bila ada pembaruan tarif, regulasi kesehatan baru, atau untuk menjaga kesegaran peringkat SEO.

1. **Buka file artikel** di `/home/gobeam/Projects/joyofcare-web/pages/blog/{kategori}/{slug}.html`.
2. **Lakukan revisi teks**, tabel harga, atau referensi klinis.
3. **Perbarui Timestamp:**
   * Di `<meta property="article:modified_time" content="YYYY-MM-DDTHH:MM:SS+07:00">`
   * Di Schema JSON-LD `"dateModified": "YYYY-MM-DDTHH:MM:SS+07:00"`
   * Di teks penutup footer: `Terakhir diperbarui: [Tanggal Baru]`.
4. **Re-generate Sitemap:** Jalankan `python3 generate_sitemap.py` agar tanggal `<lastmod>` di Google Sitemap otomatis diperbarui.

---

## 4. Pre-Publishing SEO-GEO-AIO Checklist

Gunakan daftar periksa berikut sebelum mempublikasikan artikel:

| Kriteria | Standar Kebutuhan | Status Verifikasi |
|---|---|---|
| **Title Tag** | 50–60 karakter; kata kunci utama di depan; diakhiri ` \| Joy of Care` | [ ] Terpenuhi |
| **Meta Description** | 150–160 karakter; persuasif; memuat CTA WhatsApp (08811-118-911) | [ ] Terpenuhi |
| **Canonical URL** | Huruf kecil tanpa trailing slash ganda: `https://www.joyofcare.net/blog/...` | [ ] Terpenuhi |
| **Heading Hierarchy** | Hanya 1 tag `<h1>`; sub-judul menggunakan `<h2>` dan `<h3>` rapi | [ ] Terpenuhi |
| **MedicalWebPage Schema** | Memuat `name`, `author`, `reviewedBy`, `aspect`, dan `publisher` | [ ] Terpenuhi |
| **BlogPosting Schema** | Memuat `headline`, `image`, `datePublished`, `dateModified` | [ ] Terpenuhi |
| **BreadcrumbList Schema** | Beranda › Blog › Kategori › Judul Artikel | [ ] Terpenuhi |
| **FAQPage Schema** | Minimal 3 pertanyaan & jawaban relevan yang cocok untuk featured snippets | [ ] Terpenuhi |
| **Key Takeaways Box** | 3-4 poin ringkasan yang jelas untuk AI citations (ChatGPT/Perplexity/AIO) | [ ] Terpenuhi |
| **Internal Links** | Minimal 2 tautan ke layanan komersil (Dokter, Fisioterapi, dsb) | [ ] Terpenuhi |
| **CTA WhatsApp** | Tombol CTA aktif dengan link prefilled message yang spesifik | [ ] Terpenuhi |
| **E-E-A-T Reviewer** | Byline nama dokter peninjau + kredensial STR resmi | [ ] Terpenuhi |

---

## 5. Panduan Optimalisasi Gambar (Image Optimization)

1. **Format File:**
   - Gunakan format **`.webp`** sebagai standar utama.
   - Hindari upload langsung `.png` atau `.jpg` mentah dari kamera berukuran > 1 MB.
2. **Dimensi Resolusi:**
   - **Hero / Open Graph Image:** `1200 x 630 px` (Rasio 1.91:1), ukuran file `< 120 KB`.
   - **Gambar Sisipan (In-content):** Lebar maksimal `800 px`, ukuran file `< 60 KB`.
   - **Foto Profil Penulis / Reviewer:** `200 x 200 px` (1:1), ukuran file `< 25 KB`.
3. **Konvensi Penamaan File:**
   - Gunakan huruf kecil dipisahkan tanda strip (`-`), mencerminkan isi gambar dan kata kunci.
   - *Contoh Benar:* `fisioterapi-lansia-latihan-keseimbangan.webp`
   - *Contoh Salah:* `IMG_20260905_150021.jpg`
4. **Penerapan Tag `<img>`:**
   - Wajib menyertakan atribut `alt` yang deskriptif dan bernuansa medis:
     ```html
     <img src="/images/blog/fisioterapi-lansia.webp" 
          alt="Fisioterapis Joy of Care mendampingi pasien lansia latihan berjalan di rumah" 
          width="800" height="450" loading="lazy">
     ```
   - Selalu sertakan `loading="lazy"` untuk gambar non-hero demi skor LCP yang optimal.

---

## 6. Integrasi Call to Action (CTA) WhatsApp

Untuk memaksimalkan konversi pembaca blog menjadi pasien, format URL WhatsApp harus selalu menggunakan struktur resmi:

```html
https://api.whatsapp.com/send/?phone=628811118911&text=Hi,%20saya%20tahu%20dari%20blog%20JoyofCare.%20Mau%20konsultasi%20mengenai%20[NAMA_LAYANAN_ATAU_TOPIK]
```

Parameter URL telah disesuaikan agar tim operasional customer service langsung mengetahui artikel mana yang mendatangkan calon pasien.

---

## 7. Pemeliharaan Otomatis & Pemantauan

1. **Pembaruan Sitemap Berkala:**
   Jalankan script generator setiap kali batch artikel baru diunggah:
   ```bash
   python3 /home/gobeam/Projects/joyofcare-web/pages/templates/generate_sitemap.py
   ```
2. **Uji Validasi Schema:**
   Gunakan Google Rich Results Test (`https://search.google.com/test/rich-results`) untuk memverifikasi bahwa `MedicalWebPage`, `Article`, `BreadcrumbList`, dan `FAQPage` terbaca 100% valid tanpa error.
