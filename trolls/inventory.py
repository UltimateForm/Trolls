import troll
import item
import dbinterface
import game


class Inventory(list):
    WORLDBAG: "Inventory" = None

    def __init__(self, owner: "troll.Troll" = None, *args):
        super().__init__()
        self._owner = owner
        self._equipped_weapon = None
        self._equipped_armor = None
        print(str(len(args)) + " inv")
        for i in args:
            self.store(i)

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

    def get_item_by_id(self, item_id: int):
        for i in self:
            if i.id == item_id:
                return i
        return None

    def get_item_by_name(self, item_name: str):
        for i in self:
            if i.name == item_name:
                return i
        return None

    def equip_armor(self, i: "item.Armor"):
        if not item.ItemTypes.is_armor(i.item_type):
            print(f"{i.name} Provided type {i.item_type.name} is not desired type {item.ItemTypes.ARMOR.name}")
            return
        if self.get_item_by_id(i.id) is None:
            self.store(i)
        self._equipped_armor = i
        print("Equipped armor " + i.name)

    def equip_weapon(self, i: "item.Weapon"):
        if not item.ItemTypes.is_weapon(i.item_type):
            print(f"{i.name} Provided type {i.item_type.name} is not desired type {item.ItemTypes.WEAPON.name}")
            return
        if self.get_item_by_id(i.id) is None:
            self.store(i)
        self._equipped_weapon = i
        print("Equipped weapon " + i.name)

    @classmethod
    def populate_world(cls):
        dbitems = dbinterface.get_items()
        cls.WORLDBAG = Inventory(None, *dbitems)

if __name__ == "__main__":
    items = dbinterface.get_items()
    bag = Inventory()
    for ii in items:
        bag.store(ii)
    weap = bag.get_item_by_id(15)
    bag.equip_weapon(weap)
    print(weap)
    #game.Game.weapon_info(bag.get_item_by_id(6))
