#from databricks.sdk.runtime import *
import pandas as pd
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("abc").getOrCreate()

class InvalidEnvironmentironmentEnteredError(Exception):
  def __init__(self,message = 'Invalid environment entered, suggested environments: PROD, UAT, DEV'):
    self.message = message
    super().__init__(self.message)

class InvalidRegionEnteredError(Exception):
  def __init__(self,message = 'Invalid region entered, suggested regions: Sirius, U2K2, Cordillera, Fusion, SiriusVanguard'):
    self.message = message
    super().__init__(self.message)

class MountPointNotConfiguredError(Exception):
  def __init__(self,message):
    self.message = message
    super().__init__(self.message)

def GetMaterialMappedAtSKULevel(environment,region):
    if environment.casefold() == 'PROD'.casefold():
        adls = '80049'
    elif environment.casefold() == 'UAT'.casefold():
        adls = '80158'
    elif environment.casefold() == 'DEV'.casefold():
        adls = '80046'
    else:
        raise InvalidEnvironmentironmentEnteredError()

    df_mounts = dbutils.fs.mounts()
    df_mount_pd = pd.DataFrame(df_mounts)
    if df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net/$",case=False)].empty == False  :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "None"
    elif df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net.*/BusinessDataLake/$",case=False)].empty == False :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net.*/BusinessDataLake/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "/BusinessDataLake"
    elif df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net.*/BusinessDataLake/SC/$",case=False)].empty == False :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f".{adls}adls.dfs.core.windows.net.*/BusinessDataLake/SC/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "/BusinessDataLake/SC"
    else:
        raise MountPointNotConfiguredError(f"MountPoint is not configured for the following storage account:{adls}({environment})")
    
    df_parquet = spark.read.format("parquet").load("/mnt/adls/Unilever/ManualConfig/parquet")
    df_pd = df_parquet.toPandas()

    if df_pd[df_pd['Region'].str.fullmatch(f"{region}",case=False)].empty == True:
        raise InvalidRegionEnteredError()
    else:
        df_pd = df_pd[df_pd['HierarchyGroupName'].str.fullmatch("Product",case=False) & df_pd['Region'].str.fullmatch(f"{region}",case=False)]

    regionID = df_pd['RegionID'].iloc[0]

    local_cols = df_pd['TargetAttributes_B'].iloc[0]
    local_split_cols = local_cols.split(", ")
    local_prefixed_cols = ["B." + sub for sub in local_split_cols] 
    final_local_cols = ', '.join(local_prefixed_cols)

    global_cols = df_pd['SourceAttributes_A'].iloc[0]
    global_split_cols = global_cols.split(", ")
    global_prefixed_cols = ["A." + sub for sub in global_split_cols] 
    final_global_cols = ', '.join(global_prefixed_cols)
    
    local_path = df_pd['TargetPhysicalPath'].iloc[0]
    final_local_path = local_path.replace(initialpath, '')
    complete_local_path = mntpoint + final_local_path

    global_path = df_pd['SourcePhysicalPath'].iloc[0]
    final_global_path = global_path.replace(initialpath, '')
    complete_global_path = mntpoint + final_global_path

    join_condition = df_pd['JoinCondition'].iloc[0]

    df_bdl_global = spark.read.format("delta").load(complete_global_path)
    df_bdl_global.createOrReplaceTempView('vw_bdl_hgpl')

    data_local = spark.read.format("delta").load(complete_local_path)
    data_local.createOrReplaceTempView('vw_udl_local')
    
    if '*' in df_pd["TargetAttributes_B"].iloc[0]:
        df = spark.sql(f"""Select {final_local_cols}, {final_global_cols}
                from vw_bdl_hgpl as A inner join vw_udl_local as B  
                ON {join_condition}""")
    else:
        df = spark.sql(f"""Select {final_local_cols}, {final_global_cols},  B.* except({local_cols})
                  from vw_bdl_hgpl as A inner join vw_udl_local as B  
                  ON {join_condition}""")
    return mntpoint, initialpath, regionID, final_local_cols, final_global_cols, complete_local_path, complete_global_path,df
