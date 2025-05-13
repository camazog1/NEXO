from abc import ABC, abstractmethod
from typing import List, Dict, Any
from django.http import HttpResponse


class ReportGenerator(ABC):
    @abstractmethod
    def generate_product_report(self, products: List[Dict[str, Any]], title: str = "Product Report") -> HttpResponse:
        pass
    
    @abstractmethod
    def get_content_type(self) -> str:
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        pass 