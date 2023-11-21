# from typing import Tuple
from utility.connector.connector import Connector
from pandas import DataFrame, read_csv
import json,os,tempfile
from refractio.refractio import get_dataframe
import requests
from feast import FeatureStore
import pandas as pd
from datetime import datetime

class FeastStore(Connector):
    def __init__(self):
        self.model_config = json.loads(os.getenv("model_configuration"))
        self.connection_name = None
        self.fs_name = [item["field_value"] for item in self.model_config if item['field_id']=="feature_store_name"][0]
        self.fs_view = [item["field_value"] for item in self.model_config if item['field_id']=="feature_view_name"][0]
        self.event_timestamp = [item["field_value"] for item in self.model_config if item['field_id']=="event_timestamp"][0]
        self.entity_columns = [item["field_value"] for item in self.model_config if item['field_id']=="entity_columns"][0]
        self.dataset_name = [item["field_value"] for item in self.model_config if item['field_id']=="dataset_name"][0]
        for item in self.model_config:
            if item["field_id"] == "connection_name" :
                self.connection_name = item['field_value']

    def load_data(self) -> DataFrame:
        store = self.get_feature_store(self.fs_name)
        try:
            source_dataset = self.get_source_dataframe()
            event_time_stamps = self.get_event_timestamps(self.event_timestamp,source_dataset)

            print("event_time_stamps :::: \n",event_time_stamps)
            entity_ids = self.get_entity_ids(self.entity_columns,source_dataset)

            print("entity_ids :::::: \n",entity_ids)

            entity_df = pd.DataFrame.from_dict(
                {
                    "entity_id": entity_ids,
                    self.event_timestamp : [event_time_stamps[0] for i in range(len(entity_ids))]
                }
            )

            print("Entity DataFrame is : \n",entity_df)

            data_frame_obj = store.get_historical_features(self.fs_view,entity_df )

            print("DataFrame Obj :::::: \n",data_frame_obj)

            data_frame = data_frame_obj.to_df()

            print(data_frame)

            return data_frame

        except Exception as msg:
            print("Error while loading the data from Feature store.")
            raise Exception(msg)
    
    def get_event_timestamps(self,event_timestamp,source_dataset):
        return source_dataset[event_timestamp].unique().tolist()

    def get_entity_ids(self,entity_columns,source_dataset):
        entity_ids = []
        for column_name in entity_columns:
            temp_ids = source_dataset[column_name].unique().tolist()
            entity_ids.extend(temp_ids)
        return entity_ids

    def get_source_dataframe(self):
        dataset = None
        from refractio.refractio import get_local_dataframe
        project_id = os.getenv("PROJECT_ID")
        print(f"Reading refract local dataset {self.dataset_name} using,\n"
                f"project_id: {project_id}\n")
        dataset = get_local_dataframe("/data/OLIST_ORDERS.csv")

        # try:
        #     project_id = os.getenv("PROJECT_ID")
        #     print(f"Reading refract dataset {self.dataset_name} using,\n"
        #             f"project_id: {project_id}\n"
        #             f"filter_condition: {os.getenv('filter_condition')}")
        #     dataset = get_dataframe(self.dataset_name,
        #                             project_id=project_id
        #                             )
        # except Exception as msg:
        #     print(msg)
        #     print("Not able to get dataset with published dataset info")

        # if dataset is None:
        #     try:
        #         from refractio import snowflake
        #         if not self.connection_name :
        #             snowflake.get_connection()
        #         else:
        #             snowflake.get_connection(connection_name=self.connection_name)

        #         # To read a specific dataset published from a snowflake connection
        #         dataset = snowflake.get_dataframe(self.dataset_name)

        #     except Exception as msg:
        #         print(msg)
        #         print("Not able to get dataset with connecation name ")

        # elif dataset is None:
        #     from refractio.refractio import get_local_dataframe
        #     project_id = os.getenv("PROJECT_ID")
        #     print(f"Reading refract local dataset {self.dataset_name} using,\n"
        #             f"project_id: {project_id}\n")
        #     dataset = get_local_dataframe("/data/OLIST_ORDERS.csv")
        return dataset
        
    def get_feature_store(self,feature_store_name):
            
        headers = {
            "accept": "application/json",
            "X-Project-Id": os.getenv("PROJECT_ID"),
            'X-Auth-Userid': os.getenv("userId"),
            'X-Auth-Username': os.getenv("userId"),
            'X-Auth-Email': os.getenv("userId"),
        }


        print(headers)
        url = "http://refract-common-service:5000/refract/common/api" + "/v1/get_feature_store?feature_store_name={}".format(feature_store_name)

        response = requests.get(url=url,
                                headers=headers,
                                verify=False)

        print("store_obj - ", response)
        temp_dir = tempfile.mkdtemp()

        yaml_path = os.path.join(temp_dir, "feature_store.yaml")

        if response.status_code == 200:
            # Parse the JSON response
            with open(yaml_path, 'wb') as f:
                f.write(response.content)

        store = FeatureStore(repo_path=temp_dir)

        return store
