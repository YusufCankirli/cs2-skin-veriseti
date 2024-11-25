import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#1. Eksik Verilerin İncelenmesi
file_path = 'cs2_skinler.csv'  
data = pd.read_csv(file_path, sep=";")

# Eksik verilerin yüzdesi
missing_data_percentage = data.isnull().mean() * 100

print("Sütun Bazında Eksik Veri Yüzdeleri:")
print(missing_data_percentage.sort_values(ascending=False))


#2. Fiyat Analizi (Mod, Medyan, Ortalama)

# Fiyat sütununu sayısal değerlere dönüştürme (₺ sembolünü kaldırma)
data['bynogame_fiyat_tl'] = pd.to_numeric(data['bynogame_fiyat_tl'].str.replace("₺", "").str.replace(",", ""), errors="coerce")

# Temel istatistikler
average_price = data['bynogame_fiyat_tl'].mean()
median_price = data['bynogame_fiyat_tl'].median()
mode_price = data['bynogame_fiyat_tl'].mode()[0]

print(f"Fiyatların Ortalaması: {average_price:.2f} TL")
print(f"Fiyatların Medyanı: {median_price:.2f} TL")
print(f"Fiyatların Modu: {mode_price:.2f} TL")

# En pahalı ve en ucuz ürünler
most_expensive_item = data.loc[data['bynogame_fiyat_tl'].idxmax()]
cheapest_item = data.loc[data['bynogame_fiyat_tl'].idxmin()]

print("\nEn Pahalı Ürün:")
print(most_expensive_item[['skin_isim', 'bynogame_fiyat_tl']])
print("\nEn Ucuz Ürün:")
print(cheapest_item[['skin_isim', 'bynogame_fiyat_tl']])

#3. Satış Analizi (En Çok Satılan Ürünler)
# Satış sütunlarını sayısal değerlere dönüştürme (Eksik değerleri de dikkate alıyoruz)
sales_columns = [
    "son_hafta_satılan", 
    "son_2_hafta_satılan", 
    "son_1_ay_satılan", 
    "son_2_ay_satılan", 
    "son_3_ay_satılan"
]
data[sales_columns] = data[sales_columns].apply(pd.to_numeric, errors="coerce")

# Son 1 ayda en çok satılan ürünler
top_selling_last_month = data.nlargest(5, "son_1_ay_satılan")[["skin_isim", "son_1_ay_satılan"]]
print("Son 1 Ayda En Çok Satılan Ürünler:")
print(top_selling_last_month)

# Zaman dilimlerine göre toplam satış miktarı
total_sales = data[sales_columns].sum()
print("\nZaman Dilimlerine Göre Toplam Satış Miktarı:")
print(total_sales)

# Veri türünü kontrol etme
print(data['bynogame_fiyat_tl'].dtype)

# Eğer sütun sayısal değilse, string'e dönüştürüp işleme yapalım
data['bynogame_fiyat_tl'] = data['bynogame_fiyat_tl'].astype(str)

# ₺ sembolünü kaldırıp, virgül yerine nokta kullanarak sayıya dönüştürme
data['bynogame_fiyat_tl'] = pd.to_numeric(data['bynogame_fiyat_tl'].str.replace("₺", "").str.replace(",", ""), errors="coerce")

# Fiyat verisinin istatistiksel özetini alalım
price_mode = data['bynogame_fiyat_tl'].mode()[0]
price_median = data['bynogame_fiyat_tl'].median()
price_std = data['bynogame_fiyat_tl'].std()
price_variance = data['bynogame_fiyat_tl'].var()

print(f"Satış Fiyatlarının Modu: {price_mode:.2f} TL")
print(f"Satış Fiyatlarının Medyanı: {price_median:.2f} TL")
print(f"Satış Fiyatlarının Standart Sapması: {price_std:.2f} TL")
print(f"Satış Fiyatlarının Varyansı: {price_variance:.2f}")

#4. Grafikler (Satış Trendleri ve En Çok Satılan Ürünler)

# Çizgi Grafiği: Zaman Dilimlerine Göre Toplam Satış Miktarı
plt.figure(figsize=(10, 6))
total_sales.plot(kind="line", marker="o", color="b", linestyle="--")
plt.title("Zaman Dilimlerine Göre Toplam Satış Miktarı")
plt.xlabel("Zaman Dilimi")
plt.ylabel("Satış Miktarı")
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Bar Grafiği: Son 1 Ayda En Çok Satılan 5 Ürün
plt.figure(figsize=(10, 6))
plt.barh(top_selling_last_month["skin_isim"], top_selling_last_month["son_1_ay_satılan"], color="orange")
plt.title("Son 1 Ayda En Çok Satılan 5 Ürün")
plt.xlabel("Satış Miktarı")
plt.ylabel("Ürün İsmi")
plt.gca().invert_yaxis()  # En çok satan en üstte olsun
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

#5. Histogram: Fiyat Dağılımı
plt.figure(figsize=(10, 6))
data['bynogame_fiyat_tl'].dropna().plot(kind="hist", bins=20, color="purple", edgecolor="black")
plt.title("Ürün Fiyatlarının Dağılımı")
plt.xlabel("Fiyat (TL)")
plt.ylabel("Frekans")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# Bar Grafiği: Son 3 Ayda En Çok Satılan 5 Ürün
top_selling_last_3_months = data.nlargest(5, "son_3_ay_satılan")[["skin_isim", "son_3_ay_satılan"]]
plt.figure(figsize=(10, 6))
plt.barh(top_selling_last_3_months["skin_isim"], top_selling_last_3_months["son_3_ay_satılan"], color="teal")
plt.title("Son 3 Ayda En Çok Satılan 5 Ürün")
plt.xlabel("Satış Miktarı")
plt.ylabel("Ürün İsmi")
plt.gca().invert_yaxis()  # En çok satan en üstte olsun
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()



# Sayısal sütunları seçme (fiyat ve satış verileri)
numeric_columns = ["bynogame_fiyat_tl"] + [
    "son_hafta_satılan", 
    "son_2_hafta_satılan", 
    "son_1_ay_satılan", 
    "son_2_ay_satılan", 
    "son_3_ay_satılan"
]
correlation_matrix = data[numeric_columns].corr()

# Korelasyon Matrisi Gösterimi
print("Korelasyon Matrisi:")
print(correlation_matrix)

# Heatmap (Isı Haritası) ile Görselleştirme
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Korelasyon Matrisi (Isı Haritası)")
plt.tight_layout()
plt.show()

# Scatter Plot: Fiyat ile Son 1 Ayda Satış Miktarı
plt.figure(figsize=(10, 6))
plt.scatter(data["bynogame_fiyat_tl"], data["son_1_ay_satılan"], color="blue", alpha=0.6, edgecolor="k")
plt.title("Fiyat ile Son 1 Ayda Satış Miktarı Arasındaki İlişki")
plt.xlabel("Fiyat (TL)")
plt.ylabel("Son 1 Ayda Satış Miktarı")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Scatter Plot: Son 1 Ay Satılan ile Son 3 Ay Satılan
plt.figure(figsize=(10, 6))
plt.scatter(data["son_1_ay_satılan"], data["son_3_ay_satılan"], color="green", alpha=0.6, edgecolor="k")
plt.title("Son 1 Ay Satış Miktarı ile Son 3 Ay Satış Miktarı Arasındaki İlişki")
plt.xlabel("Son 1 Ay Satış Miktarı")
plt.ylabel("Son 3 Ay Satış Miktarı")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
