# Bilgi durumları

Spec, Wayfinder ticket cevabı (`## Answer`) ve sohbette önemli her ifadeyi bu beş durumdan biriyle işaretle.

| Durum | Anlamı | Örnek (güneş santrali yerleşimi) |
| --- | --- | --- |
| **tercih** | Kullanıcının amaç veya kapsam seçimi | İlk sürümde kablo güzergâhı yok |
| **doğrulanmış** | Belirli kapsamda kanıtla desteklenmiş | Örnek DXF'te arazi sınırı tek kapalı polyline |
| **varsayım** | Henüz yeterince doğrulanmamış çalışma kabulü | Arazi eğimi yerleşimi etkilemeyecek kadar küçük |
| **öneri** | Ajanın değerlendirilmeyi bekleyen seçeneği | Yerleşim algoritmasını arazi modelinden ayırmak |
| **açık soru** | Henüz yanıtlanmamış | Panel çift sıra mı tek sıra mı? |

Kurallar:

- Kullanıcının bir varsayımı kabul etmesi onun durumunu değiştirmez: **varsayım** kalır ve `varsayım (kullanıcı kabul etti)` diye yazılır. Ne **doğrulanmış** ne de **tercih** olur.
- O varsayımla ilerleme kararı ayrıca **tercih** olarak kaydedilebilir. İki satır birbirine bağlanır, birbirinin yerine geçmez.
- Bir ifade ancak uygun kanıt (ölçüm, kaynak, veri, bağımsız hesap) varsa **doğrulanmış** olur; kanıtın ne olduğu ve hangi kapsamda geçerli olduğu yazılır.
- Örnek:
  - "İşlem süresi sabit kabul ediliyor." → **varsayım** (kullanıcı kabul ettiyse `varsayım (kullanıcı kabul etti)`).
  - "İlk sürümde bu sadeleştirmeyle ilerleyeceğiz." → **tercih**.
  - "İşlem süresi ölçülen 50 çevrimde ±%2 içinde sabit." → **doğrulanmış**, yalnız bu ölçüm kapsamında.
- Kendi önerin kullanıcı seçene kadar **öneri** kalır; kullanıcı seçerse seçim **tercih** olur. Öneri bir dünya iddiası içeriyorsa (ör. "bu sensör yeterince hassas") o iddia ayrıca **varsayım** veya **doğrulanmış** diye etiketlenir.
- Eksik veriyi sessizce doldurma. Varsayılan bir değer kullanırsan **varsayım** diye yaz ve sonucu nasıl etkilediğini belirt.
- Gerçek veri ile test/sentetik veriyi karıştırma; hangisinin kullanıldığını yaz.
