from syamaguc.syamaguc import Syamaguc


class TestSyamaguc:
    def test_name(self):
        assert Syamaguc().name == "syamaguc"

    def test_introduce(self):
        assert Syamaguc().introduce() == "My name is syamaguc"
