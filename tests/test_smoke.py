"""Minimal smoke test for funwork.

The top-level funwork package only declares __all__; it does not eagerly
import the youzan/ItemUtils submodules (which pull in demjson/requests/
urllib3 -- packages not declared as dependencies of this project), so
`import funwork` alone has no such side effects.
"""


def test_import():
    import funwork

    assert funwork is not None
