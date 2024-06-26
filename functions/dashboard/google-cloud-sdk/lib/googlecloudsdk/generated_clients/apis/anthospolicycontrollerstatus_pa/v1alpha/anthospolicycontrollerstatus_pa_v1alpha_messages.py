"""Generated message classes for anthospolicycontrollerstatus_pa version v1alpha.

anthospolicycontrollerstatus-pa.googleapis.com API.
"""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.protorpclite import messages as _messages
from apitools.base.py import encoding
from apitools.base.py import extra_types


package = 'anthospolicycontrollerstatus_pa'


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintAuditViolationsListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintAuditViolati
  onsListRequest object.

  Fields:
    pageSize: The maximum number of membership constraint audit violations to
      return. The service may return fewer than this value. If unspecified or
      0, defaults to 500 results. The maximum value is 2000; values above 2000
      will be coerced to 2000.
    pageToken: A page token, received from a previous
      ListMembershipConstraintAuditViolations call. Provide this to retrieve
      the subsequent page. When paginating, all other parameters provided to
      ListMembershipConstraintAuditViolations must match the call that
      provided the page token.
    parent: Required. The project id for which to fetch membership constraint
      audit violations. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintAuditViolationsProducerListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintAuditViolati
  onsProducerListRequest object.

  Fields:
    pageSize: The maximum number of membership constraint audit violations to
      return. The service may return fewer than this value. If unspecified or
      0, defaults to 500 results. The maximum value is 2000; values above 2000
      will be coerced to 2000.
    pageToken: A page token, received from a previous
      ListMembershipConstraintAuditViolationsProducer call. Provide this to
      retrieve the subsequent page. When paginating, all other parameters
      provided to ListMembershipConstraintAuditViolationsProducer must match
      the call that provided the page token.
    parent: Required. The project id for which to fetch membership constraint
      audit violations. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintTemplatesGetRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintTemplatesGet
  Request object.

  Fields:
    name: Required. The name of the membership constraint template to
      retrieve. Format: projects/{project_id}/membershipConstraintTemplates/{c
      onstraint_template_name}/{membership_uuid}.
  """

  name = _messages.StringField(1, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintTemplatesListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintTemplatesLis
  tRequest object.

  Fields:
    pageSize: The maximum number of membership constraint templates to return.
      The service may return fewer than this value. If unspecified or 0,
      defaults to 500 results. The maximum value is 2000; values above 2000
      will be coerced to 2000.
    pageToken: A page token, received from a previous
      ListMembershipConstraintTemplates call. Provide this to retrieve the
      subsequent page. When paginating, all other parameters provided to
      ListMembershipConstraintTemplates must match the call that provided the
      page token.
    parent: Required. The project id for which to fetch membership constraint
      templates. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintsGetRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintsGetRequest
  object.

  Fields:
    name: Required. The name of the membership constraint to retrieve. Format:
      projects/{project_id}/membershipConstraints/{constraint_template_name}/{
      constraint_name}/{membership_uuid}.
  """

  name = _messages.StringField(1, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintsListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintsListRequest
  object.

  Fields:
    pageSize: The maximum number of membership constraints to return. The
      service may return fewer than this value. If unspecified or 0, defaults
      to 500 results. The maximum value is 2000; values above 2000 will be
      coerced to 2000.
    pageToken: A page token, received from a previous
      ListMembershipConstraints call. Provide this to retrieve the subsequent
      page. When paginating, all other parameters provided to
      ListMembershipConstraints must match the call that provided the page
      token.
    parent: Required. The project id for which to fetch membership
      constraints. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipConstraintsProducerListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipConstraintsProducerLis
  tRequest object.

  Fields:
    pageSize: The maximum number of membership constraints to return. The
      service may return fewer than this value. If unspecified or 0, defaults
      to 500 results. The maximum value is 2000; values above 2000 will be
      coerced to 2000.
    pageToken: A page token, received from a previous
      ListMembershipConstraintsProducer call. Provide this to retrieve the
      subsequent page. When paginating, all other parameters provided to
      ListMembershipConstraintsProducer must match the call that provided the
      page token.
    parent: Required. The project id for which to fetch membership
      constraints. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class AnthospolicycontrollerstatusPaProjectsMembershipsListRequest(_messages.Message):
  r"""A AnthospolicycontrollerstatusPaProjectsMembershipsListRequest object.

  Fields:
    pageSize: The maximum number of memberships to return. The service may
      return fewer than this value. If unspecified or 0, defaults to 500
      results. The maximum value is 2000; values above 2000 will be coerced to
      2000.
    pageToken: A page token, received from a previous ListMembershipsProducer
      call. Provide this to retrieve the subsequent page. When paginating, all
      other parameters provided to ListMembershipsProducer must match the call
      that provided the page token.
    parent: Required. The project id for which to fetch memberships' policy
      controller status. Format: projects/{project_id}.
  """

  pageSize = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)


class ConstraintInfo(_messages.Message):
  r"""A ConstraintInfo object.

  Messages:
    InfoValue: A InfoValue object.

  Fields:
    info: A InfoValue attribute.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class InfoValue(_messages.Message):
    r"""A InfoValue object.

    Messages:
      AdditionalProperty: An additional property for a InfoValue object.

    Fields:
      additionalProperties: Additional properties of type InfoValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a InfoValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  info = _messages.MessageField('InfoValue', 1)


class ConstraintRef(_messages.Message):
  r"""Constraint represents a single constraint. Base identifying resource.

  Fields:
    constraintTemplateName: The constraint template name, lowercase of the
      constraint kind. Used for identification, not for UI display.
    name: The constraint name.
  """

  constraintTemplateName = _messages.StringField(1)
  name = _messages.StringField(2)


class ConstraintTemplateRef(_messages.Message):
  r"""ConstraintTemplateRef identifies a constraint template.

  Fields:
    name: The constraint template name.
  """

  name = _messages.StringField(1)


class GroupKind(_messages.Message):
  r"""GroupKind includes the group, kind of the K8s resource.

  Fields:
    apiGroup: The api group of the resource.
    kind: The api kind of the resource.
  """

  apiGroup = _messages.StringField(1)
  kind = _messages.StringField(2)


class KubernetesMatch(_messages.Message):
  r"""The scope of objects to which a given constraint will be applied

  Enums:
    ScopeValueValuesEnum: Matcher to match on scope of objects.

  Fields:
    excludedNamespaces: Matcher to match on objects not in excluded
      namespaces. Supports a prefix-based glob.
    groupKinds: Matcher to match on objects based on api group or kind.
    labelSelector: Matcher to match objects based on label keys or values.
    name: Matcher to match on an object's name. Supports a prefix-based glob.
    namespaceSelector: Matcher to match on namespace.
    namespaces: Matcher to match on objects in given namespaces. Supports a
      prefix-based glob.
    scope: Matcher to match on scope of objects.
  """

  class ScopeValueValuesEnum(_messages.Enum):
    r"""Matcher to match on scope of objects.

    Values:
      SCOPE_UNSPECIFIED: Unspecified scope.
      SCOPE_ALL: Scope `*`, match all resources.
      SCOPE_CLUSTER: Scope `Cluster`, match cluster-scoped resources.
      SCOPE_NAMESPACED: Scope `Namespaced`, match namespace-scoped resources.
    """
    SCOPE_UNSPECIFIED = 0
    SCOPE_ALL = 1
    SCOPE_CLUSTER = 2
    SCOPE_NAMESPACED = 3

  excludedNamespaces = _messages.StringField(1, repeated=True)
  groupKinds = _messages.MessageField('GroupKind', 2, repeated=True)
  labelSelector = _messages.StringField(3)
  name = _messages.StringField(4)
  namespaceSelector = _messages.StringField(5)
  namespaces = _messages.StringField(6, repeated=True)
  scope = _messages.EnumField('ScopeValueValuesEnum', 7)


class ListMembershipConstraintAuditViolationsProducerResponse(_messages.Message):
  r"""Response schema for ListMembershipConstraintAuditViolationsProducer.

  Fields:
    membershipConstraintAuditViolations: List of the membership-level
      constraint audit violation info.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of membership constraint audit violations in the
      response.
  """

  membershipConstraintAuditViolations = _messages.MessageField('MembershipConstraintAuditViolation', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipConstraintAuditViolationsResponse(_messages.Message):
  r"""Response schema for ListMembershipConstraintAuditViolations.

  Fields:
    membershipConstraintAuditViolations: List of the membership-level
      constraint audit violation info.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of membership constraint audit violations in the
      response.
  """

  membershipConstraintAuditViolations = _messages.MessageField('MembershipConstraintAuditViolation', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipConstraintTemplatesResponse(_messages.Message):
  r"""Response schema for ListMembershipConstraintTemplates.

  Fields:
    membershipConstraintTemplates: List of membership-level constraint
      template info.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of membership constraint templates in the response.
  """

  membershipConstraintTemplates = _messages.MessageField('MembershipConstraintTemplate', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipConstraintsProducerResponse(_messages.Message):
  r"""Response schema for ListMembershipConstraintsProducer.

  Fields:
    membershipConstraints: List of membership-level constraint info.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of membership constraints in the response.
  """

  membershipConstraints = _messages.MessageField('MembershipConstraint', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipConstraintsResponse(_messages.Message):
  r"""Response schema for ListMembershipConstraints.

  Fields:
    membershipConstraints: List of membership-level constraint info.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of membership constraints in the response.
  """

  membershipConstraints = _messages.MessageField('MembershipConstraint', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipsProducerResponse(_messages.Message):
  r"""Response schema for ListMembershipsProducer.

  Fields:
    memberships: List of the memberships in a given fleet.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of memberships in the response.
  """

  memberships = _messages.MessageField('Membership', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class ListMembershipsResponse(_messages.Message):
  r"""Response schema for ListMemberships.

  Fields:
    memberships: List of the memberships in a given fleet.
    nextPageToken: A token, which can be sent as page_token to retrieve the
      next page. If this field is omitted, there are no subsequent pages.
    totalSize: The number of memberships in the response.
  """

  memberships = _messages.MessageField('Membership', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  totalSize = _messages.IntegerField(3)


class Membership(_messages.Message):
  r"""Membership contains aggregate information about policy controller
  resources on a member cluster.

  Fields:
    featureStatus: The status of the policy controller feature.
    ref: The membership this data refers to.
    runtimeStatus: The status of the policy controller runtime configuration.
      If runtime_status is empty, then the server could not find any existing
      constraint or templates to report status.
  """

  featureStatus = _messages.MessageField('MembershipFeatureStatus', 1)
  ref = _messages.MessageField('MembershipRef', 2)
  runtimeStatus = _messages.MessageField('MembershipRuntimeStatus', 3)


class MembershipConstraint(_messages.Message):
  r"""Membership specific constraint data.

  Fields:
    constraintRef: The constraint this data refers to.
    content: The string content for the constraint resource.
    kind: The kind of the constraint on this membership, for display purposes.
    membershipRef: The membership this data refers to.
    metadata: Membership-specific constraint metadata.
    spec: Membership-specific constraint spec.
    status: Membership-specific constraint status.
  """

  constraintRef = _messages.MessageField('ConstraintRef', 1)
  content = _messages.MessageField('StringContent', 2)
  kind = _messages.StringField(3)
  membershipRef = _messages.MessageField('MembershipRef', 4)
  metadata = _messages.MessageField('MembershipConstraintMetadata', 5)
  spec = _messages.MessageField('MembershipConstraintSpec', 6)
  status = _messages.MessageField('MembershipConstraintStatus', 7)


class MembershipConstraintAuditViolation(_messages.Message):
  r"""MembershipConstraintAuditViolation encodes info relevant to a violation
  of a single constraint on a single member cluster.

  Fields:
    auditTimestamp: The audit timestamp when this violation was observed on
      the membership.
    constraintRef: The constraint ref of the violated constraint.
    errorMessage: An error message detailing the violation.
    membershipRef: The membership this violation occurs on.
    resourceRef: The resource ref of the violating K8S object.
  """

  auditTimestamp = _messages.StringField(1)
  constraintRef = _messages.MessageField('ConstraintRef', 2)
  errorMessage = _messages.StringField(3)
  membershipRef = _messages.MessageField('MembershipRef', 4)
  resourceRef = _messages.MessageField('ResourceRef', 5)


class MembershipConstraintMetadata(_messages.Message):
  r"""MembershipConstraintMetadata contains relevant fields from constraint
  metadata.

  Fields:
    constraintInfo: constraint bundle information from the metadata.annotation
      field.
    creation: metadata.creation_timestamp from the constraint.
    generation: metadata.generation from the constraint.
  """

  constraintInfo = _messages.MessageField('ConstraintInfo', 1)
  creation = _messages.StringField(2)
  generation = _messages.IntegerField(3)


class MembershipConstraintSpec(_messages.Message):
  r"""The spec defining this constraint. See https://open-policy-
  agent.github.io/gatekeeper/website/docs/howto#constraints.

  Enums:
    EnforcementActionValueValuesEnum: spec.enforcement_action.

  Fields:
    enforcementAction: spec.enforcement_action.
    kubernetesMatch: Reserved: The match specified against GCP resources.
      GCPMatch gcp_match = 3;
    parameters: The parameters a constraint expects.
  """

  class EnforcementActionValueValuesEnum(_messages.Enum):
    r"""spec.enforcement_action.

    Values:
      ENFORCEMENT_ACTION_UNSPECIFIED: Unspecified state for an enforcement
        action.
      ENFORCEMENT_ACTION_DENY: The resource is denied admission to the
        membership.
      ENFORCEMENT_ACTION_DRYRUN: Allows testing constraints without enforcing
        them.
      ENFORCEMENT_ACTION_WARN: Provides immediate feedback on why a resource
        violates a constraint.
    """
    ENFORCEMENT_ACTION_UNSPECIFIED = 0
    ENFORCEMENT_ACTION_DENY = 1
    ENFORCEMENT_ACTION_DRYRUN = 2
    ENFORCEMENT_ACTION_WARN = 3

  enforcementAction = _messages.EnumField('EnforcementActionValueValuesEnum', 1)
  kubernetesMatch = _messages.MessageField('KubernetesMatch', 2)
  parameters = _messages.MessageField('MembershipConstraintSpecParameters', 3)


class MembershipConstraintSpecParameters(_messages.Message):
  r"""Parameters specified based on the schema defined in the constraint
  template.

  Messages:
    ParametersValue: spec.parameters from the constraint.

  Fields:
    parameters: spec.parameters from the constraint.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class ParametersValue(_messages.Message):
    r"""spec.parameters from the constraint.

    Messages:
      AdditionalProperty: An additional property for a ParametersValue object.

    Fields:
      additionalProperties: Properties of the object.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a ParametersValue object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  parameters = _messages.MessageField('ParametersValue', 1)


class MembershipConstraintStatus(_messages.Message):
  r"""MembershipConstraintStatus contains high-level information from
  constraint status. Omits violation-level information from constraint status,
  which is in separate violation resources.

  Fields:
    auditTimestamp: status.audit_timestamp from the constraint.
    numViolations: status.total_violations from the constraint.
  """

  auditTimestamp = _messages.StringField(1)
  numViolations = _messages.IntegerField(2)


class MembershipConstraintTemplate(_messages.Message):
  r"""MembershipConstraintTemplate contains runtime status relevant to a
  single constraint template on a single member cluster.

  Fields:
    constraintTemplateRef: The constraint template this data refers to.
    description: annotations.description, may not be populated.
    membershipRef: The membership this data refers to.
    metadata: Membership-specific constraint template metadata.
    spec: Membership-specific constraint template spec.
    status: Membership-specific constraint template status.
  """

  constraintTemplateRef = _messages.MessageField('ConstraintTemplateRef', 1)
  description = _messages.StringField(2)
  membershipRef = _messages.MessageField('MembershipRef', 3)
  metadata = _messages.MessageField('MembershipConstraintTemplateMetadata', 4)
  spec = _messages.MessageField('MembershipConstraintTemplateSpec', 5)
  status = _messages.MessageField('MembershipConstraintTemplateStatus', 6)


class MembershipConstraintTemplateMetadata(_messages.Message):
  r"""MembershipConstraintTemplateMetadata contains relevant fields from
  constraint template metadata.

  Fields:
    creation: metadata.creation_timestamp from the constraint template.
    generation: metadata.generation from the constraint template.
  """

  creation = _messages.StringField(1)
  generation = _messages.IntegerField(2)


class MembershipConstraintTemplateSpec(_messages.Message):
  r"""The spec defining this constraint template. See https://github.com/open-
  policy-agent/frameworks/tree/master/constraint#what-is-a-constraint-
  template.

  Messages:
    PropertiesValue: spec.crd.spec.validation.openAPIV3Schema.

  Fields:
    constraintKind: spec.crd.spec.names.kind.
    properties: spec.crd.spec.validation.openAPIV3Schema.
    targets: spec.targets. Use a list of targets to account for multi-target
      templates.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class PropertiesValue(_messages.Message):
    r"""spec.crd.spec.validation.openAPIV3Schema.

    Messages:
      AdditionalProperty: An additional property for a PropertiesValue object.

    Fields:
      additionalProperties: Properties of the object.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a PropertiesValue object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  constraintKind = _messages.StringField(1)
  properties = _messages.MessageField('PropertiesValue', 2)
  targets = _messages.MessageField('Target', 3, repeated=True)


class MembershipConstraintTemplateStatus(_messages.Message):
  r"""MembershipConstratinTemplateStatus contains status information, e.g.
  whether the template has been created on the member cluster.

  Fields:
    created: status.created from the constraint template.
  """

  created = _messages.BooleanField(1)


class MembershipFeatureStatus(_messages.Message):
  r"""MembershipFeatureStatus contains aggregate data about the policy
  controller feature on a cluster that is a member of a fleet.

  Enums:
    ClusterStatusValueValuesEnum: The status of cluster underlying the
      membership.
    LifecycleStatusValueValuesEnum: The lifecycle status of the policy
      controller feature on the membership.

  Fields:
    clusterStatus: The status of cluster underlying the membership.
    lifecycleStatus: The lifecycle status of the policy controller feature on
      the membership.
  """

  class ClusterStatusValueValuesEnum(_messages.Enum):
    r"""The status of cluster underlying the membership.

    Values:
      CLUSTER_STATUS_UNSPECIFIED: The cluster status is unspecified.
      CLUSTER_ACTIVE: The cluster is active.
      CLUSTER_INACTIVE: The cluster is inactive.
    """
    CLUSTER_STATUS_UNSPECIFIED = 0
    CLUSTER_ACTIVE = 1
    CLUSTER_INACTIVE = 2

  class LifecycleStatusValueValuesEnum(_messages.Enum):
    r"""The lifecycle status of the policy controller feature on the
    membership.

    Values:
      LIFECYCLE_STATE_UNSPECIFIED: The lifecycle state is unspecified.
      NOT_INSTALLED: Policy Controller (PC) does not exist on the given
        cluster, and no k8s resources of any type that are associated with the
        PC should exist there. The cluster does not possess a membership with
        the Hub Feature controller.
      INSTALLING: The Hub Feature controller possesses a Membership, however
        Policy Controller is not fully installed on the cluster. In this state
        the hub can be expected to be taking actions to install the PC on the
        cluster.
      ACTIVE: Policy Controller (PC) is fully installed on the cluster and in
        an operational mode. In this state the Hub Feature controller will be
        reconciling state with the PC, and the PC will be performing it's
        operational tasks per that software. Entering a READY state requires
        that the hub has confirmed the PC is installed and its pods are
        operational with the version of the PC the Hub Feature controller
        expects.
      UPDATING: Policy Controller (PC) is fully installed, but in the process
        of changing the configuration (including changing the version of PC
        either up and down, or modifying the manifests of PC) of the resources
        running on the cluster. The Hub Feature controller has a Membership,
        is aware of the version the cluster should be running in, but has not
        confirmed for itself that the PC is running with that version.
      DECOMMISSIONING: Policy Controller (PC) may have resources on the
        cluster, but the Hub Feature controller wishes to remove the
        Membership. The Membership still exists.
      CLUSTER_ERROR: Policy Controller (PC) is not operational, and the Hub
        Feature controller is unable to act to make it operational. Entering a
        CLUSTER_ERROR state happens automatically when the PCH determines that
        a PC installed on the cluster is non-operative or that the cluster
        does not meet requirements set for the Hub Feature controller to
        administer the cluster but has nevertheless been given an instruction
        to do so (such as 'install').
      HUB_ERROR: In this state, the PC may still be operational, and only the
        Hub Feature controller is unable to act. The hub should not issue
        instructions to change the PC state, or otherwise interfere with the
        on-cluster resources. Entering a HUB_ERROR state happens automatically
        when the Hub Feature controller determines the hub is in an unhealthy
        state and it wishes to 'take hands off' to avoid corrupting the PC or
        other data.
      SUSPENDED: Policy Controller (PC) is installed but suspended. This means
        that the policies are not enforced, but violations are still recorded
        (through audit).
      DETACHED: PoCo Hub is not taking any action to reconcile cluster
        objects. Changes to those objects will not be overwritten by PoCo Hub.
    """
    LIFECYCLE_STATE_UNSPECIFIED = 0
    NOT_INSTALLED = 1
    INSTALLING = 2
    ACTIVE = 3
    UPDATING = 4
    DECOMMISSIONING = 5
    CLUSTER_ERROR = 6
    HUB_ERROR = 7
    SUSPENDED = 8
    DETACHED = 9

  clusterStatus = _messages.EnumField('ClusterStatusValueValuesEnum', 1)
  lifecycleStatus = _messages.EnumField('LifecycleStatusValueValuesEnum', 2)


class MembershipRef(_messages.Message):
  r"""Reference to a GKE Hub membership.

  Fields:
    id: The id of the membership, for identity purposes.
    name: The name of the membership, for display purposes.
    projectId: The project id of the membership, for checking IAM permissions.
  """

  id = _messages.StringField(1)
  name = _messages.StringField(2)
  projectId = _messages.StringField(3)


class MembershipRuntimeStatus(_messages.Message):
  r"""MembershipRuntimeStatus contains aggregate data about policy controller
  resources on a cluster that is a member of a fleet.

  Fields:
    numConstraintTemplates: The number of constraint templates on the member
      cluster.
    numConstraintViolations: The number of constraint violations on the member
      cluster.
    numConstraints: The number of constraints on the member cluster.
  """

  numConstraintTemplates = _messages.IntegerField(1)
  numConstraintViolations = _messages.IntegerField(2)
  numConstraints = _messages.IntegerField(3)


class RegoPolicy(_messages.Message):
  r"""The rego policy defining this constraint template.

  Fields:
    libs: spec.targets.libs.
    policy: spec.targets.rego.
  """

  libs = _messages.StringField(1, repeated=True)
  policy = _messages.StringField(2)


class ResourceRef(_messages.Message):
  r"""Reference to a K8S resource.

  Fields:
    groupKind: GK is the GroupKind of the K8S resource. This field may be
      empty for errors that are not associated with a specific resource.
    name: The name of the K8S resource.
    resourceNamespace: The namespace of the K8S resource. This field may be
      empty for errors that are associated with a cluster-scoped resource.
      Called resource_namespace because namespace is a C++ keyword.
  """

  groupKind = _messages.MessageField('GroupKind', 1)
  name = _messages.StringField(2)
  resourceNamespace = _messages.StringField(3)


class StandardQueryParameters(_messages.Message):
  r"""Query parameters accepted by all methods.

  Enums:
    FXgafvValueValuesEnum: V1 error format.
    AltValueValuesEnum: Data format for response.

  Fields:
    f__xgafv: V1 error format.
    access_token: OAuth access token.
    alt: Data format for response.
    callback: JSONP
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    uploadType: Legacy upload protocol for media (e.g. "media", "multipart").
    upload_protocol: Upload protocol for media (e.g. "raw", "multipart").
  """

  class AltValueValuesEnum(_messages.Enum):
    r"""Data format for response.

    Values:
      json: Responses with Content-Type of application/json
      media: Media download with context-dependent Content-Type
      proto: Responses with Content-Type of application/x-protobuf
    """
    json = 0
    media = 1
    proto = 2

  class FXgafvValueValuesEnum(_messages.Enum):
    r"""V1 error format.

    Values:
      _1: v1 error format
      _2: v2 error format
    """
    _1 = 0
    _2 = 1

  f__xgafv = _messages.EnumField('FXgafvValueValuesEnum', 1)
  access_token = _messages.StringField(2)
  alt = _messages.EnumField('AltValueValuesEnum', 3, default='json')
  callback = _messages.StringField(4)
  fields = _messages.StringField(5)
  key = _messages.StringField(6)
  oauth_token = _messages.StringField(7)
  prettyPrint = _messages.BooleanField(8, default=True)
  quotaUser = _messages.StringField(9)
  trace = _messages.StringField(10)
  uploadType = _messages.StringField(11)
  upload_protocol = _messages.StringField(12)


class StringContent(_messages.Message):
  r"""String content for a constraint resource.

  Fields:
    yaml: string json = 2;
  """

  yaml = _messages.StringField(1)


class Target(_messages.Message):
  r"""Target defines which resources this template targets.

  Fields:
    regoPolicy: Reserved: The policy defined using CEL. CELPolicy cel_policy =
      3;
    target: spec.targets.target.
  """

  regoPolicy = _messages.MessageField('RegoPolicy', 1)
  target = _messages.StringField(2)


encoding.AddCustomJsonFieldMapping(
    StandardQueryParameters, 'f__xgafv', '$.xgafv')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_1', '1')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_2', '2')
