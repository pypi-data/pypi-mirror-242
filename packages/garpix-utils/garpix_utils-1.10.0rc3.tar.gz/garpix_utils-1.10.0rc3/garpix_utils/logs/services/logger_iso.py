from django.conf import settings
import logging

from garpix_utils.logs.enums.get_enums import ActionType, ActionLevel, ActionResult

logger = logging.getLogger(settings.ISO_LOGS_NAME)


class ActionElement:

    def __init__(self, action_id: int, action_type: ActionType, name: str, level: ActionLevel):
        self.id = action_id
        self.name = name
        self.type = action_type
        self.level = level


class LoggerIso:

    @staticmethod
    def create_log(action: ActionElement, obj, obj_address, result: ActionResult,
                   params=None, sbj=None, sbj_address=None, msg=''):

        log = f'id={action.id} | act=\"{action.name}\"'
        log += f' | sbj=\"{sbj}\"' if sbj else ''
        log += f' | sbj_addr=\"{sbj_address}\"' \
               f' | act_type=\"{action.type.value}\"' \
               f' | lvl={action.level.value} | obj={obj}' \
               f' | obj_addr=\"{obj_address}\"' \
               f' | result={result.value}'
        log += f' | change=\"{params}\"' if params else ''
        log += f' | msg=\"{msg}\"'
        return log

    @staticmethod
    def write(act: ActionElement, obj, obj_address, result: ActionResult, params=None, sbj=None, sbj_address=None, msg=""):
        log = LoggerIso.create_log(act, obj, obj_address, result, params, sbj, sbj_address, msg)
        logger.info(log)

    @staticmethod
    def write_string(string):
        logger.info(string)

    @staticmethod
    def get_client_ip(request):
        # Используется для поулчения адреса субъекта
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
