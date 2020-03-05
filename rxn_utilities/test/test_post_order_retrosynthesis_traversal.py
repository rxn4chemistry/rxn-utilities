from rxn_utilities.post_order_retrosynthesis_traversal import (
    post_order_retrosynthesis_traversal
)


def test_post_order_retrosynthesis_traversal():

    tree = {
        "id": 1,
        "children": [
            {
                "id": 2,
                "children": [
                    {
                        "id": 3,
                        "children": [{}]
                    },
                    {
                        "id": 4,
                        "children": [{"id": 5}]
                    },
                    {
                        "id": 6,
                        "children": [{}]
                    }
                ]
            },
            {
                "id": 7,
                "children": [
                    {
                        "id": 8,
                        "children": [{"id": 9}]
                    },
                    {
                        "id": 10,
                        "children": [{}]
                    }
                ]
            }
        ]
    }

    expected_order = [3, 5, 4, 6, 2, 9, 8, 10, 7, 1]
    ordered_nodes = post_order_retrosynthesis_traversal(tree)
    result_order = [n["id"] for n in ordered_nodes]

    assert expected_order == result_order
