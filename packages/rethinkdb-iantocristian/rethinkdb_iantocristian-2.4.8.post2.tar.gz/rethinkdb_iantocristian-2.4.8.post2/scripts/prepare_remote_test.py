# Copyright 2018-present RethinkDB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# This file incorporates work covered by the following copyright:
#
#     Copyright 2010-present, The Linux Foundation, portions copyright Google and
#     others and used with permission or subject to their respective license
#     agreements.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import os
import sys
import uuid
from datetime import datetime
from subprocess import check_call
from time import sleep

import digitalocean
import paramiko

DROPLET_NAME = 'test-{uuid}'.format(uuid=str(uuid.uuid4()))
SSH_KEY_NAME = 'key-{name}'.format(name=DROPLET_NAME)
DROPLET_STATUS_COMPLETED = 'completed'
BINTRAY_USERNAME = os.getenv('BINTRAY_USERNAME')


class DropletSetup(object):
    def __init__(self, token, size, region):
        super(DropletSetup, self).__init__()
        self.token = token
        self.size = size
        self.region = region
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_key = None
        self.digital_ocean_ssh_key = None

        self._generate_ssh_key()
        self.droplet = digitalocean.Droplet(
            token=self.token,
            name=DROPLET_NAME,
            region=self.region,
            image='ubuntu-16-04-x64',
            size_slug=self.size,
            ssh_keys=[self.digital_ocean_ssh_key.id]
        )

    @staticmethod
    def _print_info(message):
        print('[{timestamp}]\t{message}'.format(timestamp=datetime.now().isoformat(), message=message))

    def _execute_command(self, command):
        self._print_info('executing {command}'.format(command=command))
        std_in, _, std_err = self.ssh_client.exec_command(command)
        std_in.close()

        has_err = False
        for line in std_err.readlines():
            has_err = True
            print(line.replace('\n', ''))

        if has_err:
            raise Exception('Script execution failed')

    def _generate_ssh_key(self):
        self._print_info('generating ssh key')
        self.ssh_key = paramiko.rsakey.RSAKey.generate(2048, str(uuid.uuid4()))

        self._print_info('create ssh key on DigitalOcean')
        self.digital_ocean_ssh_key = digitalocean.SSHKey(
            token=self.token,
            name=SSH_KEY_NAME,
            public_key='ssh-rsa {key}'.format(key=str(self.ssh_key.get_base64()))
        )

        self.digital_ocean_ssh_key.create()

    def create_droplet(self):
        self._print_info('creating droplet')
        self.droplet.create()

        self._print_info('waiting for droplet to be ready')
        self._wait_for_droplet()

    def _wait_for_droplet(self):
        actions = self.droplet.get_actions()
        for action in actions:
            if action.status == DROPLET_STATUS_COMPLETED:
                self.droplet.load()
                return

        self._wait_for_droplet()

    def __enter__(self):
        """
        Connect to DigitalOcean instance with forever retry.
        """
        self._print_info('connecting to droplet')
        try:
            self.ssh_client.connect(
                hostname=self.droplet.ip_address,
                username='root',
                allow_agent=True,
                pkey=self.ssh_key
            )
        except Exception as exc:
            self._print_info(str(exc))
            self._print_info('reconnecting')
            sleep(3)
            return self.__enter__()
        return self

    def install_rethinkdb(self):
        self._print_info('getting rethinkdb')
        
        self._execute_command('source /etc/lsb-release && echo "deb https://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list')
        self._execute_command('wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -')

        self._print_info('installing rethinkdb')
        self._execute_command('apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --allow-unauthenticated -y rethinkdb')
        self._execute_command('echo "bind=all" > /etc/rethinkdb/instances.d/default.conf')

    def start_rethinkdb(self):
        self._print_info('restarting rethinkdb')
        self._execute_command('/etc/init.d/rethinkdb restart')

    def run_script(self, script, script_arguments):
        self._print_info('executing script')
        os.environ["RETHINKDB_HOST"] = self.droplet.ip_address
        check_call([script, ' '.join(script_arguments)])

    def __exit__(self, *args):
        """
        Cleanup DigitalOcean instance connection.
        """
        self._print_info('destroying droplet')
        self.droplet.destroy()

        self._print_info('removing ssh key')
        self.digital_ocean_ssh_key.destroy()


def main():
    script = sys.argv[1]
    script_arguments = sys.argv[2:]

    setup = DropletSetup(
        token=os.getenv('DO_TOKEN'),
        size=os.getenv('DO_SIZE', '512MB'),
        region=os.getenv('DO_REGION', 'sfo2')
    )

    setup.create_droplet()

    with setup:
        setup.install_rethinkdb()
        setup.start_rethinkdb()
        setup.run_script(script, script_arguments)


if __name__ == '__main__':
    main()
