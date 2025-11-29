import pandas as pd
import numpy as np
from datetime import datetime
from decimal import Decimal
from .models import FinancialStatement, SMI

def process_financial_statement(file, smi_id):
    """Process uploaded financial statement file and create records."""
    
    # Read the file based on extension
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension in ['xlsx', 'xls']:
        df = pd.read_excel(file)
    elif file_extension == 'csv':
        df = pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format")

    # Expected columns
    required_columns = [
        'period',
        'total_income',
        'profit_before_tax'
    ]

    # Validate columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Get SMI instance
    try:
        smi = SMI.objects.get(id=smi_id)
    except SMI.DoesNotExist:
        raise ValueError("SMI not found")

    # Process each row
    statements = []
    for _, row in df.iterrows():
        # Convert period to date
        try:
            period = pd.to_datetime(row['period']).date()
        except:
            raise ValueError("Invalid date format in period column")

        # Convert numeric values
        try:
            total_income = Decimal(str(row['total_income']))
            profit_before_tax = Decimal(str(row['profit_before_tax']))
            
            # Calculate margins
            gross_margin = float(total_income / 100)  # Example calculation
            profit_margin = float(profit_before_tax / total_income if total_income else 0)
            
        except:
            raise ValueError("Invalid numeric values in financial data")

        # Create financial statement
        statement = FinancialStatement(
            smi=smi,
            period=period,
            total_income=total_income,
            profit_before_tax=profit_before_tax,
            gross_margin=gross_margin,
            profit_margin=profit_margin
        )
        statements.append(statement)

    # Bulk create statements
    FinancialStatement.objects.bulk_create(statements)
    
    return len(statements)
