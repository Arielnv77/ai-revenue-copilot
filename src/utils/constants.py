"""
Constants — Application-wide constant values.
"""

# Supported file extensions
SUPPORTED_EXTENSIONS = {".csv"}

# Column name patterns for auto-detection
DATE_PATTERNS = ["date", "time", "timestamp", "created", "updated", "invoice"]
REVENUE_PATTERNS = ["revenue", "sales", "amount", "total", "price", "value"]
CUSTOMER_PATTERNS = ["customer", "client", "user", "buyer", "account"]
PRODUCT_PATTERNS = ["product", "item", "sku", "description", "name"]
QUANTITY_PATTERNS = ["quantity", "qty", "count", "units"]

# RFM segment labels
RFM_SEGMENTS = {
    "Champions": "Best customers — bought recently, buy often, spend the most",
    "Loyal Customers": "Buy regularly with good frequency and spend",
    "New Customers": "Bought recently but haven't established purchase pattern",
    "Promising": "Recent buyers with average frequency",
    "At Risk": "Used to buy frequently but haven't returned recently",
    "Can't Lose Them": "Were top spenders but haven't purchased recently",
    "Lost": "Haven't purchased in a long time and infrequently",
    "Need Attention": "Moderate across all RFM dimensions",
}

# Forecast defaults
DEFAULT_FORECAST_HORIZONS = [30, 60, 90]

# API
API_V1_PREFIX = "/api/v1"
