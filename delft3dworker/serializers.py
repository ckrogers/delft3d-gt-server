from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from delft3dworker.models import Scenario
from delft3dworker.models import Scene
from delft3dworker.models import SearchForm
from delft3dworker.models import Template
from delft3dworker.models import Version_SVN

from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the User model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    # here we will write custom serialization and validation methods

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
        )


class GroupSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Group model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    # here we will write custom serialization and validation methods

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class SceneFullSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Scene model, which
    is used for detail views of scenes, providing all valuable data of
    a single model to the frontend.
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    owner = UserSerializer(read_only=True)

    state = serializers.CharField(source='get_phase_display', read_only=True)
    outdated = serializers.BooleanField(source='is_outdated', read_only=True)
    outdated_workflow = serializers.SerializerMethodField()
    outdated_changelog = serializers.CharField(read_only=True)

    class Meta:
        model = Scene
        fields = (
            'date_created',
            'date_started',
            'fileurl',
            'id',
            'info',
            'name',
            'owner',
            'parameters',
            'phase',
            'progress',
            'scenario',
            'shared',
            'state',
            'suid',
            'task_id',
            'versions',
            'workingdir',
            'outdated',
            'outdated_workflow',
            'outdated_changelog'
        )

    def get_outdated_workflow(self, obj):
        wf = obj.outdated_workflow()
        return obj.workflows[wf] if wf is not None else ""


class SceneSparseSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Scene model, which
    is used for list views of scenes, providing only essential data in
    a list of many models to the frontend.
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    state = serializers.CharField(source='get_phase_display', read_only=True)

    class Meta:
        model = Scene
        fields = (
            'suid',
            'id',
            'name',
            'owner',
            'progress',
            'shared',
            'state'
        )


class ScenarioSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Scenario model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    # here we will write custom serialization and validation methods
    state = serializers.CharField(
        source='_update_state_and_save', read_only=True)

    owner_url = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail', source='owner')

    class Meta:
        model = Scenario
        fields = (
            'id',
            'name',
            'owner_url',
            'template',
            'parameters',
            'state',
            'progress',
            'scene_set',
        )


class SearchFormSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Template model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    # here we will write custom serialization and validation methods

    class Meta:
        model = SearchForm
        fields = (
            'id',
            'name',
            'sections',
            'templates',
        )


class Version_SVNSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Version_SVN model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    class Meta:
        model = Version_SVN
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    """
    A default REST Framework ModelSerializer for the Template model
    source: http://www.django-rest-framework.org/api-guide/serializers/
    """

    # here we will write custom serialization and validation methods

    class Meta:
        model = Template
        fields = (
            'id',
            'name',
            'meta',
            'sections',
        )
