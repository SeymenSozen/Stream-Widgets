🎥 ByNoGame Stream Toolkit
ByNoGame API'sini kullanan, Python (Flask) tabanlı, OBS uyumlu hepsi bir arada bağış yönetim sistemi.

🌟 Öne Çıkan Özellikler
📊 Dinamik Bağış Barı: Hedefinizi, mevcut tutarı ve ilerleme yüzdesini gösteren animasyonlu görsel bar.

🔔 Canlı Alert Sistemi: Yeni bağış geldiğinde tetiklenen sesli ve GIF destekli uyarı ekranı (Kuyruk yapısıyla sırayla gösterim).

🏆 Liderlik Tablosu: En çok bağış yapan "Top 5" listesini şık bir tablo tasarımıyla sunar.

🛡️ Akıllı Filtreleme: Sistem mesajlarını ("ByNoGame" kullanıcı adı) otomatik olarak eler.

⚙️ Çoklu İş Parçacı (Threading): Arka planda bağışları takip ederken sunucuyu kesintisiz çalıştırır.

🚀 Kurulum ve Başlatma
1. Gereksinimler

Sisteminizde Python 3.x yüklü olmalıdır. Gerekli kütüphaneleri şu komutla yükleyin:

Bash
pip install flask requests colorama
2. API Anahtarı

Proje klasörünüzde api.key isimli bir dosya oluşturun ve içine ByNoGame API keyinizi kaydedin.

3. Çalıştırma

Bash
python Server.py
📺 OBS Entegrasyonu
OBS üzerinden Tarayıcı (Browser) kaynağı ekleyerek aşağıdaki adresleri kullanın:

Modül	URL	Önerilen Boyut
Bağış Hedef Barı	http://127.0.0.1:33333/donatebar	800 x 150
Canlı Bağış Bildirimi	http://127.0.0.1:33333/donatealert	800 x 600
Top 5 Listesi	http://127.0.0.1:33333/top5	450 x 600
📂 Proje Yapısı
Plaintext
├── Server.py             # Ana uygulama dosyası (Flask & Tracker)
├── api.key               # API anahtarınız (Gizli tutulmalıdır)
└── templates/            # HTML arayüzleri
    ├── DonateBar.html    # İlerleme barı tasarımı
    ├── DonateAlerts.html  # Bildirim ekranı tasarımı
    └── Top5.html         # Liderlik tablosu tasarımı
🛠️ Özelleştirme
Server.py içerisindeki şu değişkenleri kendi yayınınıza göre düzenleyebilirsiniz:

Hedef_Turar: Hedeflediğiniz toplam bağış miktarı.

Hedef_Metin: Barın ortasında yazacak olan hedef adı (örn: "Capture Card").

Alert_Duration: Bağış bildiriminin ekranda kalma süresi (Saniye).

Alret_Gif & Alett_Sound: Bildirimlerde kullanılacak görsel ve ses linkleri.

📜 Lisans
Bu proje tamamen açık kaynaklıdır ve geliştirilmeye uygundur.

Geliştirici Notu: Bu proje, modern yayıncı ihtiyaçlarını karşılamak üzere asenkron veri işleme mantığıyla kurgulanmıştır.