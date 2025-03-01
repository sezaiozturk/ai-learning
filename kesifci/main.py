import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler

file_path = "anket.xlsx"
df = pd.read_excel(file_path, sheet_name="Form Yanıtları 1")

df = df.drop(columns=["Unnamed: 0"], errors="ignore")

missing_percentage = (df.isnull().sum() / len(df)) * 100
print("\n Eksik Veri Yüzdeleri:")
print(missing_percentage[missing_percentage > 0])


print("\n Sayısal Değişkenlerin Betimsel İstatistikleri:")
print(df.describe())

print("\n Kategorik Değişkenlerin Dağılımı:")
categorical_columns = df.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    print(f"\n{col} Sütunu:")
    print(df[col].value_counts())

# Eksik verileri doldurma (Ortalama ile)Hata var burada
#df.select_dtypes(include=['number']).fillna(df.mean(), inplace=True)

plt.figure(figsize=(10, 5))
sns.boxplot(data=df.select_dtypes(include=["int64", "float64"]))
plt.xticks(rotation=45)
plt.title("Aykırı Değer Analizi")
plt.show()

df.hist(figsize=(12, 8), bins=20)
plt.suptitle("Veri Dağılımı")
plt.show()

label_enc = LabelEncoder()
for col in categorical_columns:
    df[col] = label_enc.fit_transform(df[col].astype(str))

scaler = StandardScaler()
df[df.select_dtypes(include=["int64", "float64"]).columns] = scaler.fit_transform(df.select_dtypes(include=["int64", "float64"]))

df.to_csv("temizlenmis_veri.csv", index=False)
print("\n✅ Veri ön işleme tamamlandı, 'temizlenmis_veri.csv' olarak kaydedildi.")
