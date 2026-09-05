import { config, fields, collection } from "@keystatic/core";

export default config({
  storage: {
    kind: "local",
  },
  collections: {
    articles: collection({
      label: "Artikel Kesehatan",
      slugField: "slug",
      path: "content/articles/*",
      format: { extension: "mdx" },
      entryLayout: "content",
      fields: {
        title: fields.text({
          label: "Judul Artikel",
          validation: { isRequired: true },
        }),
        slug: fields.slug({
          name: { label: "Slug URL" },
        }),
        metaDescription: fields.text({
          label: "Meta Description (150-160 karakter)",
          validation: { isRequired: true },
        }),
        primaryKeyword: fields.text({
          label: "Primary Keyword",
          validation: { isRequired: true },
        }),
        category: fields.select({
          label: "Kategori",
          options: [
            { label: "Perawatan Lansia", value: "perawatan-lansia" },
            { label: "Fisioterapi Rumah", value: "fisioterapi-rumah" },
            { label: "Panggil Dokter", value: "panggil-dokter" },
            { label: "Parkinson", value: "parkinson" },
            { label: "Studi Luar Negeri", value: "studi-luar-negeri" },
            { label: "Osteoporosis", value: "osteoporosis" },
            { label: "Antar Jemput RS", value: "antar-jemput-rs" },
            { label: "Perawat Homecare", value: "perawat-homecare" },
            { label: "Home Lab", value: "home-lab" },
            { label: "Vaksinasi Rumah", value: "vaksinasi-rumah" },
            { label: "Infus Vitamin", value: "infus-vitamin" },
            { label: "Kesehatan Umum", value: "kesehatan-umum" },
          ],
          defaultValue: "kesehatan-umum",
        }),
        variationType: fields.select({
          label: "Tipe Konten",
          options: [
            { label: "Panduan Lengkap", value: "panduan-lengkap" },
            { label: "Tips & Cara", value: "tips-dan-cara" },
            { label: "Yang Perlu Anda Ketahui", value: "yang-perlu-anda-ketahui" },
            { label: "Biaya & Perbandingan", value: "biaya-dan-perbandingan" },
            { label: "Kapan Harus", value: "kapan-harus" },
          ],
          defaultValue: "panduan-lengkap",
        }),
        content: fields.mdx({
          label: "Konten Artikel",
        }),
      },
    }),
  },
});
