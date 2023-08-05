#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python-gantt-csv manages the arguments of gantt.Task in csv format and
resolves dependencies between tasks. You will be able to edit tasks
without worrying about the order in which you define them.


Author : Shota Horie - horie.shouta at gmail.com


Licence : GPL v3 or any later version


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import csv
import datetime
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

import gantt    # type: ignore


__author__ = 'Shota Horie (horie.shouta at gmail.com)'
__version__ = '0.3.0'


RESOURCES: dict = {}


class GanntCsvBaseException(Exception):
    """BaseException"""


class CantResolveDependencyError(GanntCsvBaseException):
    """When can not resolve dependency"""


class TaskArgs(NamedTuple):
    """Arguments for gantt.Task"""
    name: str
    start: str
    depends_of: Optional[Tuple[str, ...]]
    duration: int
    percent_done: int
    resources: str
    color: str
    id: str


class TaskArgsPair(NamedTuple):
    """Arguments for gantt.Task"""
    order: int
    task_args: TaskArgs


TaskArgsList = List[TaskArgs]
GanttResources = List[gantt.Resource]
TaskArgsPairs = List[TaskArgsPair]


def decode_start(start: str) -> datetime.date:
    """Decode start date string from iso format..

    Args:
        start (str): ISO format date string.
            Exceptionally, 'today' is accepted and returns today's date.

    Returns:
        datetime.date: The date the project starts

    Raises:
        ValueError: Raises when string format is invalid.
    """
    if start == "today":
        return datetime.date.today()

    match_isodate = re.compile(r"[\d]+-[\d]+-[\d]+")
    m = match_isodate.search(start)
    if m:
        yeay, month, day = [int(s) for s in start.split('-')]
        return datetime.date(yeay, month, day)
    raise ValueError(f'{start} must be hyphen separated string or "today".')


def decode_depends_of(depends_of: str) -> Optional[Tuple[str, ...]]:
    """Decode depends_of split by separator character."""
    SEPARATOR_CHARACTER = ':'
    if depends_of == "None":
        return None
    if not depends_of.count(SEPARATOR_CHARACTER):
        return (depends_of,)
    return tuple(depends_of.split(SEPARATOR_CHARACTER))


def decode_percent_done(percent_done: str) -> int:
    """Decode percent_done."""
    return int(percent_done)


def decode_duration(duration: str) -> int:
    """Decode duration."""
    return int(duration)


def decode_resources(resources: str) -> Optional[GanttResources]:
    """Decode resource names split by separator character
    and create Resource object.
    """
    SEPARATOR_CHARACTER = ':'
    if resources == 'None':
        return None
    if not resources.count(SEPARATOR_CHARACTER):
        return [get_resource(resources)]
    return [get_resource(key) for key in resources.split(SEPARATOR_CHARACTER)]


def decode(row: dict) -> dict:
    """Decode gantt_Task arguments form csv format."""
    new_row = row.copy()
    for key in row:
        if key == 'name':
            pass
        if key == 'start':
            new_row[key] = decode_start(row[key])
        if key == 'depends_of':
            new_row[key] = decode_depends_of(row[key])
        if key == 'duration':
            new_row[key] = decode_duration(row[key])
        if key == 'percent_done':
            new_row[key] = decode_percent_done(row[key])
        if key == 'resources':
            new_row[key] = decode_resources(row[key])
        if key == 'color':
            pass
        if key == 'id':
            pass
    return new_row


def get_task_by_id(id_: str,
                   task_args_pairs: TaskArgsPairs) -> Optional[TaskArgsPair]:
    """Get task by id."""
    for task_args_pair in task_args_pairs:
        if task_args_pair.task_args.id == id_:
            return task_args_pair
    return None


def get_dependent_tasks(dependent_ids: Tuple[str, ...],
                        task_args_pairs: TaskArgsPairs
                        ) -> TaskArgsPairs:
    """Get dependent tasks."""
    dependent_tasks = []
    for id_ in dependent_ids:
        task = get_task_by_id(id_, task_args_pairs)
        if task:
            dependent_tasks.append(task)
    return dependent_tasks


def get_highest_dependent_order(dependent_tasks: TaskArgsPairs) -> int:
    """Get highest order number."""
    dependent_orders = [task.order for task in dependent_tasks]
    return sorted(dependent_orders)[-1]


def set_task_order(task_args_pairs: TaskArgsPairs) -> TaskArgsPairs:
    """Set number to order objects.

    Args:
        task_args_pairs (TaskArgsPairs): Description

    Returns:
        TaskArgsPairs: A list of gantt.Task arguments with order

    Raises:
        ValueError: raised when depends_of id is not correct
    """
    new_task_args_pairs: TaskArgsPairs = []
    ref_task_args_pairs: TaskArgsPairs = task_args_pairs.copy()
    for task_args_pair in task_args_pairs:
        if task_args_pair.task_args.depends_of is None:
            new_task_args_pairs.append(task_args_pair)
            continue

        dependent_tasks = get_dependent_tasks(
            task_args_pair.task_args.depends_of, ref_task_args_pairs)

        if not dependent_tasks:
            id_ = task_args_pair.task_args.id
            name = task_args_pair.task_args.name
            depends_of = task_args_pair.task_args.depends_of
            raise ValueError(f"{name}({id_}) depends of {depends_of} "
                             "which is not exist.")

        highest_order = get_highest_dependent_order(dependent_tasks)
        new_order = (highest_order + 1, task_args_pair.task_args)
        new_pair = TaskArgsPair(*new_order)
        new_task_args_pairs.append(new_pair)

        # update reference
        old_task_index = ref_task_args_pairs.index(task_args_pair)
        _ = ref_task_args_pairs.pop(old_task_index)
        ref_task_args_pairs.insert(old_task_index, new_pair)

    return new_task_args_pairs


def sort_tasks_repeatedly(task_args_list: TaskArgsList) -> TaskArgsList:
    """Repeat until dependency is resolved.

    Args:
        task_args_list (TaskArgsList): A list of gantt.Task arguments

    Returns:
        TaskArgsList: A list of gantt.Task arguments
    """
    MAX_REPETITION = len(task_args_list)
    count = 0
    while not is_valid_order(task_args_list):
        task_args_list = sort_tasks(task_args_list)

        count += 1
        if count > MAX_REPETITION:
            break

    return task_args_list


def sort_tasks(task_args_list: TaskArgsList) -> TaskArgsList:
    """Order objects referenced by other objects so that they come first.

    Args:
        task_args_list (TaskArgsList): A list of gantt.Task arguments

    Returns:
        TaskArgsList: A sorted list of gantt.Task arguments
    """
    task_args_pairs = [TaskArgsPair(i, task_args)
                       for i, task_args in enumerate(task_args_list)]
    task_args_pairs = set_task_order(task_args_pairs)
    task_args_pairs.sort(key=lambda x: x.order)
    task_args_list = [pair.task_args for pair in task_args_pairs]
    return task_args_list


def create_task(task_args: TaskArgs,
                task_id_map: Dict[str, gantt.Task]) -> gantt.Task:
    """Create gantt.Task object and add to task_id_map in place.
    task_id_map is used to retrieve dependent tasks.
    """
    new_task_args = task_args._asdict()
    keys = ['name', 'start', 'depends_of', 'duration',
            'percent_done', 'resources', 'color']
    kw = {key: new_task_args[key] for key in keys}

    if kw["depends_of"] is not None:
        # Convert from id string to gantt.Task object
        try:
            kw["depends_of"] = [task_id_map[id_] for id_ in kw["depends_of"]]
        except KeyError as key_error:
            # Fix the sort logic to avoid this error.
            message = ("Can't resolve dependency. Please sort "
                       "dependent tasks so that they appear first. "
                       f"Put Id {task_args.id} "
                       f"after {', '.join(kw['depends_of'])}.")
            raise CantResolveDependencyError(message) from key_error
    return gantt.Task(**kw)


def create_tasks(task_args_list: TaskArgsList) -> List[gantt.Task]:
    """Create objects that are referenced by other objects first.

    Args:
        task_args_list (TaskArgsList): A list of gantt.Task arguments

    Returns:
        List[gantt.Task]: A list of gantt.Task
    """
    task_id_map: Dict[str, gantt.Task] = OrderedDict()
    for task_args in task_args_list:
        task_id_map[task_args.id] = create_task(task_args, task_id_map)
    return list(task_id_map.values())


def parse_csv_task(filename: Path) -> TaskArgsList:
    """Read the arguments from the csv file.

    Args:
        filename (Path): csv file path

    Returns:
        TaskArgsList: A list of gantt.Task arguments
    """
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = reader.__next__()
        for row in reader:
            data.append(parse_task_args_str(row, header))
    return data


def parse_task_args_str(row: list, header: list) -> TaskArgs:
    """Parse task arguments

    Args:
        row (list): task argument list
        header (list): task argument names

    Returns:
        TaskArgsList: A list of gantt.Task arguments
    """
    row_dict: Dict[str, str] = OrderedDict()
    row_dict.update(zip(header, row))
    return TaskArgs(**decode(row_dict))


def is_valid_order(task_args_list: TaskArgsList) -> bool:
    """Determine if the order is correct."""
    existings: set = set()
    for task_args in task_args_list:
        existings.add(task_args.id)
        if task_args.depends_of is None:
            continue

        dependants = set(task_args.depends_of)
        if not dependants.issubset(existings):
            return False
    return True


def create_project_from_csv(filename: Path) -> gantt.Project:
    """Create tasks from the arguments read from the csv file and
    organize them into a project.

    Args:
        filename (Path): csv file path

    Returns:
        gantt.Project: gantt.Project
    """
    # Create a project
    project = gantt.Project(name=filename.stem)

    # Load csv
    task_args_list = parse_csv_task(filename)

    # Sort tasks
    task_args_list = sort_tasks_repeatedly(task_args_list)

    # Create Tasks
    tasks = create_tasks(task_args_list)
    for task in tasks:
        project.add_task(task)
    return project


def get_resource(name: str) -> gantt.Resource:
    """The same name returns the same object

    Args:
        name (str): resource name

    Returns:
        gantt.Resource: Resources identified by name
    """
    if RESOURCES.get(name):
        return RESOURCES.get(name)

    RESOURCES[name] = gantt.Resource(name)
    return RESOURCES[name]
