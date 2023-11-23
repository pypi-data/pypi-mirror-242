import sys
import os
import json
import argparse
from . import types_pb2 as pb2
from .attributes import Attributes
from google.protobuf import json_format

import base64

# ----------------------------------------
# default_args provides a minimal argument parser to start an agen 
# We need to provide invocation bindings that automatically
# account for dispatches from controller.  All of the currently
# configured runners that can call python will pass the following
# to the CLI:
#
#     - Agent spec (in JSON) --spec={...}
#     - Blackboard addr      --bb="localhost:8080"
#
# If you're modifying this code, make sure the runner that will
# dispatch your job will pass these arguments (or the arguments that
# you specify).  But note that an AgentSpec and a Blackboard address
# are required to start any agent.
def default_args(agent_filename):

    defaults =  {
        "pingInterval_ms": 1000,
        "pollInterval_ms": 1000,
        }
    
    parser = argparse.ArgumentParser(prog=agent_filename)
    parser.add_argument('--spec', help="full agent spec in JSON")
    parser.add_argument('--blackboard', help="hostname:port of the blackboard to connect to")
    args = parser.parse_args()

    blackboard = "localhost:8080"
    agent_spec = None
    if args.spec != None:

        spec_string = args.spec

        # NOTE: We *only* understand specs as json here.
        #       this could be confusing for folks who want to pass
        #       yaml files for their specs.
        # Check if user is passing a spec file vs json
        if os.path.exists(args.spec):
            with open(args.spec, "r") as f:
                spec_string = f.read()
                print("agent spec read from file:\n", spec_string)

        ##################################
        # Here thar be monsters:
        #
        # This is required for nested attributes support
        # We have to strip the attributes dictionary out of the spec structure,
        # encode it into a json string, then bytes, and stuff back
        # into the spec structure for passing to the Agent object.
        #
        # THIS NECESSITATES THAT EVERY AGENT CALL default_args
        #
        # I don't like this.
        ##################################
        
        # Decode spec as a generic python dictionary
        spec_tmp = json.loads(spec_string)

        # If attributes are specified, extract them as dict, and
        # remove it from the spec (temporarily)
        attrs = None
        if "attributes" in spec_tmp:
            attrs = spec_tmp["attributes"]
            spec_tmp.pop("attributes", None) # Remove attributes from spec

        # Re-encode the *spec* to json and decode into the protobuffer-
        # defined spec structure
        spec_string = json.dumps(spec_tmp) # After removing attributes, we need to convert back to json
        
        agent_spec = json_format.Parse(spec_string, pb2.AgentSpec())

        # Encode attrs into bytes and store place (manually)
        # in the attributes property.
        agent_spec.attributes = json.dumps(attrs).encode("utf-8")

        ##################################
        
        # Set any unset defaults
        min_ping_ms = 33
        min_poll_ms = 33
        
        if agent_spec.pingInterval_ms == 0:
            agent_spec.pingInterval_ms = defaults["pingInterval_ms"]

        if agent_spec.pollInterval_ms == 0:
            agent_spec.pollInterval_ms = defaults["pollInterval_ms"]
        
        # user set poll interval but it's too low, throw warning
        if agent_spec.pollInterval_ms != 0 and agent_spec.pollInterval_ms < min_poll_ms:
            agent_spec.pollInterval_ms = max(agent_spec.pollInterval_ms, min_poll_ms)
            print("override pollInterval_ms to %dms; please file an issue if you see this message." % (min_poll_ms))

        # user set ping interval but it's too low, throw warning
        if agent_spec.pingInterval_ms != 0 and agent_spec.pingInterval_ms < min_ping_ms:
            agent_spec.pingInterval_ms = max(agent_spec.pingInterval_ms, min_ping_ms)
            print("override pingInterval_ms to %dms; please file an issue if you see this message." % (min_ping_ms))

    else:

        default_spec = '{"name":"new-agent","pingInterval_ms":"1000","pollIntervalMs":"1000","allowedPingRetries": 3, "allowedPollRetries": 3}'

        print('No agent spec provided.  Defaulting to ', default_spec)
        print('If this is a mistake, please provide an agent spec using the --spec option')
        print('More documentation on agent specs can be found here: ')
        
        agent_spec = json_format.Parse(default_spec, pb2.AgentSpec())
        
    if args.blackboard != None:
        blackboard = args.blackboard
    else:
        print('No blackboard specified. Defaulting to "localhost:8080"')
        print('If this is a mistake, please provide a blackboard address using the --blackboard option')
    
    return (agent_spec, blackboard)
