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

- Kullanıcının bir varsayımı onaylaması onu **doğrulanmış** yapmaz; **tercih** olur. Dış dünyaya ilişkin iddianın kanıtı ayrı tutulur.
- Kendi önerin onaylanana kadar **öneri** kalır.
- Eksik veriyi sessizce doldurma. Varsayılan bir değer kullanırsan **varsayım** diye yaz ve sonucu nasıl etkilediğini belirt.
- Gerçek veri ile test/sentetik veriyi karıştırma; hangisinin kullanıldığını yaz.
