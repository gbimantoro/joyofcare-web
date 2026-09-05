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
          validation: { isRequired: true, length: { min: 50, max: 60 } },
        }),
        slug: fields.slug({
          name: { label: "Slug URL" },
          slug: {
            label: "Custom Slug",
            generate: (title) =>
              title
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, "-")
                .replace(/^-|-$/g, ""),
          },
        }),
        metaDescription: fields.text({
          label: "Meta Description (150-160 karakter)",
          validation: { isRequired: true, length: { min: 150, max: 160 } },
        }),
        primaryKeyword: fields.text({
          label: "Primary Keyword",
          validation: { isRequired: true },
        }),
        secondaryKeywords: fields.array({
          label: "Secondary Keywords",
          itemLabel: { field: "keyword" },
          fields: {
            keyword: fields.text({ label: "Keyword" }),
          },
        }),
        category: fields.select({
          label: "Kategori",
          options: [
            { label: "Healthy Aging (Lansia Sehat)", value: "healthy-aging" },
            { label: "Pengalaman Pasien", value: "pengalaman" },
            { label: "Studi Luar Negeri", value: "studi-luar-negeri" },
            { label: "Vaksinasi", value: "vaksinasi" },
          ],
          defaultValue: "healthy-aging",
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
        faq: fields.array({
          label: "FAQ (3-5 pertanyaan)",
          itemLabel: { field: "question" },
          fields: {
            question: fields.text({ label: "Pertanyaan" }),
            answer: fields.text({
              label: "Jawaban",
              multiline: true,
            }),
          },
        }),
        internalLinks: fields.array({
          label: "Internal Links",
          itemLabel: { field: "anchor" },
          fields: {
            anchor: fields.text({ label: "Anchor Text" }),
            url: fields.text({ label: "URL" }),
          },
        }),
        medicalReviewer: fields.text({
          label: "Medical Reviewer",
          defaultValue: "Tim Medis Joy of Care",
        }),
        content: fields.mdx({
          label: "Konten Artikel",
          description: "Tulis konten artikel di sini. Gunakan H2 untuk section utama.",
        }),
        ctaText: fields.text({
          label: "CTA Text",
          defaultValue: "Konsultasi Gratis via WhatsApp",
        }),
        whatsappLink: fields.text({
          label: "WhatsApp Link",
          defaultValue:
            "https://wa.me/628811118911?text=Hi,%20saya%20tahu%20dari%20web.%20Apa%20saja%20layanan%20Joy%20of%20Care?",
        }),
      },
    }),
  },
});
