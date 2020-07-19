from unittest.mock import patch
import commands
import unittest


class TestCommands(unittest.TestCase):
    @patch('commands.discord', auto_spec=True)
    def test_show_help_will_return_discord_embed_string_with_help_message(self, discord):
        discord.Embed.side_effect = lambda description: description
        output = commands.show_help()

        self.assertEqual(commands.HELP_MESSAGE, output)

    def test_roll_will_return_empty_string_when_given_empty_list(self):
        inputs = []

        output = commands.roll(inputs)

        self.assertEqual("", output)

    @patch('commands.randint', auto_spec=True)
    def test_roll_will_return_random_item_in_inputs_when_inputs_are_strings(self, randint):
        inputs = ['Alice', 'Bob', 'Charlie']
        expected_index = 2
        randint.return_value = expected_index

        output = commands.roll(inputs)

        self.assertEqual(inputs[expected_index], output)

    @patch('commands.randint', auto_spec=True)
    def test_roll_will_return_random_number_in_input_when_input_is_number(self, randint):
        inputs = ['5']
        expected_value = 3
        randint.return_value = expected_value

        output = commands.roll(inputs)

        self.assertEqual(str(expected_value), output)

    @patch('commands.randint', auto_spec=True)
    def test_roll_will_return_sum_of_random_numbers_in_inputs_when_input_is_dnd_style_dice_roll(self, randint):
        num_die = 2
        num_side = 20
        inputs = [f'{num_die}d{num_side}']
        first, second = 10, 17
        randint.side_effect = [first, second]

        output = commands.roll(inputs)

        self.assertEqual(f'({first}) + ({second}) = {first + second}', output)

    def test_roll_will_return_input_when_input_is_numerically_unparsable(self):
        unparsable_string = 'something'
        inputs = [unparsable_string]

        output = commands.roll(inputs)

        self.assertEqual(unparsable_string, output)

    def test_roll_will_return_input_when_dnd_style_dice_roll_contains_negative_number_of_dice(self):
        inputs = ['-1d10']

        output = commands.roll(inputs)

        self.assertEqual(inputs[0], output)

    def test_roll_will_return_input_when_dnd_style_dice_roll_contains_negative_number_of_sides(self):
        inputs = ['1d-10']

        output = commands.roll(inputs)

        self.assertEqual(inputs[0], output)
