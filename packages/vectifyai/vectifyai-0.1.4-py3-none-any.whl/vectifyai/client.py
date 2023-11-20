import requests
import os
from urllib.parse import unquote
from typing import List, Optional, Any
import mimetypes
from typing import Optional, Dict

class Client:

    def __init__(self, api_key: str, base_url='https://test.vectify.ai'):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {'api_key': self.api_key}
        self.sources = self.list_sources()
        if self.heartbeat() == False:
            print("* Please note some services are unavailable at the moment.")


    def _request(self, method: str, endpoint: str, data: Optional[dict] = None):
        url = f"{self.base_url}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=self.headers)
        
        response.raise_for_status()  # This will raise an exception for HTTP error codes.
        return response.json()

    def file_exists(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        response = self._request("POST", "/files/exists", data)
        return response

    def heartbeat(self):
        return self._request("GET", "/heartbeat")

    def usage(self):
        return self._request("GET", "/usage")
    
    def list_models(self) -> List[str]:
        return self._request("GET", "/models")

    def list_retrieval_agents(self) -> List[str]:
        return self._request("GET", "/retrieve/agents")
    
    def list_chat_agents(self) -> List[str]:
        return self._request("GET", "/chat/agents")

    def list_sources(self) -> List[str]:
        return self._request("GET", "/sources")
    
    def list_files(self, source_name: str = 'default') -> List[str]:
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/files", data)

    def add_source(self, source_name: str, embedding_model: Optional[str] = None, metadata_fields: Optional[Dict[str, str]] = None):
        if source_name in self.sources:
            print(f"Source '{source_name}' already exists.")
            return False

        data = {
            'source_name': source_name
        }

        if embedding_model is not None:
            data['embedding_model'] = embedding_model

        if metadata_fields is not None:
            data['metadata_fields'] = metadata_fields

        response = self._request("POST", "/sources/add", data)
        if response == False:
            print(f"Failed to add source '{source_name}'.")
            return False

        print(f"Source '{source_name}' was added.")
        self.sources.append(source_name)
        return True
    
    def delete_source(self, source_name: str):
        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False
        data = {
            'source_name': source_name
        }
        response = self._request("POST", "/sources/delete", data)
        if (response == False):
            print(f"Failed to delete source '{source_name}'.")
            return False
        print(f"Source '{source_name}' was deleted.")
        self.sources.remove(source_name)
        return True
    
    def get_source_usage(self, source_name: str):
        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/sources/usage", data)


    def add_text(self, source_name: str, text: str, metadata: Optional[dict] = None):
        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False

        data = {
            'source_name': source_name,
            'text': text,
            'metadata': metadata if metadata is not None else {}
        }

        try:
            self._request("POST", "/text/add", data)
            print(f"Text provdied was uploaded to source '{source_name}'.")
            return True
        except Exception as e:
            print(f"Failed to upload text: {e}")
            return False


    def add_file(self, source_name: str, local_path: str, metadata: dict = None):

        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False
            

        file_name = os.path.basename(local_path)

        mime_type, encoding = mimetypes.guess_type(local_path)
        if mime_type is None:
            print (f"Possibly unknown file type: '{file_name}'.")
            # return False
        elif not ('text' in mime_type or 'pdf' in mime_type or 'word' in mime_type):
             print(f"Unsupported file type: '{file_name}'. Only text, PDF and Word files are supported.")
             return False
                
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        if metadata:
            data['metadata'] = metadata

        # if self._file_exists(source_name, file_name):
        #     file_name = self._request("POST", "/files/unique-name", data)
        #     data["file_name"] = file_name

        presigned_url = self._request("POST", "/files/upload-url", data)

        path_splits = presigned_url.split('/')
        last_part = path_splits[-1].split('?')[0]
        file_name = unquote(last_part)
        data['file_name'] = file_name
        
        try:
            with open(local_path, 'rb') as file:
                files = {'file': file}
                response = requests.put(presigned_url, data=file)

            if response.status_code != 200:
                print(f"Failed to upload file. HTTP Status code: {response.status_code}")
                return False

            self._request("POST", "/files/upload-sync", data)
            print(f"File '{file_name}' was uploaded to source '{source_name}'.")
            return True
        except FileNotFoundError:
            print(f"The file {local_path} does not exist.")
            return False
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return False


    def delete_file(self, source_name: str, file_name: str):

        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False

        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/delete-url", data)
        if presigned_url == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        
        response = requests.delete(presigned_url)
        if response.status_code == 204:
            self._request("POST", "/files/delete-sync", data)
            print(f"File '{file_name}' was deleted from source '{source_name}'.")
            return True
        else:
            print(f"Failed to delete file. HTTP Status code: {response.status_code}")
            return False
    

    def download_file(self, source_name: str, file_name: str, local_path: str):

        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False

        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/download-url", data)
        if presigned_url == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        
        response = requests.get(presigned_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"File '{file_name}' from source '{source_name}' was downloaded to '{local_path}'.")
            return True
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}. Reason: {response.text}")
            return False
        

    def get_file_retrieval_status(self, source_name: str, file_name: str):
        
        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False
        
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        response = self._request("POST", "/files/retrieval-status", data)
        if response == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        return response
    

    def get_file_chunks(self, source_name: str, file_name: str):
        
        if (source_name not in self.sources):
            print(f"Source '{source_name}' does not exist.")
            return False
        
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        response = self._request("POST", "/files/chunks", data)
        if response == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        return response


    def add_openai_key(self, key: str):
        data = {
            'key': key
        }
        return self._request("POST", "/openai-key", data)
    
    def remove_openai_key(self):
        data = {
            'key': None
        }
        return self._request("POST", "/openai-key", data) 

    def retrieve(self, query: str, top_k: int, sources: List[str], agent: str = None, top_m: int = None, where: dict = None) -> dict:
        data = {
            'query': query,
            'top_k': top_k,
            'sources': sources,
            'agent': agent,
            'top_m': top_m if top_m is not None else top_k,
            'where': where
        }
        return self._request("POST", "/retrieve", data)
