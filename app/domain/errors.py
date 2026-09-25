class DomainError(Exception):
    pass

class ValidationError(DomainError):
    pass

class DuplicateAssignmentError(DomainError):
    """Se lanza cuando intentas asignar el mismo técnico que ya tiene el ticket"""
    pass
