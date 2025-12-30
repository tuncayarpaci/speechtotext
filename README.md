## Önemli: Mikrofon Erişimi Hakkında
Dış IP (10.1.1.1) üzerinden bağlandığınızda tarayıcı mikrofonu engeller. 
Çözüm için Chrome üzerinde şu ayarı yapın:
1. chrome://flags/#unsafely-treat-insecure-origin-as-secure adresine gidin.
2. 'http://10.1.1.1:3333' adresini güvenli listeye ekleyip tarayıcıyı yeniden başlatın.
