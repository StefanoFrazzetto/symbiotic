from app.devices.actions import Action
from unittest import TestCase

import pytest


class Test_Action_Unit(TestCase):

    def test_instantiate1(self):
        action = Action()
        self.assertIsNotNone(action)
        self.assertIsNone(action.func)

    def test_instantiate2(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)

    def test_instantiate3(self):
        with pytest.raises(ValueError):
            # no function, but parameters passed
            action = Action(parameters={'some-key': 'some-value'})


class Test_Action_Integration(TestCase):

    def test_call_action_returns_result1(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        value = action()
        self.assertEqual(value, 'fnct-passed-test')

    def test_call_action_returns_result2(self):
        def job():
            return {'key': 42}

        action = Action(job)
        value = action()
        self.assertEqual(value['key'], 42)

    def test_call_action_does_not_return_result1(self):
        def job():
            print('test')
            pass

        action = Action(job)
        value = action()
        self.assertIsNone(value)

    def test_call_action_does_not_return_result2(self):
        action = Action()
        with pytest.raises(TypeError):
            # action w/o job called
            action()
