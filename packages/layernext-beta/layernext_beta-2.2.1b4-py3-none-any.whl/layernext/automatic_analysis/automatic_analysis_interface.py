import requests
import json
import traceback
from .support import generate_unique_id
from .status_check_autotag_collection import main_collection
from .status_check_autotag_population import main_population
from .status_check_autoannotate_project import main_annotation
from .status_check_embedding_collection import main_embedding
from .status_check_embedding_population import main_population_embedding
"""
Class to initiate AutomaticAnalysisClientInterface(class which handles all the API request and responses reagrding to automatic analysis) and handle functions integrated to it
"""


class AutomaticAnalysisInterface:

    def __init__(self, auth_token: str, automatic_analysis_url: str):
        self.auth_token = auth_token
        self.automatic_analysis_url = automatic_analysis_url

    def inference_model_upload(self, storage_url, bucket_name, object_key, model_id, label_list, model_name, task):

        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            "storage_url": storage_url,
            "bucket_name": bucket_name,
            "object_key": object_key,
            "model_ID": model_id,
            "model_name": model_name,
            "label_list": label_list,
            "task": task
        }
        url = f'{self.automatic_analysis_url}/model_setup'    
        
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            print(response.json())
        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with Automatic Analysis application")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
    """
    Making the payload and sending it to the given API endpoint in and handle responses in regarding to autotagging
    """

    def tagger_detail_send(self, application, collection_id, item_type, model_id, input_resolution,confidence_threshold):
        task = "auto_tagging"
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        payload = {
        "Application":application,
        "ItemType":item_type,
        "collectionId":collection_id,
        "ModelID":model_id,
        "UniqueID":unique_id,
        "InputResolution":input_resolution,
        "Confidence" : confidence_threshold,
        "Task"   : task
        }
        url = f'{self.automatic_analysis_url}'
        try:
            if application == 'collection_autotag':
                main_collection(url, payload, hed, unique_id,task)
            elif application == 'population_autotag':
                main_population(url, payload, hed, unique_id,task)
        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with Automatic Analysis application")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
    
    
    def annotater_detail_send(self,application,project_id,model_id, annotation_type, **kwargs):
        task="auto_annotation"
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        auto_annotation_op = kwargs["auto_annotation_operation"] if "auto_annotation_operation" in kwargs else "user-model"
        payload = {
        "Application":application,
        "ProjectID":project_id,
        "ModelID":model_id,
        "UniqueID":unique_id,
        "Prompt": kwargs["prompt"] if "prompt" in kwargs else [],
        "AnnotationType": annotation_type,
        "Confidence" : kwargs["confidence_threshold"] if "confidence_threshold" in kwargs else 0.5,
        "Autoannotation_op" : auto_annotation_op,
        "Labels" : kwargs["labels"] if "labels" in kwargs else {},
        "Task"   : task
        }
        url = f'{self.automatic_analysis_url}' 

        try:
            #response = requests.post(url=url, json=payload, headers=hed)
            main_annotation(url,payload,hed,unique_id,task, auto_annotation_op)
            #print(response.json())
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with Automatic Analysis application")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()

    def embedding_detail_send(self, collection_id, model_id, application,item_type, query, filters):
        task="embedding"
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        payload = {
            "collectionId": collection_id,
            "ModelID": model_id,
            "UniqueID": unique_id,
            "Task" : task,
            "Application" : application,
            "ItemType":item_type,
            "Query":query,
            "Filters":filters
        }
        url = f'{self.automatic_analysis_url}'    
        try:
            if application == 'collection_embedding':
                main_embedding(url,payload,hed,unique_id,task)
            elif application == 'population_embedding':
                main_population_embedding(url,payload,hed,unique_id,task)
            #print(response.json())
        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with Automatic Analysis application")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()

    def prompt_detail_send(self, name, shape, **kwargs):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
        "bbox": kwargs["bbox"] if "bbox" in kwargs else {},
        "clicks": kwargs["clicks"] if "clicks" in kwargs else [],
        "shape" : shape,
        "uniqueName"   : name
        }
        url = f'{self.automatic_analysis_url}' 
        try:
            response = requests.post(url=f'{url}/dataIn_prompt_infer', json=payload, headers=hed)
            # main_annotation(url,payload,hed,unique_id,task, auto_annotation_op)
            #print(response.json())
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with Automatic Analysis application")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()