# Başlangıç kartı ve spec şablonu

## Başlangıç kartı (ilk oturum soru listesi)

Kart spec'e kopyalanmaz; ilk oturumda neyin bilinip neyin sorulacağını görmek içindir. Eldeki bilgiyle doldur, yalnız yaklaşımı değiştiren eksikleri sor.

| Alan | Doldurulacak bilgi |
| --- | --- |
| Proje adı | Kısa ad |
| Problem ve kullanıcı | Kimin hangi ihtiyacı? |
| Beklenen fayda | Hangi iş, karar veya süre iyileşecek? |
| Mevcut durum | Fikir, elle yapılan süreç, prototip, mevcut yazılım |
| Bu çalışmanın hedefi | İlk sürüm, belirli özellik, karar veya deney |
| Kaynaklar | Dosyalar, veri, çizimler, standartlar, mevcut kod |
| Kısıtlar | Zaman, ortam, erişim, zorunlu teknoloji |
| Öğrenme ihtiyacı | Kullanıcının bu projede öğrenmesi gereken fiziksel proses veya alan bilgisi |
| Açık noktalar | Bilinmeyen ve yaklaşımı etkileyen konular |

**Öğrenme ihtiyacı** alanı boş değilse: o kavramı yalnız sorma, kısa açıkla, kaynağını ver ve bilgi tabanı kullanılıyorsa kavram notu açmayı öner.

## Spec şablonu (`docs/spec.md`)

Her başlıkta bilinmeyeni boş bırak veya **açık soru** diye işaretle. Projeye uymayan başlığı gerekçesiyle "uygulanamaz" yaz; yapay gereksinim üretme.

```markdown
# <Proje adı> — Spec

Durum: taslak | uygulanıyor · Son güncelleme: YYYY-MM-DD
Bilgi tabanı notu: yok | <bağlantı veya yol>
Karar haritası: yok | .scratch/<effort>/map.md (wayfinder)

## 1. Problem ve hedef
Neyi, kimin için çözüyoruz? Çıktının faydası ne? (tek paragraf)
Ana senaryo: girdi → beklenen davranış → sonuç.

## 2. Kapsam
- İçeride:
- Bilerek dışarıda (gerekçe):
- Kapsamda ama net değil:
- Gerçek kısıtlar:

## 3. Girdi, çıktı ve veri sözleşmeleri
Her önemli girdi/çıktı için aşağıdaki sözleşme tablosu. Büyürse docs/data-contracts.md'ye taşı, burada bağlantı bırak.
| Ad | Yön | Kaynak/sahip | Biçim/şema | Birim | Zorunlu | Geçerlilik kuralı | Eksik/hatalı veride davranış |
Zaman verisi varsa: zaman dilimi, sıklık, sıralama.
Örnek girdi ve beklenen çıktı (gerçek mi sentetik mi?).

## 4. Alan kuralları, modeller ve varsayımlar
Denklemler, sabitler, birimler, sınır koşulları, sadeleştirmeler, geçerlilik aralığı.
Her varsayım: etiket · kaynak · geçerli olduğu koşul · nasıl kontrol edilir.
Dış kısıtlar (standart, yönetmelik, üretici verisi) ayrı listede, kaynaklı.

## 5. Bileşenler ve akış
3–6 kutu: sorumluluk, girdi, çıktı, hata davranışı.
Örnek: veri okuma → doğrulama → model → algoritma → çıktı. Sınıf tasarımı değil.

## 6. Kabul kriterleri ve doğrulama
- Kullanıcı sonucu:
- Davranış (normal, sınır, hata):
- Alan doğruluğu (bağımsız referansla):
- Gerekirse hız / güvenilirlik:
Sayı veya tolerans koyuyorsan gerekçesini yaz; keyfî eşik üretme.

## 7. Açık sorular ve riskler
| Soru | Etkilediği başlık | Çözüm yolu | Çözülmeden ilerlenir mi? | Durum |
Çözülen soru silinmez: "çözüldü → <ticket veya ADR bağlantısı>" diye işaretlenir.
Harita varsa açık soruların asıl yeri Wayfinder ticket'larıdır; burada yalnız bağlantı kalır.

## Kapanan kararlar (özet)
- <karar sonucu> · <tercih|doğrulanmış|varsayım> · <ticket/ADR bağlantısı>
```

## Gerektiğinde eklenecek başlıklar

Yalnız gerçekten ilgiliyse: dış servis/API (kota, hata, sürüm), hassas veri (erişim, saklama), fiziksel kontrol (bkz. mühendislik eki), mevcut yazılım değişikliği (korunacak davranış, geriye uyumluluk), üretimde çalışma (dağıtım, yedek, geri dönüş).
