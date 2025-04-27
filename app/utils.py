import pandas as pd
from app.iris import IrisSample
from app import mongodb
from sklearn.model_selection import train_test_split

def process_csv(file):
    df = pd.read_csv(file.file)
    expected_fields = set(IrisSample.__annotations__.keys())
    csv_fields = set(df.columns)

    if validate_csv_fields(expected_fields, csv_fields) is False:
        return [], f"CSV fields {csv_fields} do not match expected fields {expected_fields}"
    
    records = df.to_dict(orient="records")
    return records, None

def validate_csv_fields(expected_fields, csv_fields):
    if csv_fields != expected_fields:
        return False
    
    return True

def split_data():
    samples = mongodb.get_samples()
    X = IrisSample.extract_features(samples)
    y = IrisSample.extract_labels(samples)

    # Split into training and test sets
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.datasets import load_iris
# import pandas as pd

# # Load dataset
# df = pd.read_csv("data/iris.csv")
# # Optional: check your columns
# print(df.columns)

# # sns.pairplot(df, hue="species")
# # plt.suptitle("Pairwise Feature Plot (Subset of Iris)", y=1.02)
# # plt.show()


# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt

# X = df.drop("species", axis=1)
# y = df["species"]

# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X)

# plt.figure(figsize=(6, 5))
# for species in y.unique():
#     plt.scatter(
#         X_pca[y == species, 0],
#         X_pca[y == species, 1],
#         label=species
#     )

# plt.xlabel("PCA 1")
# plt.ylabel("PCA 2")
# plt.title("PCA Projection of Iris Data")
# plt.legend()
# plt.show()