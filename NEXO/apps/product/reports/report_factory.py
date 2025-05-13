from typing import Optional
from .report_generator import ReportGenerator
from .pdf_report_generator import PDFReportGenerator
from .excel_report_generator import ExcelReportGenerator


class ReportFactory:
    
    
    @staticmethod
    def get_report_generator(format_type: str) -> Optional[ReportGenerator]:
        
        format_type = format_type.lower()
        
        if format_type == 'pdf':
            return PDFReportGenerator()
        elif format_type in ['excel', 'xlsx']:
            return ExcelReportGenerator()
        else:
            return None 