import { config, fields, collection } from '@keystatic/core';

export default config({
  storage: {
    kind: 'github',
    repo: 'gbimantoro/joyofcare-web',
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
            { label: 'Vaksinasi', value: 'vaksinasi' },
            { label: 'Home Lab', value: 'home-lab' },
            { label: 'Infus Vitamin', value: 'infus-vitamin' },
            { label: 'Perawat Homecare', value: 'perawat-homecare' },
            { label: 'Antar Jemput RS', value: 'antar-jemput-rs' },
            { label: 'Kesehatan Umum', value: 'kesehatan-umum' },
          ],
          validation: { isRequired: true },
        }),
        author: fields.text({
          label: 'Penulis',
          defaultValue: 'Tim Medis Joy of Care',
        }),
        reviewer: fields.text({
          label: 'Reviewer Medis',
          defaultValue: 'dr. Sarah Wijaya, Sp.FR',
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
