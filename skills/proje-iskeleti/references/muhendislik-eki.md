# Mühendislik ve proses yazılımı eki

Fiziksel bir prosese bağlı yazılımda (güneş santrali, sulama, HVAC, enerji depolama gibi) spec'e şu kontrolleri ekle. Kullanıcı yazılım tarafında güçlü, fiziksel prosesi öğreniyor olabilir; bu ek o boşluğu görünür kılmak içindir.

## 1. Öğrenme ihtiyacı
- Başlangıç kartındaki "öğrenme ihtiyacı" alanını doldur: bu projede hangi fiziksel kavramlar gerekli?
- Kavramı kullanıcıya kısa açıkla, kaynağını ver; bilgi tabanı kullanılıyorsa orada kavram notu açmayı öner.
- Kullanıcının alan bilgisi gerektiren sorusunu kesin bilgi gibi cevaplama; kaynak göster veya **varsayım** de.

## 2. Dış kısıtlar
Standart, yönetmelik, şebeke/kurum şartı ve üretici verisi **varsayım değildir**; spec 4. başlıkta ayrı listede, kaynağı ve sürümü/tarihiyle yazılır. Kaynağı yoksa **açık soru** olur.

## 3. Birim politikası
- Projede tek birim sistemi (varsayılan SI) ve açıları derece mi radyan mı olduğu spec'te yazılsın.
- Birim değişken adında veya tipinde görünsün (`mesafe_m`, `guc_kW`).
- Girdi dosyasının birimi belirsizse (DXF'te mm mi m mi) sessizce varsayma; sor veya doğrulama adımı ekle.

## 4. Doğrulama sırası
1. **El hesabı:** Tek basit senaryoyu elle veya hesap tablosunda hesapla; kod aynı sonucu vermeli.
2. **Bağımsız referans:** Mümkünse ticari araç (örn. güneş santrali için PVsyst), yayımlanmış örnek veya ölçümle karşılaştır.
3. **Sınır durumları:** Sıfır, en büyük, geçersiz girdi, fiziksel sınırın kenarı.

Uygulamanın mantığını aynen tekrar eden test tek başına doğruluk kanıtı değildir.

## 5. Hassasiyet
Kritik her varsayım için sor: "Bu değer gerçekçi aralığında değişirse sonuç ne kadar değişir?" Aralığı parametreye göre seç, sabit bir yüzde kullanma:
- parametrenin fiziksel olarak mümkün aralığı (ör. mevsimsel sıcaklık, toprak türüne göre iletkenlik),
- ölçüm belirsizliği veya sensör doğruluğu,
- kaynakta, standartta veya üretici verisinde verilen tolerans,
- bunlar yoksa anlamlı senaryolar (en kötü / tipik / en iyi).

±%10 gibi tek bir yüzde yalnız parametre için anlamlıysa ve daha iyi bilgi yoksa örnek yaklaşım olarak kullanılır. Seçilen aralık ve gerekçesi spec'in 4. başlığında varsayımın yanına yazılır. Sonucu çok oynatan varsayım açık sorular listesinde en üste çıkar ve doğrulama önceliği alır.

## 6. Donanım / sensör (yalnız fiziksel sisteme bağlanıyorsa)
- Ölçüm aralığı, çözünürlük, örnekleme sıklığı
- Sensör veya iletişim hatasında davranış
- Güvenli duruma geçiş ve elle müdahale
- Çalışma sınırları (sıcaklık, basınç, akım vb.)

## İlk dilim örneği
Tek bir senaryoyu (bir arazi, bir gün, bir ev) uçtan uca hesapla ve el hesabı / bağımsız referansla kontrol et. Bütün altyapıyı kurup sonucu sona bırakma.
