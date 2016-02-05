from __future__ import absolute_import

import signal

from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery.signals import task_revoked
from celery.utils.log import get_task_logger

from docker import Client

logger = get_task_logger(__name__)


@shared_task(bind=True, base=AbortableTask)
def rundocker(self, name, uuid, workingdir):
    
    """Task to run docker container"""
    
    logger.info('Creating docker container')
    docker_run = DockerRun(name, workingdir)

    logger.info('Running docker container')
    docker_run.start()

    for log in docker_run.log():
        
        logger.info(log)

        # check for abortion
        if (self.is_aborted()):
            logger.info('ABORTING')
            items = log.split(',')
            self.update_state(state='ABORTING', meta={
                'time_to_finish': items[0].strip(),
                'percent_completed': 'abort procedure...',
                'timesteps_left': items[2].strip()
            })
            docker_run.stop()
        else:
            items = log.split(',')
            if len(items) == 3:
                self.update_state(state='SIMULATING', meta={
                    'time_to_finish': items[0].strip(),
                    'percent_completed': items[1].strip(),
                    'timesteps_left': items[2].strip()
                })
    
    logger.info('Destroying docker container')
    docker_run.remove()
    
    return


class DockerRun():

    """Class to run docker containers with specific configs"""

    def __init__(self, name, workingdir, base_url='unix://var/run/docker.sock'):

        self.name = name
        self.workingdir = workingdir        
        self.base_url = base_url

        self.client = Client(base_url=self.base_url)

        self._create_container()

    def start(self):
        self.client.start(container=self.id)

    def stop(self):
        self.client.stop(container=self.id)

    def log(self):
        self.log = self.client.logs(container=self.id,
                               stream=True, stdout=True, stderr=True)
        return self.log

    def remove(self):
        self.client.remove_container(container=self.id)

    def _create_container(self):

        config = self.client.create_host_config(binds=[
             '{0}:/data'.format(self.workingdir),
         ])

        self.container = self.client.create_container(self.name, host_config=config)
        self.id = self.container.get('Id')

