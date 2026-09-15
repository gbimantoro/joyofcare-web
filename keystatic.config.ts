import { config, fields, collection, singleton } from '@keystatic/core';

export default config({
  storage: {
    kind: 'github',
    repo: 'gbimantoro/joyofcare-web',
  },
  singletons: {
    siteSettings: singleton({
      label: 'Pengaturan Situs & Analitik',
      path: 'src/content/settings/site',
      format: 'json',
      schema: {
        gaMeasurementId: fields.text({
          label: 'Google Analytics 4 Measurement ID',
          description: 'ID pelacakan GA4 untuk seluruh halaman website (contoh: G-K4XR1K77PK)',
          defaultValue: 'G-K4XR1K77PK',
          validation: { isRequired: true },
        }),
        siteName: fields.text({
          label: 'Nama Situs',
          defaultValue: 'Joy of Care',
        }),
        siteUrl: fields.text({
          label: 'Domain Utama (Canonical)',
          defaultValue: 'https://joyofcare.net',
        }),
        whatsappNumber: fields.text({
          label: 'Nomor WhatsApp Hotline',
          defaultValue: '628811118911',
        }),
      },
    }),
  },
  collections: {
    articles: collection({
      label: 'Artikel',
      slugField: 'slug',
      path: 'src/content/articles/*',
      schema: {
        slug: fields.slug({
          name: { label: 'Slug' },
        }),
        title: fields.text({
          label: 'Judul',
          validation: { isRequired: true, length: { max: 60 } },
        }),
        metaTitle: fields.text({
          label: 'Meta Title (50-60 chars)',
          validation: { length: { max: 60 } },
        }),
        metaDescription: fields.text({
          label: 'Meta Description (150-160 chars)',
          validation: { length: { max: 160 } },
        }),
        category: fields.select({
          label: 'Kategori',
          options: [
            { label: 'Perawatan Lansia', value: 'perawatan-lansia' },
            { label: 'Fisioterapi Rumah', value: 'fisioterapi-rumah' },
            { label: 'Panggil Dokter', value: 'panggil-dokter' },
            { label: 'Parkinson', value: 'parkinson' },
            { label: 'Osteoporosis', value: 'osteoporosis' },
            { label: 'Studi Luar Negeri', value: 'studi-luar-negeri' },
            { label: 'Vaksinasi Rumah', value: 'vaksinasi-rumah' },
            { label: 'Home Lab', value: 'home-lab' },
            { label: 'Infus Vitamin', value: 'infus-vitamin' },
            { label: 'Perawat Homecare', value: 'perawat-homecare' },
            { label: 'Antar Jemput RS', value: 'antar-jemput-rs' },
            { label: 'Kesehatan Umum', value: 'kesehatan-umum' },
            { label: 'Kesehatan Lingkungan', value: 'kesehatan-lingkungan' },
          ],
          defaultValue: 'panggil-dokter',
        }),
        author: fields.text({
          label: 'Penulis',
          defaultValue: 'Tim Kontributor Artikel',
        }),
        reviewer: fields.text({
          label: 'Reviewer Medis',
          defaultValue: 'Tim Medis Joy of Care',
        }),
        date: fields.date({
          label: 'Tanggal Publikasi',
          validation: { isRequired: true },
        }),
        featuredImage: fields.image({
          label: 'Gambar Utama',
          publicPath: '/images/',
        }),
        keywords: fields.text({
          label: 'Keywords (comma separated)',
        }),
        internalLinks: fields.text({
          label: 'Internal Links (comma separated slugs)',
        }),
        body: fields.mdx({
          label: 'Konten Artikel',
          description: 'Tulis konten artikel dalam format MDX',
        }),
      },
    }),
  },
});
