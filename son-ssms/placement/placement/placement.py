"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import logging
import yaml
from sonsmbase.smbase import sonSMbase

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("ssm-placement-1")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class PlacementSSM(sonSMbase):
    def __init__(self):

        self.smtype = 'ssm'
        self.sfname = 'default'
        self.name = 'placement'
        self.id = '1'
        self.version = 'v0.1'
        self.description = 'Placement SSM'

        super(self.__class__, self).__init__(smtype= self.smtype,
                                             sfname= self.sfname,
                                             name= self.name,
                                             id = self.id,
                                             version= self.version,
                                             description= self.description)

    def on_registration_ok(self):
        LOG.debug("Received registration ok event.")

        # Register to task topic and to place topic
        topic = 'placement.ssm' + self.sfuuid

        self.manoconn.subscribe(self.on_place,topic= topic)

        print(topic)

    def on_place(self, ch, method, properties, payload):

        if properties.app_id != self.name:
            message = {'placement': ['from_ssm']}
            payload = yaml.dump(message)
            self.manoconn.notify(topic= 'placement.ssm' + self.uuid , msg= payload, correlation_id=properties.correlation_id)

def main():
    PlacementSSM()

if __name__ == '__main__':
    main()
