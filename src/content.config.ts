import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ base: './src/content/articles', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    metaTitle: z.string().optional(),
    metaDescription: z.string().optional(),
    category: z.string(),
    author: z.string().default('Tim Medis Joy of Care'),
    reviewer: z.string().default('dr. Sarah Wijaya, Sp.FR'),
    date: z.coerce.date(),
    featuredImage: z.string().optional(),
    keywords: z.string().optional(),
    internalLinks: z.string().optional(),
    slug: z.string(),
  }),
});

export const collections = { articles };
