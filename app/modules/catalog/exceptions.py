class CatalogError(Exception):
    """Базовая ошибка каталога."""


class NotFoundError(CatalogError):
    """Сущность не найдена."""


class ValidationError(CatalogError):
    """Бизнес-правило нарушено."""
