from typing import Dict, List, Callable


def has_children(node: Dict) -> bool:
    """
    Check if the input node has children, return
    true if it does or false if it is a leaf

    Args:
        node (Dict): Dictionary representing a node
            in the retrosynthesis tree
    Returns:
        bool: whether the node has children or not
    """

    result = False
    if 'children' in node and len(node['children']) > 0:
        for child in node['children']:
            if child:
                result = True

    return result


def has_children_with_synthesis(node: Dict) -> bool:
    """
    Check if the input node has children that contain an action sequence.

    Args:
        node (Dict): Dictionary representing a node
            in the retrosynthesis tree
    Returns:
        bool: whether the node has children with syntheses or not
    """

    result = False
    if 'children' in node and len(node['children']) > 0:
        for child in node['children']:
            try:
                if child['configuration']['action_sequence']:
                    result = True
            except Exception:
                pass

    return result


def post_order_traversal(tree: Dict) -> List:
    """
    Given a retrosynthesis tree it returns a post-order traversal
    of the tree nodes in a list. The retrosynthesis steps can be
    then executed in this order.
    For more details on tree traversals:
    https://en.wikipedia.org/wiki/Tree_traversal

    Args:
        tree (Dict): Dictionary representing a retrosynthesis tree
            Example form:
            tree = {
                "children": [
                    {
                        "children": [...],
                        "configuration":
                            {
                                "action_sequence": [...]
                            }
                    },
                    {
                        ...
                    },
                    ...
                ],
                "configuration":
                    {
                        "action_sequence": [...]
                    }
            }

    Returns:
        List: List with references to the subtrees based on the post-order
            traversal of the tree

    """

    result = []

    if 'children' in tree:
        for child in tree['children']:
            result.extend(post_order_traversal(child))
    if tree:
        result.append(tree)

    return result


def get_nodes(tree: Dict, condition: Callable[[Dict], bool]) -> List:
    """
    Given a retrosynthesis tree it returns the nodes matching a condition over
    a traversal.
    For more details on tree traversals:
    https://en.wikipedia.org/wiki/Tree_traversal

    Args:
        tree (Dict): Dictionary representing a retrosynthesis tree
            Example form:
            tree = {
                "children": [
                    {
                        "children": [...],
                        "configuration":
                            {
                                "action_sequence": [...]
                            }
                    },
                    {
                        ...
                    },
                    ...
                ],
                "configuration":
                    {
                        "action_sequence": [...]
                    }
            }
        condition (Callable[[Dict], bool]): a function that is used to select nodes.

    Returns:
        List: List with references to the nodes evaluated as true by the condition.

    """

    nodes = []

    if 'children' in tree:
        for child in tree['children']:
            nodes.extend(get_nodes(child, condition))
    if condition(tree):
        nodes.append(tree)

    return nodes
