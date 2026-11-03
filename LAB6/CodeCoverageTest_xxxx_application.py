"""
Unit tests for bike_share_rental application to achieve line coverage >= 90%.
Target Application: bike_share_rental.py
Course: Software Engineering Lab 6 - Code Coverage Analysis
Student SRN: PES1UG24CS477
"""

import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# ==========================================
# Unit Tests for ride_cost(bike_type, minutes, is_subscriber, is_peak)
# ==========================================
def test_ride_cost_unknown_bike_type():
    """Test that an unknown bike type raises ValueError."""
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("hoverboard", 30, False, False)


def test_ride_cost_invalid_duration_zero_and_negative():
    """Test that zero or negative minutes raise ValueError."""
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", -15, False, False)


def test_ride_cost_subscriber_within_free_period():
    """Test subscriber ride within first 30 minutes (cost should be 0)."""
    assert ride_cost("standard", 25, True, False) == 0


def test_ride_cost_subscriber_beyond_free_period():
    """Test subscriber ride exceeding first 30 minutes."""
    # 60 mins -> blocks = 2. Subscriber: blocks = 1. cost = 1 * 20 = 20
    assert ride_cost("standard", 60, True, False) == 20


def test_ride_cost_non_subscriber_standard():
    """Test non-subscriber standard ride with regular duration."""
    # 45 mins -> blocks = 2. cost = 2 * 20 = 40
    assert ride_cost("standard", 45, False, False) == 40


def test_ride_cost_peak_hour_electric():
    """Test peak hour surcharge on electric bike."""
    # 30 mins -> blocks = 1. cost = 1 * 35 + 15 = 50
    assert ride_cost("electric", 30, False, True) == 50


def test_ride_cost_peak_hour_cargo():
    """Test cargo bike during peak hour (exempt from peak surcharge)."""
    # 30 mins -> blocks = 1. cost = 1 * 50 = 50 (no +15)
    assert ride_cost("cargo", 30, False, True) == 50


def test_ride_cost_extended_duration_over_180():
    """Test ride exceeding 180 minutes incurs long-duration surcharge."""
    # 200 mins -> blocks = 7. cost = 7 * 20 + 100 = 240
    assert ride_cost("standard", 200, False, False) == 240


# ==========================================
# Unit Tests for dock_status(bikes_docked, capacity)
# ==========================================
def test_dock_status_invalid_capacity():
    """Test non-positive station capacity raises ValueError."""
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, -5)


def test_dock_status_invalid_bike_count_negative():
    """Test negative bikes_docked raises ValueError."""
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)


def test_dock_status_invalid_bike_count_exceeds_capacity():
    """Test bikes_docked exceeding capacity raises ValueError."""
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(15, 10)


def test_dock_status_empty():
    """Test empty station status."""
    assert dock_status(0, 10) == "empty"


def test_dock_status_full():
    """Test full station status."""
    assert dock_status(10, 10) == "full"


def test_dock_status_few_bikes():
    """Test station with few bikes remaining (1 or 2 bikes)."""
    assert dock_status(1, 10) == "few bikes"
    assert dock_status(2, 10) == "few bikes"


def test_dock_status_few_slots():
    """Test station with few slots remaining (1 or 2 slots)."""
    # 8 docked out of 10 -> 2 free slots
    assert dock_status(8, 10) == "few slots"
    # 9 docked out of 10 -> 1 free slot
    assert dock_status(9, 10) == "few slots"


def test_dock_status_available():
    """Test balanced station status."""
    assert dock_status(5, 10) == "available"


# ==========================================
# Unit Tests for can_unlock(account_balance, has_active_ride, age)
# ==========================================
def test_can_unlock_with_active_ride():
    """Test user with an active ride cannot unlock another bike."""
    assert can_unlock(500, True, 25) is False


def test_can_unlock_underage():
    """Test user below age 16 cannot unlock a bike."""
    assert can_unlock(200, False, 15) is False


def test_can_unlock_minor_balance_threshold():
    """Test minor (age 16-17) requires balance >= 100."""
    assert can_unlock(100, False, 16) is True
    assert can_unlock(150, False, 17) is True
    assert can_unlock(99, False, 16) is False
    assert can_unlock(0, False, 17) is False


def test_can_unlock_adult_balance_threshold():
    """Test adult (age >= 18) requires balance >= 50."""
    assert can_unlock(50, False, 18) is True
    assert can_unlock(100, False, 25) is True
    assert can_unlock(49, False, 18) is False
    assert can_unlock(0, False, 30) is False
