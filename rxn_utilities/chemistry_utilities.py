# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED
"""Chemistry-related utilties."""
from typing import Dict

import requests

CHEMICAL_NAME_TO_PROPERTIES = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/property/MolecularFormula,CanonicalSMILES,IsomericSMILES/CSV"


class ChemicalPropertiesRetrievalError(RuntimeError):
    """Error in chemical properties retrieval."""

    pass


def get_chemical_properties(chemical_name: str) -> Dict:
    """
    Get chemical properties from a chemical name.

    Args:
        chemical_name (str): name of the chemical.

    Returns:
        Dict: dictionary containing: cid, chemical_formula, smiles.

    Raises:
        ChemicalPropertiesRetrievalError: error retriving the properties.
    """
    try:
        response_text = requests.get(
            CHEMICAL_NAME_TO_PROPERTIES.format(chemical_name=chemical_name)
        ).text
        properties = [
            a_property.strip('"')
            for a_property in response_text.split("\n")[1].split(",")
        ]
        return {
            "cid": properties[0],
            "chemical_formula": properties[1],
            "smiles": properties[2],
            "isomeric_smiles": properties[3],
        }
    except Exception:
        raise ChemicalPropertiesRetrievalError(
            "error retrieving chemical properties for {}".format(chemical_name)
        )
