from sksk_app import db
from sksk_app.models import Level, E_Group
import sksk_app.utils.edit as edit

# LevelManager
def test_add_level(app):
    level_name = "ハン検4級"
    description = "거예요, 아서, 러"
    with app.app_context():
        edit.LevelManager.add_level(level_name,description)
        level = Level.query.filter(Level.level==level_name)
    
    assert level is not None

# E_GroupManager
def test_add_e_group(app):
    level = 1
    e_group_name = "指示詞"
    description = "입나다"
    position = 1
    with app.app_context():
        edit.E_GroupManager.add_e_group(level, e_group_name, description, position)
        e_group = E_Group.query.filter(E_Group.e_group==e_group_name)

    assert e_group is not None
