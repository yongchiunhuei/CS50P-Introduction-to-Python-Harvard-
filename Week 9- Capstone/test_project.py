import pytest
from project import audit_mission, get_route_options, handle_recharge, launch_navigation

# 1. Testing the Energy Audit Logic (The Core Math)
def test_audit_mission():
    """Test the mission audit logic with various battery/distance scenarios."""
    # Scenario: 100% SOC, 65km distance. 
    # Logic: 75kWh total * 1.0 = 75kWh. 65km / 6.5 efficiency = 10kWh used.
    # 65kWh remaining / 75kWh total = 86.7%
    is_viable, soc= audit_mission(100,65)
    assert is_viable is True
    assert soc == 86.7

    # Scenario: Critical Battery (Should fail 10% buffer)
    is_viable, soc = audit_mission(15, 65)
    assert is_viable is False
    assert soc <10

# 2. Testing Route Options (Verification of Structure)
def test_get_route_options():
    """Verify get_route_options exists and handles invalid keys/routes gracefully."""
    # In a real mission, check if the function raises a ValueError for bad inputs
    with pytest.raises(ValueError):
        get_route_options("Invalid_Origin", "Invalid_Dest")

# 3. Testing Recharge Handler (Logic Guard)
def test_handle_recharge():
    """Ensure handle_recharge is defined for sector recovery."""
    # We verify the function is callable
    assert callable(handle_recharge)

# 4. Testing Navigation Launch (Portal Verification)
def test_launch_navigation():
    """Verify launch_navigation protocol is defined."""
    # We verify the function is callable
    assert callable(launch_navigation)

