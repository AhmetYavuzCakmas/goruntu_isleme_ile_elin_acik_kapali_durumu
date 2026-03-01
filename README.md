# goruntu_isleme_ile_elin_acik_kapali_durumu

Bu proje, Python, OpenCV ve MediaPipe kullanarak gerçek zamanlı el tespiti (Hand Tracking) gerçekleştirmektedir.
Kamera görüntüsü üzerinden el landmark noktaları tespit edilir ve elin açık veya kapalı olduğu basit bir algoritma ile belirlenir.

Kullanılan Teknolojiler

Python
OpenCV
MediaPipe


Nasıl Çalışır?

Webcam üzerinden görüntü alınır.
Görüntü BGR formatından RGB formatına çevrilir.
MediaPipe Hands modeli ile eldeki 21 landmark noktası tespit edilir.
Orta parmak kökü (landmark 9) ile orta parmak ucu (landmark 12) karşılaştırılır.
Eğer parmak ucu aşağıdaysa → KAPALI
Eğer parmak ucu yukarıdaysa → ACIK
Sonuç ekrana yazdırılır ve landmark bağlantıları çizilir.


Algoritma Mantığı

MediaPipe her el için 21 adet koordinat üretir.
Bu projede:
Landmark 9 → Orta parmak eklemi
Landmark 12 → Orta parmak ucu
Y ekseni aşağı doğru arttığı için:
if y1 > y:
    KAPALI
else:
    ACIK
mantığı kullanılmıştır.


Projenin Amacı

Gerçek zamanlı görüntü işleme öğrenmek
MediaPipe landmark yapısını anlamak
El hareketi ile kontrol sistemleri geliştirmek için temel oluşturmak
