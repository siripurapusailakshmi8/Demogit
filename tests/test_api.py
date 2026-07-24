import pytest
from conftest import BASE_URL

@pytest.mark.api
def test_get_employee(mock_session, employee):
    """Get employee created in setup"""
    employee_id = employee
    response = mock_session.get(f"{BASE_URL}/employee/{employee_id}")
    assert response.status_code == 200

    json_data = response.json()
    assert json_data['status'] == "success"
    assert json_data['data']['id'] == int(employee_id)
    assert json_data['data']['employee_name'] == "Test Employee"


@pytest.mark.api
def test_update_employee(mock_session, employee):
    """Update employee salary using setup employee"""
    employee_id = employee
    payload = {"employee_salary": 50000}
    response = mock_session.put(f"{BASE_URL}/update/{employee_id}", json=payload)
    assert response.status_code == 200

    json_data = response.json()
    assert json_data['status'] == "success"
    assert "Successfully! Record has been updated." in json_data['message']

    # Optional: Verify update via GET
    get_resp = mock_session.get(f"{BASE_URL}/employee/{employee_id}")
    assert get_resp.json()['data']['employee_salary'] == 50000
