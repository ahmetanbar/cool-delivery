class Data:
    input_with_5_delivery_5_pickup = {
        "depot": {
            "x": 0,
            "y": 0,
            "location_index": 0
        },
        "vehicle": {
            "capacity": 150
        },
        "events": [
            {
                "id": 1,
                "x": 45,
                "y": 37,
                "location_index": 1,
                "capacity": 25,
                "type": "delivery"
            },
            {
                "id": 2,
                "x": 92,
                "y": 47,
                "location_index": 2,
                "capacity": 38,
                "type": "delivery"
            },
            {
                "id": 3,
                "x": 14,
                "y": 30,
                "location_index": 3,
                "capacity": 20,
                "type": "delivery"
            },
            {
                "id": 4,
                "x": 4,
                "y": 49,
                "location_index": 4,
                "capacity": 29,
                "type": "delivery"
            },
            {
                "id": 5,
                "x": 60,
                "y": 68,
                "location_index": 5,
                "capacity": 38,
                "type": "delivery"
            },
            {
                "id": 6,
                "x": 75,
                "y": 66,
                "location_index": 6,
                "capacity": 13,
                "type": "pickup"
            },
            {
                "id": 7,
                "x": 39,
                "y": 68,
                "location_index": 7,
                "capacity": 37,
                "type": "pickup"
            },
            {
                "id": 8,
                "x": 61,
                "y": 22,
                "location_index": 8,
                "capacity": 42,
                "type": "pickup"
            },
            {
                "id": 9,
                "x": 58,
                "y": 59,
                "location_index": 9,
                "capacity": 36,
                "type": "pickup"
            },
            {
                "id": 10,
                "x": 94,
                "y": 98,
                "location_index": 10,
                "capacity": 11,
                "type": "pickup"
            }
        ],
        "distance_matrix": [
            [
                0,
                58,
                103,
                33,
                49,
                90,
                99,
                78,
                64,
                82,
                135
            ],
            [
                58,
                0,
                48,
                31,
                42,
                34,
                41,
                31,
                21,
                25,
                78
            ],
            [
                103,
                48,
                0,
                79,
                88,
                38,
                25,
                57,
                39,
                36,
                51
            ],
            [
                33,
                31,
                79,
                0,
                21,
                59,
                70,
                45,
                47,
                52,
                104
            ],
            [
                49,
                42,
                88,
                21,
                0,
                59,
                73,
                39,
                63,
                54,
                102
            ],
            [
                90,
                34,
                38,
                59,
                59,
                0,
                15,
                21,
                46,
                9,
                45
            ],
            [
                99,
                41,
                25,
                70,
                73,
                15,
                0,
                36,
                46,
                18,
                37
            ],
            [
                78,
                31,
                57,
                45,
                39,
                21,
                36,
                0,
                50,
                21,
                62
            ],
            [
                64,
                21,
                39,
                47,
                63,
                46,
                46,
                50,
                0,
                37,
                82
            ],
            [
                82,
                25,
                36,
                52,
                54,
                9,
                18,
                21,
                37,
                0,
                53
            ],
            [
                135,
                78,
                51,
                104,
                102,
                45,
                37,
                62,
                82,
                53,
                0
            ]
        ]
    }

    output_with_5_delivery_5_pickup = {
        "cost": 363,
        "events": [
            {
                "id": 0,
                "x": 0,
                "y": 0,
                "location_index": 0,
                "capacity": 150,
                "type": "depot_start"
            },
            {
                "id": 3,
                "x": 14,
                "y": 30,
                "location_index": 3,
                "capacity": 20,
                "type": "delivery"
            },
            {
                "id": 4,
                "x": 4,
                "y": 49,
                "location_index": 4,
                "capacity": 29,
                "type": "delivery"
            },
            {
                "id": 7,
                "x": 39,
                "y": 68,
                "location_index": 7,
                "capacity": 37,
                "type": "pickup"
            },
            {
                "id": 5,
                "x": 60,
                "y": 68,
                "location_index": 5,
                "capacity": 38,
                "type": "delivery"
            },
            {
                "id": 10,
                "x": 94,
                "y": 98,
                "location_index": 10,
                "capacity": 11,
                "type": "pickup"
            },
            {
                "id": 2,
                "x": 92,
                "y": 47,
                "location_index": 2,
                "capacity": 38,
                "type": "delivery"
            },
            {
                "id": 6,
                "x": 75,
                "y": 66,
                "location_index": 6,
                "capacity": 13,
                "type": "pickup"
            },
            {
                "id": 9,
                "x": 58,
                "y": 59,
                "location_index": 9,
                "capacity": 36,
                "type": "pickup"
            },
            {
                "id": 1,
                "x": 45,
                "y": 37,
                "location_index": 1,
                "capacity": 25,
                "type": "delivery"
            },
            {
                "id": 8,
                "x": 61,
                "y": 22,
                "location_index": 8,
                "capacity": 42,
                "type": "pickup"
            },
            {
                "id": 0,
                "x": 0,
                "y": 0,
                "location_index": 0,
                "capacity": 139,
                "type": "depot_end"
            }
        ],
        "solver": "branch_and_bound"
    }
