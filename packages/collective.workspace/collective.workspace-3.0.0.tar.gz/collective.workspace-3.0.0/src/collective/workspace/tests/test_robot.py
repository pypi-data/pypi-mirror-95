# coding=utf-8
from collective.workspace.testing import COLLECTIVE_WORKSPACE_ROBOT_TESTING
from plone.testing import layered

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("workspace.robot"),
                layer=COLLECTIVE_WORKSPACE_ROBOT_TESTING,
            )
        ]
    )
    return suite
