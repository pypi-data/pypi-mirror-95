from typing import List, Union, Dict, Set

from plomberie import Task
from plomberie.exceptions import CircularDependencyException


class Manager:
    def __init__(self):
        pass

    def launch(self, root_task: Task) -> None:
        dependency_map = self.__get_dependency_map(root_task)
        while dependency_map:
            ready_to_run = set(task for task, dependencies in dependency_map.items() if not dependencies)
            for task in ready_to_run:
                task.run()
            dependency_map = {
                task: dependencies - ready_to_run
                for task, dependencies in dependency_map.items() if dependencies
            }

    def __get_dependency_map(self, task: Task) -> Dict[Task, Set[Task]]:
        dependency_map: Dict[Task, Set[Task]] = {}
        tasks: Set[Task] = {task}
        while tasks:
            task = tasks.pop()
            dependencies = self.__get_dependencies(task)
            dependency_map[task] = dependencies
            self.__detect_circular_dependency(dependency_map)
            tasks.update(dependencies)
        return dependency_map

    # TODO: is there a more efficient way to detect circular dependencies?
    def __detect_circular_dependency(self, dependency_map: Dict[Task, Set[Task]]) -> None:
        for task, dependencies in dependency_map.items():
            dependency_stack = set(dependencies)
            while dependency_stack:
                dependency = dependency_stack.pop()
                if task == dependency:
                    raise CircularDependencyException()
                dependency_stack.update(self.__get_dependencies(dependency))

    @staticmethod
    def __get_dependencies(task: Task) -> Set[Task]:
        dependencies: Union[Task, List[Task]] = task.depends_on()
        if not dependencies:
            return set()
        return {dependencies} if isinstance(dependencies, Task) else set(dependencies)
