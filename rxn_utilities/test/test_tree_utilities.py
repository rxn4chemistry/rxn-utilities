from rxn_utilities.tree_utilities import (
    post_order_traversal, has_children, has_children_with_synthesis
)

tree = {
    "id":
        1,
    "children":
        [
            {
                "id":
                    2,
                "children":
                    [
                        {
                            "id": 3,
                            "children": [{}]
                        }, {
                            "id": 4,
                            "children": [{
                                "id": 5
                            }]
                        }, {
                            "id": 6,
                            "children": [{}]
                        }
                    ]
            }, {
                "id": 7,
                "children": [{
                    "id": 8,
                    "children": [{
                        "id": 9
                    }]
                }, {
                    "id": 10,
                    "children": [{}]
                }]
            }
        ]
}

dummy_action = {
    "name": "chemspeed_control_reactor",
    "parameters":
        {
            "temperature": 25,
            "stirring_speed": 300,
            "pressure": 1000,
            "reactor_id": "R1",
            "reflux": False
        },
    "content": {}
}

tree_with_synthesis = {
    "id":
        1,
    "configuration": {
        "action_sequence": [dummy_action]
    },
    "children":
        [
            {
                "id":
                    2,
                "configuration": {
                    "action_sequence": [dummy_action]
                },
                "children":
                    [
                        {
                            "id": 3,
                            "children": [{}]
                        },
                        {
                            "id": 4,
                            "configuration": {
                                "action_sequence": [dummy_action]
                            },
                            "children": [{
                                "id": 5
                            }]
                        },
                        {
                            "id": 6,
                            "children": [{}]
                        },
                    ]
            },
            {
                "id":
                    7,
                "configuration": {
                    "action_sequence": [dummy_action]
                },
                "children":
                    [
                        {
                            "id": 8,
                            "configuration": {
                                "action_sequence": []
                            },
                            "children": [{
                                "id": 9
                            }]
                        }, {
                            "id": 10,
                            "children": [{}]
                        }
                    ]
            },
        ]
}


def test_has_children():
    assert has_children(tree) is True
    assert has_children(tree['children'][0]) is True
    assert has_children(tree['children'][1]) is True
    assert has_children(tree['children'][0]['children'][0]) is False
    assert has_children(tree['children'][0]['children'][1]) is True
    assert has_children(tree['children'][0]['children'][2]) is False
    assert has_children(tree['children'][1]['children'][0]) is True
    assert has_children(tree['children'][1]['children'][1]) is False


def test_has_children_with_synthesis():
    # the only ones with a synthesis are the root, its first child,
    # and the second child of the first child
    assert has_children_with_synthesis(tree_with_synthesis) is True
    assert has_children_with_synthesis(tree_with_synthesis['children'][0]) is True
    assert has_children_with_synthesis(tree_with_synthesis['children'][1]) is False
    assert has_children_with_synthesis(tree_with_synthesis['children'][0]['children'][0]) is False
    assert has_children_with_synthesis(tree_with_synthesis['children'][0]['children'][1]) is False
    assert has_children_with_synthesis(tree_with_synthesis['children'][0]['children'][2]) is False
    assert has_children_with_synthesis(tree_with_synthesis['children'][1]['children'][0]) is False
    assert has_children_with_synthesis(tree_with_synthesis['children'][1]['children'][1]) is False


def test_post_order_traversal():
    expected_order = [3, 5, 4, 6, 2, 9, 8, 10, 7, 1]
    ordered_nodes = post_order_traversal(tree)
    result_order = [n["id"] for n in ordered_nodes]

    assert expected_order == result_order
