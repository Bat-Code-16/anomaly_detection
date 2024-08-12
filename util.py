from kneed import KneeLocator
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import silhouette_score,davies_bouldin_score


def drop_values(df:pd.DataFrame,col_list:list[str]):
    for column in col_list:
        
        if column in df.columns:
            df = df[df[column] <= 1e6]  # Update df1 with the filtered result
    return df


def drop_columns(df:pd.DataFrame,col_name:list[str]):
    df=df.drop(columns=col_name,axis=1,inplace=True)
    return df


def make_deviceid_dict(df: pd.DataFrame, unique:int):
    # Convert unique DeviceIDs to a list
    unique_device_ids = df["DeviceID"].unique().tolist()
    
    # Select the first `unique` number of device IDs
    unique_device = unique_device_ids[:unique]
    
    # Initialize dictionary to hold DataFrames for each device ID
    device_list = {}
    
    for device_id in unique_device:
        # Filter DataFrame by device ID
        filtered_df = df[df["DeviceID"] == device_id]
        
        # Use the device ID as the key in the dictionary
        device_list[f"device_{device_id}"] = filtered_df

    return [unique_device, device_list]


def optimal_k(inertia_score):
    kneedle=KneeLocator(range(2,11),inertia_score,curve="convex", direction="decreasing")
    optimal_k=kneedle.elbow
    return optimal_k



def k_score(data: pd.DataFrame):
    scaler = MinMaxScaler()
    silhouette_scores = []
    inertia_scores = []
    db_scores = []
    
    # Fit KMeans for k ranging from 2 to 10
    for k in range(2, 11):
        model = KMeans(n_clusters=k, random_state=42)
        scaled_data = scaler.fit_transform(data)
        model.fit(scaled_data)
        
        # Append inertia (Elbow Method)
        inertia_scores.append(model.inertia_)
        
        # Calculate silhouette score
        score = silhouette_score(scaled_data, model.labels_)
        silhouette_scores.append(score)

        # Calculate Davies-Bouldin Score
        db_score = davies_bouldin_score(scaled_data, model.labels_)
        db_scores.append(db_score)
    
    optimal_v = optimal_k(inertia_scores)

    # Plotting the elbow curve (Inertia)
    plt.figure(figsize=(18, 7))
    
    plt.subplot(1, 4, 1)
    plt.plot(range(2, 11), inertia_scores, marker='o')
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for Optimal k")
    plt.grid(True)
    
    # Plotting the silhouette scores
    plt.subplot(1, 4, 2)
    plt.plot(range(2, 11), silhouette_scores, marker='o', color='r')
    plt.xlabel("Number of clusters")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score for Optimal k")
    plt.grid(True)

    # Plotting the Davies-Bouldin scores
    plt.subplot(1, 4, 3)
    plt.plot(range(2, 11), db_scores, marker='o', color='g')
    plt.xlabel("Number of clusters")
    plt.ylabel("DB Score")
    plt.title("DB Score for Optimal k")
    plt.grid(True)
    
    # Plotting the elbow curve with optimal k
    plt.subplot(1, 4, 4)
    plt.plot(range(2, 11), inertia_scores, 'bo-', label='SSE')
    plt.axvline(x=optimal_v, color='r', linestyle='--', label=f'Optimal k={optimal_v}')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.title("Elbow Method with Optimal k")
    plt.legend()
    plt.grid(True)
    
    plt.show()
    return optimal_v



def k_score_each_device( device_list: dict,device_feature:list[str]):
    
    knee_curve_dict = {}

    for device_name, device in device_list.items():
        scaler = MinMaxScaler()

        data = device[device_feature]
        scaled_data = scaler.fit_transform(data)
        inertia_scores = []
        silhouette_scores = []
        db_scores = []

        # Fit KMeans for k ranging from 2 to 10
        for k in range(2, 11):
            model = KMeans(n_clusters=k, random_state=42)
            model.fit(scaled_data)
            
            # Append inertia (Elbow Method)
            inertia_scores.append(model.inertia_)
            
            # Calculate silhouette score
            score = silhouette_score(scaled_data, model.labels_)
            silhouette_scores.append(score)

            # Calculate Davies-Bouldin Score
            db_score = davies_bouldin_score(scaled_data, model.labels_)
            db_scores.append(db_score)
        
        optimal_v = optimal_k(inertia_scores)
        knee_curve_dict[device_name] = optimal_v

        # Plotting the metrics
        plt.figure(figsize=(20, 6))
        
        plt.subplot(1, 4, 1)
        plt.plot(range(2, 11), inertia_scores, marker='o')
        plt.xlabel("Number of clusters")
        plt.ylabel("Inertia")
        plt.title(f"Elbow Method for {device_name}")
        plt.grid(True)
        
        plt.subplot(1, 4, 2)
        plt.plot(range(2, 11), silhouette_scores, marker='o', color='r')
        plt.xlabel("Number of clusters")
        plt.ylabel("Silhouette Score")
        plt.title(f"Silhouette Score")
        plt.grid(True)

        plt.subplot(1, 4, 3)
        plt.plot(range(2, 11), db_scores, marker='o', color='g')
        plt.xlabel("Number of clusters")
        plt.ylabel("DB Score")
        plt.title("Davies-Bouldin Score ")
        plt.grid(True)
        
        plt.subplot(1, 4, 4)
        plt.plot(range(2, 11), inertia_scores, 'bo-', label='SSE')
        plt.axvline(x=optimal_v, color='r', linestyle='--', label=f'Optimal k={optimal_v}')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Sum of Squared Errors (SSE)')
        plt.title(f"Elbow Method for {device_name}")
        plt.legend()
        plt.grid(True)
        
        plt.show()
    
    return knee_curve_dict

        


