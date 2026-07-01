import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib

# ============================
# 1) خواندن داده
# ============================
df = pd.read_csv("data/housePrice.csv")

print("=== اطلاعات اولیه ===")
print(df.info())
print(df.describe())

# ============================
# 2) نمودارهای اولیه
# ============================
numeric_df = df.select_dtypes(['number'])

sns.pairplot(numeric_df)
plt.show()

sns.histplot(df['Price'], kde=True)
plt.title("Price Distribution")
plt.show()

sns.histplot(df['Area'], kde=True)
plt.title("Area Distribution")
plt.show()

# ============================
# 3) Heatmap کامل
# ============================
plt.figure(figsize=(12, 10))
sns.heatmap(numeric_df.corr(), annot=True, cmap='viridis')
plt.title("Correlation Heatmap (Numeric Columns)")
plt.show()

# ============================
# 4) تبدیل Address به داده عددی
# ============================
df_encoded = pd.get_dummies(df, columns=['Address'])

# ============================
# 5) استخراج مهم‌ترین ویژگی‌ها با Random Forest
# ============================
X = df_encoded.drop(['Price', 'Price(USD)'], axis=1)
y = df_encoded['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)

importances = rf_model.feature_importances_

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("=== مهم‌ترین ویژگی‌ها ===")
print(feature_importance.head(20))

# ذخیره مدل
joblib.dump(rf_model, "models/random_forest_model.pkl")

# ============================
# 6) مدل پیش‌بینی قیمت (Linear Regression)
# ============================
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

print("Linear Regression Accuracy:", lr_model.score(X_test, y_test))
print("Random Forest Accuracy:", rf_model.score(X_test, y_test))

# ============================
# 7) پیش‌بینی قیمت یک خانه جدید
# ============================

sample = {
    'Area': 120,
    'Room': 3,
    'Parking': True,
    'Warehouse': True,
    'Elevator': True,
}

for col in df_encoded.columns:
    if col.startswith("Address_"):
        sample[col] = 0

sample['Address_Farmanieh'] = 1

sample_df = pd.DataFrame([sample])

predicted_price = rf_model.predict(sample_df)[0]
print("Predicted Price:", predicted_price)
