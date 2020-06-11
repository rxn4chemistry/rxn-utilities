"""Chemistry-related utilties."""
import requests
from typing import Dict

CHEMICAL_NAME_TO_PROPERTIES = (
    'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/property/MolecularFormula,CanonicalSMILES/CSV'
)


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
            CHEMICAL_NAME_TO_PROPERTIES.format(
                chemical_name=chemical_name
            )
        ).text
        properties = [
            a_property.strip('"')
            for a_property in response_text.split('\n')[1].split(',')
        ]
        return {
            'cid': properties[0],
            'chemical_formula': properties[1],
            'smiles': properties[2],
        }
    except Exception:
        raise ChemicalPropertiesRetrievalError(
            'error retrieving chemical properties for {}'.format(chemical_name)
        )
