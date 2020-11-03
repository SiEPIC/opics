import numpy as np
import pytest
import opics as op
from opics.libraries.ebeam import components, component_factory


@pytest.mark.parametrize("component_type", components)
def test_properties_components(component_type, num_regression):
    w = np.linspace(1.52, 1.58, 3) * 1e-6
    f = op.c / w
    c = component_factory[component_type](f=f)
    s = c.get_data()
    s.pop("xunit")
    s.pop("yunit")
    num_regression.check(s)
