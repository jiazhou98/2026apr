# Problem: Task Scheduler with Subtasks and Deadline Updates
# Design and implement an online TaskScheduler. Each task has:

# id: a unique string identifier;
# deadline: an integer deadline;
# subtasks: optional list of task ids. When this task is consumed, all of its subtasks should also be marked as consumed.
# The scheduler supports the following operations.

# Operations
# ADD id deadline k sub1 sub2 ... subk

# Add a task with id id, deadline deadline, and k subtasks.
# If id has already been consumed, the add fails and outputs None.
# If id exists but has not been consumed, overwrite its deadline and subtask list, and output OK.
# Otherwise, add it and output OK.
# CONSUME

# Consume the unconsumed task with the smallest deadline.
# If there is a tie, consume the lexicographically smallest id.
# Output the consumed task id.
# Mark this task as consumed.
# If it has subtasks, mark all direct and indirect subtask ids as consumed as well. Even if a subtask has not been added yet, it is still recorded as consumed and cannot be added or updated later.
# If no task is available, output None.
# UPDATE id newDeadline

# If task id has already been consumed, output None.
# If task id does not exist, output None.
# Otherwise, update its deadline to newDeadline and output OK.
# Input Format
# The first line contains an integer q, the number of operations.

# Each of the next q lines is one operation:

# ADD id deadline k sub1 sub2 ... subk
# CONSUME
# UPDATE id newDeadline
# Output Format
# Print one line for each operation:

# ADD / UPDATE: print OK or None;
# CONSUME: print the consumed task id, or None if no task is available.
# Constraints
# 1 <= q <= 2 * 10^5
# Task ids and subtask ids are non-empty strings without spaces
# 0 <= deadline <= 10^9
# The total number of subtask references across all operations is at most 2 * 10^5
# Example
# Input:

# 6
# ADD 1 2 0
# ADD 2 1 0
# CONSUME
# UPDATE 1 5
# CONSUME
# CONSUME
# Output:

# OK
# OK
# 2
# OK
# 1
# None

from enum import Enum
import heapq


class Status(Enum):
    TODO = 1
    CONSUMED = 2
    DEPRECATED = 3


class Task:
    def __init__(self, taskid: str, ddl: int, subtasks: list[str]):
        self.taskid = taskid
        self.ddl = ddl
        self.subtasks = subtasks
        self.state = Status.TODO

    def __lt__(self, other):
        if self.ddl != other.ddl:
            return self.ddl < other.ddl
        return self.taskid < other.taskid


class TaskScheduler:
    def __init__(self):
        self.heap = []
        self.task_map = {}
        self.consumed = set()

    def add(self, task_id: str, deadline: int, subtasks: list[str]):
        if task_id in self.consumed:
            return None

        if task_id in self.task_map:
            self.task_map[task_id].state = Status.DEPRECATED

        new_task = Task(task_id, deadline, subtasks)
        self.task_map[task_id] = new_task
        heapq.heappush(self.heap, new_task)

        return "OK"

    def consume(self):
        while self.heap:
            top = self.heap[0]

            if top.state != Status.TODO or top.taskid in self.consumed:
                heapq.heappop(self.heap)
            else:
                break

        if not self.heap:
            return None

        task = heapq.heappop(self.heap)
        consumed_id = task.taskid

        self._consume_cascade(consumed_id)

        return consumed_id

    def _consume_cascade(self, task_id: str):
        stack = [task_id]

        while stack:
            cur_id = stack.pop()

            if cur_id in self.consumed:
                continue

            self.consumed.add(cur_id)

            if cur_id in self.task_map:
                cur_task = self.task_map[cur_id]
                cur_task.state = Status.CONSUMED

                for sub_id in cur_task.subtasks:
                    stack.append(sub_id)

    def update(self, task_id: str, deadline: int):
        if task_id in self.consumed:
            return None

        if task_id not in self.task_map:
            return None

        old_task = self.task_map[task_id]
        old_task.state = Status.DEPRECATED

        new_task = Task(task_id, deadline, old_task.subtasks)
        self.task_map[task_id] = new_task
        heapq.heappush(self.heap, new_task)

        return "OK"



