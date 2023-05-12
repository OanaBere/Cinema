from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 obiect_sters: Entity):
        self.repository = repository
        self.obiect_sters = obiect_sters

    def undo(self):
        self.repository.create(self.obiect_sters)

    def redo(self):
        self.repository.delete(self.obiect_sters.id_entity)
