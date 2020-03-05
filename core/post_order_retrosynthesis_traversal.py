from typing import Dict, List


def post_order_retrosynthesis_traversal(tree: Dict) -> List:
    """
    Given a retrosynthesis tree it returns a post-order traversal
    of the tree nodes in a list. The retrosynthesis steps can be
    then executed in this order.
    For more details on tree traversals:
    https://en.wikipedia.org/wiki/Tree_traversal

    Args:
        tree(Dict): Dictionary representing a retrosynthesis tree
            Example form:
            tree = {
                "children": [
                    {
                        "children": [...]
                        "action_sequence": [...]
                    },
                    {
                        ...
                    },
                    ...
                ]
                "action_sequence": [...]
            }

    Returns:
        List: List with references to the subtrees based on the post-order
            traversal of the tree

    """

    result = []

    if 'children' in tree:
        for c in tree['children']:
            result.extend(post_order_retrosynthesis_traversal(c))
    if tree:
        result.append(tree)

    return result
