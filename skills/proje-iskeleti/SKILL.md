---
name: proje-iskeleti
description: Yeni bir projeye ya da kapsamlı bir özelliğe koda başlamadan önce kullanıcıyla birlikte hedefi ve kapsamı netleştirir, 7 başlıklı spec'i (docs/spec.md) yazar, varsayım / tercih / doğrulanmış bilgiyi ayırır, veri sözleşmelerini ve kabul kriterlerini belirler, ilk uygulanabilir dilimi tanımlar. Çok oturumluk karar işi için kullanıcıyı Matt Pocock'un orijinal Wayfinder'ına yönlendirir ve Wayfinder oturumlarında çözülen kararları spec'e işler. Tetik - "yeni proje", "proje iskeleti", "spec yazalım", "spec çıkar", "projeye başlamadan önce", "bu özelliği tasarlayalım", "spec'i güncelle", "haritayı spec'e işle", "/proje-iskeleti". Kullanma - küçük düzeltme, spec'i net projede rutin görev.
---

# Proje iskeleti

Koda başlamadan önce ajanın koddan asla çıkaramayacağı bilgiyi yazıya dökmek: hedef, kapsam, alan kuralları ve varsayımlar, veri sözleşmeleri, kabul kriterleri. Spec kullanıcıyla birlikte yazılır; senin rolün sorgulamak, eksik göstermek, seçenek ve önerini sunmaktır. Kullanıcının tercih sorularını onun yerine cevaplayıp kapatma.

Bu skill **spec'in sahibidir**. Çok oturumluk karar haritasını kendisi işletmez; onu Matt Pocock'un orijinal `wayfinder` skill'i işletir (`mattpocock-skills` plugin'i). Kendi karar haritası, karar kaydı veya ticket biçimi uydurma.

## Hangi moddasın

- **A. Başlangıç:** Yeni proje veya özellik, `docs/spec.md` yok ya da boş → "A. Başlangıç yolu".
- **B. Wayfinder oturumundan çağrıldın:** Bir Wayfinder haritasının `## Notes` bölümü seni çağırdı veya kullanıcı "haritayı spec'e işle" dedi → "B. Spec senkronu". Çağrı bağlamında `açılış` geçiyorsa (harita yeni kuruldu, ticket kapanmadı) → "B0. Harita açılışı". Başlangıç yolunu baştan çalıştırma.
- **Yalnız çizim:** Kullanıcı "haritayı çiz" dediyse yalnız "Görselleştirme" bölümündeki betiği çalıştır; spec'e dokunma.
- **C. Kapanış:** Harita **tamamlandı** (bkz. "Harita durumu") veya harita hiç gerekmedi → "C. Uygulamaya geçiş". Harita tamamlanmadıysa C'ye geçme; durumu raporla.

## Belgeler nerede durur

İlke: güncel spec, kararlar ve plan **proje çalışma klasöründe** durur. Ayrı bir bilgi tabanı (ör. Obsidian vault) kullanılıyorsa orada yalnız öğrenme notları, araştırma ve spec'e bağlantı tutulur.

| Dosya (proje klasörü) | Sahibi | İçerik |
| --- | --- | --- |
| `docs/spec.md` | bu skill | 7 başlıklı güncel proje tanımı; Wayfinder'ın **Destination**'ı |
| `docs/plan.md` | bu skill | ilk uçtan uca dilimin planı |
| `docs/data-contracts.md` | bu skill, gerekirse | spec 3. başlık büyürse veri sözleşmeleri |
| `docs/harita.md`, `docs/harita.html` | bu skill (betikle üretilir) | karar şeması (Mermaid) ve etkileşimli bağ grafiği; elle düzenlenmez |
| `.scratch/<effort>/map.md`, `.scratch/<effort>/issues/NN-*.md` | wayfinder | karar haritası ve karar ticket'ları (local-markdown tracker) |
| `GLOSSARY.md`, `docs/adr/` | domain-modeling | terimler; yalnız geri alması zor, gerekçesiz şaşırtıcı, gerçek ödünleşimli kararlar için ADR |
| `docs/agents/*.md`, `CLAUDE.md`/`AGENTS.md` içinde `## Agent skills` | setup-matt-pocock-skills | tracker ve domain doc yapılandırması |

- Bir karar tek yerde yaşar: haritalı işte ticket'ın `## Answer` bölümünde; spec yalnız sonucu yazar ve ticket'a bağlantı verir. Aynı gerekçeyi iki yerde tutma.
- Ayrı karar kaydı klasörü (`docs/kararlar/`) veya kendi harita dosyası açma; orijinal tracker'ın yollarını (`.scratch/<effort>/…`) değiştirme.
- Bilgi tabanı kullanılıyorsa proje klasörünün onun dışında olduğunu doğrula; belirsizse sor.

### Karar kayıtları kalıcı proje belgesidir

Local-markdown tracker kullanılan projede `.scratch/<effort>/map.md` ve `.scratch/<effort>/issues/*.md` **kalıcı proje belgeleridir**: `docs/spec.md` onlara bağlantı verir. Git dışında kalırlarsa spec'teki bağlantılar başka bir bilgisayarda veya klonda çalışmaz.

- Harita ve ilk ticket dosyaları oluştuktan sonra (ilk spec senkronunda) ve C'de kontrol et: `git check-ignore .scratch/<effort>/map.md .scratch/<effort>/issues/<bir-ticket>.md` (`-v` olmadan). Yazdırılan her yol dışlanıyor; hiçbir şey yazdırmazsa dışlanmıyor. Hangi kuralın etkili olduğunu görmek için `-v` eklenebilir; `!` ile başlayan kural dosyanın dışlanmadığını gösterir.
- Dışlanıyorlarsa kullanıcıya hangi kuralın dışladığını göster ve dar bir düzeltme öner. Git, dışlanmış bir klasörün içindeki dosyayı geri alamaz; bu yüzden `.scratch/` klasör kuralı yerine şu satırlar kullanılır:

  ```gitignore
  .scratch/*
  !.scratch/<effort>/
  .scratch/<effort>/*
  !.scratch/<effort>/map.md
  !.scratch/<effort>/issues/
  ```

  `.gitignore` dosyasını kullanıcı onaylamadan değiştirme.
- `.scratch/` altındaki her şeyi topluca sürümlemeyi önerme. Kalıcı olanlar harita ve ticket dosyalarıdır; geçici çıktılar (deneme çıktıları, büyük ara dosyalar) dışlanmış kalır. Emin olmadığın dosyayı kullanıcıya sor. Wayfinder'ın research/prototype bulguları zaten ayrı git dallarında durur.
- Kalıcı kayıtları ilgili spec değişikliğiyle aynı commit'te sürümlemeyi öner; commit'i kullanıcı istemeden atma.
- Bu skill'in dağıtım reposundaki `.gitignore` kullanıcı projeleri için değildir; projeye kopyalanmaz.

## Görselleştirme (`docs/harita.md`, `docs/harita.html`)

Haritanın ve spec'in durumunu tek bakışta göstermek için [scripts/harita_ciz.py](scripts/harita_ciz.py) iki dosyayı **baştan üretir** ([scripts/harita_sablon.html](scripts/harita_sablon.html) şablonuyla):

- **`docs/harita.md` — karar şeması (Mermaid):** ticket başına bir kutu (başlık, `Type`, durum), `Blocked by` satırlarından oklar, kapanan ticket'ta map'in `Decisions so far` özeti, sis ve kapsam dışı ayrı gruplarda, altında ticket tablosu. Obsidian, GitHub ve VS Code önizlemesi çizer.
- **`docs/harita.html` — etkileşimli kuvvet grafiği:** spec, 7 başlığı, ticket'lar, sis ve kapsam dışı maddeleri düğüm; bağlar yalnız dosyalarda yazılı olandan çizilir (`Blocked by` oku; spec başlığındaki ticket bağlantısı; sis/kapsam dışı maddesinde geçen "spec N"; bağı yazılı olmayan kapsam dışı maddesi 2. başlığa). Düğüm üzerine gelince bağları öne çıkar ve özetini gösterir, tıklayınca dosyayı açar. Tarayıcıda açılır; d3 cdnjs'ten yüklenir.
- Renk durumu gösterir: kapalı, çalışılabilir, sahiplenilmiş, bloklu; sis kesikli, kapsam dışı soluk.
- **Kaynaklar yalnız okunur:** ticket başlık satırları, `map.md` bölümleri, `docs/spec.md`. Ticket gövdesi (`## Question`, `## Answer`) okunmaz. Betik ticket, map veya spec dosyasına yazmaz.
- **Uydurma bağ yok:** Dosyalarda yazılı olmayan bağ çizilmez; sis maddeleri ticket'lara bağlanmaz.
- Çalıştırma, proje kökünde: `python <skill klasörü>/scripts/harita_ciz.py` (birden çok harita varsa `--effort <ad>`). Çıktının son satırındaki harita durumu senin "Harita durumu" değerlendirmenin yerine geçmez; Destination'ı sen kontrol edersin.
- `docs/harita.md` ve `docs/harita.html` üretilmiş dosyalardır; elle düzeltme yapma, kaynağı düzelt ve yeniden üret. İlgili spec değişikliğiyle aynı commit'te sürümlenmesini öner.
- Betik çalışmazsa (Python yok, harita bulunamadı) spec işini durdurma; "Görselleştirme üretilemedi: <neden>" de.

## A. Başlangıç yolu

1. Mevcut bağlamı oku: varsa bilgi tabanındaki proje notu, proje klasöründe `docs/`, `GLOSSARY.md`, `docs/adr/`, `CLAUDE.md`/`AGENTS.md`, varsa `.scratch/`. Erişemediğini söyle.
2. [Başlangıç kartını](references/spec-sablonu.md) eldeki bilgiyle doldur; bilineni, öneriyi, bilinmeyeni ayır.
3. Hedefi iki üç cümleyle geri söyle; kullanıcı onaylasın.
4. Yaklaşımı en çok etkileyen eksik sorudan başla. Bu skill'in kendi fazında **tek seferde bir soru** sor; cevaplanmış tercihi tekrar sorma. (Wayfinder içindeki grilling turları kendi kuralıyla, birden çok soruyla ilerler; onu değiştirme.)
5. `docs/spec.md` taslağını [şablonla](references/spec-sablonu.md) yaz; bilinmeyeni **açık soru** bırak, uydurma. Veri sözleşmelerini 3. başlıkta, kabul kriterlerini 6. başlıkta somutlaştır.
6. Mühendislik / proses projesinde [mühendislik ekini](references/muhendislik-eki.md) uygula.
6a. Görselleştirmeyi üret: henüz harita yoksa betik yalnız spec düğümlerini çizer.
7. **Harita gerekir mi?** Açık sorular tek oturumda kullanıcıyla çözülebiliyorsa harita açma; sor-cevapla ve C'ye geç. Açık kararlar birbirine bağlıysa, araştırma/prototip/hazırlık işi bekliyorsa veya tek oturuma sığmıyorsa → "Wayfinder'a geçiş".

## Wayfinder'a geçiş

`wayfinder` ve `setup-matt-pocock-skills` **kullanıcı tarafından çağrılan** skill'lerdir (`disable-model-invocation: true`). Sen onları Skill aracıyla çağıramazsın; çağırmış gibi davranma. Kullanıcıya şu adımları ver:

1. **Proje klasöründe bir kez:** `/mattpocock-skills:setup-matt-pocock-skills`. Tracker sorusunda uzak repo yoksa **local markdown** önerilir. Bu skill `CLAUDE.md` / `AGENTS.md` dosyasına `## Agent skills` bloğu ve `docs/agents/` ekler. Bilgi tabanı klasöründe değil, proje klasöründe çalıştırılır. Projede `.scratch/` dosyalarını dışlayan geniş bir `.gitignore` kuralı varsa kullanıcıyı şimdiden uyar (bkz. "Karar kayıtları kalıcı proje belgesidir"); asıl kontrol harita oluştuktan sonra yapılır.
2. **Haritayı başlat:** `/mattpocock-skills:wayfinder` ve aşağıdaki geçiş metnini mesaja ekle. Metni sen hazırla, `docs/spec.md` içindeki açık sorulardan ve kapsam dışı listesinden besle:

```text
Destination: <proje> için docs/spec.md'nin 7 başlığı uygulanabilir düzeyde dolu
(ilk uçtan uca dilimin kapsamı, girdileri, kuralları ve kabul ölçütü tanımlı).

Notes:
- Alan: <kısa alan tanımı>. Dil: Türkçe.
- Spec senkronu: Bir ticket'ın ## Answer bölümü yazılıp Status: resolved yapıldıktan ve
  map.md'nin Decisions so far bölümüne işaretçi eklendikten SONRA, oturumu bitirmeden
  Call the Skill tool with "proje-iskeleti" ve şu bağlamı ver:
  "mod B · map: .scratch/<effort>/map.md · ticket: .scratch/<effort>/issues/<NN-slug>.md · spec: docs/spec.md".
- Harita açılışı: Haritayı ve ilk ticket'ları yazdıktan SONRA, charting oturumunu bitirmeden
  Call the Skill tool with "proje-iskeleti" ve şu bağlamı ver:
  "mod B · açılış · map: .scratch/<effort>/map.md · spec: docs/spec.md".
- proje-iskeleti ticket çözülmeden önce yüklenirse spec'i güncellemez; yukarıdaki çağrı yine yapılır.
- Senkron tamamlanamazsa kararı yeniden açma veya yeniden çözme; eksik senkronu kullanıcıya bildir.
- Bilgi durumları: tercih / doğrulanmış / varsayım / öneri / açık soru ayrı tutulur; kullanıcının kabul ettiği varsayım yine varsayımdır.
- Başlangıç bağlamı: docs/spec.md (taslak), açık sorular 7. başlıkta.
```

3. Sonraki oturumlarda kullanıcı `/mattpocock-skills:wayfinder <map yolu>` ile bir sonraki ticket'ı çözer. Wayfinder oturum başına bir ticket çözer (araştırma ticket'ları hariç).

Not: Wayfinder'ın research ve prototype ticket'ları bulguları atılabilir git dallarına (`research/<ad>`) kaydeder ve dalı push eder. Proje klasörü git deposu değilse veya uzak repo yoksa bunu kullanıcıya önceden söyle.

## Harita durumu

Ticket durumlarını kurulu local-markdown tracker kurallarıyla oku (`setup-matt-pocock-skills` → `issue-tracker-local.md`); kendi durum adı uydurma. Proje başka bir tracker kullanıyorsa (GitHub, GitLab…) durumları ve sahiplenmeyi projenin `docs/agents/issue-tracker.md` dosyasına göre oku; aşağıdaki ayrım aynen geçerlidir.

| Durum | Tracker'daki karşılığı |
| --- | --- |
| açık, sahiplenilmemiş | `Status:` satırı `claimed` veya `resolved` değil |
| sahiplenilmiş | `Status: claimed` (bir oturum üzerinde çalışıyor) |
| kapalı | `Status: resolved` |
| bloklu | `Blocked by:` listesindeki ticket'lardan en az biri `resolved` değil |
| çalışılabilir (frontier) | açık, sahiplenilmemiş ve bloklu değil |

Haritayı şu üç durumdan birine koy:

1. **Tamamlandı:** `resolved` olmayan ticket kalmamış, `## Not yet specified` boş ve Destination karşılanmış. (Kapsam dışı sayılıp kapatılan ticket'lar `## Out of scope` bölümünde durur; tamamlanmayı engellemez.)
2. **Devam ediyor:** En az bir çalışılabilir ticket var. Sıradakini Wayfinder seçer.
3. **Takıldı:** Açık ticket var ama çalışılabilir ticket yok. Harita **tamamlanmamıştır**. Nedeni ayır ve kullanıcıya göster:
   - **Sahiplenilmiş iş:** Ticket'lar `claimed` ya da `claimed` bir ticket'ı bekliyor (`Blocked by:`). Başka bir oturum çalışıyor olabilir. Sahiplenmenin bayat olup olmadığını kullanıcıya sor; `claimed` durumunu kendin geri alma.
   - **Bağımlılık döngüsü:** `Blocked by:` satırları döngü oluşturuyor (ör. 03 → 04 → 03). Döngüyü yazarak göster; ticket'ları düzenlemek Wayfinder oturumunun işidir.
   - **Dış engel:** Ticket var olmayan bir dosyayı ya da dışarıda yapılacak bir işi bekliyor (erişim, veri temini). Gerekirse Wayfinder bir `task` ticket'ı açar.

`Not yet specified` dolu ama hiç açık ticket yoksa da harita tamamlanmamıştır: sisin ticket'a dönüşmesi gerekir (Wayfinder'ın işi).

Harita tamamlanması uygulamaya geçiş demek değildir; C kontrolü ayrıca yapılır.

## B0. Harita açılışı (charting oturumunun sonunda)

Wayfinder haritayı kurarken kullanıcıyla varış noktasını ve kapsamı netleştirir; bu kararlar ticket'a değil `map.md`'ye (Destination, Out of scope) yazılır ve B'nin ön koşullarını karşılamaz. B0 bunları spec'e bir kez işler.

**Ön koşul:** `map.md` var, en az bir ticket dosyası var. Değilse "Harita açılışı bekliyor: <eksik>" de.

**Adımlar:**
1. `map.md`'nin Destination, Out of scope ve Not yet specified bölümlerini oku; spec'in 2. ve 7. başlığıyla karşılaştır.
2. Kullanıcının charting sırasında verdiği kapsam kararlarını 2. başlığa **tercih** olarak yaz; kaynağı `harita açılışı <tarih>` ve `map.md` bağlantısı. `Kapanan kararlar` bölümüne ekleme: orası ticket ve ADR içindir.
3. 7. başlıktaki her açık soruyu karşılığına bağla: ticket'a dönüştüyse `açık → <ticket bağlantısı>`, sise gittiyse `açık → haritada Not yet specified`, kapsam dışı sayıldıysa `kapsam dışı → map.md`. Satırları silme.
4. Spec başlığındaki `Karar haritası:` satırını harita yoluna çevir.
5. Karar kayıtlarının Git tarafından dışlanmadığını kontrol et (bkz. "Karar kayıtları kalıcı proje belgesidir").
6. Görselleştirmeyi üret.
7. Ne değiştiğini kullanıcıya kısaca göster. Haritada olup spec'le çelişen bir şey varsa sessizce düzeltme; farkı göster ve sor.

Wayfinder dosyalarına (map, ticket) yazma; haritayı yeniden kurma.

## B. Spec senkronu (Wayfinder oturumunda)

Wayfinder'ın akışı önceliklidir: yeni soru üretme, ticket'ın kararını değiştirme, ticket ve map dosyalarına yazma.

**Bağlam:** Çağrıda map, ticket ve spec yolu verilmiş olmalı. Verilmediyse map'in `Decisions so far` bölümündeki son işaretçiden ticket'ı bul; birden fazla aday varsa kullanıcıya sor.

**Ön koşul (üçü birden):**
- ticket dosyasında `## Answer` var,
- ticket `Status: resolved`,
- map'in `Decisions so far` bölümünde bu ticket'a işaretçi var.

Biri eksikse spec'i **güncelleme**: "Spec senkronu bekliyor: <ticket> · eksik: <ön koşul>" de ve Wayfinder kendi adımlarını bitirdikten sonra seni yeniden çağırmalı diye hatırlat. Çözülmemiş bir kararı çözülmüş gibi spec'e yazma.

**Adımlar:**

1. Ticket'ın sorusunu ve cevabını oku; hangi spec başlığını etkilediğini bul.
2. **Tekrar kontrolü:** Senkronun yapılıp yapılmadığını yalnız `## Kapanan kararlar` bölümüne bak: bu ticket'a bağlantı veren bir satır var mı? (7. başlıktaki açık soru bağlantıları ve "senkron bekliyor" satırları senkron sayılmaz; onlar ticket'a senkrondan önce de bağlantı verir.)
   - **Satır varsa:** 3–5. adımları atla, yeni özet veya bağlantı ekleme. Yalnız mevcut satırın ve ilgili başlığın cevapla tutarlı olduğunu kontrol et; tutarsızsa farkı kullanıcıya göster ve yerinde düzelt. Sonra 7. adıma geç.
   - **Satır yoksa:** 3. adımdan devam et.
3. İlgili başlığı güncelle; sonucu kısa yaz ve ticket'a bağlantı ver: `([NN · başlık](../.scratch/<effort>/issues/NN-slug.md))`. `## Kapanan kararlar` bölümüne bu ticket için tek satır ekle.
4. Bilgi durumunu etiketle ([bilgi-durumlari.md](references/bilgi-durumlari.md)). Kullanıcının kabul ettiği bir varsayım `varsayım (kullanıcı kabul etti)` olarak kalır; bu varsayımla ilerleme kararı ayrıca `tercih` olarak yazılabilir. Kanıt yoksa `doğrulanmış` yazma.
5. 7. başlıktaki ilgili açık soruyu silme; "çözüldü → ticket bağlantısı" diye işaretle. Bu ticket için "senkron bekliyor" satırı varsa kaldır.
6. Karar spec'te çelişki doğuruyorsa düzeltmeyi kullanıcıya göster; spec'i sessizce yeniden yazma.
7. Harita durumunu ve geçiş kontrolünü tek satırla söyle: "Harita: <tamamlandı | devam ediyor | takıldı (neden)> · Geçiş için kalan: …". İlk senkronda karar kayıtlarının Git tarafından dışlanmadığını da kontrol et.
8. Görselleştirmeyi yeniden üret (`docs/harita.md`, `docs/harita.html`). Tekrar kontrolünde satır bulunduğu için 3–5. adımlar atlansa bile bu adım yapılır: Wayfinder bu arada yeni ticket açmış olabilir.

**Senkron tamamlanamazsa** (spec yok, yazılamıyor, çelişki kullanıcı kararı bekliyor): ticket'a ve map'e dokunma, kararı yeniden açma veya yeniden çözme. Kullanıcıya "Spec senkronu eksik: <ticket> → <neden>" de. Spec yazılabiliyorsa 7. başlığa "senkron bekliyor → <ticket bağlantısı>" satırı ekle; sonraki çağrı bu satırı tamamlayıp kaldırır.

## C. Uygulamaya geçiş

Önce harita durumunu belirle (harita varsa). "Tamamlandı" değilse bu bölüme geçme; durumu ve nedenini raporla.

Geçiş kontrolü:

- Bu dilimin amacı ve kapsamı açık mı?
- Girdiler mevcut mu; eksik veya hatalı girdinin davranışı veri sözleşmesinde tanımlı mı?
- Temel alan kuralları ve varsayımlar yazılı ve etiketli mi? Kabul edilmiş varsayımlar ve geçerlilik koşulları görünür mü?
- Çıktı ve bileşen bağlantıları belli mi?
- Kabul ölçütü ve kontrol yöntemi belirli mi?
- Spec'te "senkron bekliyor" satırı kaldı mı?
- Karar kayıtları sürümleniyor mu (bkz. "Karar kayıtları kalıcı proje belgesidir")?

Geçerse görselleştirmeyi son kez üret, ilk uçtan uca dilimin küçük planını `docs/plan.md`'ye yaz (karar özeti için `docs/harita.md`'ye bağlantı ver) ve uygulamayı temiz yeni oturumda başlatmayı öner. Geçmezse eksikleri listele; harita varsa yeni ticket gerektiğini söyle (ticket'ı Wayfinder açar).

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
