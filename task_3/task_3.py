from typing import Dict, List, Tuple, Union


def compose_points(
    intervals: Dict[str, List[int]]
) -> List[Tuple[int, int, int]]:
    """ Compose points. """

    start_stop_indexes = []

    for jndex, interval_values in enumerate(intervals.values()):
        for index, timestamp in enumerate(interval_values):
            start_stop_indexes.append(
                (timestamp, 1 if index % 2 == 0 else -1, jndex)
            )

    start_stop_indexes.sort()
    return start_stop_indexes


def appearance(intervals: Dict[str, List[int]]) -> int:
    """ Calculate appearances. """

    start_stop_indexes = compose_points(intervals)

    common_time = 0
    part_time = 0
    indicator = 0
    present: Dict[int, int] = dict()
    for point in start_stop_indexes:
        indicator += point[1]
        if point[1] > 0:
            present[point[2]] = present.get(point[2], 0) + 1
        else:
            present[point[2]] = present.get(point[2], 0) - 1
        if (
            indicator > 2 and not part_time
            and all([present.get(0), present.get(1), present.get(2)])
        ):
            part_time = point[0]
        elif (
            (indicator == 2 or not all([present.get(0), present.get(2)]))
            and part_time
        ):
            common_time += abs(part_time-point[0])
            part_time = 0

    return common_time


if __name__ == '__main__':
    tests: List[Dict[str, Union[Dict[str, List[int]], int]]] = [
        {
            'data': {
                'lesson': [1594663200, 1594666800],
                'pupil': [
                    1594663340, 1594663389, 1594663390, 1594663395,
                    1594663396, 1594666472
                ],
                'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
            },
            'answer': 3117,
         },
        {
            'data': {
                'lesson': [1594702800, 1594706400],
                'pupil': [
                    1594702789, 1594704500, 1594702807, 1594704542,
                    1594704512, 1594704513, 1594704564, 1594705150,
                    1594704581, 1594704582, 1594704734, 1594705009,
                    1594705095, 1594705096, 1594705106, 1594706480,
                    1594705158, 1594705773, 1594705849, 1594706480,
                    1594706500, 1594706875, 1594706502, 1594706503,
                    1594706524, 1594706524, 1594706579, 1594706641
                ],
                'tutor': [
                    1594700035, 1594700364, 1594702749, 1594705148,
                    1594705149, 1594706463
                ]
            },
            'answer': 3577
         },

        {
            'data': {
                'lesson': [1594692000, 1594695600],
                'pupil': [1594692033, 1594696347],
                'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
            },
            'answer': 3565,
         },
    ]

    for index, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], (
            f'Error on test case {index}, got {test_answer}, '
            f'expected {test["answer"]}'
        )
