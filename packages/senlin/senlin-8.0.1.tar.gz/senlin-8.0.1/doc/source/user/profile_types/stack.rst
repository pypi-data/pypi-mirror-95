..
  Licensed under the Apache License, Version 2.0 (the "License"); you may
  not use this file except in compliance with the License. You may obtain
  a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
  License for the specific language governing permissions and limitations
  under the License.

.. _ref-stack-profile:

=============
Stack Profile
=============

The stack profile instantiates nodes that are associated with heat stack
instances.

Properties
~~~~~~~~~~

.. schemaprops::
  :package: senlin.profiles.os.heat.stack.StackProfile

Sample
~~~~~~

Below is a typical spec for a stack profile:

.. literalinclude :: /../../examples/profiles/heat_stack/nova_server/heat_stack_nova_server.yaml
  :language: yaml
