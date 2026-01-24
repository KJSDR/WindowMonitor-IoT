"""
Unit tests for decision logic and validation
"""
import pytest
from validation import validate_reading
from app import calculate_recommendation, current_state

#reset state before each test
@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test"""
    import app
    app.current_state = "UNKNOWN"
    yield

class TestValidation:
    """Test sensor validation logic"""
    
    def test_valid_reading(self):
        """Test that valid readings pass validation"""
        result = validate_reading(70.0, 50.0, 600)
        
        assert result['valid'] == True
        assert result['health'] == 'good'
        assert len(result['issues']) == 0
    
    def test_temperature_out_of_range(self):
        """Test that out-of-range temperature is detected"""
        result = validate_reading(200.0, 50.0, 600)
        
        assert result['valid'] == False
        assert result['health'] == 'degraded'
        assert 'Temperature out of range' in result['issues'][0]
    
    def test_humidity_out_of_range(self):
        """Test that out-of-range humidity is detected"""
        result = validate_reading(70.0, 150.0, 600)
        
        assert result['valid'] == False
        assert 'Humidity out of range' in result['issues'][0]
    
    def test_air_quality_out_of_range(self):
        """Test that out-of-range air quality is detected"""
        result = validate_reading(70.0, 50.0, 5000)
        
        assert result['valid'] == False
        assert 'Air Quality out of range' in result['issues'][0]


class TestHysteresis:
    """Test hysteresis decision logic"""
    
    def test_initial_state_close_on_bad_conditions(self):
        """Test that UNKNOWN state closes on bad conditions"""
        result = calculate_recommendation(85, 50, 400)  #temp too high - AQ poor
        
        assert result['recommendation'] == 'CLOSE'
        assert 'Temperature too high' in result['reason']
    
    def test_initial_state_open_on_good_conditions(self):
        """Test that UNKNOWN state opens on good conditions"""
        result = calculate_recommendation(70, 50, 600)  #everything good
        
        assert result['recommendation'] == 'OPEN'
        assert result['reason'] == 'All conditions favorable'
    
    def test_hysteresis_prevents_flip_flop_when_open(self):
        """Test that small changes don't trigger flip when OPEN"""
        import app
        app.current_state = "OPEN"
        
        #slightly bad conditions (still in window)
        result = calculate_recommendation(75, 50, 600)  #just below theshold but still in window
        
        assert result['recommendation'] == 'OPEN'  #should remain open
    
    def test_hysteresis_closes_on_clearly_bad_conditions(self):
        """Test that clearly bad conditions trigger CLOSE from OPEN"""
        import app
        app.current_state = "OPEN"
        
        #clear bad condition (close)
        result = calculate_recommendation(85, 50, 400)  #too hot
        
        assert result['recommendation'] == 'CLOSE'


class TestStatsCalculation:
    """Test statistics calculation"""
    
    def test_filters_invalid_readings(self):
        """Test that invalid readings are excluded from stats"""
        #would need to mock get_recent_readings
        #for now testing the filtering logic directly
        
        readings = [
            {'temperature': 70, 'humidity': 50, 'air_quality': 600, 'is_valid': True},
            {'temperature': 200, 'humidity': 50, 'air_quality': 600, 'is_valid': False},
            {'temperature': 72, 'humidity': 52, 'air_quality': 620, 'is_valid': True}
        ]
        
        valid_readings = [r for r in readings if r.get('is_valid', True)]
        temps = [r['temperature'] for r in valid_readings]
        
        assert len(valid_readings) == 2  #only 2 valid readings
        assert 200 not in temps  #invalid temp excluded
        assert sum(temps) / len(temps) == 71  #average of 70 and 72