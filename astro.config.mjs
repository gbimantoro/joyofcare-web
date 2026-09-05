import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import keystatic from '@keystatic/astro';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  integrations: [
    mdx(),
    keystatic(),
  ],
  output: 'server',
  adapter: cloudflare(),
  trailingSlash: 'always',
});
