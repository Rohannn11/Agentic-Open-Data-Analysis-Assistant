from abc import ABC, abstractmethod
from data.canonical import IndicatorSeries

class BaseAdapter(ABC):
    """
    The Interface.
    Every adapter MUST implement these methods.
    """
    
    @abstractmethod
    def fetch_data(self, country_code: str, indicator_code: str, start_year: int, end_year: int) -> IndicatorSeries:
        """
        Fetches data from the source and returns it in OUR Canonical format.
        """
        pass