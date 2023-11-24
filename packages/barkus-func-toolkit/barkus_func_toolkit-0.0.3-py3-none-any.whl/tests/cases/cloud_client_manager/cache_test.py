from unittest.mock import Mock
from barkus_function_toolkit.cloud_client_manager import ClientCache as Sut
import pytest

def test_load_should_only_initialize_classes_once():
    cls = Mock()
      
    Sut.load("key", cls)
    Sut.load("key", cls)

    cls.assert_called_once()

def test_failed_import_should_re_raise_the_exception():
    exp = ModuleNotFoundError("mock")
      
    with pytest.raises(ModuleNotFoundError) as mnf:
        Sut.failed_import(exp, "pkg_name")

    assert repr(mnf.value) == """ModuleNotFoundError('mock\\nRun ( pip install barkus-func-toolkit[pkg_name] ) to fix it')"""