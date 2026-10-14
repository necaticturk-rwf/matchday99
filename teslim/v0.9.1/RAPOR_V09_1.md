# MATCHDAY 99 v0.9.1

Önceki v0.9 yaması hatalıydı: yeni bayrak atlası VRAM'de `x=512..575` bölgesine yazılarak oyunun kalıcı yüz, saç, vücut ve arayüz dokularını eziyordu. Takım seçimi ve kısa maç testi bu hatayı yakalamadı; önceki v0.9 raporunun oynanabilirlik sonucu geçersizdir. Hata emülatörde yeniden üretildi ve aşağıdaki düzeltme doğrulandı.

## Düzeltme

- Küçük kulüp bayrakları, 368 piksel genişliğindeki menünün görünür `x=8..375` alanının dışındaki `x=376..383` şeridine taşındı. Orijinal 384 piksel ekran modu ve projeksiyon merkezi korundu. Menü çizim sınırı ve framebuffer temizleme işlemleri bu şeridi koruyor; 512 piksel maç ekranı aynı kalıyor.
- Büyük 64×28 bayraklar, maç ayarları onaylandıktan hemen sonra geçici olarak hazırlanıyor; iki seçili takımın bayrakları oyunun mevcut `x=560, y=0/28` tamponlarına, 24×8 skorbord bayrakları da mevcut `x=688/694, y=198` tamponlarına kopyalanıyor. Stadyum önizleme alanı seçim ve ayar ekranlarında korunuyor; iki bayrak kopyasından sonra orijinal önizleme dokuları yeniden yükleniyor.
- DATSEL/DATSEL2 özgün dokuları kayıpsız yeniden sıkıştırıldı. İlk 50 DATSEL ve 12 DATSEL2 bloğu açıldığında özgünleriyle birebir aynı. Dosya boyutları, ISO yerleşimleri ve CD okuma sayıları değişmedi. TIM olmayan Konami sıkıştırması oyunun kendi çözme/yükleme rutinleriyle kullanılmaya devam ediyor.
- Hedef 20 takımın 16 renkli CLUT'ları RGB555 olarak güncellendi; siyah renk şeffaflaşmıyor. 22×16 seçim, 24×8 skorbord ve 64×28 büyük bayraklar kaynak PNG'lerden en yakın komşu örneklemesiyle hazırlanıyor. Dar ayar simgesi 22×16 bayrağın ortasından 16×16 kırpılarak aynı atlası kullanıyor.

## Doğrulama

PCSX-ReARMed libretro `c881679`, HLE BIOS ve yazılımsal GPU kullanıldı. ePSXe bu ortamda mevcut değildi; ePSXe uyumluluğu yerel olarak ayrıca gözlenmelidir.

- 20 kulübün tamamı takım seçim ekranında açıldı. Üretilen GPU komutlarının doku sayfası, UV koordinatları ve CLUT'ları doğrulandı; gerçek VRAM pikselleri kaynak grafiklerle eşleşti.
- 20 kulübün her biri için iki seçili takımın 64×28 büyük bayrak ve 24×8 skorbord kopyaları gerçek emülatör VRAM'inde doğrulandı.
- Bütün bu seçim durumlarında özgün DAT2D yüz/vücut/arayüz bölgeleri ve sekiz stadyum önizleme bloğu yerinde kaldı. Özgün üst üste yazılan doku kayıtları son yükleme sırasına göre değerlendirildi.
- Crystal Palace–Tottenham maçında bayrak seremonisi, iki takımın fotoğrafları ve maçın başlaması görüntülendi. Aynı girişlerle v0.8 karşılaştırması yapıldı: yüz/saç/vücut bölgesi `x=512..575,y=256..511`, forma bölgesi `x=640..703,y=384..511` ve bayrak dışındaki tüm palet sözcükleri birebir aynı.
- Eski v0.9'a aynı doku kontrolü uygulandığında 12.357 VRAM sözcüğü farklı çıktı; düzeltmede bu bölgede fark sıfır. Bu kontrol bildirilen hatayı yakalayabiliyor.
- Oyuncu adları, özellikler, pozisyonlar, forma numaraları ve kadroları içeren dosyalar değişmedi. v0.8'in önceki Track 01 sürümünden farklı olan 4.900 baytının tamamı aynen korundu. 240 ISO dosyası bayt düzeyinde aynı; grafik dosyaları içindeki özgün dokular da yukarıdaki gibi korundu.
- Yalnızca `/BIN/DATSEL.BIN`, `/BIN/DATSEL2.BIN`, `/BIN/DAT2D.BIN`, `/SELECT.BIN` ve `/SLUS_010.14` içindeki gerekli grafik/yükleme kodu değişti. SELECT ve SLUS kod değişiklikleri açık konum listesiyle sınırlandı; DAT2D değişiklikleri yalnızca 20 hedef bayrak paletiyle sınırlı.
- Değişen 173 CD sektörünün EDC/ECC değerleri yeniden üretildi ve doğrulandı; sektör başlıkları/XA alt başlıkları aynı. Diğer sektörler aynı. 11 ses izi kopyalanıyor ve SHA-256 ile doğrulanıyor.
- Teslim edilen Python uygulayıcısıyla v0.8 ve bozuk v0.9'dan iki ayrı çıktı oluşturuldu; ikisi de aynı hedef SHA-256'ya ulaştı. Bozuk yama CRC'si ve dolu çıktı klasörü reddedildi. Kaynaklara yazılmıyor.

## Kullanım

ZIP'i çıkarın ve `BASLA.txt` adımlarını uygulayın. `apply_v09_1.py` Python 3 standart kütüphanesi ile çalışır ve kaynak sürümü SHA-256 ile tanır. Ayrı BPS dosyaları Flips gibi bir BPS uygulayıcısıyla da kullanılabilir; ardından yeni CUE ve özgün 11 ses izi aynı klasöre konmalıdır.

Yeni `ISS Pro Evolution - MATCHDAY99_v09_1.cue` dosyasından oyunu baştan açın. Eski save state'ler eski sürümün bozuk RAM/VRAM'ini içerdiğinden yüklenmemelidir. Normal hafıza kartı dosyaları değiştirilmiyor.

Doğrulama belirli menü akışı ve Crystal Palace–Tottenham maçını kapsar; tüm oyun modlarının, bütün stadyum/hava seçeneklerinin veya uzun süreli maçların eksiksiz testi yapıldığı anlamına gelmez. Makine tarafından okunabilir sonuçlar `validation.json` içinde, girdi/çıktı/yama SHA-256'ları `manifest.json` içindedir.

Hedef Track 01 SHA-256: `ba8c9560305e466c76e11e5a23d480afbd06db1001eee5170dd03e0a4cd74d8a`.
