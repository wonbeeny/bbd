# coding : utf-8
# author : WONBEEN

from .base import (
    Attrs, 
    mk_Output
)
from .utils import (
    read_json,
    get_logger
)
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
        self.user_id = kwargs["user_id"] if "user_id" in kwargs else None
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

    def run(self, user_json):        
        if self.task == "record":
            preprocessor = self.preprocessor(self.user_id, self.user_text)
            PreOutput = preprocessor()
        else:
            pass    # 다른 task 들어오면 상황 봐서 추가할수도 있음
        
        try:
            if PreOutput.trial:                
                PostProcessor = self.postprocessor(PreOutput.trial, PreOutput.errors)
                PostOutput = PostProcessor(user_json, self.user_id, PreOutput.outputs)
                
                if PostOutput.trial:
                    return mk_Output(self.user_id, True)
                else:
                    logType = f"An error occurred in the PostProcessor class in {self.task}."
                    logger.error(logType)
                    return mk_Output(self.user_id, False, logType, PostOutput.errors)
            else:
                logType = f"An error occurred in the PreProcessor class in {self.task}."
                logger.error(logType)
                return mk_Output(self.user_id, False, logType, PreOutput.errors)
        except:
            logType = f"Invalid PostProcessor class in {self.task}."
            logger.error(logType)
            return mk_Output(self.user_id, False, logType, PreOutput.errors)