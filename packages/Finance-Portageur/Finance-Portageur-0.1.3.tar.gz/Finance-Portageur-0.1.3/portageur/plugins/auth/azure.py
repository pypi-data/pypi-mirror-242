import yaml, copy, six, pdb, os
from dataclasses import dataclass
#from seleya import *
#from seleya.Toolset import blob_service
from portageur.kdutils.singleton import Singleton
from portageur.plugins.auth.base import BaseAuth, ModelManager, ChatModelManager
from portageur.plugins.models.chat_models import AzureChatOpenAI as AzureChatOpenAIImpl
from portageur.plugins.models.embeddings import OpenAIEmbeddings as OpenAIEmbeddingsImpl


@dataclass
class AzureOpenAIAuth(BaseAuth):
    auth_index: int = 0
    api_key: str = ''
    api_base: str = ''
    api_version: str = ''
    api_type: str = ''


@six.add_metaclass(Singleton)
class AzureOpenAIManager(ModelManager):
    name = 'azureai'

    def __init__(self, config_path):
        self.auth_config(config_path=config_path)

    def auth_config(self, config_path):
        if not os.path.exists(config_path):
            '''
            SeleyaAPI.login(username=os.environ['seleya_username'],
                            password=os.environ['seleya_password'])
            blob_service.BlobService().download_file(
                container_name='data',
                remote_file_name=os.path.join("molecule", "config.yml"),
                local_file_name=config_path)
            '''
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        openai_config = config.get('azureopenai', {})
        self.auths = super(AzureOpenAIManager,
                           self).auth_config(openai_config, AzureOpenAIAuth)

model_manager = AzureOpenAIManager(config_path=os.environ['USER_FILE'])

class AzureOpenAI(object):
    def __init__(self, ai_class, **kwargs):
        self.kwargs = copy.deepcopy(kwargs)
        self.ai_class = ai_class

    def instance(self):
        auth = model_manager.idle_auth()
        with auth:
            model = self.ai_class(openai_api_key=auth.api_key,
                                        openai_api_base=auth.api_base,
                                        openai_api_version=auth.api_version,
                                        openai_api_type=auth.api_type,
                                        **self.kwargs)
        return model.impl

    def predict(self, messages):
        auth = model_manager.idle_auth()
        with auth:
            model = self.ai_class(openai_api_key=auth.api_key,
                                        openai_api_base=auth.api_base,
                                        openai_api_version=auth.api_version,
                                        openai_api_type=auth.api_type,
                                        **self.kwargs)
            results = model.predict(messages=messages)
        return results

    async def apredict(self, messages):
        auth = model_manager.idle_auth()
        with auth:
            model = self.ai_class(openai_api_key=auth.api_key,
                                        openai_api_base=auth.api_base,
                                        openai_api_version=auth.api_version,
                                        openai_api_type=auth.api_type,
                                        **self.kwargs)
            results = await model.apredict(messages=messages)
        return results

class AzureChatOpenAI(AzureOpenAI):

    def __init__(self, **kwargs):
        super(AzureChatOpenAI,self).__init__(AzureChatOpenAIImpl, **kwargs)

class OpenAIEmbeddings(AzureOpenAI):

    def __init__(self, **kwargs):
        super(OpenAIEmbeddings,self).__init__(OpenAIEmbeddingsImpl, **kwargs)