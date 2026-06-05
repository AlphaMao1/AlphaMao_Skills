
try:
    print("Attempting to import openpyxl...")
    import openpyxl
    print(f"openpyxl version: {openpyxl.__version__}")
    
    print("Importing Workbook...")
    from openpyxl import Workbook
    
    print("Importing styles...")
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    print("Importing utils...")
    from openpyxl.utils import get_column_letter
    
    print("Importing chart...")
    from openpyxl.chart import BarChart, Reference
    
    print("SUCCESS: All imports worked!")
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()
