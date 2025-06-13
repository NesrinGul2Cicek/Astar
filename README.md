# Drone Teslimat Optimizasyonu

Bu proje, farklı özelliklere sahip drone’ların belirli teslimatları en verimli şekilde gerçekleştirmesini hedefleyen bir **rota planlama ve optimizasyon sistemidir**. Sistem; **Genetik Algoritma**, **A\*** arama algoritması, **no-fly zone (uçuşa yasak bölge)** kontrolü, **vizüalizasyon** ve **performans analizi** modüllerinden oluşur.

## 🚀 Amaç

- Drone'ların batarya kapasitelerini ve yük taşıma limitlerini dikkate alarak
- Teslimatların önceliklerine uygun
- Yasaklı hava sahalarına girmeyen
- Enerji tüketimi minimum ve başarı oranı maksimum teslimat planı oluşturmak.

---

## 🧠 Kullanılan Yöntemler

- **Genetik Algoritma**: Teslimat planlarını optimize etmek için kullanılır. Bireyler, teslimatların drone’lara atanma şeklidir.
- **A\* (A-Star) Algoritması**: Drone’un başlangıç noktasından hedef teslimat noktasına en kısa ve geçerli yolu bulmak için kullanılır. No-fly zone’lar göz önüne alınır.
- **Enerji Tüketimi Modeli**: Drone’un kat ettiği mesafeye bağlı olarak batarya tüketimi hesaplanır.
- **Performans Analizi**: Başarı oranı, ortalama enerji tüketimi ve algoritma süresi gibi metrikler hesaplanır.
- **Matplotlib ile Görselleştirme**: Drone’ların rotaları, teslimat noktaları ve yasak bölgeler harita üzerinde gösterilir.

---

## 🧰 Kurulum ve Kullanım

### Gereksinimler

- Python >= 3.8
- `matplotlib`
- `numpy`

### Kurulum

```bash
git clone https://github.com/kullanici/drone-optimization.git
cd drone-optimization
pip install -r requirements.txt

