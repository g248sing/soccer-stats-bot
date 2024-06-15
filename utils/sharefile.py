import os
from io import BytesIO
import pathlib
from typing import BinaryIO, Union
from pathlib import Path

from azure.storage.fileshare import (
    ShareClient, 
    ShareDirectoryClient,
    ShareFileClient, 
)

from utils.singleton import Singleton


class DirClientWrapper:    
    def __init__(self, path: str, client: ShareDirectoryClient=None) -> None:
        """
        Need azure client or local path of dir.
        """
        # check if the client is valid
        self.client = client
        self.path = path
        if isinstance(client, ShareDirectoryClient):
            return
        self.client = None
        # chekc if none of the args is valid
        if self.path is None:
            raise ValueError("No valid client or local path of dir passed")
        
        self.path = Path(path)
    
    def list_dir(self):
        """
        list files and sub-dirs in the directory
        """
        if self.client is None:
            return os.listdir(self.path)
        
        print(f'Getting subdirs for dir: {self.path}')
        # [Azure function start]
        return list(self.client.list_directories_and_files())
        # [Azure function end]
    

class FileClientWrapper:
    def __init__(self, path: str, client: ShareFileClient=None) -> None:
        """
        Need azure client or local path of the file.
        """
        # check if the client is valid
        self.client = client
        self.path = path
        if isinstance(client, ShareFileClient):
            return
        self.client = None
        # check if none of the args is valid
        if self.path is None:
            raise ValueError("No valid client or local path of dir passed")
        
        self.path = Path(path)
        
    def read(self) -> BinaryIO:
        if self.client is None:
            return open(self.path, 'rb')

        print(f'Getting file...{self.path}')
        # [Azure function start]
        return BytesIO(self.client.download_file().readall())
        # [Azure function end]

    def write(self, buff: BytesIO):
        if self.client is None:
            with open(self.path, 'wb') as f:
                f.write(buff)
            return
        # [Azure function start]
        self.client.upload_file(buff)
        # [Azure function end]



class _ShareFile(metaclass=Singleton):
    LOCAL = "LOCAL" in os.environ
    
    def __init__(self) -> None:
        self.client = None
        if not self.LOCAL:
            # [Azure function start]
            self.CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            self.SHARE_NAME = os.getenv('AZURE_STORAGE_SHARE_NAME')
            self.client = ShareClient.from_connection_string(self.CONNECTION_STRING, self.SHARE_NAME)
            # [Azure function end]

    def download_static(self, path: Union[str, Path]) -> BytesIO:
        """
        Make sure that the static file is availaible locally.
        Call this everytime accessing a local file if it wasn't
        present in the deployment to heroku as heroku might have
        removed them.
        """
        if not isinstance(path, Path):
            path = Path(path)
        # if not already exists
        if not path.exists():
            try:
                # [Azure function start]
                fc = self.client.get_file_client(str(path))
                dir_path = os.path.dirname(path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(path, 'wb') as fh:
                    stream = fc.download_file()
                    fh.write(stream.readall())
                # [Azure function end]
            except Exception as e:
                # TODO: log
                ...
        return open(path, 'rb')

    def get_file_client(self, path) -> FileClientWrapper:
        if self.LOCAL or Path(path).exists():
            return FileClientWrapper(path=path)
        if not isinstance(path, str):
            path = str(path)
        # [Azure function start]
        return FileClientWrapper(path=path, client=self.client.get_file_client(path))
        # [Azure function end]

    def upload_file(self, path, object: BytesIO):
        pass

    def delete_file(self):
        raise NotImplementedError("No")

    def get_dir_client(self, path) -> DirClientWrapper:
        if self.LOCAL or Path(path).exists():
            return DirClientWrapper(path=path)
        if not isinstance(path, str):
            path = str(path)
        # [Azure function start]
        return DirClientWrapper(path=path, client=self.client.get_directory_client(path))
        # [Azure function end]

    def delete_dir(self):
        raise NotImplementedError("No")

ShareFile = _ShareFile()
