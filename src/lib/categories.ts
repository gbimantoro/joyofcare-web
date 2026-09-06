export interface Category {
  slug: string;
  label: string;
}

/** Single source of truth for article categories (slug -> display label).
 *  Values match the `category` frontmatter field used in migrated MDX files.
 */
export const CATEGORIES: Category[] = [
  { slug: 'perawatan-lansia', label: 'Perawatan Lansia' },
  { slug: 'fisioterapi-rumah', label: 'Fisioterapi Rumah' },
  { slug: 'panggil-dokter', label: 'Panggil Dokter' },
  { slug: 'parkinson', label: 'Parkinson' },
  { slug: 'studi-luar-negeri', label: 'Studi Luar Negeri' },
  { slug: 'osteoporosis', label: 'Osteoporosis' },
  { slug: 'antar-jemput-rs', label: 'Antar Jemput RS' },
  { slug: 'vaksinasi-rumah', label: 'Vaksinasi Rumah' },
  { slug: 'infus-vitamin', label: 'Infus Vitamin' },
  { slug: 'perawat-homecare', label: 'Perawat Homecare' },
  { slug: 'kesehatan-umum', label: 'Kesehatan Umum' },
  { slug: 'home-lab', label: 'Home Lab' },
];

export function categoryLabel(slug: string): string {
  return CATEGORIES.find((c) => c.slug === slug)?.label ?? slug;
}

export const CATEGORY_SLUGS = CATEGORIES.map((c) => c.slug);