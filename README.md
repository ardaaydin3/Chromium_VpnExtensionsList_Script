Bu script, Chrome Web Mağazasından VPN ve proxy extensionlarını aramak ve toplamak için oluşturulmuştur. Bu script'in işlevleri: 

1. Chrome Web Mağazasında "vpn" ve "proxy" anahtar kelimeleriyle arama yapıyor.

2. Hem İngilizce hem de Türkçe dillerinde arama gerçekleştiriyor.
3. Bulunan extensionların ID ve adlarını topluyor.
4. Tekrarlanan uzantıları temizliyor.
5. Sonuçları bir CSV Dosyalarına kaydediyor.

Bu script tarafından elde edilen VPN/Proxy extension listesi, tehdit tespiti için kullanılabilir. Özellikle SIEM, SOAR ve XDR ürünlerinden fayda sağlayabilir:

SIEM: Kullanıcıların Chrome Tarayıcılarında bu uzantılardan herhangi birini yüklediği log'lar (Eventcode=4663, Imageloaded) tespit edilirse, korelasyon kurallarıyla alarm üretebilir.

SOAR: Otomasyon playbooklarında bu uzantı ID'leri ile eşleşen durumlar otomatik olarak karantinaya alınabilir veya kullanıcı bilgilendirilmesi yapılabilir.
