from unittest import TestCase

import pytest
from symbiotic.core import _scheduler
from symbiotic.devices.actions import Action, ActionScheduler


class Test_Action_Unit(TestCase):

    def test_init1(self):
        action = Action()
        self.assertIsNotNone(action)
        self.assertIsNone(action.func)

    def test_init2(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)

    def test_init3(self):
        with pytest.raises(TypeError):
            # no function, but parameters passed
            action = Action(parameters={'some-key': 'some-value'})
            self.assertIsNotNone(action)

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

    def test_call_action_no_args_returns_result(self):
        def job():
            return 'fnct-passed-test'

        action = Action(job)
        value = action()
        self.assertEqual(value, 'fnct-passed-test')

    def test_call_action_with_args_returns_result(self):
        def job(*args):
            return {'key': args[0]}

        action = Action(job, 42)
        value = action()
        self.assertEqual(value['key'], 42)

    def test_call_action_with_kwargs_returns_result(self):
        def job(**kwargs):
            value = kwargs.get('value')
            return value + '-passed'

        action = Action(job, value='test')
        self.assertIsNotNone(action)
        self.assertIsNotNone(action.func)

        value = action()
        self.assertEqual(value, 'test-passed')

    def test_call_action_no_return(self):
        def job():
            print('test')
            pass

        action = Action(job)
        value = action()
        self.assertIsNone(value)

    def test_call_action_should_raise_error(self):
        action = Action()
        with pytest.raises(AttributeError):
            # action w/o job called
            action()


class Test_ActionScheduler_Unit(TestCase):

    def test_init_no_args(self):
        scheduler = ActionScheduler()
        self.assertIsNotNone(scheduler)
        self.assertIsNone(scheduler.func)
        self.assertIsNone(scheduler.name)
        self.assertEqual(len(scheduler.kwargs), 0)
        self.assertEqual(len(scheduler.actions), 0)

    def test_init_with_name_kwargs(self):
        def somefunc(*args):
            pass

        scheduler = ActionScheduler(somefunc, name='scheduler')
        self.assertIsNotNone(scheduler)
        self.assertIsNotNone(scheduler.func)
        self.assertEqual(scheduler.name, 'scheduler')
        self.assertEqual(len(scheduler.kwargs), 0)
        self.assertEqual(len(scheduler.actions), 0)

    def test_init_with_job_kwargs(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc, someparam='value')
        self.assertIsNotNone(scheduler)
        self.assertIsNotNone(scheduler.func)
        self.assertEqual(len(scheduler.kwargs), 1)
        self.assertEqual(scheduler.kwargs, {'someparam': 'value'})
        self.assertEqual(len(scheduler.actions), 0)

    def test_add_action_with_kwargs1(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc, someparam=42)
        scheduler.add().every().day

        # check the action has been added
        self.assertEqual(len(scheduler.actions), 1)

        # ensure inner values have been set correctly
        self.assertIsNotNone(scheduler.actions[0])
        action = scheduler.actions[0]
        self.assertEqual(action.func.args, ())
        self.assertEqual(action.func.keywords, {'someparam': 42})
        self.assertIsNotNone(action.job)

        # ensure the job has not been added to the scheduler
        self.assertEqual(len(_scheduler.jobs), 0)

    def test_add_action_with_kwargs2(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc)
        scheduler.add(someparam='value').every().sunday.at('23:59')

        # check the action has been added
        self.assertEqual(len(scheduler.actions), 1)

        # ensure inner values have been set correctly
        action = scheduler.actions[0]
        self.assertEqual(action.func.args, ())
        self.assertEqual(action.func.keywords, {'someparam': 'value'})
        self.assertIsNotNone(action.job)
        self.assertIsNotNone(scheduler.actions[0])

        # ensure the job has not been added to the scheduler
        self.assertEqual(len(_scheduler.jobs), 0)


class Test_ActionScheduler_Integration(TestCase):
    """ Tests for integration with the `scheduler` lib. """

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        # Ensure the previous test hasn't left any jobs in the queue
        err = 'The job scheduler queue is not empty'
        assert len(_scheduler.jobs) == 0, err
        yield
        # Clear any jobs added by a test
        _scheduler.clear()
        assert len(_scheduler.jobs) == 0, err

    def test_add_action_with_kwargs1(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc, someparam='value')
        scheduler.add().every().sunday.at('23:59')
        scheduler._finalize()

        # ensure the job has been added to the scheduler
        self.assertEqual(len(_scheduler.jobs), 1)
        # ensure the action has a reference to the job
        self.assertEqual(_scheduler.jobs[0], scheduler.actions[0].job)

    def test_add_action_with_kwargs2(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc)
        scheduler.add(someparam='value').every().sunday.at('23:59')
        scheduler._finalize()

        # ensure the job has been added to the scheduler
        self.assertEqual(len(_scheduler.jobs), 1)
        # ensure the action has a reference to the job
        self.assertEqual(_scheduler.jobs[0], scheduler.actions[0].job)

    def test_add_no_action_should_fail1(self):
        scheduler = ActionScheduler()

        with pytest.raises(TypeError):
            scheduler.add().every().sunday.at('23:59')

        # action not added
        self.assertEqual(len(scheduler.actions), 0)
        # ensure the job scheduler queue is empty
        self.assertEqual(len(_scheduler.jobs), 0)

    def test_add_no_action_should_fail2(self):
        scheduler = ActionScheduler(someparam='bla')

        with pytest.raises(TypeError):
            scheduler.add().every().sunday.at('23:59')

        # action not added
        self.assertEqual(len(scheduler.actions), 0)
        # ensure the job scheduler queue is empty
        self.assertEqual(len(_scheduler.jobs), 0)

    def test_clear_jobs(self):
        def somefunc(**kwargs):
            pass

        scheduler = ActionScheduler(somefunc)
        scheduler.add().every().sunday.at('23:59')
        scheduler._finalize()

        self.assertEqual(len(scheduler.actions), 1)
        self.assertEqual(len(_scheduler.jobs), 1)

        scheduler.clear()
        self.assertEqual(len(scheduler.actions), 0)
        self.assertEqual(len(_scheduler.jobs), 0)
