from __future__ import absolute_import

import os

from six.moves import configparser
from django.test import TestCase
from mock import patch

from delft3dcontainermanager.tasks import delft3dgt_pulse
from delft3dcontainermanager.tasks import get_docker_ps
from delft3dcontainermanager.tasks import get_docker_log
from delft3dcontainermanager.tasks import do_docker_create
from delft3dcontainermanager.tasks import do_docker_start
from delft3dcontainermanager.tasks import do_docker_stop
from delft3dcontainermanager.tasks import do_docker_remove
from delft3dcontainermanager.tasks import do_docker_sync_filesystem


class TaskTest(TestCase):
    mock_options = {
        'autospec': True,
        # 'containers.return_value': [{'a': 'test'}]
    }

    @patch('delft3dcontainermanager.tasks.call_command')
    def test_delft3dgt_pulse(self, mock):
        """
        Assert that de delft3dgt_pulse task
        calls the containersync_sceneupdate() function.
        """
        delft3dgt_pulse.delay()
        mock.assert_called_with('containersync_sceneupdate')

    @patch('delft3dcontainermanager.tasks.Client', **mock_options)
    def test_get_docker_ps(self, mockClient):
        """
        Assert that the docker_ps task
        calls the docker client.containers() function.
        """
        get_docker_ps.delay()
        mockClient.return_value.containers.assert_called_with(all=True)

    def test_get_docker_log(self):
        """
        TODO: write test
        """
        delay = get_docker_log.delay("id")
        self.assertEqual(delay.result, {})

    @patch('delft3dcontainermanager.tasks.Client', **mock_options)
    def test_do_docker_create(self, mockClient):
        """
        Assert that the docker_create task
        calls the docker client.create_container() function.
        """
        image = "IMAGENAME"
        volumes = ['/:/data/output:z',
                   '/:/data/input:ro']
        command = "echo test"
        config = {}
        environment = None
        label = {"type": "delft3d"}
        folder = ['input', 'output']
        workingdir = os.path.join(os.getcwd(), 'test')
        folders = [os.path.join(workingdir, f) for f in folder]
        parameters = {u'test':
                      {u'1': u'a', u'2': u'b', 'units': 'ignoreme'}
                      }
        mockClient.return_value.create_host_config.return_value = config

        do_docker_create.delay(image, volumes, folders, command, label,
                               parameters, environment=None)

        # Assert that docker is called
        mockClient.return_value.create_container.assert_called_with(
            image,
            host_config=config,
            command=command,
            environment=environment,
            labels=label
        )

        # Assert that folders are created
        listdir = os.listdir(workingdir)
        for f in listdir:
            self.assertIn(f, listdir)

        for folder in folders:
            ini = os.path.join(folder, 'input.ini')
            self.assertTrue(os.path.isfile(ini))

            config = configparser.SafeConfigParser()
            config.readfp(open(ini))
            for key in parameters.keys():
                self.assertTrue(config.has_section(key))
                for option, value in parameters[key].items():
                    if option != 'units':
                        self.assertTrue(config.has_option(key, option))
                        self.assertEqual(config.get(key, option), value)
                    else:  # units should be ignored
                        self.assertFalse(config.has_option(key, option))

    def test_do_docker_start(self):
        """
        TODO: write test
        """
        delay = do_docker_start.delay("id")
        self.assertEqual(delay.result, False)

    def test_do_docker_stop(self):
        """
        TODO: write test
        """
        delay = do_docker_stop.delay("id")
        self.assertEqual(delay.result, False)

    def test_do_docker_remove(self):
        """
        TODO: write test
        """
        delay = do_docker_remove.delay("id")
        self.assertEqual(delay.result, False)

    def test_do_docker_sync_filesystem(self):
        """
        TODO: write test
        """
        delay = do_docker_sync_filesystem.delay("id")
        self.assertEqual(delay.result, False)
