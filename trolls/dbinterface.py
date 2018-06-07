import sqlite3
import os
import item
import troll
import damage


db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\trollsdata\\items.db"


def get_items():
    connection = sqlite3.connect(db_path)
    items = []
    for i in connection.execute('SELECT * FROM Item'):
        name = i[1]
        type_id = i[2]
        i_type = item.ItemTypes(connection.execute('SELECT * FROM ItemType WHERE Id = ?', str(type_id)).fetchone()[2])
        level = i[3]
        mods_id = i[4]
        mods_row = connection.execute('SELECT * FROM Mods WHERE Id = "%s"' % str(mods_id)).fetchone()
        mods = troll.Mods(mods_row[2], mods_row[3], mods_row[4], mods_row[5], mods_row[6], mods_row[7])
        armor = i[5]
        block_chance = i[6]
        dmg = i[7]

        pri_dmg_type_id = i[8]
        pri_dmg_row = connection.execute('SELECT * FROM DamageTypes WHERE Id = ?', (str(pri_dmg_type_id),)).fetchone()\
            if pri_dmg_type_id is not None else None
        pri_dmg_type = damage.Damage(pri_dmg_row[2]) if pri_dmg_row is not None else None

        sec_dmg_type_id = i[9]
        sec_dmg_row = connection.execute('SELECT * FROM DamageTypes WHERE Id = ?', (str(sec_dmg_type_id),)).fetchone()\
            if sec_dmg_type_id is not None else None
        sec_dmg_type = damage.Damage(sec_dmg_row[2]) if sec_dmg_row is not None else None

        ter_dmg_type_id = i[10]
        ter_dmg_row = connection.execute('SELECT * FROM DamageTypes WHERE Id = ?', (str(ter_dmg_type_id),)).fetchone()\
            if ter_dmg_type_id is not None else None
        ter_dmg_type = damage.Damage(ter_dmg_row[2]) if ter_dmg_row is not None else None
        fire_resis = i[11]
        cold_resis = i[12]
        elect_resis = i[13]
        weight = i[14]
        it = item.Item(name, i_type, level, mods, armor=armor,block_chance=block_chance,damage=dmg,
                       primary_damage_type=pri_dmg_type,secondary_damage_type=sec_dmg_type,
                       tertiary_damage_type=ter_dmg_type, fire_resistance=fire_resis, cold_resistance=cold_resis,
                       electric_resistance=elect_resis, weight=weight)
        it.id = i[0]
        items.append(it)
    connection.close()
    return items


if __name__ == "__main__":
    get_items()