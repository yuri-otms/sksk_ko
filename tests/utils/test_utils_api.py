import sksk_app.utils.api as api

def test_ja_to_ko(app):
    japanese = '母は公務員です。'
    with app.app_context():
        ja_to_ko = api.Papago.ja_to_ko(japanese)

    assert ja_to_ko == '어머니는 공무원입니다.'

def test_ko_to_ja(app):
    foreign_l = '어머니는 공무원입니다.'
    with app.app_context():
        ko_to_ja = api.Papago.ko_to_ja(foreign_l)
    
    assert ko_to_ja == '母は公務員です。'