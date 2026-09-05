#!/usr/bin/env python3
"""Replace price card headings with CTA text on service pages."""
import re, os

BASE = "/home/gobeam/Projects/joyofcare-web/pages"

# Per-file replacements for the right-hand card heading
REPLACE = {
    "layanan-fisioterapi-ke-rumah.html": [
        ("<h3 style=\"margin-bottom:16px\">Biaya Fisioterapi</h3>",
         "<h3 style=\"margin-bottom:16px\">Informasi Layanan &amp; Harga</h3><p style=\"margin-bottom:12px\">Fisioterapis berlisensi siap datang ke rumah Anda. Hubungi kami untuk konsultasi gratis dan informasi layanan terkini.</p>"),
    ],
    "homelab.html": [
        ("<h3 style=\"margin-bottom:16px\">Paket HOMELAB</h3>",
         "<h3 style=\"margin-bottom:16px\">Paket Pemeriksaan Lab di Rumah</h3><p style=\"margin-bottom:12px\">Tersedia paket Diabetes, Healthy Aging, dan pemeriksaan lainnya. Kunjungan lab gratis untuk area Jakarta, Tangerang, dan Tangerang Selatan.</p>"),
    ],
    "layanan-perawat-di-rumah.html": [
        ("<h3 style=\"margin-bottom:16px\">Biaya Perawat</h3>",
         "<h3 style=\"margin-bottom:16px\">Layanan Perawat Homecare</h3><p style=\"margin-bottom:12px\">Tersedia paket harian (24 jam), mingguan, dan bulanan. Hubungi kami untuk informasi dan penyesuaian kebutuhan perawatan.</p>"),
    ],
    "infus-suntik-vitamin-di-rumah.html": [
        ("<h3 style=\"margin-bottom:16px\">Pilihan Layanan</h3>",
         "<h3 style=\"margin-bottom:16px\">Pilihan Layanan Infus &amp; Vitamin</h3><p style=\"margin-bottom:12px\">Suntik Vitamin C, infus B Kompleks, paket imun booster, dan nebulisasi dilakukan oleh dokter berlisensi di rumah Anda.</p>"),
    ],
}

for fname, pairs in REPLACE.items():
    path = os.path.join(BASE, fname)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    for old, new in pairs:
        if old in html:
            html = html.replace(old, new)
            print(f"Replaced in {fname}: {old[:40]}...")
        else:
            print(f"NOT FOUND in {fname}: {old[:40]}...")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
