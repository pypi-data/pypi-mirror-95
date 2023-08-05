# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetJobResult',
    'AwaitableGetJobResult',
    'get_job',
]

@pulumi.output_type
class GetJobResult:
    """
    Information about a Job.
    """
    def __init__(__self__, caffe2_settings=None, caffe_settings=None, chainer_settings=None, cluster=None, cntk_settings=None, constraints=None, container_settings=None, creation_time=None, custom_mpi_settings=None, custom_toolkit_settings=None, environment_variables=None, execution_info=None, execution_state=None, execution_state_transition_time=None, horovod_settings=None, id=None, input_directories=None, job_output_directory_path_segment=None, job_preparation=None, mount_volumes=None, name=None, node_count=None, output_directories=None, provisioning_state=None, provisioning_state_transition_time=None, py_torch_settings=None, scheduling_priority=None, secrets=None, std_out_err_path_prefix=None, tensor_flow_settings=None, tool_type=None, type=None):
        if caffe2_settings and not isinstance(caffe2_settings, dict):
            raise TypeError("Expected argument 'caffe2_settings' to be a dict")
        pulumi.set(__self__, "caffe2_settings", caffe2_settings)
        if caffe_settings and not isinstance(caffe_settings, dict):
            raise TypeError("Expected argument 'caffe_settings' to be a dict")
        pulumi.set(__self__, "caffe_settings", caffe_settings)
        if chainer_settings and not isinstance(chainer_settings, dict):
            raise TypeError("Expected argument 'chainer_settings' to be a dict")
        pulumi.set(__self__, "chainer_settings", chainer_settings)
        if cluster and not isinstance(cluster, dict):
            raise TypeError("Expected argument 'cluster' to be a dict")
        pulumi.set(__self__, "cluster", cluster)
        if cntk_settings and not isinstance(cntk_settings, dict):
            raise TypeError("Expected argument 'cntk_settings' to be a dict")
        pulumi.set(__self__, "cntk_settings", cntk_settings)
        if constraints and not isinstance(constraints, dict):
            raise TypeError("Expected argument 'constraints' to be a dict")
        pulumi.set(__self__, "constraints", constraints)
        if container_settings and not isinstance(container_settings, dict):
            raise TypeError("Expected argument 'container_settings' to be a dict")
        pulumi.set(__self__, "container_settings", container_settings)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if custom_mpi_settings and not isinstance(custom_mpi_settings, dict):
            raise TypeError("Expected argument 'custom_mpi_settings' to be a dict")
        pulumi.set(__self__, "custom_mpi_settings", custom_mpi_settings)
        if custom_toolkit_settings and not isinstance(custom_toolkit_settings, dict):
            raise TypeError("Expected argument 'custom_toolkit_settings' to be a dict")
        pulumi.set(__self__, "custom_toolkit_settings", custom_toolkit_settings)
        if environment_variables and not isinstance(environment_variables, list):
            raise TypeError("Expected argument 'environment_variables' to be a list")
        pulumi.set(__self__, "environment_variables", environment_variables)
        if execution_info and not isinstance(execution_info, dict):
            raise TypeError("Expected argument 'execution_info' to be a dict")
        pulumi.set(__self__, "execution_info", execution_info)
        if execution_state and not isinstance(execution_state, str):
            raise TypeError("Expected argument 'execution_state' to be a str")
        pulumi.set(__self__, "execution_state", execution_state)
        if execution_state_transition_time and not isinstance(execution_state_transition_time, str):
            raise TypeError("Expected argument 'execution_state_transition_time' to be a str")
        pulumi.set(__self__, "execution_state_transition_time", execution_state_transition_time)
        if horovod_settings and not isinstance(horovod_settings, dict):
            raise TypeError("Expected argument 'horovod_settings' to be a dict")
        pulumi.set(__self__, "horovod_settings", horovod_settings)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if input_directories and not isinstance(input_directories, list):
            raise TypeError("Expected argument 'input_directories' to be a list")
        pulumi.set(__self__, "input_directories", input_directories)
        if job_output_directory_path_segment and not isinstance(job_output_directory_path_segment, str):
            raise TypeError("Expected argument 'job_output_directory_path_segment' to be a str")
        pulumi.set(__self__, "job_output_directory_path_segment", job_output_directory_path_segment)
        if job_preparation and not isinstance(job_preparation, dict):
            raise TypeError("Expected argument 'job_preparation' to be a dict")
        pulumi.set(__self__, "job_preparation", job_preparation)
        if mount_volumes and not isinstance(mount_volumes, dict):
            raise TypeError("Expected argument 'mount_volumes' to be a dict")
        pulumi.set(__self__, "mount_volumes", mount_volumes)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if node_count and not isinstance(node_count, int):
            raise TypeError("Expected argument 'node_count' to be a int")
        pulumi.set(__self__, "node_count", node_count)
        if output_directories and not isinstance(output_directories, list):
            raise TypeError("Expected argument 'output_directories' to be a list")
        pulumi.set(__self__, "output_directories", output_directories)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if provisioning_state_transition_time and not isinstance(provisioning_state_transition_time, str):
            raise TypeError("Expected argument 'provisioning_state_transition_time' to be a str")
        pulumi.set(__self__, "provisioning_state_transition_time", provisioning_state_transition_time)
        if py_torch_settings and not isinstance(py_torch_settings, dict):
            raise TypeError("Expected argument 'py_torch_settings' to be a dict")
        pulumi.set(__self__, "py_torch_settings", py_torch_settings)
        if scheduling_priority and not isinstance(scheduling_priority, str):
            raise TypeError("Expected argument 'scheduling_priority' to be a str")
        pulumi.set(__self__, "scheduling_priority", scheduling_priority)
        if secrets and not isinstance(secrets, list):
            raise TypeError("Expected argument 'secrets' to be a list")
        pulumi.set(__self__, "secrets", secrets)
        if std_out_err_path_prefix and not isinstance(std_out_err_path_prefix, str):
            raise TypeError("Expected argument 'std_out_err_path_prefix' to be a str")
        pulumi.set(__self__, "std_out_err_path_prefix", std_out_err_path_prefix)
        if tensor_flow_settings and not isinstance(tensor_flow_settings, dict):
            raise TypeError("Expected argument 'tensor_flow_settings' to be a dict")
        pulumi.set(__self__, "tensor_flow_settings", tensor_flow_settings)
        if tool_type and not isinstance(tool_type, str):
            raise TypeError("Expected argument 'tool_type' to be a str")
        pulumi.set(__self__, "tool_type", tool_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="caffe2Settings")
    def caffe2_settings(self) -> Optional['outputs.Caffe2SettingsResponse']:
        """
        Caffe2 job settings.
        """
        return pulumi.get(self, "caffe2_settings")

    @property
    @pulumi.getter(name="caffeSettings")
    def caffe_settings(self) -> Optional['outputs.CaffeSettingsResponse']:
        """
        Caffe job settings.
        """
        return pulumi.get(self, "caffe_settings")

    @property
    @pulumi.getter(name="chainerSettings")
    def chainer_settings(self) -> Optional['outputs.ChainerSettingsResponse']:
        """
        Chainer job settings.
        """
        return pulumi.get(self, "chainer_settings")

    @property
    @pulumi.getter
    def cluster(self) -> Optional['outputs.ResourceIdResponse']:
        """
        Resource ID of the cluster associated with the job.
        """
        return pulumi.get(self, "cluster")

    @property
    @pulumi.getter(name="cntkSettings")
    def cntk_settings(self) -> Optional['outputs.CNTKsettingsResponse']:
        """
        CNTK (aka Microsoft Cognitive Toolkit) job settings.
        """
        return pulumi.get(self, "cntk_settings")

    @property
    @pulumi.getter
    def constraints(self) -> Optional['outputs.JobPropertiesResponseConstraints']:
        """
        Constraints associated with the Job.
        """
        return pulumi.get(self, "constraints")

    @property
    @pulumi.getter(name="containerSettings")
    def container_settings(self) -> Optional['outputs.ContainerSettingsResponse']:
        """
        If the container was downloaded as part of cluster setup then the same container image will be used. If not provided, the job will run on the VM.
        """
        return pulumi.get(self, "container_settings")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        The creation time of the job.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="customMpiSettings")
    def custom_mpi_settings(self) -> Optional['outputs.CustomMpiSettingsResponse']:
        """
        Custom MPI job settings.
        """
        return pulumi.get(self, "custom_mpi_settings")

    @property
    @pulumi.getter(name="customToolkitSettings")
    def custom_toolkit_settings(self) -> Optional['outputs.CustomToolkitSettingsResponse']:
        """
        Custom tool kit job settings.
        """
        return pulumi.get(self, "custom_toolkit_settings")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.EnvironmentVariableResponse']]:
        """
        A collection of user defined environment variables to be setup for the job.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="executionInfo")
    def execution_info(self) -> Optional['outputs.JobPropertiesResponseExecutionInfo']:
        """
        Information about the execution of a job.
        """
        return pulumi.get(self, "execution_info")

    @property
    @pulumi.getter(name="executionState")
    def execution_state(self) -> str:
        """
        The current state of the job. Possible values are: queued - The job is queued and able to run. A job enters this state when it is created, or when it is awaiting a retry after a failed run. running - The job is running on a compute cluster. This includes job-level preparation such as downloading resource files or set up container specified on the job - it does not necessarily mean that the job command line has started executing. terminating - The job is terminated by the user, the terminate operation is in progress. succeeded - The job has completed running successfully and exited with exit code 0. failed - The job has finished unsuccessfully (failed with a non-zero exit code) and has exhausted its retry limit. A job is also marked as failed if an error occurred launching the job.
        """
        return pulumi.get(self, "execution_state")

    @property
    @pulumi.getter(name="executionStateTransitionTime")
    def execution_state_transition_time(self) -> str:
        """
        The time at which the job entered its current execution state.
        """
        return pulumi.get(self, "execution_state_transition_time")

    @property
    @pulumi.getter(name="horovodSettings")
    def horovod_settings(self) -> Optional['outputs.HorovodSettingsResponse']:
        """
        Specifies the settings for Horovod job.
        """
        return pulumi.get(self, "horovod_settings")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inputDirectories")
    def input_directories(self) -> Optional[Sequence['outputs.InputDirectoryResponse']]:
        """
        A list of input directories for the job.
        """
        return pulumi.get(self, "input_directories")

    @property
    @pulumi.getter(name="jobOutputDirectoryPathSegment")
    def job_output_directory_path_segment(self) -> str:
        """
        A segment of job's output directories path created by Batch AI. Batch AI creates job's output directories under an unique path to avoid conflicts between jobs. This value contains a path segment generated by Batch AI to make the path unique and can be used to find the output directory on the node or mounted filesystem.
        """
        return pulumi.get(self, "job_output_directory_path_segment")

    @property
    @pulumi.getter(name="jobPreparation")
    def job_preparation(self) -> Optional['outputs.JobPreparationResponse']:
        """
        The specified actions will run on all the nodes that are part of the job
        """
        return pulumi.get(self, "job_preparation")

    @property
    @pulumi.getter(name="mountVolumes")
    def mount_volumes(self) -> Optional['outputs.MountVolumesResponse']:
        """
        Collection of mount volumes available to the job during execution. These volumes are mounted before the job execution and unmounted after the job completion. The volumes are mounted at location specified by $AZ_BATCHAI_JOB_MOUNT_ROOT environment variable.
        """
        return pulumi.get(self, "mount_volumes")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nodeCount")
    def node_count(self) -> Optional[int]:
        """
        The job will be gang scheduled on that many compute nodes
        """
        return pulumi.get(self, "node_count")

    @property
    @pulumi.getter(name="outputDirectories")
    def output_directories(self) -> Optional[Sequence['outputs.OutputDirectoryResponse']]:
        """
        A list of output directories for the job.
        """
        return pulumi.get(self, "output_directories")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioned state of the Batch AI job
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="provisioningStateTransitionTime")
    def provisioning_state_transition_time(self) -> str:
        """
        The time at which the job entered its current provisioning state.
        """
        return pulumi.get(self, "provisioning_state_transition_time")

    @property
    @pulumi.getter(name="pyTorchSettings")
    def py_torch_settings(self) -> Optional['outputs.PyTorchSettingsResponse']:
        """
        pyTorch job settings.
        """
        return pulumi.get(self, "py_torch_settings")

    @property
    @pulumi.getter(name="schedulingPriority")
    def scheduling_priority(self) -> Optional[str]:
        """
        Scheduling priority associated with the job.
        """
        return pulumi.get(self, "scheduling_priority")

    @property
    @pulumi.getter
    def secrets(self) -> Optional[Sequence['outputs.EnvironmentVariableWithSecretValueResponse']]:
        """
        A collection of user defined environment variables with secret values to be setup for the job. Server will never report values of these variables back.
        """
        return pulumi.get(self, "secrets")

    @property
    @pulumi.getter(name="stdOutErrPathPrefix")
    def std_out_err_path_prefix(self) -> Optional[str]:
        """
        The path where the Batch AI service stores stdout, stderror and execution log of the job.
        """
        return pulumi.get(self, "std_out_err_path_prefix")

    @property
    @pulumi.getter(name="tensorFlowSettings")
    def tensor_flow_settings(self) -> Optional['outputs.TensorFlowSettingsResponse']:
        """
        TensorFlow job settings.
        """
        return pulumi.get(self, "tensor_flow_settings")

    @property
    @pulumi.getter(name="toolType")
    def tool_type(self) -> Optional[str]:
        """
        Possible values are: cntk, tensorflow, caffe, caffe2, chainer, pytorch, custom, custommpi, horovod.
        """
        return pulumi.get(self, "tool_type")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetJobResult(GetJobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobResult(
            caffe2_settings=self.caffe2_settings,
            caffe_settings=self.caffe_settings,
            chainer_settings=self.chainer_settings,
            cluster=self.cluster,
            cntk_settings=self.cntk_settings,
            constraints=self.constraints,
            container_settings=self.container_settings,
            creation_time=self.creation_time,
            custom_mpi_settings=self.custom_mpi_settings,
            custom_toolkit_settings=self.custom_toolkit_settings,
            environment_variables=self.environment_variables,
            execution_info=self.execution_info,
            execution_state=self.execution_state,
            execution_state_transition_time=self.execution_state_transition_time,
            horovod_settings=self.horovod_settings,
            id=self.id,
            input_directories=self.input_directories,
            job_output_directory_path_segment=self.job_output_directory_path_segment,
            job_preparation=self.job_preparation,
            mount_volumes=self.mount_volumes,
            name=self.name,
            node_count=self.node_count,
            output_directories=self.output_directories,
            provisioning_state=self.provisioning_state,
            provisioning_state_transition_time=self.provisioning_state_transition_time,
            py_torch_settings=self.py_torch_settings,
            scheduling_priority=self.scheduling_priority,
            secrets=self.secrets,
            std_out_err_path_prefix=self.std_out_err_path_prefix,
            tensor_flow_settings=self.tensor_flow_settings,
            tool_type=self.tool_type,
            type=self.type)


def get_job(experiment_name: Optional[str] = None,
            job_name: Optional[str] = None,
            resource_group_name: Optional[str] = None,
            workspace_name: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobResult:
    """
    Use this data source to access information about an existing resource.

    :param str experiment_name: The name of the experiment. Experiment names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    :param str job_name: The name of the job within the specified resource group. Job names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str workspace_name: The name of the workspace. Workspace names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    """
    __args__ = dict()
    __args__['experimentName'] = experiment_name
    __args__['jobName'] = job_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:batchai:getJob', __args__, opts=opts, typ=GetJobResult).value

    return AwaitableGetJobResult(
        caffe2_settings=__ret__.caffe2_settings,
        caffe_settings=__ret__.caffe_settings,
        chainer_settings=__ret__.chainer_settings,
        cluster=__ret__.cluster,
        cntk_settings=__ret__.cntk_settings,
        constraints=__ret__.constraints,
        container_settings=__ret__.container_settings,
        creation_time=__ret__.creation_time,
        custom_mpi_settings=__ret__.custom_mpi_settings,
        custom_toolkit_settings=__ret__.custom_toolkit_settings,
        environment_variables=__ret__.environment_variables,
        execution_info=__ret__.execution_info,
        execution_state=__ret__.execution_state,
        execution_state_transition_time=__ret__.execution_state_transition_time,
        horovod_settings=__ret__.horovod_settings,
        id=__ret__.id,
        input_directories=__ret__.input_directories,
        job_output_directory_path_segment=__ret__.job_output_directory_path_segment,
        job_preparation=__ret__.job_preparation,
        mount_volumes=__ret__.mount_volumes,
        name=__ret__.name,
        node_count=__ret__.node_count,
        output_directories=__ret__.output_directories,
        provisioning_state=__ret__.provisioning_state,
        provisioning_state_transition_time=__ret__.provisioning_state_transition_time,
        py_torch_settings=__ret__.py_torch_settings,
        scheduling_priority=__ret__.scheduling_priority,
        secrets=__ret__.secrets,
        std_out_err_path_prefix=__ret__.std_out_err_path_prefix,
        tensor_flow_settings=__ret__.tensor_flow_settings,
        tool_type=__ret__.tool_type,
        type=__ret__.type)
