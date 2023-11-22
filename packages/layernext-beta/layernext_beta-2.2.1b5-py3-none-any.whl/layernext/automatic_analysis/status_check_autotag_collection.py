import requests
import time
import threading
from urllib.parse import quote_plus
from tqdm import tqdm

"""
Status reporting of collection auto tagging through getting constant updates from DB collection until the request is timied out.
"""
insufficient_load = False
"""
Sending the main request to invokde flask app endpoint and start autotagging on the server side. 
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param payload:payload of the request sent
@param headers: headers of the reqeust sent
""" 
def send_request(url, payload, headers):
    try:
        global insufficient_load
        insufficient_load = False
        response = requests.post(url=f"{url}/dataIn", json=payload, headers=headers, timeout=30)
        if response.json()['LOAD'] == 'insufficient':
            insufficient_load = True
            print(response.json())
    except requests.exceptions.Timeout:
        #print("The request timed out")
        pass
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

"""
Sending and receving the get status reqeust periodically to return the current status reagarding the autotagging process happening 
and reporting status to the SDK terminal
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param unique_id: a unique id generated to identify which autotagging process to refer. 
@param headers: headers of the reqeust sent
"""         
def get_status(url,unique_id,task,headers):
    flag, print_status_flag, initialize_progress_bar, progress_bar_end ,inference_flag, initialize_upload_progress_bar, start_upload, initialize_progress_bar_download = True, True, True, False, True, True, False,True
    status_message = "Started Autotagging"
    dot_count = 0
    state_start_end_flags=[[True,True],[True,True],[True,True],[True,True]]
    while flag:
        payload = {
        "unique_id":unique_id,
        "Task" : task
        }
        response = requests.post(f'{url}/get_status',json=payload,headers=headers)
        document = response.json()['status']
        #print(document)
        global insufficient_load
        if insufficient_load:
            flag = False
            print_status_flag = False
        new_status_message = status_message
        if document=='NotFound':
            new_status_message = status_message
        else:
            if state_start_end_flags[3][0]:
                print("Started Creating Inference EndPoint")
                state_start_end_flags[3][0]=False 
            if len(document['model_name_registered'])==1:
                print("Error occured while creating the inference endpoint")
                print(document['model_name_registered'][0])
                print_status_flag = False
                flag=False
            if len(document['collection_name_registered'])==1:
                print("Error occured while trying to find layernext collectiion details")
                print(document['collection_name_registered'][0])
                print_status_flag = False
                flag=False
            if len(document['end_point_initialization'])==1:
                new_status_message="Inference EndPoint Creating.. Stay Tuned"    
            if len(document['end_point_initialization'])==2:
                if document['end_point_initialization'][1]=='Ended':
                    if state_start_end_flags[3][1]:
                        print("Inference EndPoint Created!!!")
                        state_start_end_flags[3][1]=False
                    if state_start_end_flags[0][0]:
                        print("Started Auto Tagging the Collection")
                        no_of_pages=document['number_of_pages']
                        page_size = document['page_size']
                        total_files = document['number_of_files']
                        print(f"Total Number of Files in the Collection : {total_files}")
                        print_status_flag = False
                        state_start_end_flags[0][0]=False 
                    new_status_message="Downloading the Collection"
                    if initialize_progress_bar_download:                            
                        constraint = document['number_of_files']
                        pbar_download = tqdm(total=constraint, desc="Collection Auto tagging in Progress : ", ncols=100, unit="item") 
                        initialize_progress_bar_download = False
                    if len(document['downloaded_pages'])>0:
                        if len(document['downloaded_pages'])<no_of_pages:     
                            pages = len(document['downloaded_pages'])
                            second_len = page_size*pages
                            difference=second_len - pbar_download.n
                            pbar_download.update(difference)
                        else:
                            second_len = len(document['downloaded_pages'])
                            difference=constraint - pbar_download.n
                            pbar_download.update(difference)
                            pbar_download.close()
                            print("Successfully Completed the Process \u2714 \u2714 \u2714")
                            flag=False
                else:
                    print("Error occured while creating the inference endpoint")
                    print(document['end_point_initialization'][1])
                    print_status_flag = False
                    flag=False
            if len(document['metadata_upload'])==1:
                print("Error occured while trying to upload metadata tags for collection")
                print(document['metadata_upload'][0])
                #pbar_upload.close()
                print_status_flag = False
                flag=False
            if len(document['predictor_invoke'])==1:
                print("Error occured while invoking inference endpoint")
                print(document['predictor_invoke'][0])
                #pbar.close()
                print_status_flag = False
                flag=False

        if new_status_message != status_message:
            status_message = new_status_message
            dot_count = 0
        dots = '.' * (dot_count % 4) 
        padded_message = f'{status_message} {dots}'.ljust(100)
        if print_status_flag:
            print(f'{padded_message}', end='\r', flush=True)
            
        dot_count += 1

        time.sleep(1)
"""
combining about two processes as two threads to run them parallely
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param payload:payload of the request sent
@param headers: headers of the reqeust sent
@param unique_id: a unique id generated to identify which autotagging process to refer. 
"""  
def main_collection(url,payload,headers,unique_id,task): 
    request_thread = threading.Thread(target=send_request, args=(url, payload, headers))
    status_thread = threading.Thread(target=get_status, args=(url,unique_id,task,headers))
    request_thread.start()
    status_thread.start()

    request_thread.join()
    #print("request thread finished")
    status_thread.join()
    #print("status thread finished")