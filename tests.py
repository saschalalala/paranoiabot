from django.test import TestCase

# Create your tests here.

from .models import Player


class PlayerTestCase(TestCase):
    def setUp(self):
        from .models import Clearance
        Player.objects.create(telegram_id="132456",
                              name="foo",
                              gm=False,
                              clearance=Clearance(1),
                              home_sector="AC",
                              clone_number=1,
                              custom_player_name="Hans",
                              pp=25)
        Player.objects.create(telegram_id="132456",
                              name="bar",
                              gm=False,
                              clearance=Clearance(1),
                              home_sector="AC",
                              clone_number=1,
                              custom_player_name="",
                              pp=25)

    def test_player_name(self):
        """ Names are created correctly """
        with_custom_name = Player.objects.get(name="foo")
        without_custom_name = Player.objects.get(name="bar")
        asserted_name = "{0.name}-{0.clearance}-{0.home_sector}-{0.clone_number}".format(without_custom_name)
        self.assertEqual(with_custom_name.get_player_name(), with_custom_name.custom_player_name)
        self.assertEqual(without_custom_name.get_player_name(), asserted_name)
        with_custom_name.set_custom_player_name("bar")
        self.assertEqual(with_custom_name.get_player_name(), 'bar')

    def test_operations(self):
        """ Test various operations """
        from .models import Clearance
        test_player = Player.objects.get(name="bar")
        clearance_before_test = test_player.clearance
        clones_before_test = test_player.clone_number
        pp_before_test = test_player.pp
        pp_to_be_added = 1000
        pp_to_be_taken = 500

        test_player.increment_clearance()
        self.assertEqual(test_player.clearance, Clearance(clearance_before_test.value + 1))
        test_player.decrement_clearance()
        self.assertEqual(test_player.clearance, clearance_before_test)

        test_player.increment_clone()
        self.assertEqual(test_player.clone_number, clones_before_test + 1)
        test_player.decrement_clone()
        self.assertEqual(test_player.clone_number, clones_before_test)

        test_player.add_pp(pp_to_be_added)
        self.assertEqual(test_player.pp, pp_before_test + pp_to_be_added)
        test_player.remove_pp(pp_to_be_taken)
        self.assertEqual(test_player.pp, pp_before_test + pp_to_be_added - pp_to_be_taken)
