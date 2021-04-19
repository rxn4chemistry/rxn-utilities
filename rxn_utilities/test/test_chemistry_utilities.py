# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED
"""Testing chemistry utilities."""
import pytest
from rxn_utilities.chemistry_utilities import (
    ChemicalPropertiesRetrievalError, get_chemical_properties
)


def test_chemical_properties_retrieval_error():
    with pytest.raises(ChemicalPropertiesRetrievalError):
        raise ChemicalPropertiesRetrievalError('test')
    with pytest.raises(RuntimeError):
        raise ChemicalPropertiesRetrievalError('test')


def test_get_chemical_properties():
    chemical_name = 'tert-Butyldiphenylphosphine'
    groundtruth = {
        'cid': '80102',
        'chemical_formula': 'C16H19P',
        'smiles': 'CC(C)(C)P(C1=CC=CC=C1)C2=CC=CC=C2',
        'isomeric_smiles': 'CC(C)(C)P(C1=CC=CC=C1)C2=CC=CC=C2'
    }
    assert groundtruth == get_chemical_properties(chemical_name=chemical_name)
    with pytest.raises(ChemicalPropertiesRetrievalError):
        get_chemical_properties('this is not a molecule')
