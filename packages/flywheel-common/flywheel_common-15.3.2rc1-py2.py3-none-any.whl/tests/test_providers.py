import datetime
import pytest

from flywheel_common.errors import ValidationError
from flywheel_common.providers import ProviderClass
from flywheel_common.providers.creds import Creds
from flywheel_common.providers.provider import BaseProvider
from flywheel_common.providers.storage.base import BaseStorageProvider
from flywheel_common.providers.compute.base import BaseComputeProvider, BaseComputeSchema


# === Model Tests ===
def test_creds():

    cred_test = Creds(
        provider_class='test',
        provider_type='anything',
        provider_label='Test creds',
        config=None)

    assert cred_test.provider_class == 'test'
    assert cred_test.provider_type == 'anything'
    assert cred_test.label == 'Test creds'

    # No schema
    with pytest.raises(ValueError):
        cred_test.validate()

def test_provider():

    provider_test = BaseProvider(
        provider_class='test',
        provider_type='anything',
        provider_label='Test provider',
        config=None,
        creds=None)

    assert provider_test.provider_class == 'test'
    assert provider_test.provider_type == 'anything'
    assert provider_test.label == 'Test provider'

    # No schema
    with pytest.raises(ValueError):
        provider_test.validate()

def test_storage_provider(mocker):

    mocker.patch('flywheel_common.providers.storage.base.create_flywheel_fs', return_value={'storage': 'test'})

    # No schema
    with pytest.raises(ValueError):
        provider_test = BaseStorageProvider(
            provider_class=ProviderClass.storage.value,
            provider_type='local',
            provider_label='Test local provider',
            config={'path': '/var/'},
            creds=None)

    # Skip schema validation but crate the object
    mocker.patch('flywheel_common.providers.storage.base.BaseProvider.validate', return_value=True)
    provider_test = BaseStorageProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider',
        config={'path': '/var/'},
        creds=None)

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.storage_plugin == {'storage': 'test'}


def test_compute_provider(mocker):
    """Test validation on all the required fields for base compute"""
    origin = { 'type': 'user', 'id': 'user@test.com' }
    # Dont use defaults to confirm they are set in the model correctly
    config = {
        'queue_threshold': 5,
        'max_compute': 6,
        'machine_type': 'test',
        'disk_size': 7,
        'swap_size': '99G',
        'preemptible': 9,
        'region': 'test region',
        'zone': 'test zone'
    }

    provider_test = BaseComputeProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider',
        config=config,
        creds=None)
    provider_test.origin = origin
    provider_test.created = provider_test.modified = datetime.datetime.now()
    provider_test._schema = BaseComputeSchema()

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.config['queue_threshold'] == 5
    assert provider_test.config['max_compute'] == 6
    assert provider_test.config['machine_type'] == 'test'
    assert provider_test.config['disk_size'] == 7
    assert provider_test.config['swap_size'] == '99G'
    assert provider_test.config['preemptible'] == 9
    assert provider_test.config['region'] == 'test region'
    assert provider_test.config['zone'] == 'test zone'

    # No errors should be thrown here
    provider_test.validate()

    provider_test.config['queue_threshold'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['queue_threshold'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['queue_threshold'] = 5

    provider_test.config['max_compute'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['max_compute'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['max_compute'] = 6

    provider_test.config['machine_type'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['machine_type'] = 999
    # Numbers are convered to strings so this is valid
    provider_test.validate()
    provider_test.config['machine_type'] = ''
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['machine_type'] = 'test'

    provider_test.config['disk_size'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['disk_size'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['disk_size'] = 7

    provider_test.config['swap_size'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = 99
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = 0
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = 99.0
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = '0G'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = '99GG'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = '99'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = '99X'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['swap_size'] = '99T'
    provider_test.validate()
    provider_test.config['swap_size'] = '99K'
    provider_test.validate()
    provider_test.config['swap_size'] = '99M'
    provider_test.validate()
    provider_test.config['swap_size'] = '99G'
    provider_test.validate()

    provider_test.config['preemptible'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['preemptible'] = 'String'
    # It converts string to a bool value on validate
    provider_test.validate()
    provider_test.config['preemptible'] = 333
    # Converts number to bool on validate as well
    provider_test.validate()
    provider_test.config['preemptible'] = True

    del provider_test.config['zone']
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['zone'] = None
    provider_test.validate()
    provider_test.config['zone'] = ''
    provider_test.validate()
    provider_test.config['zone'] = 'test zone'

    del provider_test.config['region']
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['region'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['region'] = ''
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['region'] = 'test region'

    # Create a second instance to validate isolation of config and attributes
    origin = {'type': 'user2', 'id': 'user2@test.com'}
    # Dont use defaults to confirm they are set in the model correctly
    config = {
        'queue_threshold': 25,
        'max_compute': 26,
        'machine_type': '2test',
        'disk_size': 27,
        'swap_size': '100G',
        'preemptible': True,
        'region': '2test region',
        'zone': '2test zone'
    }
    provider_test2 = BaseComputeProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider 2',
        config=config,
        creds=None)
    provider_test2.origin = origin
    provider_test2.created = provider_test.modified = datetime.datetime.now()
    provider_test2._schema = BaseComputeSchema()
    provider_test2.validate()

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.config['queue_threshold'] == 5
    assert provider_test.config['max_compute'] == 6
    assert provider_test.config['machine_type'] == 'test'
    assert provider_test.config['disk_size'] == 7
    assert provider_test.config['swap_size'] == '99G'
    assert provider_test.config['preemptible'] == True
    assert provider_test.config['region'] == 'test region'
    assert provider_test.config['zone'] == 'test zone'
    #Add the second
    assert provider_test2.label == 'Test local provider 2'
    assert provider_test2.provider_class == ProviderClass.storage.value
    assert provider_test2.provider_type == 'local'
    assert provider_test2.config['queue_threshold'] == 25
    assert provider_test2.config['max_compute'] == 26
    assert provider_test2.config['machine_type'] == '2test'
    assert provider_test2.config['disk_size'] == 27
    assert provider_test2.config['swap_size'] == '100G'
    assert provider_test2.config['preemptible'] == True
    assert provider_test2.config['region'] == '2test region'
    assert provider_test2.config['zone'] == '2test zone'
