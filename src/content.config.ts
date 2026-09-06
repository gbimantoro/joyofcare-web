import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ base: './src/content/articles', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    metaTitle: z.string().optional(),
    metaDescription: z.string(),
    category: z.string(),
    author: z.string().default('Tim Kontributor Artikel'),
    reviewer: z.string().default('Tim Medis Joy of Care'),
    date: z.coerce.date(),
    slug: z.string(),
    featuredImage: z.string().optional(),
    primaryKeyword: z.string().optional(),
    secondaryKeywords: z.array(z.string()).optional(),
    internalLinks: z.array(z.string()).optional(),
    faq: z.array(z.object({ question: z.string(), answer: z.string() })).optional(),
    clinicalReferences: z.array(z.string()).optional(),
  }),
});

export const collections = { articles };