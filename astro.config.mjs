import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import keystatic from '@keystatic/astro';

export default defineConfig({
  integrations: [
    mdx(),
    keystatic(),
  ],
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
});
