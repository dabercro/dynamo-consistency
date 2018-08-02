from common.inventory import InventoryManager
from common.dataformat import File
from common.dataformat import Dataset
from common.interface.mysql import MySQL

class InvLoader(object):
    """
    Creates an InventoryManager object, if needed,
    and stores it globally for the module.
    It also holds a list of datasets in the deletion queue.
    """
    def __init__(self):
        """Initializer for the object"""
        self.inv = None
        self.deletions = None

    def get_inventory(self):
        """
        Make an inventory, if needed, and return it.

        :returns: Any InventoryManager in the vicinity.
        :rtype: common.inventory.InventoryManager
        """
        if self.inv is None:
            self.inv = InventoryManager()

        return self.inv


INV = InvLoader()

