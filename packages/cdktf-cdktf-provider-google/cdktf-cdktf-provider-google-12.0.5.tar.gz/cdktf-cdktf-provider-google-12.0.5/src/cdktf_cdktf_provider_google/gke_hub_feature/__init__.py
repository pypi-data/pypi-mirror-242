'''
# `google_gke_hub_feature`

Refer to the Terraform Registory for docs: [`google_gke_hub_feature`](https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class GkeHubFeature(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeature",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature google_gke_hub_feature}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        fleet_default_member_config: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature google_gke_hub_feature} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15da6eaa3ff0c55b3dff385d70176ea2bd8835bf45ef327deb74c261fd6ac44a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubFeatureConfig(
            location=location,
            fleet_default_member_config=fleet_default_member_config,
            id=id,
            labels=labels,
            name=name,
            project=project,
            spec=spec,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GkeHubFeature resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubFeature to import.
        :param import_from_id: The id of the existing GkeHubFeature that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubFeature to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaea1ebfac8ca28455fa4c0f1b0f746f0c3797b35647135f50498c8df8812c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFleetDefaultMemberConfig")
    def put_fleet_default_member_config(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfig(
            configmanagement=configmanagement, mesh=mesh
        )

        return typing.cast(None, jsii.invoke(self, "putFleetDefaultMemberConfig", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        fleetobservability: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        '''
        value = GkeHubFeatureSpec(
            fleetobservability=fleetobservability,
            multiclusteringress=multiclusteringress,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.
        '''
        value = GkeHubFeatureTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFleetDefaultMemberConfig")
    def reset_fleet_default_member_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetDefaultMemberConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="fleetDefaultMemberConfig")
    def fleet_default_member_config(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigOutputReference", jsii.get(self, "fleetDefaultMemberConfig"))

    @builtins.property
    @jsii.member(jsii_name="resourceState")
    def resource_state(self) -> "GkeHubFeatureResourceStateList":
        return typing.cast("GkeHubFeatureResourceStateList", jsii.get(self, "resourceState"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GkeHubFeatureSpecOutputReference":
        return typing.cast("GkeHubFeatureSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubFeatureStateList":
        return typing.cast("GkeHubFeatureStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubFeatureTimeoutsOutputReference":
        return typing.cast("GkeHubFeatureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="fleetDefaultMemberConfigInput")
    def fleet_default_member_config_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"], jsii.get(self, "fleetDefaultMemberConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["GkeHubFeatureSpec"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae9a2ce391dcaa8ee000a5107c326540f8b9c30bea48ffb61b5cfdf21e4bda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c4356cc9f935ee9239eef88ebf69a26f09857659e653ec9afc97c6f1a3084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87906e5e9de78c2b73f818d12a9adc4ece5fdcb25a576b7c847697b305fdfbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86172f659954d4ad2a80245204f7c53fc1b655e13d03eba59c7731da1117141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922739c77119c248f5d1192543d5aff17fef63c95a65453f19cd71901acbfc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "fleet_default_member_config": "fleetDefaultMemberConfig",
        "id": "id",
        "labels": "labels",
        "name": "name",
        "project": "project",
        "spec": "spec",
        "timeouts": "timeouts",
    },
)
class GkeHubFeatureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: builtins.str,
        fleet_default_member_config: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fleet_default_member_config, dict):
            fleet_default_member_config = GkeHubFeatureFleetDefaultMemberConfig(**fleet_default_member_config)
        if isinstance(spec, dict):
            spec = GkeHubFeatureSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = GkeHubFeatureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a972c15bd6c1e15f9e9f64da9624d0c473d944f00af1591b7529f310c108616)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument fleet_default_member_config", value=fleet_default_member_config, expected_type=type_hints["fleet_default_member_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if fleet_default_member_config is not None:
            self._values["fleet_default_member_config"] = fleet_default_member_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if spec is not None:
            self._values["spec"] = spec
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_default_member_config(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"]:
        '''fleet_default_member_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        '''
        result = self._values.get("fleet_default_member_config")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''GCP labels for this Feature.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The full, unique name of this Feature resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["GkeHubFeatureSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GkeHubFeatureSpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubFeatureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubFeatureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfig",
    jsii_struct_bases=[],
    name_mapping={"configmanagement": "configmanagement", "mesh": "mesh"},
)
class GkeHubFeatureFleetDefaultMemberConfig:
    def __init__(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        '''
        if isinstance(configmanagement, dict):
            configmanagement = GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GkeHubFeatureFleetDefaultMemberConfigMesh(**mesh)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c6c3cb298d5d3abbba7b33fc9cea3023e11cac6602ef4726ff31d133391199)
            check_type(argname="argument configmanagement", value=configmanagement, expected_type=type_hints["configmanagement"])
            check_type(argname="argument mesh", value=mesh, expected_type=type_hints["mesh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configmanagement is not None:
            self._values["configmanagement"] = configmanagement
        if mesh is not None:
            self._values["mesh"] = mesh

    @builtins.property
    def configmanagement(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement"], result)

    @builtins.property
    def mesh(self) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigMesh"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    jsii_struct_bases=[],
    name_mapping={"config_sync": "configSync"},
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagement:
    def __init__(
        self,
        *,
        config_sync: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        '''
        if isinstance(config_sync, dict):
            config_sync = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(**config_sync)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b2618b3fdf90fc25064fbb89ebddfdaa38c42afff93f3abdc040773f5ee8ea)
            check_type(argname="argument config_sync", value=config_sync, expected_type=type_hints["config_sync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_sync is not None:
            self._values["config_sync"] = config_sync

    @builtins.property
    def config_sync(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
    jsii_struct_bases=[],
    name_mapping={"git": "git", "oci": "oci", "source_format": "sourceFormat"},
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        git: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        oci: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        if isinstance(git, dict):
            git = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c0aea23d86f0a5e0b6e17a11161be2637487e29297ebb1b70f545ad223a337)
            check_type(argname="argument git", value=git, expected_type=type_hints["git"])
            check_type(argname="argument oci", value=oci, expected_type=type_hints["oci"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if git is not None:
            self._values["git"] = git
        if oci is not None:
            self._values["oci"] = oci
        if source_format is not None:
            self._values["source_format"] = source_format

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in hierarchical or unstructured mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
    jsii_struct_bases=[],
    name_mapping={
        "secret_type": "secretType",
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "https_proxy": "httpsProxy",
        "policy_dir": "policyDir",
        "sync_branch": "syncBranch",
        "sync_repo": "syncRepo",
        "sync_rev": "syncRev",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit:
    def __init__(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c84c552a77e21b661dc33c9bf0f36cf74727c9adf91b4d2601ab26a2c27556)
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument sync_branch", value=sync_branch, expected_type=type_hints["sync_branch"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_rev", value=sync_rev, expected_type=type_hints["sync_rev"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_type": secret_type,
        }
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if sync_branch is not None:
            self._values["sync_branch"] = sync_branch
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_rev is not None:
            self._values["sync_rev"] = sync_rev
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def secret_type(self) -> builtins.str:
        '''Type of secret configured for access to the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS Proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff91e5395c7d8494383f90cd73c09d2dd8b49f8b0408245612c2b52b9815babc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSyncBranch")
    def reset_sync_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncBranch", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncRev")
    def reset_sync_rev(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRev", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncBranchInput")
    def sync_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRevInput")
    def sync_rev_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRevInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196b0d51f9f540fe5bc003f1a4a3f5f830a78f245d58b6df67a8291babedd3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value)

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b40806f21bec7a33a3d0a05adc0db6118625cea44a8ed6e7f93c17938cacbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value)

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787a7c1a4723d01285e104ffc9a78e7c0fc4878f37dfa1b7c033a4647f59d339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value)

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55d2b640c416d2540e2b93c5d6420d7642ec244062ce1819f1962ddb0a343d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value)

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5515e78bff91ea3fb4fe1bcb228d6579445fb10a28bdd077e74e40b2f0b81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value)

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41515055982a396422d049350ebb71da25079c1e73696caa73461890b0467bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value)

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8216d27dda54e295217b0a394961ae66152058b7f93adc6c4a18471bed346862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value)

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c2a3cc7605b23f3132ed161966b87a9c1677f4fc79584b44168df3e8c646e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdd6231f4960552f423fbff7d1fc3c8ebc66edccb859514c866c5876b6c0dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
    jsii_struct_bases=[],
    name_mapping={
        "secret_type": "secretType",
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "policy_dir": "policyDir",
        "sync_repo": "syncRepo",
        "sync_wait_secs": "syncWaitSecs",
        "version": "version",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci:
    def __init__(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        :param version: Version of ACM installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce9168f80bcbf2ed6498d161e113a23c96a174d7f2ebd50d3fd19c0bc5180d0)
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_type": secret_type,
        }
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def secret_type(self) -> builtins.str:
        '''Type of secret configured for access to the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of ACM installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c15e3ca25981c7f03e2408f1ac7a88101b6a3cebd01fb356eea913dd96892b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21ec10a1a4ba51ef2af5fec57de8407c6721ed69dd52aa9e03a4b07fbc762b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value)

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d5997a29f7a9eed5397903e2a0630110e9d3a9ef9503bd2a4fe6a166593de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value)

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2308501d92e0f66a791e4d27daddfd971712e3a1034dd35a5e98810a5eea6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value)

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0925139c6ba0bd061b4ae3c8e19e7eea4c89fd800a55b8d8e638e59bef70ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value)

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c1d3c4621f9d7c9f1a2aca9621a651d5f5027c7e314896431269896fdfedd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c2299add112fd41088c3fb23b0e5d70ab93879bdb52c2e1ec3665e6a259868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323b074cd209eb6944e126eb1514a94dac1f8ce03c40a2bab080388f6be6bc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10866afd9d433a8facfa7d40612b05ad041b1bc7563026466a83f65fa3e15b38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGit")
    def put_git(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(
            secret_type=secret_type,
            gcp_service_account_email=gcp_service_account_email,
            https_proxy=https_proxy,
            policy_dir=policy_dir,
            sync_branch=sync_branch,
            sync_repo=sync_repo,
            sync_rev=sync_rev,
            sync_wait_secs=sync_wait_secs,
        )

        return typing.cast(None, jsii.invoke(self, "putGit", [value]))

    @jsii.member(jsii_name="putOci")
    def put_oci(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        :param version: Version of ACM installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(
            secret_type=secret_type,
            gcp_service_account_email=gcp_service_account_email,
            policy_dir=policy_dir,
            sync_repo=sync_repo,
            sync_wait_secs=sync_wait_secs,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putOci", [value]))

    @jsii.member(jsii_name="resetGit")
    def reset_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGit", []))

    @jsii.member(jsii_name="resetOci")
    def reset_oci(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOci", []))

    @jsii.member(jsii_name="resetSourceFormat")
    def reset_source_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFormat", []))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

    @builtins.property
    @jsii.member(jsii_name="gitInput")
    def git_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0005589a138e2476a6d151250eda755a236b9174826dce767021f5d8d1fd5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df7297b9140068ea436f0d9e8c411e74ff63b0ea1e3bac1b259544f76e75f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5e528563f1854bc24f47208a109ce6d765fefe5b5b1d8c9d20b42d1a90d5a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        git: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        oci: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(
            git=git, oci=oci, source_format=source_format
        )

        return typing.cast(None, jsii.invoke(self, "putConfigSync", [value]))

    @jsii.member(jsii_name="resetConfigSync")
    def reset_config_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigSync", []))

    @builtins.property
    @jsii.member(jsii_name="configSync")
    def config_sync(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bcde01ed2bc266b78a27d6599b009218e3e8edaf01d1a37d49fab108ae1b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigMesh",
    jsii_struct_bases=[],
    name_mapping={"management": "management"},
)
class GkeHubFeatureFleetDefaultMemberConfigMesh:
    def __init__(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70aa677d42337c252333b2bb6e9e543e1628acdd851dcfa2b3198a55dcb8e09)
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management": management,
        }

    @builtins.property
    def management(self) -> builtins.str:
        '''Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        result = self._values.get("management")
        assert result is not None, "Required property 'management' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed1734dd7111c9c92f93bd59b8e880bc995fe09f06001bb6ce8b06158bc6d14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9e2e90cf66625ffb49d6e97ac3e92eba6b16fb920507b37e1c6f7d07cd59ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f31e7c0a95ca8fd5449f298e72bbcc8be66ccc4710cedddf99847b219999a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureFleetDefaultMemberConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee1feb5904aedc22f8e0941935b9df22576374ea2ba206d55bed9109d999bc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        config_sync: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(
            config_sync=config_sync
        )

        return typing.cast(None, jsii.invoke(self, "putConfigmanagement", [value]))

    @jsii.member(jsii_name="putMesh")
    def put_mesh(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigMesh(management=management)

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="resetConfigmanagement")
    def reset_configmanagement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigmanagement", []))

    @jsii.member(jsii_name="resetMesh")
    def reset_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMesh", []))

    @builtins.property
    @jsii.member(jsii_name="configmanagement")
    def configmanagement(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference, jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference, jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "configmanagementInput"))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(self) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfcbef1a6482f9561f8124ac2c93a3bd22c7b53e212f7c4bf06552a7d9e8612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureResourceState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureResourceState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureResourceStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceStateList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fa5def0c74b8743eb9dde5b12030b076d80f4991a1b7cb4ac34f6e941bb2f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureResourceStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169e4dbd3e43a7981594669bdccb7718cef6c8c85402578e2ec5b7ece57b8af3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureResourceStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e90d2820e7dd4f098245f37a003b5de2956ec80f4c1248e1674d643af918857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6376c67b67fb947da465a31a757336f1ffe10f32c58c4a2ac52ddf911da9cb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaef58b50a8ece292d1202c1fa9c1b4833922d8bc5445706a29e38808cec8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class GkeHubFeatureResourceStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceStateOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9b755f910d09e2cc696919bb5bf80e0cbea3b02a17dfa4b51c8ab6b7f57016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hasResources")
    def has_resources(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasResources"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureResourceState]:
        return typing.cast(typing.Optional[GkeHubFeatureResourceState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureResourceState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0301590450c6283eebb008508d183857209ec55a5ae10acc873fc46846ae2e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "fleetobservability": "fleetobservability",
        "multiclusteringress": "multiclusteringress",
    },
)
class GkeHubFeatureSpec:
    def __init__(
        self,
        *,
        fleetobservability: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        '''
        if isinstance(fleetobservability, dict):
            fleetobservability = GkeHubFeatureSpecFleetobservability(**fleetobservability)
        if isinstance(multiclusteringress, dict):
            multiclusteringress = GkeHubFeatureSpecMulticlusteringress(**multiclusteringress)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a716320b8f8b882d1cad6fcfc3c62e854fb6fab48035624c314bc71304c2453b)
            check_type(argname="argument fleetobservability", value=fleetobservability, expected_type=type_hints["fleetobservability"])
            check_type(argname="argument multiclusteringress", value=multiclusteringress, expected_type=type_hints["multiclusteringress"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fleetobservability is not None:
            self._values["fleetobservability"] = fleetobservability
        if multiclusteringress is not None:
            self._values["multiclusteringress"] = multiclusteringress

    @builtins.property
    def fleetobservability(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservability"]:
        '''fleetobservability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        '''
        result = self._values.get("fleetobservability")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservability"], result)

    @builtins.property
    def multiclusteringress(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecMulticlusteringress"]:
        '''multiclusteringress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        '''
        result = self._values.get("multiclusteringress")
        return typing.cast(typing.Optional["GkeHubFeatureSpecMulticlusteringress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservability",
    jsii_struct_bases=[],
    name_mapping={"logging_config": "loggingConfig"},
)
class GkeHubFeatureSpecFleetobservability:
    def __init__(
        self,
        *,
        logging_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        if isinstance(logging_config, dict):
            logging_config = GkeHubFeatureSpecFleetobservabilityLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030a905466c4f9658d40701158addfebf98ef14c6c84a43cdd13d5ba7a55670b)
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_config": "defaultConfig",
        "fleet_scope_logs_config": "fleetScopeLogsConfig",
    },
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfig:
    def __init__(
        self,
        *,
        default_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        if isinstance(default_config, dict):
            default_config = GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(**default_config)
        if isinstance(fleet_scope_logs_config, dict):
            fleet_scope_logs_config = GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(**fleet_scope_logs_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052b23094a3454b7a310041016ec2a7c7ba987f03eacf5ac5a28c8328074811e)
            check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
            check_type(argname="argument fleet_scope_logs_config", value=fleet_scope_logs_config, expected_type=type_hints["fleet_scope_logs_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_config is not None:
            self._values["default_config"] = default_config
        if fleet_scope_logs_config is not None:
            self._values["fleet_scope_logs_config"] = fleet_scope_logs_config

    @builtins.property
    def default_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"]:
        '''default_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        '''
        result = self._values.get("default_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"], result)

    @builtins.property
    def fleet_scope_logs_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"]:
        '''fleet_scope_logs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        result = self._values.get("fleet_scope_logs_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f07004b1ba6f1f8d8210a6d8f55a5b9e71793ea2dd271410e09057bf670ce)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eefa415f8be9ad5f0084e817c76a09dfcd7f3d4ebc38d5c8d8005bf3ca26347)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b36e41c88ff90e7c3ac695aaa0d8a66814ac975ea59594c975ce23ec284dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abb6ffe810d324d665591d0e1dc7deeb2de562a5571ecfafa46e3ed8801e8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cdac985bb9fb598a09f83796f0d95e39afb6c9258d8a3f9b900ff953ba91a5)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d8228dc60e23fa3ca020047c75c220dbb36cdcf72e723161170edb0817fd0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d5864bccefcbd7788e4cf6385173e4cafc7cde89842f64b6035871d08d2dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19855e3fa053dde6fb0ff5978dc5bdc59eff9aa0a1c445915bbb3dc3bdba55a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d845075062d30d7e7f9f6a20d4a519ea3dd3c5b2bd23e55ac16814d01a83f188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultConfig")
    def put_default_config(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(
            mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultConfig", [value]))

    @jsii.member(jsii_name="putFleetScopeLogsConfig")
    def put_fleet_scope_logs_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(
            mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putFleetScopeLogsConfig", [value]))

    @jsii.member(jsii_name="resetDefaultConfig")
    def reset_default_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultConfig", []))

    @jsii.member(jsii_name="resetFleetScopeLogsConfig")
    def reset_fleet_scope_logs_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetScopeLogsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="defaultConfig")
    def default_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference, jsii.get(self, "defaultConfig"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfig")
    def fleet_scope_logs_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference, jsii.get(self, "fleetScopeLogsConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultConfigInput")
    def default_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "defaultConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfigInput")
    def fleet_scope_logs_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "fleetScopeLogsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eefb77c01d055b0e63a5526402c6a1a51e3434075a2c39d13f641b987098b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureSpecFleetobservabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb4c97d07dd08c1bd71296d80b57fadaffa68ec990d5d377d04725e7b97412c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        default_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfig(
            default_config=default_config,
            fleet_scope_logs_config=fleet_scope_logs_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27a2569d413f9d62089e0030491958ab16fcc8141fbae5bec1cdd5f53342a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecMulticlusteringress",
    jsii_struct_bases=[],
    name_mapping={"config_membership": "configMembership"},
)
class GkeHubFeatureSpecMulticlusteringress:
    def __init__(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42001b933a09bfedcafd2135e2449a44c8b807f8de748095bcca334fd6e37a1)
            check_type(argname="argument config_membership", value=config_membership, expected_type=type_hints["config_membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_membership": config_membership,
        }

    @builtins.property
    def config_membership(self) -> builtins.str:
        '''Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        result = self._values.get("config_membership")
        assert result is not None, "Required property 'config_membership' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecMulticlusteringress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecMulticlusteringressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecMulticlusteringressOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e787769b7a1016f6952abb8601447de6098f294856b79bae4749ab46b10b75d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="configMembershipInput")
    def config_membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configMembershipInput"))

    @builtins.property
    @jsii.member(jsii_name="configMembership")
    def config_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configMembership"))

    @config_membership.setter
    def config_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3bd2b56883c6f3693de74d0998420c8e5f70cec3de660eeb795d5876487e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configMembership", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecMulticlusteringress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecMulticlusteringress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a5845702568e545287521eb4cd522f450b7df32043774f3410e63faf03a0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GkeHubFeatureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39987c2a69b04624c5f234f3f934c5a5ab7e6ef463c757767db320c09d73bdba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFleetobservability")
    def put_fleetobservability(
        self,
        *,
        logging_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        value = GkeHubFeatureSpecFleetobservability(logging_config=logging_config)

        return typing.cast(None, jsii.invoke(self, "putFleetobservability", [value]))

    @jsii.member(jsii_name="putMulticlusteringress")
    def put_multiclusteringress(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        value = GkeHubFeatureSpecMulticlusteringress(
            config_membership=config_membership
        )

        return typing.cast(None, jsii.invoke(self, "putMulticlusteringress", [value]))

    @jsii.member(jsii_name="resetFleetobservability")
    def reset_fleetobservability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetobservability", []))

    @jsii.member(jsii_name="resetMulticlusteringress")
    def reset_multiclusteringress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMulticlusteringress", []))

    @builtins.property
    @jsii.member(jsii_name="fleetobservability")
    def fleetobservability(self) -> GkeHubFeatureSpecFleetobservabilityOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityOutputReference, jsii.get(self, "fleetobservability"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringress")
    def multiclusteringress(
        self,
    ) -> GkeHubFeatureSpecMulticlusteringressOutputReference:
        return typing.cast(GkeHubFeatureSpecMulticlusteringressOutputReference, jsii.get(self, "multiclusteringress"))

    @builtins.property
    @jsii.member(jsii_name="fleetobservabilityInput")
    def fleetobservability_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservability], jsii.get(self, "fleetobservabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringressInput")
    def multiclusteringress_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecMulticlusteringress], jsii.get(self, "multiclusteringressInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpec]:
        return typing.cast(typing.Optional[GkeHubFeatureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8d8fa0eab991fd969df830414c08fea85d71a97075b940824875cddddda560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a24cda2552f89ea775c9ffc65f2c0d0c35caf4e7c7a7ffad8f87fa96ea2159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45448dda26a2061969daf29a989b088aa27d4bf4407c6ce7e21b3030355fe26c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3737c59ce12a8e1bc5d7484507e1729fef47944a49ed18a599192efa9df091f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a547b379a8e7b218b291197b37e794805cf23ead34d227e6a90cb734c565ba00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17300cad930d1605c5bf21980a0e6522a4d4a3c29b79ec3f2857c4dd82c16e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class GkeHubFeatureStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209a2a3497d66f97f3799730c0741e9854a7cb044c80973f3010e807ec8dc864)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubFeatureStateStateList":
        return typing.cast("GkeHubFeatureStateStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureState]:
        return typing.cast(typing.Optional[GkeHubFeatureState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a4b5463573e3596c2418486fd0c5d64039cd4e23fa475eaf7880dc3f10535f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureStateState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureStateState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureStateStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateStateList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc070dd9ef24311bd600f204701b63923e80dc51075755a10d27ee2056271a6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureStateStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a60b7232d286898e96c0f89aaf766b7f2604e7fa451ebcf5bc428fef6b6ce7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureStateStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72eeb9c5c491886ee3a0f76920b2be92b6db291d80b5a491fa3a1fd69f8fe30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f67886f891b39422f70a8882e4d651e4189e55183855dec13a7d40d7b193777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c470d04d92bb6a6388776232ed7338fcec64c389b99929eb48f85f84333fb6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class GkeHubFeatureStateStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateStateOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1d91a8d54c84d61f80ea6cd8788ef3871449fa15aeddada9e9b50f822c5d71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureStateState]:
        return typing.cast(typing.Optional[GkeHubFeatureStateState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureStateState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1213261b9efa354ff823baa647b452b75f2a2f72c74e30297547cbaf888e92c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubFeatureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf89b32285c28e02e496862b4900cced96d984060b303179a8af09c5f45a8e83)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.7.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa96931188e82b4d32061d7d49abb25b81d966a4a43568d69480a7f41ef3a828)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a99e9f6faca5ec732456bf1268e1bbb8c1dcce0b7b5abb6d2af0d7eb313a0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695232b98c003b755334fd66d011ec42779f5b5bb17b050396ab97640305e7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2012273f21a1b1460fbd0a640e059067a6e84a431e11df4a639de8a74a3883e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a999d1e826cd91ca7848d0f14250a8b6cce08065cb7ab3bf7b3779673777876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GkeHubFeature",
    "GkeHubFeatureConfig",
    "GkeHubFeatureFleetDefaultMemberConfig",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigMesh",
    "GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigOutputReference",
    "GkeHubFeatureResourceState",
    "GkeHubFeatureResourceStateList",
    "GkeHubFeatureResourceStateOutputReference",
    "GkeHubFeatureSpec",
    "GkeHubFeatureSpecFleetobservability",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityOutputReference",
    "GkeHubFeatureSpecMulticlusteringress",
    "GkeHubFeatureSpecMulticlusteringressOutputReference",
    "GkeHubFeatureSpecOutputReference",
    "GkeHubFeatureState",
    "GkeHubFeatureStateList",
    "GkeHubFeatureStateOutputReference",
    "GkeHubFeatureStateState",
    "GkeHubFeatureStateStateList",
    "GkeHubFeatureStateStateOutputReference",
    "GkeHubFeatureTimeouts",
    "GkeHubFeatureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__15da6eaa3ff0c55b3dff385d70176ea2bd8835bf45ef327deb74c261fd6ac44a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaea1ebfac8ca28455fa4c0f1b0f746f0c3797b35647135f50498c8df8812c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae9a2ce391dcaa8ee000a5107c326540f8b9c30bea48ffb61b5cfdf21e4bda2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c4356cc9f935ee9239eef88ebf69a26f09857659e653ec9afc97c6f1a3084(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87906e5e9de78c2b73f818d12a9adc4ece5fdcb25a576b7c847697b305fdfbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86172f659954d4ad2a80245204f7c53fc1b655e13d03eba59c7731da1117141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922739c77119c248f5d1192543d5aff17fef63c95a65453f19cd71901acbfc37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a972c15bd6c1e15f9e9f64da9624d0c473d944f00af1591b7529f310c108616(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c6c3cb298d5d3abbba7b33fc9cea3023e11cac6602ef4726ff31d133391199(
    *,
    configmanagement: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    mesh: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigMesh, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b2618b3fdf90fc25064fbb89ebddfdaa38c42afff93f3abdc040773f5ee8ea(
    *,
    config_sync: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c0aea23d86f0a5e0b6e17a11161be2637487e29297ebb1b70f545ad223a337(
    *,
    git: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    oci: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    source_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c84c552a77e21b661dc33c9bf0f36cf74727c9adf91b4d2601ab26a2c27556(
    *,
    secret_type: builtins.str,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    sync_branch: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_rev: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff91e5395c7d8494383f90cd73c09d2dd8b49f8b0408245612c2b52b9815babc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196b0d51f9f540fe5bc003f1a4a3f5f830a78f245d58b6df67a8291babedd3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b40806f21bec7a33a3d0a05adc0db6118625cea44a8ed6e7f93c17938cacbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a7c1a4723d01285e104ffc9a78e7c0fc4878f37dfa1b7c033a4647f59d339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55d2b640c416d2540e2b93c5d6420d7642ec244062ce1819f1962ddb0a343d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5515e78bff91ea3fb4fe1bcb228d6579445fb10a28bdd077e74e40b2f0b81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41515055982a396422d049350ebb71da25079c1e73696caa73461890b0467bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8216d27dda54e295217b0a394961ae66152058b7f93adc6c4a18471bed346862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c2a3cc7605b23f3132ed161966b87a9c1677f4fc79584b44168df3e8c646e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdd6231f4960552f423fbff7d1fc3c8ebc66edccb859514c866c5876b6c0dac(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce9168f80bcbf2ed6498d161e113a23c96a174d7f2ebd50d3fd19c0bc5180d0(
    *,
    secret_type: builtins.str,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c15e3ca25981c7f03e2408f1ac7a88101b6a3cebd01fb356eea913dd96892b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21ec10a1a4ba51ef2af5fec57de8407c6721ed69dd52aa9e03a4b07fbc762b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d5997a29f7a9eed5397903e2a0630110e9d3a9ef9503bd2a4fe6a166593de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2308501d92e0f66a791e4d27daddfd971712e3a1034dd35a5e98810a5eea6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0925139c6ba0bd061b4ae3c8e19e7eea4c89fd800a55b8d8e638e59bef70ff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c1d3c4621f9d7c9f1a2aca9621a651d5f5027c7e314896431269896fdfedd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c2299add112fd41088c3fb23b0e5d70ab93879bdb52c2e1ec3665e6a259868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323b074cd209eb6944e126eb1514a94dac1f8ce03c40a2bab080388f6be6bc4d(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10866afd9d433a8facfa7d40612b05ad041b1bc7563026466a83f65fa3e15b38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0005589a138e2476a6d151250eda755a236b9174826dce767021f5d8d1fd5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df7297b9140068ea436f0d9e8c411e74ff63b0ea1e3bac1b259544f76e75f20(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5e528563f1854bc24f47208a109ce6d765fefe5b5b1d8c9d20b42d1a90d5a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bcde01ed2bc266b78a27d6599b009218e3e8edaf01d1a37d49fab108ae1b4e(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70aa677d42337c252333b2bb6e9e543e1628acdd851dcfa2b3198a55dcb8e09(
    *,
    management: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed1734dd7111c9c92f93bd59b8e880bc995fe09f06001bb6ce8b06158bc6d14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9e2e90cf66625ffb49d6e97ac3e92eba6b16fb920507b37e1c6f7d07cd59ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f31e7c0a95ca8fd5449f298e72bbcc8be66ccc4710cedddf99847b219999a2(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee1feb5904aedc22f8e0941935b9df22576374ea2ba206d55bed9109d999bc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfcbef1a6482f9561f8124ac2c93a3bd22c7b53e212f7c4bf06552a7d9e8612(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fa5def0c74b8743eb9dde5b12030b076d80f4991a1b7cb4ac34f6e941bb2f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169e4dbd3e43a7981594669bdccb7718cef6c8c85402578e2ec5b7ece57b8af3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e90d2820e7dd4f098245f37a003b5de2956ec80f4c1248e1674d643af918857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376c67b67fb947da465a31a757336f1ffe10f32c58c4a2ac52ddf911da9cb1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaef58b50a8ece292d1202c1fa9c1b4833922d8bc5445706a29e38808cec8bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9b755f910d09e2cc696919bb5bf80e0cbea3b02a17dfa4b51c8ab6b7f57016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0301590450c6283eebb008508d183857209ec55a5ae10acc873fc46846ae2e7d(
    value: typing.Optional[GkeHubFeatureResourceState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a716320b8f8b882d1cad6fcfc3c62e854fb6fab48035624c314bc71304c2453b(
    *,
    fleetobservability: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservability, typing.Dict[builtins.str, typing.Any]]] = None,
    multiclusteringress: typing.Optional[typing.Union[GkeHubFeatureSpecMulticlusteringress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030a905466c4f9658d40701158addfebf98ef14c6c84a43cdd13d5ba7a55670b(
    *,
    logging_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052b23094a3454b7a310041016ec2a7c7ba987f03eacf5ac5a28c8328074811e(
    *,
    default_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fleet_scope_logs_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f07004b1ba6f1f8d8210a6d8f55a5b9e71793ea2dd271410e09057bf670ce(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eefa415f8be9ad5f0084e817c76a09dfcd7f3d4ebc38d5c8d8005bf3ca26347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b36e41c88ff90e7c3ac695aaa0d8a66814ac975ea59594c975ce23ec284dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abb6ffe810d324d665591d0e1dc7deeb2de562a5571ecfafa46e3ed8801e8e3(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cdac985bb9fb598a09f83796f0d95e39afb6c9258d8a3f9b900ff953ba91a5(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d8228dc60e23fa3ca020047c75c220dbb36cdcf72e723161170edb0817fd0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d5864bccefcbd7788e4cf6385173e4cafc7cde89842f64b6035871d08d2dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19855e3fa053dde6fb0ff5978dc5bdc59eff9aa0a1c445915bbb3dc3bdba55a3(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d845075062d30d7e7f9f6a20d4a519ea3dd3c5b2bd23e55ac16814d01a83f188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eefb77c01d055b0e63a5526402c6a1a51e3434075a2c39d13f641b987098b2(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb4c97d07dd08c1bd71296d80b57fadaffa68ec990d5d377d04725e7b97412c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27a2569d413f9d62089e0030491958ab16fcc8141fbae5bec1cdd5f53342a74(
    value: typing.Optional[GkeHubFeatureSpecFleetobservability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42001b933a09bfedcafd2135e2449a44c8b807f8de748095bcca334fd6e37a1(
    *,
    config_membership: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e787769b7a1016f6952abb8601447de6098f294856b79bae4749ab46b10b75d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3bd2b56883c6f3693de74d0998420c8e5f70cec3de660eeb795d5876487e66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a5845702568e545287521eb4cd522f450b7df32043774f3410e63faf03a0eb(
    value: typing.Optional[GkeHubFeatureSpecMulticlusteringress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39987c2a69b04624c5f234f3f934c5a5ab7e6ef463c757767db320c09d73bdba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8d8fa0eab991fd969df830414c08fea85d71a97075b940824875cddddda560(
    value: typing.Optional[GkeHubFeatureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a24cda2552f89ea775c9ffc65f2c0d0c35caf4e7c7a7ffad8f87fa96ea2159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45448dda26a2061969daf29a989b088aa27d4bf4407c6ce7e21b3030355fe26c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3737c59ce12a8e1bc5d7484507e1729fef47944a49ed18a599192efa9df091f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a547b379a8e7b218b291197b37e794805cf23ead34d227e6a90cb734c565ba00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17300cad930d1605c5bf21980a0e6522a4d4a3c29b79ec3f2857c4dd82c16e78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209a2a3497d66f97f3799730c0741e9854a7cb044c80973f3010e807ec8dc864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a4b5463573e3596c2418486fd0c5d64039cd4e23fa475eaf7880dc3f10535f(
    value: typing.Optional[GkeHubFeatureState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc070dd9ef24311bd600f204701b63923e80dc51075755a10d27ee2056271a6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a60b7232d286898e96c0f89aaf766b7f2604e7fa451ebcf5bc428fef6b6ce7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72eeb9c5c491886ee3a0f76920b2be92b6db291d80b5a491fa3a1fd69f8fe30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f67886f891b39422f70a8882e4d651e4189e55183855dec13a7d40d7b193777(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470d04d92bb6a6388776232ed7338fcec64c389b99929eb48f85f84333fb6a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1d91a8d54c84d61f80ea6cd8788ef3871449fa15aeddada9e9b50f822c5d71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1213261b9efa354ff823baa647b452b75f2a2f72c74e30297547cbaf888e92c0(
    value: typing.Optional[GkeHubFeatureStateState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf89b32285c28e02e496862b4900cced96d984060b303179a8af09c5f45a8e83(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa96931188e82b4d32061d7d49abb25b81d966a4a43568d69480a7f41ef3a828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a99e9f6faca5ec732456bf1268e1bbb8c1dcce0b7b5abb6d2af0d7eb313a0b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695232b98c003b755334fd66d011ec42779f5b5bb17b050396ab97640305e7ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2012273f21a1b1460fbd0a640e059067a6e84a431e11df4a639de8a74a3883e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a999d1e826cd91ca7848d0f14250a8b6cce08065cb7ab3bf7b3779673777876(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
