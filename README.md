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

Skill üç modda çalışır:

| Mod | Ne zaman | Ne yapar |
| --- | --- | --- |
| A. Başlangıç | Yeni proje veya özellik | Başlangıç kartı, spec taslağı, harita gerekip gerekmediği kararı |
| B. Spec senkronu | Wayfinder haritasının `Notes` bölümü skill'i çağırdığında | Çözülen ticket'ı ilgili spec başlığına işler, ticket'a bağlantı verir, bilgi durumunu etiketler |
| C. Uygulamaya geçiş | Harita bittiğinde veya hiç gerekmediğinde | Geçiş kontrolü ve `docs/plan.md` |

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
   Destination: <proje> için docs/spec.md'nin 7 başlığı uygulanabilir düzeyde dolu ve
   uygulamaya geçiş kontrolünü geçiyor (ilk uçtan uca dilim tanımlı).

   Notes:
   - Her oturumda: Call the Skill tool with "proje-iskeleti" (spec senkronu, mod B).
   - Kalıcı tercih: Ticket çözülüp ## Answer yazıldıktan ve map'e işaretçi eklendikten sonra,
     oturumu bitirmeden proje-iskeleti'nin "B. Spec senkronu" adımlarını uygula.
   ```

4. **Kararları tek tek çöz.** Her yeni oturumda:
   ```text
   /mattpocock-skills:wayfinder .scratch/<effort>/map.md
   ```

5. **Harita bitince:** "uygulamaya geçiş" de. Skill kontrolü yapar ve `docs/plan.md` dosyasını yazar.

Komut adları plugin'in ad alanıyla yazılmıştır (`mattpocock-skills:`). Komut menüsünde kısa adlarıyla da görünebilirler.

## Dosya yapısı

```text
skills/proje-iskeleti/
  SKILL.md                      skill talimatı (modlar, geçiş akışı, kurallar)
  references/
    spec-sablonu.md             başlangıç kartı, 7 başlıklı spec ve veri sözleşmesi şablonu
    bilgi-durumlari.md          beş bilgi durumu
    muhendislik-eki.md          proses ve mühendislik projeleri için ek kontroller
```

Skill'in proje klasöründe oluşturduğu ya da kullandığı dosyalar:

| Dosya | Sahibi |
| --- | --- |
| `docs/spec.md`, `docs/plan.md`, gerekirse `docs/data-contracts.md` | proje-iskeleti |
| `.scratch/<effort>/map.md`, `.scratch/<effort>/issues/NN-*.md` | wayfinder |
| `GLOSSARY.md`, `docs/adr/` | domain-modeling |
| `docs/agents/*.md`, `CLAUDE.md`/`AGENTS.md` içindeki `## Agent skills` bloğu | setup-matt-pocock-skills |

## Doğrulama durumu

**Yapılan kontroller:**
- `mattpocock-skills` 1.3.1 resmî kanaldan kuruldu. `claude plugin list` ve `claude plugin details` çıktıları doğrulandı.
- Kurulu skill dosyaları paketin GitHub'daki ana dalıyla karşılaştırıldı. Fark birkaç cümleden ibaret, local-markdown tracker kuralları birebir aynı.
- `wayfinder` ve `setup-matt-pocock-skills` skill'lerinin kullanıcı tarafından çağrıldığı frontmatter'dan doğrulandı.
- Örnek bir projede dosya tutarlılığı kontrolü yapıldı. Wayfinder'ın local-markdown kurallarına göre harita, ticket, `Blocked by` ve `## Answer` dosyaları **elle** yazıldı. Bir betik şunları kontrol etti:
  - frontier'ın doğru hesaplanması
  - harita işaretçisinin var olması
  - spec'teki ticket bağlantılarının çalışması

**Henüz yapılmayan:**
- Gerçek bir uçtan uca Wayfinder oturumu tamamlanmadı. Yani `/mattpocock-skills:wayfinder` ile harita kurup bir kararı kapatmak denenmedi.
- **Otomatik spec senkronu doğrulanmadı.** Wayfinder'ın `Notes` üzerinden `proje-iskeleti`'yi gerçekten çağırıp `docs/spec.md`'yi güncellediği henüz gözlenmedi. Bu bir tasarım hedefi, doğrulanmış bir özellik değil.
- Skill gerçek bir projede kullanılmadı.
- Sadece Claude Code için yazıldı. Codex ve diğer ajanlarda denenmedi.

## Kaynaklar

- Matt Pocock, *Skills For Real Engineers*: <https://github.com/mattpocock/skills>
- Orijinal Wayfinder: <https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md>
- Skill çağırma kuralları: <https://github.com/mattpocock/skills/blob/main/.agents/invocation.md>

## Lisans

[MIT](LICENSE). Bağımlılık olan `mattpocock/skills` paketi kendi MIT lisansıyla dağıtılır ve bu repoya dahil değildir.
