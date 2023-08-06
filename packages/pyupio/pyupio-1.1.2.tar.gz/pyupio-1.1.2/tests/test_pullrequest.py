# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from unittest import TestCase
from pyup.pullrequest import PullRequest
from datetime import datetime, timedelta


def pullrequest_factory(title, state="open", url="http://foo.bar",
                        created_at=datetime.now(), number=1):
    return PullRequest(
        title=title,
        state=state,
        url=url,
        created_at=created_at,
        number=number
    )


class PullRequestTypeTest(TestCase):
    def test_update(self):
        pr = pullrequest_factory(title="Update this and that")
        self.assertEqual(pr.type, "update")
        self.assertTrue(pr.is_update)

    def test_security(self):
        pr = pullrequest_factory(title="Security is not provided here")
        self.assertEqual(pr.type, "security")
        self.assertTrue(pr.is_security)

    def test_pin(self):
        pr = pullrequest_factory(title="Pin this on thta")
        self.assertEqual(pr.type, "pin")
        self.assertTrue(pr.is_pin)

    def test_initial(self):
        pr = pullrequest_factory(title="Initial Update")
        self.assertEqual(pr.type, "initial")
        self.assertTrue(pr.is_initial)

    def test_unknown(self):
        pr = pullrequest_factory(title="Foo")
        self.assertEqual(pr.type, "unknown")
        #self.assertTrue(pr.is_scheduled)

    def test_compile(self):
        pr = pullrequest_factory(title="Compile foo.txt")
        self.assertEqual(pr.type, "compile")
        self.assertTrue(pr.is_compile)

    def test_scheduled(self):
        pr = pullrequest_factory(title="Scheduled foo in bar")
        self.assertEqual(pr.type, "scheduled")
        self.assertTrue(pr.is_scheduled)

    def test_is_valid(self):
        pr = pullrequest_factory(title="Scheduled foo in bar")
        self.assertTrue(pr.is_valid)

        pr = pullrequest_factory(title="Compile foo.txt")
        self.assertTrue(pr.is_valid)

        pr = pullrequest_factory(title="Initial Update")
        self.assertTrue(pr.is_valid)

        pr = pullrequest_factory(title="Pin this on thta")
        self.assertTrue(pr.is_valid)

        pr = pullrequest_factory(title="Update this and that")
        self.assertTrue(pr.is_valid)

class PullRequestEQTest(TestCase):
    def test_is_eq(self):
        pr1 = pullrequest_factory("yay", number=1)
        pr2 = pullrequest_factory("yay", number=2)
        self.assertNotEqual(pr1, pr2)
        pr1.number = pr2.number
        self.assertEqual(pr1, pr2)
        pr1.number = 3
        self.assertNotEqual(pr1, pr2)
        pr2.number = 3
        self.assertEqual(pr1, pr2)


class PullRequestStateTest(TestCase):

    def test_is_open(self):
        pr = pullrequest_factory(title="the foo", state="closed")
        self.assertEqual(pr.is_open, False)
        pr.state = "open"
        self.assertEqual(pr.is_open, True)


class PullRequestRequirementTestCase(TestCase):

    def test_initial_non(self):
        pr = pullrequest_factory(title="Initial PR")
        self.assertEqual(pr.get_requirement(), None)

    def test_pin(self):
        pr = pullrequest_factory(title="Pin django")
        self.assertEqual(pr.get_requirement(), "django")

    def test_update(self):
        pr = pullrequest_factory(title="Update django")
        self.assertEqual(pr.get_requirement(), "django")

    def test_some_bogus(self):
        pr = pullrequest_factory(title="Uhm?")
        self.assertEqual(pr.get_requirement(), None)

    def test_with_prefix(self):
        pr = pullrequest_factory(title="Some Prefix | Update django")
        self.assertEqual(pr.get_requirement("Some Prefix |"), 'django')

        flask = pullrequest_factory(title="Pin flask")
        flask_prefix = pullrequest_factory(title="Some Prefix | Pin flask")
        self.assertIsNotNone(flask.get_requirement())
        self.assertEqual(flask.get_requirement(), flask_prefix.get_requirement("Some Prefix |"))
