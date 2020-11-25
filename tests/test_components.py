import numpy as np
import pytest
import opics as op
from opics.libraries.ebeam import components_list, component_factory


@pytest.mark.parametrize("component_type", components_list)
def test_properties_components(component_type: str, num_regression) -> None:
    w = np.linspace(1.52, 1.58, 3) * 1e-6
    f = op.c / w
    c = component_factory[component_type](f=f)
    s = c.get_data()
    s.pop("xunit")
    s.pop("yunit")
    num_regression.check(s)
