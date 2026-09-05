#!/bin/bash

# Remove prices from JoyofCare service pages and replace with WhatsApp CTA

PAGES_DIR="/home/gobeam/Projects/joyofcare-web/pages"

# WhatsApp CTA replacement text
WA_CTA='Hubungi WhatsApp JoC untuk informasi harga dan konsultasi gratis: <a href="https://wa.me/628811118911?text=Hi,%20saya%20tahu%20dari%20web.%20Mau%20tanya%20harga%20layanan">Chat WhatsApp</a>'

# Files to update
FILES=(
    "homelab.html"
    "infus-suntik-vitamin-di-rumah.html"
    "layanan-fisioterapi-ke-rumah.html"
    "layanan-perawat-di-rumah.html"
    "panggil-dokter-ke-rumah.html"
    "index.html"
)

for FILE in "${FILES[@]}"; do
    FILEPATH="$PAGES_DIR/$FILE"
    if [ ! -f "$FILEPATH" ]; then
        echo "SKIP: $FILE not found"
        continue
    fi
    
    echo "Processing: $FILE"
    
    # Backup original
    cp "$FILEPATH" "$FILEPATH.bak"
    
    # Remove price tables (table with class price-table)
    # Pattern: from <table class="price-table"> to </table>
    sed -i -E '/<table class="price-table">/,/<\/table>/c\          <p style="color:var(--color-primary);font-weight:600;text-align:center;padding:20px 0;">Hubungi WhatsApp JoC untuk informasi harga dan konsultasi gratis</p>' "$FILEPATH"
    
    # Remove price mentions in text (Rp X.XXX.XXX patterns)
    sed -i 's/Mulai Rp [0-9.,]*//g' "$FILEPATH"
    sed -i 's/Rp [0-9.,]*//g' "$FILEPATH"
    sed -i 's/harga all-in[^.]*./harga kompetitif yang sudah termasuk transport./g' "$FILEPATH"
    sed -i 's/harga already termasuk[^.]*./sudah termasuk transport./g' "$FILEPATH"
    
    # Update FAQ answers that mention prices
    # Panggil dokter FAQ
    if [ "$FILE" = "panggil-dokter-ke-rumah.html" ]; then
        sed -i 's/Biaya all-in mulai dari Rp 380.000 sudah termasuk transport dokter. Harga bervariasi tergantung jenis pemeriksaan dan wilayah./Hubungi WhatsApp JoC untuk informasi harga terkini dan konsultasi gratis./g' "$FILEPATH"
    fi
    
    # Homelab FAQ - remove price references
    if [ "$FILE" = "homelab.html" ]; then
        sed -i 's/hemat s.d Rp 200.000/harga kompetitif/g' "$FILEPATH"
    fi
    
    # Update CTA buttons to use wa.me format
    sed -i 's|https://api.whatsapp.com/send/?phone=628811118911|https://wa.me/628811118911|g' "$FILEPATH"
    
    # Remove the "*Harga sudah termasuk transport" notes
    sed -i '/\*Harga sudah termasuk transport/d' "$FILEPATH"
    
    # Update buttons that say "Tanya Harga" to "Chat WhatsApp"
    sed -i 's/Tanya Harga via WhatsApp/Chat WhatsApp/g' "$FILEPATH"
    sed -i 's/Pesan HOMELAB via WhatsApp/Chat WhatsApp/g' "$FILEPATH"
    
    echo "  -> Updated: $FILE"
done

# Update JSON-LD FAQ schema in panggil-dokter (has price in schema)
PANGGIL_DOKTER="$PAGES_DIR/panggil-dokter-ke-rumah.html"
if [ -f "$PANGGIL_DOKTER" ]; then
    sed -i 's/Biaya all-in mulai dari Rp 380.000 sudah termasuk transport dokter. Harga bervariasi tergantung jenis pemeriksaan dan wilayah./Hubungi WhatsApp JoC untuk informasi harga terkini dan konsultasi gratis./g' "$PANGGIL_DOKTER"
fi

echo ""
echo "=== Price Removal Complete ==="
echo "Files updated:"
for FILE in "${FILES[@]}"; do
    echo "  - $FILE"
done