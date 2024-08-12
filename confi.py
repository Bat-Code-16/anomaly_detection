from datetime import datetime
def date_to_ts(start_date,end_date):
    ts=(start_date.timestamp())*1000,
    te=(end_date.timestamp())*1000,
    return ts, te

start_date=datetime(2024, 7, 1)
end_date=datetime(2024, 8, 1)

ts,tt=date_to_ts(start_date,end_date)
print(ts,tt)


# plt.subplot(1, 3, 1)
        # plt.plot(range(2,11), knee_curve_dict.values(), 'bo-', label='SSE')
        # plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
        # plt.xlabel('Number of clusters (k)')
        # plt.ylabel('Sum of Squared Errors (SSE)')
        # plt.title('Elbow Method with Kneedle')
        # plt.legend()
    
            
        # Plotting the silhouette scores
        # plt.subplot(1, 3, 2)
        # plt.plot(range(2, 11), silhouette_scores, marker='o', color='r')
        # plt.xlabel("Number of clusters")
        # plt.ylabel("Silhouette Score")
        # plt.title("Silhouette Score for Optimal k")
        # plt.grid(True)

        # plt.subplot(1, 3, 3)
        # plt.plot(range(2, 11), db_scores, marker='o', color='r')
        # plt.xlabel("Number of clusters")
        # plt.ylabel("DB Score")
        # plt.title("DB Score for Optimal k")
        # plt.grid(True)
        
        
        
# Calculate silhouette score
            # score = silhouette_score(scaled_data, model.labels_)
            # silhouette_scores.append(score)
            
            # # Calculate db score
            # db_score=davies_bouldin_score(scaled_data,model.labels_)
            # db_scores.append(db_score)
            
silhouette_scores=[]
db_scores=[]