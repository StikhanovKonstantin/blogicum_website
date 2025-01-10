from http import HTTPStatus

from enum import Enum


class Statuses(Enum):
    """enum - хранит статусы ошибок, используется во view-кастомных ошибок."""

    ERROR_404 = HTTPStatus.NOT_FOUND
    ERROR_403 = HTTPStatus.FORBIDDEN
    ERROR_500 = HTTPStatus.INTERNAL_SERVER_ERROR
