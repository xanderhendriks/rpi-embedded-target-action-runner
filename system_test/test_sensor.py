
def test_version(serial_command_response, version_to_check, git_hash_to_check):
    """
    Check the version
    """
    serial_command_response.command('v')
    response = serial_command_response.response()

    print(f'response: {response}')

    assert response == f'image_id: 1, version: {version_to_check}-{git_hash_to_check}'


def test_sensor(serial_command_response):
    """
    Test the sensor output
    """
    serial_command_response.command('s')
    response = serial_command_response.response()

    print(f'response: {response}')

    assert response == 'sensor: 65535'
