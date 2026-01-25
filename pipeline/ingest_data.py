#!/usr/bin/env python
# coding: utf-8

# In[3]:





# In[1]:


import pandas as pd

df = pd.read_parquet("green_tripdata_2025-11.parquet")
df.head()


# In[2]:


df.columns


# In[4]:


len(df)


# In[3]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# In[5]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[7]:


engine


# In[9]:


import pyarrow.parquet as pq
import pandas as pd

parquet_file = pq.ParquetFile("green_tripdata_2025-11.parquet")

for batch in parquet_file.iter_batches(batch_size=100_000):
    df = batch.to_pandas()
    print(len(df))
    break   # hapus ini kalau mau proses semua


# In[13]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[ ]:





# In[3]:





# In[1]:


import pandas as pd

df = pd.read_parquet("green_tripdata_2025-11.parquet")
df.head()


# In[2]:


df.columns


# In[4]:


len(df)


# In[3]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# In[19]:


from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/ny_taxi")


# In[20]:


engine


# In[21]:


with engine.connect() as conn:
    print("Connected!")


# In[23]:


df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')


# In[22]:


engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/ny_taxi"
)

parquet_file = pq.ParquetFile("green_tripdata_2025-11.parquet")

for batch in parquet_file.iter_batches(batch_size=100_000):
    df = batch.to_pandas()
    break  # test dulu

print(pd.io.sql.get_schema(df, name="green_taxi_data", con=engine))


# In[38]:


for i, batch in enumerate(parquet_file.iter_batches(batch_size=100_000)):
    df = batch.to_pandas()

    df.to_sql(
        name="green_taxi_data",
        con=engine,
        if_exists="append" if i > 0 else "replace",
        index=False
    )

    print(f"Inserted batch {i}")

