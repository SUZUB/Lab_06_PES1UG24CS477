"""
Branch Coverage Unit Tests for bike_share_rental application.
Ensures every control structure (if, else, elif) evaluates to both True and False,
covering all boundary conditions and edge cases to achieve >= 90% branch coverage.

Target Application: bike_share_rental.py
Course: Software Engineering Lab 6 - Branch Coverage Analysis
Student SRN: PES1UG24CS477
"""

import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# ==============================================================================
# Branch Coverage Tests for ride_cost(bike_type, minutes, is_subscriber, is_peak)
# ==============================================================================

def test_ride_cost_unknown_bike_type_branch():
    """Branch: bike_type not in RATE_PER_30_MIN -> True."""
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("unicycle", 30, False, False)


def test_ride_cost_invalid_duration_branches():
    """Branch: minutes <= 0 -> True (both zero and negative values)."""
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", -5, False, False)


def test_ride_cost_subscriber_blocks_le_zero_branch():
    """
    Branch: is_subscriber == True AND blocks <= 0 -> True.
    A ride of 20 minutes produces (20+29)//30 = 1 block.
    Subscriber discount reduces blocks by 1 -> blocks = 0 <= 0 -> cost 0.
    """
    assert ride_cost("standard", 20, is_subscriber=True, is_peak=False) == 0


def test_ride_cost_subscriber_blocks_gt_zero_branch():
    """
    Branch: is_subscriber == True AND blocks <= 0 -> False.
    A ride of 60 minutes produces 2 blocks.
    Subscriber discount reduces blocks by 1 -> blocks = 1 > 0 -> cost > 0.
    """
    # 1 block * 20 = 20
    assert ride_cost("standard", 60, is_subscriber=True, is_peak=False) == 20


def test_ride_cost_non_subscriber_branch():
    """Branch: is_subscriber == False."""
    # 45 minutes -> 2 blocks * 20 = 40
    assert ride_cost("standard", 45, is_subscriber=False, is_peak=False) == 40


def test_ride_cost_peak_non_cargo_branch():
    """
    Branch: is_peak == True AND bike_type != 'cargo' -> True.
    Applies peak fee of +15.
    """
    # electric: 30 mins -> 1 block * 35 + 15 = 50
    assert ride_cost("electric", 30, is_subscriber=False, is_peak=True) == 50


def test_ride_cost_peak_cargo_branch():
    """
    Branch: is_peak == True AND bike_type != 'cargo' -> False (bike_type == 'cargo').
    Cargo bike is exempt from peak fee.
    """
    # cargo: 30 mins -> 1 block * 50 = 50 (no +15)
    assert ride_cost("cargo", 30, is_subscriber=False, is_peak=True) == 50


def test_ride_cost_non_peak_cargo_branch():
    """Branch: is_peak == False with cargo bike."""
    assert ride_cost("cargo", 30, is_subscriber=False, is_peak=False) == 50


def test_ride_cost_duration_boundary_180_branches():
    """
    Branch: minutes > 180 -> True vs False.
    Boundary testing at 180 and 181 minutes.
    """
    # Boundary 180 mins: 6 blocks * 20 = 120 (no surcharge)
    assert ride_cost("standard", 180, is_subscriber=False, is_peak=False) == 120
    # Boundary 181 mins: 7 blocks * 20 + 100 = 240 (surcharge applied)
    assert ride_cost("standard", 181, is_subscriber=False, is_peak=False) == 240


# ==============================================================================
# Branch Coverage Tests for dock_status(bikes_docked, capacity)
# ==============================================================================

def test_dock_status_capacity_le_zero_branches():
    """Branch: capacity <= 0 -> True (zero and negative capacity)."""
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, -10)


def test_dock_status_bikes_docked_negative_branch():
    """Branch: bikes_docked < 0 -> True."""
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)


def test_dock_status_bikes_docked_gt_capacity_branch():
    """Branch: bikes_docked > capacity -> True."""
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)


def test_dock_status_empty_branch():
    """Branch: bikes_docked == 0 -> True."""
    assert dock_status(0, 10) == "empty"


def test_dock_status_full_branch():
    """Branch: free_slots == 0 (bikes_docked == capacity) -> True."""
    assert dock_status(10, 10) == "full"


def test_dock_status_few_bikes_boundary_branches():
    """
    Branch: bikes_docked <= 2 -> True.
    Tests boundary values 1 and 2 with capacity > 4.
    """
    assert dock_status(1, 10) == "few bikes"
    assert dock_status(2, 10) == "few bikes"


def test_dock_status_few_slots_boundary_branches():
    """
    Branch: bikes_docked > 2 AND free_slots <= 2 -> True.
    Tests boundary values where free_slots are 1 or 2.
    """
    # capacity = 10, docked = 8 -> free_slots = 2
    assert dock_status(8, 10) == "few slots"
    # capacity = 10, docked = 9 -> free_slots = 1
    assert dock_status(9, 10) == "few slots"


def test_dock_status_available_branch():
    """
    Branch: bikes_docked > 2 AND free_slots > 2 -> Fall-through to 'available'.
    """
    # capacity = 10, docked = 5 -> free_slots = 5
    assert dock_status(5, 10) == "available"


# ==============================================================================
# Branch Coverage Tests for can_unlock(account_balance, has_active_ride, age)
# ==============================================================================

def test_can_unlock_active_ride_branches():
    """Branch: has_active_ride == True vs False."""
    assert can_unlock(200, has_active_ride=True, age=25) is False
    assert can_unlock(200, has_active_ride=False, age=25) is True


def test_can_unlock_age_under_16_branches():
    """
    Branch: age < 16 -> True vs False.
    Boundary testing at age 15 and age 16.
    """
    assert can_unlock(200, has_active_ride=False, age=15) is False
    assert can_unlock(200, has_active_ride=False, age=16) is True


def test_can_unlock_minor_age_16_17_balance_branches():
    """
    Branch: age < 18 (age 16, 17) -> evaluates account_balance >= 100 (True / False).
    Boundary testing at balance 99 and 100.
    """
    # Minor age 16: balance 100 -> True
    assert can_unlock(100, has_active_ride=False, age=16) is True
    # Minor age 16: balance 99 -> False
    assert can_unlock(99, has_active_ride=False, age=16) is False
    # Minor age 17: balance 150 -> True
    assert can_unlock(150, has_active_ride=False, age=17) is True
    # Minor age 17: balance 50 -> False
    assert can_unlock(50, has_active_ride=False, age=17) is False


def test_can_unlock_adult_age_ge_18_balance_branches():
    """
    Branch: age >= 18 -> evaluates account_balance >= 50 (True / False).
    Boundary testing at balance 49 and 50.
    """
    # Adult age 18: boundary balance 50 -> True
    assert can_unlock(50, has_active_ride=False, age=18) is True
    # Adult age 18: boundary balance 49 -> False
    assert can_unlock(49, has_active_ride=False, age=18) is False
    # Adult age 30: balance 40 -> False
    assert can_unlock(40, has_active_ride=False, age=30) is False
    # Adult age 30: balance 60 -> True
    assert can_unlock(60, has_active_ride=False, age=30) is True
