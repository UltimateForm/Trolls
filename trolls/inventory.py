import troll
import item
import dbinterface
import game


class Inventory(list):
    def __init__(self, owner: "troll.Troll" = None, *args):
        super().__init__(*args)
        self._owner = owner
        self._equipped_weapon = None
        self._equipped_armor = None

    @property
    def owner(self):
        return self._owner

    @property
    def equipped_weapon(self):
        return self._equipped_weapon

    @property
    def equipped_armor(self):
        return self._equipped_armor

    def store(self, i: "item.Item"):
        existing_item = self.get_item_by_id(i.id)
        if existing_item is not None:
            existing_item.amount += 1
        else:
            self.append(i)

    def get_item_by_id(self, item_id: int) -> item.Item:
        for i in self:
            if i.id == item_id:
                return i
        return None

    def get_item_by_name(self, item_name: str) -> item.Item:
        for i in self:
            if i.name == item_name:
                return i
        return None

    def equip_armor(self, i: "item.Item"):
        if self.get_item_by_id(i.id) is None:
            self.store(i)
        self._equipped_armor = i

    def equip_weapon(self, i: "item.Item"):
        if self.get_item_by_id(i.id) is None:
            self.store(i)
        self._equipped_weapon = i

if __name__ == "__main__":
    items = dbinterface.get_items()
    bag = Inventory()
    for ii in items:
        bag.store(ii)
    game.Game.weapon_info(bag.get_item_by_id(6))

