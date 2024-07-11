# coding : utf-8
# author : WONBEEN

from .base import Attrs
from .utils import read_json, get_logger
from .register import (
    record2sheet
)

logger = get_logger(__name__)

TASK_MAP = {
    "record": record2sheet
} # task와 모듈을 매핑

class worker(Attrs):
    def __init__(self, task, **kwargs):
        """
        고객의 정보와 고객이 요청한 정보를 정의
        Args:
            task (:obj: `str`):
                고객이 요청한 task
        """
        task_module = self._get_task_module(task)
        self.task = task
        self.user_text = kwargs["user_text"] if "user_text" in kwargs else None
        self.set(task_module)

    def _get_task_module(self, task):
        """
        고객이 선택한 task에 맞는 모듈 선택
        """
        if task in TASK_MAP:
            return TASK_MAP[task]
        else:
            raise NotImplementedError(f"`{task}` task hasn't been developed yet.")

    def set(self, module):
        """
        task에 맞게 환경을 설정. task module에서 필수적인 attribute가 개발되었다면 해당 클래스의 object를 선언.
        task에서 특정 class가 개발되지 않았다면 에러 발생.
            - module.PreProcessor
            - module.PostProcessor
        """
        self.preprocessor = module.PreProcessor
        self.postprocessor = module.PostProcessor

    def run(self, json_key_path, sheet_url):        
        preprocessor = self.preprocessor(self.user_text, self.task)
        PreOutput = preprocessor()
        logger.info("Success PreProcessor.")
                  
        try:
            PostProcessor = self.postprocessor(json_key_path, sheet_url)
            PostOutput = PostProcessor(PreOutput.outputs)
            logger.info("Success PostProcessor.")
        except Exception as e:
            message = f"Invalid PostProcessor class in {self.task}."
            logger.error(message)
            raise e
            
        return PostOutput