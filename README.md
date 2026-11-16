# proje-iskeleti

Orijinal Wayfinder ile birlikte çalışan, fikirleri uygulanabilir proje spec'lerine dönüştüren bir Claude Code skill'i.

Koda başlamadan önce, ajanın koddan hiçbir zaman çıkaramayacağı bilgiyi yazıya döker: hedef, kapsam, alan kuralları ve varsayımlar, veri sözleşmeleri, kabul kriterleri. Spec'i ajan tek başına yazmaz. Kullanıcıyla birlikte yazılır, ajan sorgulayan taraftır.

> **Durum: deneme sürümü.** Ayrıntılar aşağıdaki [Doğrulama durumu](#doğrulama-durumu) bölümünde.

## Ne yapar

- Projenin hedefini ve kapsamını netleştirir (başlangıç kartı).
- 7 başlıklı bir spec yazar (`docs/spec.md`):
  1. Problem ve hedef
  2. Kapsam
  3. Girdi, çıktı ve veri sözleşmeleri
  4. Alan kuralları, modeller ve varsayımlar
  5. Bileşenler ve akış
  6. Kabul kriterleri ve doğrulama
  7. Açık sorular ve riskler
- Bilgiyi beş duruma ayırır: **tercih**, **doğrulanmış**, **varsayım**, **öneri**, **açık soru**.
- Uygulamaya geçiş kontrolünü yapar ve ilk uçtan uca dilimin planını yazar (`docs/plan.md`).
- Mühendislik ve proses yazılımı için ek kontroller içerir:
  - öğrenme ihtiyacı
  - dış kısıtlar (standart, yönetmelik)
  - birim politikası
  - el hesabıyla doğrulama
  - hassasiyet analizi
  - donanım/sensör arayüzü
- Birden çok oturum gerektiren karar işlerini **kendisi yürütmez**. Bu iş için kullanıcıyı Matt Pocock'un orijinal `wayfinder` skill'ine yönlendirir. Wayfinder oturumlarında kapanan kararları spec'e işlemek üzere tasarlanmıştır (spec senkronu).
- Haritayı ve spec'i görselleştirir: `docs/harita.md` (Mermaid karar şeması) ve `docs/harita.html` (etkileşimli bağ grafiği). Bkz. [Görselleştirme](#görselleştirme).

Skill üç modda çalışır (B'nin harita açılışı için ayrı bir adımı vardır):

| Mod | Ne zaman | Ne yapar |
| --- | --- | --- |
| A. Başlangıç | Yeni proje veya özellik | Başlangıç kartı, spec taslağı, harita gerekip gerekmediği kararı |
| B0. Harita açılışı | Wayfinder haritayı kurduktan sonra, `Notes` talimatıyla | Harita kurulurken verilen kapsam kararlarını spec'e **tercih** olarak işler, 7. başlıktaki açık soruları ticket'a, sise ya da kapsam dışına bağlar, görselleştirmeyi üretir |
| B. Spec senkronu | Wayfinder bir ticket'ı kapattıktan sonra, `Notes` talimatıyla skill açıkça çağrıldığında | Ön koşulları kontrol eder (`## Answer`, `Status: resolved`, harita işaretçisi), çözülen kararı ilgili spec başlığına bir kez işler, ticket'a bağlantı verir, bilgi durumunu etiketler; tamamlanamazsa eksik senkronu bildirir |
| C. Uygulamaya geçiş | Harita **tamamlandığında** veya hiç gerekmediğinde | Geçiş kontrolü ve `docs/plan.md` |

Harita durumu üçe ayrılır:
- **Tamamlandı:** Açık ticket yok, `Not yet specified` boş, hedef karşılanmış.
- **Devam ediyor:** Çalışılabilir ticket var.
- **Takıldı:** Açık ticket var ama çalışılabilir yok. Nedeni sahiplenilmiş iş, bağımlılık döngüsü ya da dış engel olabilir.

Harita tamamlanması uygulamaya geçiş demek değildir; geçiş kontrolü ayrıca yapılır.

## Bağımlılık: Matt Pocock'un skills paketi

Karar haritasını bu repo değil, **ayrı ve bağımsız** bir paket yürütür: [mattpocock/skills](https://github.com/mattpocock/skills) (MIT lisanslı, telif hakkı Matt Pocock'a ait). Bu repoda o paketin hiçbir dosyası yoktur. Paket kendi resmî kanalından kurulur:

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

Kullanılan orijinal skill'ler:
- `wayfinder`
- `setup-matt-pocock-skills`
- `grilling`
- `domain-modeling`
- local-markdown issue tracker kuralları

`proje-iskeleti` bu paketin 1.3.1 sürümüne göre yazıldı.

`wayfinder` ve `setup-matt-pocock-skills` **kullanıcı tarafından çağrılan** skill'lerdir. Paketin kendi frontmatter'ında `disable-model-invocation: true` tanımlıdır, ayrıntısı paketin `.agents/invocation.md` belgesinde. Bu yüzden başka bir skill onları çağıramaz ve `proje-iskeleti` de çağırmaz. Kullanıcıya yazacağı komutu ve yapıştıracağı geçiş metnini hazırlar. Ters yönde ise Wayfinder, haritanın `## Notes` bölümünde adı geçen skill'leri çağırır. `proje-iskeleti` bu yolla devreye girmek üzere tasarlandı.

## Kurulum

1. Bağımlılığı kur (yukarıdaki komut).
2. Bu repodaki `skills/proje-iskeleti` klasörünü Claude Code'un skill klasörüne kopyala:
   - Bütün projelerde kullanmak için kişisel skill klasörü: `~/.claude/skills/proje-iskeleti/`
   - Sadece tek bir projede kullanmak için: `<proje>/.claude/skills/proje-iskeleti/`

```bash
git clone https://github.com/HalukCanturk/proje-iskeleti.git
cp -r proje-iskeleti/skills/proje-iskeleti ~/.claude/skills/
```

3. Yeni bir Claude Code oturumu aç. Skill listesinde `proje-iskeleti` görünmeli.

## Örnek kullanım

Boş bir proje klasöründe (`git init` önerilir):

1. **Spec taslağı:**
   ```text
   proje iskeleti: Sayaç CSV dosyalarından günlük enerji tüketim raporu üreten küçük bir araç.
   ```
   Skill başlangıç kartını doldurur, sana sorular sorar ve `docs/spec.md` taslağını yazar. Bir karar haritası gerekiyorsa Wayfinder için geçiş metnini hazırlar.

2. **Proje başına bir kez kurulum** (tracker sorusunda uzak repo yoksa *local markdown* seç):
   ```text
   /mattpocock-skills:setup-matt-pocock-skills
   ```

3. **Haritayı kur.** Komutu yaz ve 1. adımda hazırlanan geçiş metnini aynı mesaja yapıştır:
   ```text
   /mattpocock-skills:wayfinder
   ```
   Geçiş metni şuna benzer:
   ```text
   Destination: <proje> için docs/spec.md'nin 7 başlığı uygulanabilir düzeyde dolu
   (ilk uçtan uca dilimin kapsamı, girdileri, kuralları ve kabul ölçütü tanımlı).

   Notes:
   - Spec senkronu: Bir ticket'ın ## Answer bölümü yazılıp Status: resolved yapıldıktan ve
     map.md'nin Decisions so far bölümüne işaretçi eklendikten SONRA, oturumu bitirmeden
     Call the Skill tool with "proje-iskeleti" ve şu bağlamı ver:
     "mod B · map: .scratch/<effort>/map.md · ticket: .scratch/<effort>/issues/<NN-slug>.md · spec: docs/spec.md".
   - proje-iskeleti ticket çözülmeden önce yüklenirse spec'i güncellemez; yukarıdaki çağrı yine yapılır.
   - Harita açılışı: Haritayı ve ilk ticket'ları yazdıktan SONRA, charting oturumunu bitirmeden
     Call the Skill tool with "proje-iskeleti" ve şu bağlamı ver:
     "mod B · açılış · map: .scratch/<effort>/map.md · spec: docs/spec.md".
   - Senkron tamamlanamazsa kararı yeniden açma veya yeniden çözme; eksik senkronu kullanıcıya bildir.
   ```
   Tam metin `SKILL.md` içindeki "Wayfinder'a geçiş" bölümündedir.

4. **Kararları tek tek çöz.** Her yeni oturumda:
   ```text
   /mattpocock-skills:wayfinder .scratch/<effort>/map.md
   ```

5. **Harita tamamlanınca:** "uygulamaya geçiş" de. Skill önce harita durumunu, sonra geçiş kontrolünü yapar ve `docs/plan.md` dosyasını yazar.

Komut adları plugin'in ad alanıyla yazılmıştır (`mattpocock-skills:`). Komut menüsünde kısa adlarıyla da görünebilirler.

## Dosya yapısı

```text
skills/proje-iskeleti/
  SKILL.md                      skill talimatı (modlar, geçiş akışı, kurallar)
  references/
    spec-sablonu.md             başlangıç kartı, 7 başlıklı spec ve veri sözleşmesi şablonu
    bilgi-durumlari.md          beş bilgi durumu
    muhendislik-eki.md          proses ve mühendislik projeleri için ek kontroller
  scripts/
    harita_ciz.py               docs/harita.md ve docs/harita.html üretir (yalnız okur)
    harita_sablon.html          etkileşimli grafiğin şablonu
```

Skill'in proje klasöründe oluşturduğu ya da kullandığı dosyalar:

| Dosya | Sahibi |
| --- | --- |
| `docs/spec.md`, `docs/plan.md`, gerekirse `docs/data-contracts.md` | proje-iskeleti |
| `docs/harita.md`, `docs/harita.html` (üretilir, elle düzenlenmez) | proje-iskeleti (`harita_ciz.py`) |
| `.scratch/<effort>/map.md`, `.scratch/<effort>/issues/NN-*.md` | wayfinder |
| `GLOSSARY.md`, `docs/adr/` | domain-modeling |
| `docs/agents/*.md`, `CLAUDE.md`/`AGENTS.md` içindeki `## Agent skills` bloğu | setup-matt-pocock-skills |

## Görselleştirme

`scripts/harita_ciz.py` proje kökünde çalışır ve iki dosya üretir:

- **`docs/harita.md`:** Mermaid karar şeması. Ticket'lar kutu, `Blocked by` satırları ok, renk durumu gösterir (kapalı, çalışılabilir, sahiplenilmiş, bloklu); sis ve kapsam dışı ayrı gruplarda; altında ticket tablosu. Obsidian, GitHub ve VS Code önizlemesi çizer.
- **`docs/harita.html`:** Obsidian'ın grafik görünümüne benzer etkileşimli bağ grafiği (d3). Düğümler spec ve başlıkları, ticket'lar, sis ve kapsam dışı maddeler. Üzerine gelince bağlar öne çıkar, tıklayınca dosya açılır. Tarayıcıda açılır; d3 cdnjs'ten yüklenir.

```bash
python ~/.claude/skills/proje-iskeleti/scripts/harita_ciz.py
```

Betik yalnız okur: ticket başlık satırları (`Type`, `Status`, `Blocked by`), `map.md` bölümleri ve `docs/spec.md`. Ticket gövdesi okunmaz. Bağlar yalnız dosyalarda yazılı olandan çizilir. Skill betiği A, B0, B ve C modlarında kendisi çalıştırır.

## Karar kayıtları ve Git

Local-markdown tracker kullanılan bir projede `.scratch/<effort>/map.md` ve `.scratch/<effort>/issues/*.md` **kalıcı proje belgeleridir**. `docs/spec.md` bu dosyalara bağlantı verir. Git dışında kalırlarsa bağlantılar başka bir bilgisayarda çalışmaz. Tracker'ın yolları orijinal paketin kuralıdır, değiştirilmez.

- **Kopyalama uyarısı:** Bu reponun `.gitignore` dosyası sadece skill dağıtımı içindir. Kendi projene kopyalama, çünkü `.scratch/` satırı karar kayıtlarını dışlar.
- **Kontrol:** Projende şu komutu çalıştır:
  ```bash
  git check-ignore .scratch/<effort>/map.md .scratch/<effort>/issues/01-<slug>.md
  ```
  Yazdırılan her yol dışlanıyor demektir. Hiçbir şey yazdırmazsa dosyalar sürümlenebilir. `-v` ile hangi kuralın etkili olduğu görülebilir, ama dikkat: `-v`, `!` ile başlayan geri alma kurallarını da yazdırır. `!` ile başlayan bir kural dosyanın dışlanmadığını gösterir.
- **Düzeltme:** Dışlanıyorlarsa `.scratch/` klasörünü tümden dışlayan kuralı şu dar kurallarla değiştir:
  ```gitignore
  .scratch/*
  !.scratch/<effort>/
  .scratch/<effort>/*
  !.scratch/<effort>/map.md
  !.scratch/<effort>/issues/
  ```
  Git, dışlanmış bir klasörün içindeki dosyayı geri alamaz. Bu yüzden önce klasörü değil içeriğini dışlamak gerekir.
- **Toplu sürümleme yapma:** `.scratch/` altındaki her şeyi sürümleme. Kalıcı olanlar harita ve ticket dosyaları. Geçici çıktılar dışlanmış kalır. Wayfinder'ın research/prototype bulguları zaten ayrı git dallarında durur.

## Doğrulama durumu

**Yapılan kontroller:**
- `mattpocock-skills` 1.3.1 resmî kanaldan kuruldu. `claude plugin list` ve `claude plugin details` çıktıları doğrulandı.
- Kurulu skill dosyaları paketin GitHub'daki ana dalıyla karşılaştırıldı. Fark birkaç cümleden ibaret, local-markdown tracker kuralları birebir aynı.
- `wayfinder` ve `setup-matt-pocock-skills` skill'lerinin kullanıcı tarafından çağrıldığı frontmatter'dan doğrulandı.
- Örnek bir projede dosya tutarlılığı kontrolü yapıldı. Wayfinder'ın local-markdown kurallarına göre harita, ticket, `Blocked by` ve `## Answer` dosyaları **elle** yazıldı. Bir betik şunları kontrol etti:
  - frontier'ın doğru hesaplanması
  - harita işaretçisinin var olması
  - spec'teki ticket bağlantılarının çalışması
- "Karar kayıtları ve Git" bölümündeki `.gitignore` kuralları gerçek `git` ile ayrı bir deneme deposunda sınandı. Eski `.scratch/` kuralı harita ve ticket dosyalarını dışlıyordu. Önerilen kurallarla yalnız `map.md` ve `issues/` takip edildi, geçici dosyalar ve başka klasörler dışlandı. `git check-ignore -v` komutunun `!` kuralını da yazdırdığı bu testte görüldü ve talimat buna göre yazıldı.

- **Uçtan uca deneme (2026-11-16, küçük bir deneme deposu):** mod A spec taslağı; `setup-matt-pocock-skills` (local markdown); `/mattpocock-skills:wayfinder` ile harita, 5 ticket ve `Blocked by` bağları; bir **research** ticket'ının alt ajanla çözülüp kapanması; ardından `Notes` talimatıyla `proje-iskeleti`'nin mod B için çağrılması, üç ön koşulun kontrolü ve `docs/spec.md` senkronu gözlendi.
- Aynı denemede bir boşluk bulundu: harita kurulurken verilen kapsam kararları yalnız `map.md`'ye yazılıyor, mod B bunları işlemiyordu. B0 (harita açılışı) bu yüzden eklendi.
- `harita_ciz.py` deneme deposunda haritalı ve haritasız durumda çalıştırıldı; `docs/harita.html` tarayıcıda çizildi.

**Henüz yapılmayan:**
- **Grilling** ticket'ında kullanıcı kararının spec'e senkronu gözlenmedi; gözlenen tek senkron research ticket'ındaydı.
- B0 (harita açılışı) yalnız talimat olarak yazıldı; gerçek bir charting oturumunda denenmedi. Eklenmeden önceki denemede aynı hizalama elle yapıldı.
- Tekrar çağrıda kopya oluşturmama, eksik senkron bildirimi, "takıldı" harita durumunun ayrımı ve mod C gerçek bir oturumda gözlenmedi.
- Skill gerçek bir projede kullanılmadı.
- Sadece Claude Code için yazıldı. Codex ve diğer ajanlarda denenmedi.

## Kaynaklar

- Matt Pocock, *Skills For Real Engineers*: <https://github.com/mattpocock/skills>
- Orijinal Wayfinder: <https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md>
- Skill çağırma kuralları: <https://github.com/mattpocock/skills/blob/main/.agents/invocation.md>

## Lisans

[MIT](LICENSE). Bağımlılık olan `mattpocock/skills` paketi kendi MIT lisansıyla dağıtılır ve bu repoya dahil değildir.
