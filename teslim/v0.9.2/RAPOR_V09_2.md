# MATCHDAY 99 v0.9.2 — kulüp formaları

20 Premier League kulübünün iç saha ve deplasman formaları, kullanıcının seçtiği geleneksel kulüp renkleriyle güncellendi. Forma simgeleri de aynı renkleri gösteriyor. Kırmızı-mavi Palace, siyah-beyaz Newcastle, amber-siyah Hull, kırmızı-beyaz Brentford/Sunderland, kırmızı-siyah Bournemouth ve mavi-beyaz Brighton için çizgili dokular; Arsenal ve Aston Villa için farklı gövde/kol renkleri kullanıldı. Açık renkli formalarda koyu, koyu formalarda açık numara renkleri seçildi. Numara değerleri değişmedi.

## Teknik değişiklik

- Temel sürüm doğrulanmış v0.9.1'dir. Bu sürüme göre yalnızca 20 hedef `BIN/TEX_nn.BIN` forma dosyası ve `SELECT.BIN` içindeki 40 menü forma paleti değişti. 224 ISO dosyası birebir aynı; v0.9.1 bayrak grafikleri, paletleri, yükleme/VRAM düzeltmesi ve program kodu aynı.
- Her TEX dosyasında iki 128×128, 8 bpp doku bulunur. Yalnızca forma/şort/çorap/kol UV alanı olan `x=0..63,y=0..79` güncellendi. Bu alanın dışındaki numara glifleri, ten/yüz pikselleri ve diğer piksel verileri korundu.
- Forma paletleri 256 RGB555 renkten oluşur. Yalnızca forma bileşenlerine ve numara rengine ait 16 tonlu gruplar `1,2,3,4,5,6,15` değişti. Ayrı ten/ayakkabı/kaleci ve diğer varlık paletleri değişmedi. Gölgeler için koyulaşan renk rampaları kullanıldı.
- Yerleşik uyumlu forma şablonlarından gerekli giysi alanları alınarak geleneksel desenler oluşturuldu. Dokular Konami formatıyla yeniden sıkıştırıldı; iki doku akışının değişen uzunlukları için başlık ve tanımlayıcı RAM işaretçileri taşındı. Diğer varlıkların açılmış içerikleri, tanımlayıcı boyutları ve VRAM koordinatları aynı kaldı. Dosya boyutları ve ISO sektör yerleşimleri korunuyor.
- Menü forma simgesi, oyunun mevcut ortak şablonunu ve 16 renkli paletlerini kullanır. Çizgili takımların küçük simgesi iki kulüp rengini mevcut panel deseniyle gösterir; maç içindeki formalar çizgilidir.
- Yeni VRAM atlası veya çalışma zamanı kodu eklenmedi. Oyunun mevcut forma yükleme yolu kullanılır.

## Korunan oyuncu verileri

Oyuncu isimleri, kadrolar, mevkiler, forma numarası değerleri, özellikler ve puanlar aynı kaldı. SELECT'teki değişiklikler yalnızca `0x370c4 + 64*team_slot + 32*kit` adresindeki 32 baytlık menü paletleriyle sınırlı. Program kodu, takım/oyuncu kayıtları ve tüm diğer ISO dosyaları v0.9.1 ile karşılaştırıldı. v0.9.1'in v0.8'i koruduğuna ilişkin önceki kontroller de geçerlidir.

## Testler

PCSX-ReARMed libretro `c881679`, HLE BIOS ve yazılımsal GPU kullanıldı. ePSXe bu ortamda mevcut değildi; test iddiası PCSX-ReARMed içindir.

- 20 kulübün her biri aynı kulüple eşleştirilerek hem iç saha hem deplasman forması maça yüklendi. Toplam 40 forma için ayar menüsü, iki takımın fotoğrafları ve maçın başlaması yakalandı.
- Gerçek emülatör VRAM'inde forma pikselleri ve 256 renkli maç paletleri beklenen dokularla eşleşti. Oyunun maç sırasında yerleştirdiği şort numarası için kullanılan 8×8 piksel bölgesi doku karşılaştırmasından ayrı tutuldu; kaynak numara gliflerinin aynen kaldığı dosya düzeyinde kontrol edildi. Beyaz Spurs ve lacivert deplasman formalarının sırt numaraları görüntüde okunuyor.
- Menüde iki takımın forma paletleri beklenen 16 RGB555 renk ile birebir eşleşti.
- Her kulüp için aynı takımlar/girişler kullanılarak bağımsız v0.9.1 referans maçı çalıştırıldı. Yüz/saç atlası `x=512..575,y=256..511` her eşleşmede referansla birebir aynı. Farklı takımların yüz atlasları birbirinden farklı olduğundan karşılaştırma aynı takımlar arasında yapıldı.
- Yüz, ten, ayakkabı, kaleci, numara ve diğer TEX varlıklarının giysi dışı açılmış verileri korundu. Başlıklardaki taşınan işaretçiler yeniden çözülerek bütün liste ve varlıklara ulaşılabildiği doğrulandı.
- Değişen 222 sektörün EDC/ECC değerleri yeniden üretildi ve doğrulandı. Senkron, sektör ve XA başlıkları aynı; diğer sektörler aynı. 11 ses izi kopyalanır ve SHA-256 ile doğrulanır.
- Python uygulayıcısı kaynağa yazmaz; v0.9.1, v0.8 veya eski v0.9'dan aynı hedef çıktıyı üretir. Tam BIN/CUE yeni bir klasöre yazılır. Çıktı ve kopyalanan sesler doğrulanmadan başarı mesajı verilmez.

Bu testler tüm kulüp formalarını kapsar; tüm oyun modları, hava/stadyum seçenekleri veya uzun sezonlar test edilmedi. Makine sonuçları `binary-validation.json` ve `emulator-validation.json` içindedir. Forma renkleri `FORMA_RENKLERI.json` dosyasında listelenmiştir. Kaleci kit verileri mevcut oyundan korunur.

Hedef Track 01 SHA-256: `2b6a0fa935d82a63df9f8ea7ec5f1b71fd70f2bb71ebe46ee995b054cfe8b34d`.

## Kurulum

`BASLA.txt` adımlarını uygulayın. Yeni `ISS Pro Evolution - MATCHDAY99_v09_2.cue` dosyasından baştan açın. Önceki sürümün save state'i eski forma paletlerini ve dokularını yükleyebileceğinden kullanılmamalıdır. Normal hafıza kartı dosyaları değiştirilmez.

Python uygulayıcısı standart kütüphaneyle çalışır. Ayrı BPS yamaları Flips gibi bir BPS aracıyla da uygulanabilir; bu durumda uygun kaynak sürümün yaması seçilmeli, yeni CUE ile 11 orijinal ses BIN'i aynı çıktı klasörüne konmalıdır.
