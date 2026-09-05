# Joy of Care CMS (Keystatic)

Headless CMS untuk mengelola artikel kesehatan Joy of Care.

## Setup

```bash
cd cms
npm install
npm run dev
```

Buka http://localhost:3000/keystatic untuk akses admin panel.

## Fitur

- ✅ Editor WYSIWYG untuk artikel (MDX)
- ✅ SEO fields: title, meta description, keywords
- ✅ FAQ management untuk schema markup
- ✅ Internal links management
- ✅ Kategori artikel (Healthy Aging, Pengalaman, Studi Luar Negeri, Vaksinasi)
- ✅ 5 tipe konten (Panduan, Tips, Biaya, dll)
- ✅ Medical reviewer byline
- ✅ WhatsApp CTA otomatis

## Struktur Konten

```
content/articles/
├── panduan-lengkap-panggil-dokter/
│   └── index.mdx
├── tips-cara-fisioterapi-lansia/
│   └── index.mdx
└── ...
```

## Deploy

CMS bisa di-deploy sebagai Vercel/Netlify app terpisah:
```bash
npm run build
vercel deploy
```
