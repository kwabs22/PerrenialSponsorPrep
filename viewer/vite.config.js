import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { resolve } from 'path';

export default defineConfig({
  plugins: [svelte()],
  base: './',
  assetsInclude: ['**/*.md'],
  server: {
    fs: {
      // Allow serving files from parent directory
      allow: ['..']
    }
  }
});
