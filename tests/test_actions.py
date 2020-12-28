from app.devices.actions import Action
from unittest import TestCase

import pytest


class Test_Action_Unit(TestCase):

    def test_init1(self):
        action = Action()
        self.assertIsNotNone(action)
        self.assertIsNone(action.func)
        self.assertIsNotNone(action.logger)  # superclass attribute

    def test_init2(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)
        self.assertIsNotNone(action.logger)  # superclass attribute

    def test_init3(self):
        with pytest.raises(ValueError):
            # no function, but parameters passed
            action = Action(parameters={'some-key': 'some-value'})

    def test_init4(self):
        def job(*args: int):
            return args[0] + 1

        action = Action(job, 9)
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)

    def test_init5(self):
        def job(**kwargs):
            value = kwargs.get('value')
            return value + '-passed'

        action = Action(job, 9)
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)


class Test_Action_Integration(TestCase):

    def test_call_action_returns_result1(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        value = action()
        self.assertEqual(value, 'fnct-passed-test')

    def test_call_action_returns_result_args(self):
        def job(*args):
            return {'key': args[0]}

        action = Action(job, 42)
        value = action()
        self.assertEqual(value['key'], 42)

    def test_call_action_returns_result_kwargs(self):
        def job(**kwargs):
            value = kwargs.get('value')
            return value + '-passed'

        action = Action(job, value='test')
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)

        value = action()
        self.assertEqual(value, 'test-passed')

    def test_call_action_no_return1(self):
        def job():
            print('test')
            pass

        action = Action(job)
        value = action()
        self.assertIsNone(value)

    def test_call_action_no_return2(self):
        action = Action()
        with pytest.raises(TypeError):
            # action w/o job called
            action()
