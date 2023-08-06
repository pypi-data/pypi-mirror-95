# Modifications © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from trainingopz.logger.ml_log import MLLog


class ArtifactRegistry:
    def __init__(self):
        self._logger = MLLog("ArtifactRegistry", logging.DEBUG, False).logger

    def register(self, artifact):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')
