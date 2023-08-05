import pathlib

from tests.utils import TestCase
from tests.mocks import MockedXmlConfig


class TestXmlConfig(TestCase):
    CONFIG_NAME = 'config.xml'

    def test_config_saved(self):
        '''
        Tests that the config file is created correctly.
        '''
        config = self.make_config(MockedXmlConfig, 'saved')
        config['string'] = 'string'
        config['integer'] = 0
        config['float'] = 0.1
        config['dict'] = {}
        config['list'] = []
        self.assertEqual(
            config,
            {
                'string': 'string',
                'integer': 0,
                'float': 0.1,
                'dict': {},
                'list': []
            }
        )
        config.save()
        self.assertFileExists(
            (
                pathlib.Path('./__tmp__') /
                self.__class__.__name__ /
                f'saved_{self.CONFIG_NAME}'
            )
        )

    def test_config_loaded(self):
        config = self.make_config(MockedXmlConfig, 'load')
        config['string'] = 'string'
        config['integer'] = 0
        config['float'] = 0.1
        config['dict'] = {}
        config['list'] = []
        config.save()

        conf = self.make_config(MockedXmlConfig, 'load')
        self.assertEqual(
            conf,
            {
                'string': 'string',
                'integer': 0,
                'float': 0.1,
                'dict': {},
                'list': []
            }
        )

    def test_mutating_subkey(self):
        '''
        Test that mutating a non-existing subkey generates the proper
        tree-like structure.
        '''
        config = self.make_config(MockedXmlConfig, 'mutating')
        config['foo']['bar'] = 'baz'
        self.assertEqual(
            config, {'foo': {'bar': 'baz'}}
        )

    def test_config_identity(self):
        '''
        Test that the config file's instance is cached in a Singleton-type
        design pattern. Ensures limited memory footprint when working with
        config files.
        '''
        config = self.make_config(MockedXmlConfig, 'identity')
        self.assertIs(config, self.make_config(MockedXmlConfig, 'identity'))
        self.assertIsNot(
            config, self.make_config(MockedXmlConfig, 'identity_false')
        )
