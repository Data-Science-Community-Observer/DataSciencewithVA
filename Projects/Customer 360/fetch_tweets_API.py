# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import os
import pandas as pd

# Define storage path on remote server
server_path = "/workspace/Customer 360/tweets_data"
os.makedirs(server_path, exist_ok=True)  # Ensure the directory exists

# File path to store tweets
file_path = os.path.join(server_path, "amazon_tweets.csv")

# Test: Save a dummy DataFrame
df = pd.DataFrame([["2024-03-07", "This is a sample tweet about Amazon."]], columns=["Timestamp", "Tweet"])
df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

print(f"File saved at {file_path}")

