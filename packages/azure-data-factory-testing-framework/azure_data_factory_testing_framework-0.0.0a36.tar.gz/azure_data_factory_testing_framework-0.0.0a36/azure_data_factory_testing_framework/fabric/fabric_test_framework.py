from typing import List

from azure_data_factory_testing_framework.exceptions.pipeline_activities_circular_dependency_error import (
    PipelineActivitiesCircularDependencyError,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_activity import FabricActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_control_activity import FabricControlActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_execute_pipeline_activity import (
    FabricExecutePipelineActivity,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_for_each_activity import FabricForEachActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_if_condition_activity import (
    FabricIfConditionActivity,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_until_activity import FabricUntilActivity
from azure_data_factory_testing_framework.fabric.models.fabric_pipeline import FabricPipeline
from azure_data_factory_testing_framework.fabric.models.repositories.fabric_repository_factory import (
    FabricRepositoryFactory,
)
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameter


class FabricTestFramework:
    def __init__(self, fabric_root_folder_path: str = None, should_evaluate_child_pipelines: bool = False) -> None:
        """Initializes the test framework allowing you to evaluate pipelines and activities.

        Args:
            fabric_root_folder_path: optional path to the folder containing the data factory files.
            The repository attribute will be populated with the data factory entities if provided.
            should_evaluate_child_pipelines: optional boolean indicating whether child pipelines should be evaluated. Defaults to False.
        """
        if fabric_root_folder_path is not None:
            self.repository = FabricRepositoryFactory.parse_from_folder(fabric_root_folder_path)
        else:
            self.repository = FabricRepositoryFactory([])

        self.should_evaluate_child_pipelines = should_evaluate_child_pipelines

    def evaluate_activity(self, activity: FabricActivity, state: PipelineRunState) -> List[FabricActivity]:
        """Evaluates a single activity given a state. Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activity: The activity to evaluate.
            state: The state to use for evaluating the activity.

        Returns:
             A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        return self.evaluate_activities([activity], state)

    def evaluate_pipeline(self, pipeline: FabricPipeline, parameters: List[RunParameter]) -> List[FabricActivity]:
        """Evaluates all pipeline activities using the provided parameters.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            pipeline: The pipeline to evaluate.
            parameters: The parameters to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        pipeline.validate_parameters(parameters)
        state = PipelineRunState(parameters, pipeline.get_run_variables())
        return self.evaluate_activities(pipeline.activities, state)

    def evaluate_activities(self, activities: List[FabricActivity], state: PipelineRunState) -> List[FabricActivity]:
        """Evaluates all activities using the provided state.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activities: The activities to evaluate.
            state: The state to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        while len(state.scoped_pipeline_activity_results) != len(activities):
            any_activity_evaluated = False
            for activity in filter(
                lambda a: a.name not in state.scoped_pipeline_activity_results
                and a.are_dependency_condition_met(state),
                activities,
            ):
                evaluated_activity = activity.evaluate(state)
                if not self._is_iteration_activity(evaluated_activity) or (
                    isinstance(evaluated_activity, FabricExecutePipelineActivity)
                    and not self.should_evaluate_child_pipelines
                ):
                    yield evaluated_activity

                any_activity_evaluated = True
                state.add_activity_result(activity.name, activity.status)

                if self._is_iteration_activity(activity):
                    if isinstance(activity, FabricExecutePipelineActivity) and self.should_evaluate_child_pipelines:
                        execute_pipeline_activity: FabricExecutePipelineActivity = activity
                        pipeline = self.repository.get_pipeline_by_name(
                            execute_pipeline_activity.pipeline.reference_name,
                        )

                        # Evaluate the pipeline with its own scope
                        for child_activity in self.evaluate_pipeline(
                            pipeline,
                            activity.get_child_run_parameters(state),
                        ):
                            yield child_activity

                    if isinstance(activity, FabricControlActivity):
                        control_activity: FabricControlActivity = activity
                        for child_activity in control_activity.evaluate_control_activity_iterations(
                            state,
                            self.evaluate_activities,
                        ):
                            yield child_activity

            if not any_activity_evaluated:
                raise PipelineActivitiesCircularDependencyError()

    @staticmethod
    def _is_iteration_activity(activity: FabricActivity) -> bool:
        return (
            isinstance(activity, FabricUntilActivity)
            or isinstance(activity, FabricForEachActivity)
            or isinstance(activity, FabricIfConditionActivity)
            or isinstance(activity, FabricExecutePipelineActivity)
        )
