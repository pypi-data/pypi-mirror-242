import sys
import os
import json
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from logger_local.Logger import Logger
from .constants_url_profile_local import UrlProfileLocalConstants

load_dotenv()
logger = Logger.create_logger(
    object= UrlProfileLocalConstants.OBJECT_FOR_LOGGER_CODE)

class url:
    def __init__(self, url_id, profile_id):
        self.profile_id = profile_id
        self.url_id = url_id

    def __dict__(self):
        return {
            'profile_id': self.profile_id,
            'url_id': self.url_id    
        }


class UrlProfilesLocal(GenericCRUD):
    
    def __init__(self):
        INIT_METHOD_NAME = '__init__'
        
        logger.start(INIT_METHOD_NAME)
        super().__init__(schema_name="profile_url",default_table_name='profile_url_table',default_id_column_name='url')

        logger.end(INIT_METHOD_NAME)


    def insert(self,url_id: str,url_type_id: int,profile_id: int):
        INSERT_URL_PROFILE_METHOD_NAME = 'insert_url_profile'
        logger.start(INSERT_URL_PROFILE_METHOD_NAME,
                     object={"url_id": url_id})
        data = {'profile_id': profile_id,
                'url_type_id':url_type_id,
                'url':url_id}
        GenericCRUD.insert(self,table_name="profile_url_table",data_json=data)
        logger.end(INSERT_URL_PROFILE_METHOD_NAME)


    def update(self,url_id: str,url_type_id: int,profile_id: int):

        UPDATE_URL_PROFILE_METHOD_NAME = 'update_url_profile'
        logger.start(UPDATE_URL_PROFILE_METHOD_NAME,
                     object={"url_id": url_id})
        data = {'profile_id': profile_id,
                'url_type_id':url_type_id,
                'url':url_id}
        GenericCRUD.update_by_id(self, data_json=data,id_column_name='profile_id',id_column_value=profile_id,order_by='start_timestamp desc')
        logger.end(UPDATE_URL_PROFILE_METHOD_NAME)
    
    def delete_url(self,profile_id: int):
        DELETE_URL_PROFILE_METHOD_NAME = 'delete_url_profile' 
        logger.start(DELETE_URL_PROFILE_METHOD_NAME,
                     object={"profile_id": profile_id})
        GenericCRUD.delete_by_id(self,id_column_name='profile_id',id_column_value=profile_id)
        logger.end(DELETE_URL_PROFILE_METHOD_NAME)    
    
    def get_last_url_id_by_profile_id(self,profile_id: int) -> url:
        GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_url_id_by_profile_id"
        logger.start(GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        url_id = GenericCRUD.select_multi_tuple_by_where(self, view_table_name="profile_url_view", select_clause_value="url",
                                                             where=f"profile_id = {profile_id}", limit=1, order_by="start_timestamp desc")
        logger.end(GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME,
                   object={'url_id': url_id})
        if not url_id:
            return None
        return url_id[0] [0]  

    
        
