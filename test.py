"""Unit tests for the Discord bot, tested via pytest"""
import commands

### command.py tests

class TestShowHelp():
    def test_nonempty(self):
        assert commands.ALL_COMMANDS['help']()

class TestRoll():
    class TestList():
        def test_space(self):
            assert commands.roll([' ']) == ' '

        def test_one(self):
            res = set()
            for _ in range(10):
                res.add(commands.roll(['Alice']))

            assert len(res) == 1
            assert res.pop() == 'Alice'

        def test_equal(self):
            # aggregate and count up how many of each occurs
            aggr = {'Alice': 0, 'Bob': 0, 'Charlie': 0}
            for _ in range(1000):
                res = commands.roll(['Alice', 'Bob', 'Charlie'])
                aggr[res] += 1

            # by law of large numbers each of the above should be 'roughly' 1/3
            # though 333 each is expected, we give leeway and expect 300 instead
            for k in aggr:
                assert aggr[k] > 300

    class TestNumbersStandard():
        def test_zero(self):
            assert commands.roll(['0']) == '0'

        def test_negative(self):
            assert commands.roll(['-5']) == '-5'

        def test_one(self):
            assert commands.roll(['1']) == '1'

        def test_dice(self):
            # aggregate and count occurances
            aggr = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
            for _ in range(2000):
                res = commands.roll(['6'])
                aggr[res] += 1
            # as in the case of test_equal above, we expect around 333
            # rolls, but give leeway and expect 300 instead
            for k in aggr:
                assert aggr[k] > 300
