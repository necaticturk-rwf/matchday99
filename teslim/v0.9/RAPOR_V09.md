> **GEÇERSİZ / ESKİ RAPOR:** v0.9 oyuncu dokularını bozuyordu. [v0.9.1 düzeltme raporunu okuyun](../v0.9.1/RAPOR_V09_1.md).

# MATCHDAY 99 v0.9 — Kulüp bayrakları güncellemesi

Release v1.0.0 içindeki v0.8 dosyasından üretildi. Oyun: ISS Pro Evolution (USA), SLUS-01014.

## Kullanım

BIN/CUE ZIP'ini tamamen çıkarın; emülatörde `ISS Pro Evolution - MATCHDAY99_v09.cue` dosyasını açın. 12 BIN izini aynı klasörde tutun. CUE olmadan Track 01'i açmak ses izlerini dışarıda bırakabilir. Yeni sürümü normal açılışla başlatın: v0.8 kayıt durumları eski grafik/kod belleğini geri getirebilir. Özgün v0.8 dosyalarını yedek olarak tutun.

Küçük yama paketi: v0.8 RAR'ını tamamen çıkardıktan sonra Python 3 ile:

```text
python apply_v09.py "v08_dosya_klasoru" "yeni_v09_klasoru"
```

Betik tüm kaynak dosyaları doğrular, 11 ses izini değişmeden kopyalar ve yeni BIN/CUE'yi ayrı klasöre yazar. Dolu hedef klasörünü ve yanlış v0.8 dosyasını reddeder. Pillow, NumPy veya bir PS1 BIOS dosyası yama için gerekmez. BPS dosyası ayrıca standart BPS uygulayıcılarıyla Track 01'e uygulanabilir; bu durumda yeni CUE ve ses izlerini kendiniz aynı klasöre yerleştirin.

## Teknik değişiklik

- Kulüp ZIP'i bütünlük kontrolünden geçti. Paketin 20 takım yuvası eşleştirmesi, mevcut kulüp isimleri ve emülatör seçimleri ile kontrol edildi. Yuva numaraları sıfırdan başlar; liste TEAM_FLAG_SLOTS.csv'dedir.
- Bu akıştaki bayraklar bağımsız TIM dosyaları değildir. DATSEL.BIN özel Konami LZ sıkıştırması ve VRAM aktarım kayıtları içerir. Açıcı oyun yürütülebilir dosyasında 0x8001c680 adresinde çözümlendi; yeniden sıkıştırılan bloklar özgün açıcı ile bayt düzeyinde kontrol edildi.
- Ortak ülke dokuları, takım başına CLUT kullanarak farklı ülkelerde tekrar kullanılır. Başka takımları bozmamak için 20 yeni doku kimliği (64–83) ayrıldı; özgün 50 DATSEL doku bloğu açılmış biçimde aynen korundu.
- Kaynak PNG'ler 64×40 ve 16 renklidir. Test edilen oyunda 22×16 seçim, 24×8 skor, 16×20 dikey küçük simge ve 64×28 büyük bayrak biçimleri kullanılır. Bu dört biçim mevcut piksel indeksleriyle en yakın komşu örnekleme ile üretildi.
- PS1 paletleri RGB555, 16 giriş/32 bayttır. Opak siyah 0x8000 olarak kodlandı; kaynak PNG'lerde saydamlık yoktur. 24 bit kaynak renkleri PS1'in 5 bit kanallarına çevrildiği için bazı çok yakın renkler birleşir.
- Yeni menü dokuları VRAM (512,256) sayfasında; büyük bayraklar (512,0) bölgesindedir. Bunlar menü yüklemesinde geçici olarak yüklenir; maç kendi gerekli grafiklerini yeniden yükler.
- DAT2D.BIN içinde yalnızca bu 20 takımın CLUT verileri değişti. İlk palet ofseti 0xe79c; takım s için ofset 0xe79c + 32*s. CLUT kimliği 184+s, VRAM X=16*((184+s)%16), Y=496+((184+s)//16).
- SELECT.BIN'de 0x2c464 tabanlı grafik kimliği tablosunun yalnızca 20 hedef girişi değişti. Paylaşılan dokulardan ayrı alanlara erişebilmek için bayrak çizimi ve bayrak VRAM kopyalama rutinlerindeki grafik adresleme talimatları da uyarlandı. **Bu yalnızca PNG değişimi değildir; ROM içinde grafik adresleme kodu da içerir.** Oyuncu/maç mantığı değiştirilmedi. Tam ofsetler ve önce/sonra baytları manifest.json içindedir.
- Değişen ISO dosyaları: /BIN/DATSEL.BIN (LBA 6000), /BIN/DAT2D.BIN (LBA 5300), /SELECT.BIN (LBA 870). Dosya boyları, LBA'lar, CUE zamanlamaları ve ses izleri korunmuştur. DATSEL yeni içerik boyu 228.328 bayt; özgün dosya boyu 229.064 bayt olarak tutuldu.

## Koruma ve test sonuçları

- RAR'daki 16 dosyanın boyu ve CRC32 değeri arşiv kayıtlarıyla doğrulandı. Özgün arşiv ve tüm çıkarılmış v0.8 dosyaları ayrı tutuldu.
- v0.8'e göre diğer 242 çıkarılabilir ISO dosyası bayt bayt aynıdır. SELECT değişiklikleri yalnızca bildirilen grafik kodu/tablo alanlarına; DAT2D değişiklikleri yalnızca hedef paletlere sınırlıdır. Oyuncu isimleri, numaraları, mevkileri, özellikleri, takım isimleri ve önceki veriler bu alanların dışında aynen korunmuştur.
- Arşivdeki eski Track 01 ile v0.8 arasında bulunan 4.900 farklı baytın tümü v0.9'da aynen korunmuştur. v0.9 değişiklikleriyle bunların kesişimi sıfırdır. Arşivdeki eski kopya temiz perakende ROM olarak varsayılmadı; yalnızca önceki değişiklikleri karşılaştırmak için kullanıldı.
- Değişen 117 ham sektörün EDC/ECC'si yeniden üretildi ve doğrulandı; sektör başlıkları, XA alt başlıkları ve diğer sektörler değişmedi. 11 CD ses izi aynıdır.
- PCSX ReARMed (c881679), HLE BIOS ve yazılım GPU ile normal açılış test edildi. 20 kulübün her biri seçildi; gerçek GPU çizim komutları, doku sayfası, UV'ler, 16 renkli CLUT ve bütün bayrak pikselleri doğrulandı. Dört boyutun tamamı için 20 kulübün gerçek VRAM içeriği kaynak grafiklerle eşleşti.
- Crystal Palace–Ireland ve Crystal Palace–Tottenham maçları başlatıldı. Maç ayarları, kulüp seçimi, skor tabelası ve canlı maç görüntüsü kontrol edildi. Son dosya BPS yamasıyla yeniden üretildikten sonra normal açılış ve Crystal Palace–Tottenham maçı tekrar test edildi.
- BPS uygulaması hedef BIN'i birebir üretti; yanlış kaynak ve bozulmuş yama reddedildi. Python betiğinin ürettiği 12 BIN dosyası teslim edilen dosyalarla aynıdır.
- Emülatör kanıtları ekran görüntülerindedir. Gerçek PlayStation 1, diğer emülatörler, tüm oyun modları, diller, tüm takım eşleşmeleri, maç sonları ve uzun sezon oynanışı test edilmedi. Bu testler kapsamında HLE BIOS kullanıldı; bir Sony BIOS dosyası pakete eklenmedi.

## SHA-256

Kaynak v0.8 Track 01: `7d2f3bd3827e36d3badeee14871674fcc3bc91e693928437f3b089de70d9372c`

Hedef v0.9 Track 01: `cd19a0452a1ad901ca997fa5c7a597a9a1316d6083d07dd42ec79eaebb0acd9d`

BPS yama: `32c5564480a8937ff83be58fd39ee3b9a7e0d7118b5492d9633032130d1b5401`

Ayrıntılı makine kontrolleri validation.json ve patch-validation.json dosyalarındadır.
