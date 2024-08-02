import pandas as pd
import matplotlib.pyplot as plt
from stepmix.stepmix import StepMix
import numpy as np
import seaborn as sns
import os

def main():
    file = input("File path: ")
    min_cluster = input("Minimum number of clusters to test: ")
    max_cluster = input("Maximum number of clusters to test: ")
    check_file(file)
    check_table(file)
    min_cluster, max_cluster = check_cluster(min_cluster, max_cluster)
    Q, demo = load_transform(file)
    n = decide_cluster_num(Q, min_cluster, max_cluster)
    Q2, combined = cluster_analysis(n, Q, demo)
    print(cluster_mean(Q2))
    summarise(combined)
    visualise(combined)

def check_file(file):
    try:
        # Check if the file exists
        if not os.path.exists(file):
            raise ValueError("The path/file does not exist.")
        # Check if the file is a csv file
        if not file.lower().endswith(".csv"):
            raise ValueError("The file is not a csv file.")
    except(ValueError):
        raise

def check_table(file):
    try:
        # Check if the columns are correct
        df = pd.read_csv(file)
        columns = df[["Serial", "Area", "Age", "Sex", "Q1", "Q2", "Q3", "Q4", "Q5"]]
        if df["Area"].max()>3 or df["Area"].min()<1:
            raise ValueError("Incorrect option values for Area")
        if df["Age"].max()>3 or df["Area"].min()<1:
            raise ValueError("Incorrect option values for Age")
        if df["Sex"].max()>2 or df["Area"].min()<1:
            raise ValueError("Incorrect option values for Sex")
    except(KeyError):
        raise KeyError("Incorrect file structure")

def check_cluster(min_cluster, max_cluster):
    while True:
        try:
            min_cluster = int(min_cluster)
            max_cluster = int(max_cluster)
            if max_cluster >= min_cluster and min_cluster>=2 and max_cluster<=10:
                return min_cluster, max_cluster
            else:
                min_cluster = input("Minimum number of clusters to test: ")
                max_cluster = input("Maximum number of clusters to test: ")
                pass
        except (ValueError):
            raise ValueError("Cluster number should be an integer between 2 and 10")

def load_transform(file):
    # Load data
    df = pd.read_csv(file)
    # Create subset of data
    Q = df.iloc[:, 4:9]
    demo = df[["Serial", "Area", "Age", "Sex"]]
    # Drop rows with NA question response
    Q = Q.dropna()
    return Q, demo

def decide_cluster_num(Q, min_cluster, max_cluster):
    # Define a range of cluster numbers to evaluate
    n_clusters_range = range(min_cluster, max_cluster+1)

    # Initialize an empty list to store BIC values
    bic_values = []

    for n_clusters in n_clusters_range:
        # Create and fit the LCA model
        model = StepMix(n_components=n_clusters, measurement="categorical", verbose=1, random_state=123)
        model.fit(Q)

        # Get BIC value for current model and append to list
        bic = model.bic(Q)
        bic_values.append(bic)

    # Return the number of clusters with minimum BIC
    min_BIC = min(bic_values)
    min_BIC_index = bic_values.index(min_BIC) + min_cluster
    return min_BIC_index

def cluster_analysis(n, Q, demo):
    # Categorical latent class model
    model = StepMix(n_components=n, measurement="categorical", verbose=1, random_state=123)

    # Fit model
    model.fit(Q)

    # Class predictions
    Q['cluster'] = model.predict(Q)
    Q.index.name = 'Serial'

    # Merge with demographics
    combined = pd.merge(Q, demo, how="left", on="Serial")
    combined.to_csv("combined.csv")
    return Q, combined

def cluster_mean(Q):
    cluster_mean = Q.groupby("cluster").mean()
    return cluster_mean

def summarise(combined):
    # Dictionary to map coded values to labels
    Area_labels = {1:'District A', 2:'District B', 3:'District C'}
    Age_labels = {1: '18-34', 2: '35-64', 3: '65+'}
    Sex_labels = {1: 'Male', 2: 'Female'}

    # Generate tables on cluster distribution by demographic variables
    for v in ["Area", "Age", "Sex"]:
        v_cluster = combined[["cluster", v]]
        cross_tab = pd.crosstab(index=v_cluster["cluster"], columns=v_cluster[v], values=1, aggfunc='sum')
        column_totals = cross_tab.sum(axis=0)
        percentage = (cross_tab / column_totals)
        label = f"{v}_labels"
        percentage.rename(columns=locals()[label], inplace=True)
        percentage.to_csv(f"{v}.csv")

def visualise(combined):
    # Labels for axis
    area_axis = ['District A', 'District B', 'District C']
    age_axis = ['18-34', '35-64', '65+']
    sex_axis = ['Male', 'Female']

    # Generate random noise in the range 0 to 0.5
    xnoise, ynoise = np.random.random(len(combined))/2, np.random.random(len(combined))/2

    # Plot the scatterplot for area vs age
    plt.figure(1)
    sns.scatterplot(x=combined["Area"]+xnoise, y=combined["Age"]+ynoise,
                hue=combined['cluster'], data=combined, palette='viridis')

    plt.xticks([1.25, 2.25, 3.25], area_axis)
    plt.yticks([1.25, 2.25, 3.25], age_axis)
    plt.xlabel('Area')
    plt.ylabel('Age')
    plt.savefig("Fig 1.png")

    # Plot the scatterplot for area vs sex
    plt.figure(2)
    sns.scatterplot(x=combined["Area"]+xnoise, y=combined["Sex"]+ynoise,
                hue=combined['cluster'], data=combined, palette='viridis')

    plt.xticks([1.25, 2.25, 3.25], area_axis)
    plt.yticks([1.25, 2.25], sex_axis)
    plt.xlabel('Area')
    plt.ylabel('Sex')
    plt.savefig("Fig 2.png")
    
    # Plot the scatterplot for age vs sex
    plt.figure(3)
    sns.scatterplot(x=combined["Age"]+xnoise, y=combined["Sex"]+ynoise,
                hue=combined['cluster'], data=combined, palette='viridis')

    plt.xticks([1.25, 2.25, 3.25], age_axis)
    plt.yticks([1.25, 2.25], sex_axis)
    plt.xlabel('Age')
    plt.ylabel('Sex')
    plt.savefig("Fig 3.png")

if __name__ == "__main__":
    main()
