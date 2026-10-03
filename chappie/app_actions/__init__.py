"""Every action of the Chappie app, reachable by the brain under the user's policy.

The app's own REST surface is the action catalog (``catalog``): one entry per
OpenAPI operation, built in-process from the live FastAPI app, minus the
operations Chappie must never touch (secrets, sign-ins, its own policy). The
person decides per action whether Chappie may run it freely, must ask first,
or may never run it (``policy``); ``history`` keeps what Chappie ran recently.
"""
