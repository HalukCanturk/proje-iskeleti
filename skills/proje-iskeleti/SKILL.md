---
name: proje-iskeleti
description: Yeni bir projeye ya da kapsamlı bir özelliğe koda başlamadan önce kullanıcıyla birlikte hedefi ve kapsamı netleştirir, 7 başlıklı spec'i (docs/spec.md) yazar, varsayım / tercih / doğrulanmış bilgiyi ayırır, veri sözleşmelerini ve kabul kriterlerini belirler, ilk uygulanabilir dilimi tanımlar. Çok oturumluk karar işi için kullanıcıyı Matt Pocock'un orijinal Wayfinder'ına yönlendirir ve Wayfinder oturumlarında çözülen kararları spec'e işler. Tetik - "yeni proje", "proje iskeleti", "spec yazalım", "spec çıkar", "projeye başlamadan önce", "bu özelliği tasarlayalım", "spec'i güncelle", "haritayı spec'e işle", "/proje-iskeleti". Kullanma - küçük düzeltme, spec'i net projede rutin görev.
---

# Proje iskeleti

Koda başlamadan önce ajanın koddan asla çıkaramayacağı bilgiyi yazıya dökmek: hedef, kapsam, alan kuralları ve varsayımlar, veri sözleşmeleri, kabul kriterleri. Spec kullanıcıyla birlikte yazılır; senin rolün sorgulamak, eksik göstermek, seçenek ve önerini sunmaktır. Kullanıcının tercih sorularını onun yerine cevaplayıp kapatma.

Bu skill **spec'in sahibidir**. Çok oturumluk karar haritasını kendisi işletmez; onu Matt Pocock'un orijinal `wayfinder` skill'i işletir (`mattpocock-skills` plugin'i). Kendi karar haritası, karar kaydı veya ticket biçimi uydurma.

## Hangi moddasın

- **A. Başlangıç:** Yeni proje veya özellik, `docs/spec.md` yok ya da boş → aşağıdaki "Başlangıç yolu".
- **B. Wayfinder oturumundan çağrıldın:** Bir Wayfinder haritasının `## Notes` bölümü seni çağırdı veya kullanıcı "haritayı spec'e işle" dedi → "Spec senkronu". Başlangıç yolunu baştan çalıştırma.
- **C. Kapanış:** Harita bitti (açık, bloklanmamış ticket yok, "Not yet specified" boş) veya harita hiç gerekmedi → "Uygulamaya geçiş".

## Belgeler nerede durur

İlke: güncel spec, kararlar ve plan **proje çalışma klasöründe** durur. Ayrı bir bilgi tabanı (ör. Obsidian vault) kullanılıyorsa orada yalnız öğrenme notları, araştırma ve spec'e bağlantı tutulur.

| Dosya (proje klasörü) | Sahibi | İçerik |
| --- | --- | --- |
| `docs/spec.md` | bu skill | 7 başlıklı güncel proje tanımı; Wayfinder'ın **Destination**'ı |
| `docs/plan.md` | bu skill | ilk uçtan uca dilimin planı |
| `docs/data-contracts.md` | bu skill, gerekirse | spec 3. başlık büyürse veri sözleşmeleri |
| `.scratch/<effort>/map.md`, `.scratch/<effort>/issues/NN-*.md` | wayfinder | karar haritası ve karar ticket'ları (local-markdown tracker) |
| `GLOSSARY.md`, `docs/adr/` | domain-modeling | terimler; yalnız geri alması zor, gerekçesiz şaşırtıcı, gerçek ödünleşimli kararlar için ADR |
| `docs/agents/*.md`, `CLAUDE.md`/`AGENTS.md` içinde `## Agent skills` | setup-matt-pocock-skills | tracker ve domain doc yapılandırması |

- Bir karar tek yerde yaşar: haritalı işte ticket'ın `## Answer` bölümünde; spec yalnız sonucu yazar ve ticket'a bağlantı verir. Aynı gerekçeyi iki yerde tutma.
- Ayrı karar kaydı klasörü (`docs/kararlar/`) veya kendi harita dosyası açma.
- Bilgi tabanı kullanılıyorsa proje klasörünün onun dışında olduğunu doğrula; belirsizse sor.

## A. Başlangıç yolu

1. Mevcut bağlamı oku: varsa bilgi tabanındaki proje notu, proje klasöründe `docs/`, `GLOSSARY.md`, `docs/adr/`, `CLAUDE.md`/`AGENTS.md`, varsa `.scratch/`. Erişemediğini söyle.
2. [Başlangıç kartını](references/spec-sablonu.md) eldeki bilgiyle doldur; bilineni, öneriyi, bilinmeyeni ayır.
3. Hedefi iki üç cümleyle geri söyle; kullanıcı onaylasın.
4. Yaklaşımı en çok etkileyen eksik sorudan başla. Bu skill'in kendi fazında **tek seferde bir soru** sor; cevaplanmış tercihi tekrar sorma. (Wayfinder içindeki grilling turları kendi kuralıyla, birden çok soruyla ilerler; onu değiştirme.)
5. `docs/spec.md` taslağını [şablonla](references/spec-sablonu.md) yaz; bilinmeyeni **açık soru** bırak, uydurma. Veri sözleşmelerini 3. başlıkta, kabul kriterlerini 6. başlıkta somutlaştır.
6. Mühendislik / proses projesinde [mühendislik ekini](references/muhendislik-eki.md) uygula.
7. **Harita gerekir mi?** Açık sorular tek oturumda kullanıcıyla çözülebiliyorsa harita açma; sor-cevapla ve C'ye geç. Açık kararlar birbirine bağlıysa, araştırma/prototip/hazırlık işi bekliyorsa veya tek oturuma sığmıyorsa → "Wayfinder'a geçiş".

## Wayfinder'a geçiş

`wayfinder` ve `setup-matt-pocock-skills` **kullanıcı tarafından çağrılan** skill'lerdir (`disable-model-invocation: true`). Sen onları Skill aracıyla çağıramazsın; çağırmış gibi davranma. Kullanıcıya şu adımları ver:

1. **Proje klasöründe bir kez:** `/mattpocock-skills:setup-matt-pocock-skills`. Tracker sorusunda uzak repo yoksa **local markdown** önerilir. Bu skill `CLAUDE.md` / `AGENTS.md` dosyasına `## Agent skills` bloğu ve `docs/agents/` ekler. Bilgi tabanı klasöründe değil, proje klasöründe çalıştırılır.
2. **Haritayı başlat:** `/mattpocock-skills:wayfinder` ve aşağıdaki geçiş metnini mesaja ekle. Metni sen hazırla, `docs/spec.md` içindeki açık sorulardan ve kapsam dışı listesinden besle:

```text
Destination: <proje> için docs/spec.md'nin 7 başlığı uygulanabilir düzeyde dolu ve
uygulamaya geçiş kontrolünü geçiyor (ilk uçtan uca dilim tanımlı).

Notes:
- Alan: <kısa alan tanımı>. Dil: Türkçe.
- Her oturumda: Call the Skill tool with "proje-iskeleti" (spec senkronu, mod B).
- Kalıcı tercih: Ticket çözülüp ## Answer yazıldıktan ve map'e işaretçi eklendikten sonra, oturumu bitirmeden
  proje-iskeleti'nin "B. Spec senkronu" adımlarını uygula: docs/spec.md'de ilgili başlığı güncelle,
  ticket'a bağlantı ver, bilgi durumunu etiketle.
- Bilgi durumları: tercih / doğrulanmış / varsayım / öneri / açık soru ayrı tutulur.
- Başlangıç bağlamı: docs/spec.md (taslak), açık sorular 7. başlıkta.
```

3. Sonraki oturumlarda kullanıcı `/mattpocock-skills:wayfinder <map yolu>` ile bir sonraki ticket'ı çözer. Wayfinder oturum başına bir ticket çözer (araştırma ticket'ları hariç).

Not: Wayfinder'ın research ve prototype ticket'ları bulguları atılabilir git dallarına (`research/<ad>`) kaydeder ve dalı push eder. Proje klasörü git deposu değilse veya uzak repo yoksa bunu kullanıcıya önceden söyle.

## B. Spec senkronu (Wayfinder oturumunda)

Yeni soru üretme ve ticket'ın kararını değiştirme; Wayfinder'ın akışı önceliklidir. Ticket çözülüp `## Answer` yazıldıktan sonra:

1. Ticket'ın sorusunu ve cevabını oku; hangi spec başlığını etkilediğini bul.
2. `docs/spec.md`'de o başlığı güncelle; sonucu kısa yaz ve ticket'a bağlantı ver: `([NN · başlık](../.scratch/<effort>/issues/NN-slug.md))`.
3. Bilgi durumunu etiketle ([bilgi-durumlari.md](references/bilgi-durumlari.md)): kullanıcı tercihi mi, kaynakla doğrulanmış mı, hâlâ varsayım mı?
4. 7. başlıktaki ilgili açık soruyu kaldırma; "çözüldü → ticket bağlantısı" diye işaretle.
5. Kararın spec'te çelişki doğurduğunu görürsen düzeltmeyi kullanıcıya göster; spec'i sessizce yeniden yazma.
6. Geçiş kontrolünü yeniden değerlendir ve tek satırla söyle: "Geçiş için kalan: …".

## C. Uygulamaya geçiş

Kontrol:

- Bu dilimin amacı ve kapsamı açık mı?
- Girdiler mevcut mu; eksik veya hatalı girdinin davranışı veri sözleşmesinde tanımlı mı?
- Temel alan kuralları ve varsayımlar yazılı ve etiketli mi?
- Çıktı ve bileşen bağlantıları belli mi?
- Kabul ölçütü ve kontrol yöntemi belirli mi?
- Yaklaşımı kökten değiştirecek çözülmemiş engel var mı (açık ticket, "Not yet specified" maddesi)?

Geçerse ilk uçtan uca dilimin küçük planını `docs/plan.md`'ye yaz ve uygulamayı temiz yeni oturumda başlatmayı öner. Geçmezse eksikleri listele; harita varsa yeni ticket gerektiğini söyle (ticket'ı Wayfinder açar).

## Sürekli kurallar

- Teknoloji (dil, framework, veritabanı) kullanıcı seçmediyse kendiliğinden seçme; seçenek ve ödünleşim sun.
- Uygulama sırasında bir varsayım veya karar değişirse aynı oturumda `docs/spec.md`'yi güncelle. Kod ile spec çelişirse dur ve sor.
- Orijinal plugin dosyalarını düzenleme; bize özgü kurallar yalnız bu skill'de durur.
- `AGENTS.md`/`CLAUDE.md` kısa kalır: amaç, belge yolları, gerçek doğrulama komutları. Spec'i oraya kopyalama.

## Referanslar

- [spec-sablonu.md](references/spec-sablonu.md): başlangıç kartı, 7 başlıklı spec, veri sözleşmesi şablonu
- [bilgi-durumlari.md](references/bilgi-durumlari.md): beş bilgi durumu
- [muhendislik-eki.md](references/muhendislik-eki.md): proses ve mühendislik projelerine ek kontroller

Kaynaklar: "Proje İskeleti ve Wayfinder — Genel Ajan Rehberi" (yazarın kendi çalışma notu, yayımlanmadı); `mattpocock-skills` 1.3.1 (`wayfinder`, `setup-matt-pocock-skills`, `grilling`, `domain-modeling`, local-markdown tracker). Henüz gerçek bir projede denenmedi.
