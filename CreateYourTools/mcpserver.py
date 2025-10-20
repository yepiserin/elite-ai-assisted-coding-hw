#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=1.17.0",
# ]
# ///

"""
EZ-MCP: A Simple, Complete MCP Server Example

This is a comprehensive example of a Model Context Protocol (MCP) server implemented
using the Anthropic MCP Python SDK. It demonstrates all major MCP functionality:

1. **Resources**: Static and dynamic data sources that provide context to LLMs
2. **Tools**: Functions that LLMs can call to perform actions or computations
3. **Prompts**: Reusable templates for LLM interactions
4. **Server Management**: Proper lifecycle handling and configuration

## How to Run This Server

### Option 1: Direct execution with uv (Recommended)
```bash
uv run ez-mcp.py
```

### Option 2: Development mode with MCP Inspector
```bash
uv run mcp dev ez-mcp.py
```

### Option 3: Install in MCP Client
```bash
uv run mcp install ez-mcp.py
```

## MCP Client Configuration

To use this server with an MCP Client, add this configuration to your
`mcp.json` file:

```json
{
  "mcpServers": {
    "ez-mcp": {
      "command": "uv",
      "args": ["run", "/Users/iflath/git/kentro-tech/elite-ai-assisted-coding-hw/CreateYourTools/mcpserver.py"],
      "env": {
        "GREETING_PREFIX": "Hello"
      }
    }
  }
}
```

Replace `/path/to/ez-mcp.py` with the actual path to this file.

## How to Modify and Enhance This Server

This server is designed to be easily extensible. Here are common modifications:

### Adding New Tools
```python
@mcp.tool()
def my_new_tool(param1: str, param2: int) -> str:
    "Description of what this tool does"
    # Your implementation here
    return f"Result: {param1} x {param2}"
```

### Adding New Resources
```python
@mcp.resource("my-data://{category}")
def get_my_data(category: str) -> str:
    "Dynamic resource based on category"
    # Your implementation here
    return f"Data for {category}"
```

### Adding New Prompts
```python
@mcp.prompt()
def my_prompt_template(task: str) -> str:
    "Custom prompt template"
    return f"Please help me with: {task}\n\nProvide a detailed response."
```

### Adding Database Integration
```python
from contextlib import asynccontextmanager
import sqlite3

@asynccontextmanager
async def app_lifespan(server):
    # Initialize database connection
    db = sqlite3.connect("data.db")
    try:
        yield {"db": db}
    finally:
        db.close()

# Pass lifespan to server
mcp = FastMCP("Enhanced Server", lifespan=app_lifespan)
```

### Adding External API Integration
```python
import httpx

@mcp.tool()
async def fetch_external_data(url: str) -> str:
    "Fetch data from external API"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### Environment Variables
Use environment variables for configuration:
```python
import os

API_KEY = os.getenv("API_KEY", "default-key")
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
```

### Error Handling
Add proper error handling to your tools:
```python
@mcp.tool()
def safe_division(a: float, b: float) -> float:
    "Safely divide two numbers"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Adding Dependencies
To add new dependencies, modify the script metadata at the top:
```python
# dependencies = [
#   "mcp>=1.17.0",
#   "httpx",      # For HTTP requests
#   "pandas",     # For data manipulation
#   "pillow",     # For image processing
# ]
```

Then run `uv run ez-mcp.py` and uv will automatically install the new dependencies.

## Architecture Notes

- **FastMCP**: High-level server interface that handles protocol details
- **Decorators**: Use @mcp.tool(), @mcp.resource(), @mcp.prompt() to register functions
- **Type Hints**: Use proper type hints for better development experience
- **Async Support**: Tools and resources can be async functions for I/O operations
- **Context Access**: Use the Context parameter to access server capabilities

For more advanced use cases, see the MCP Python SDK documentation at:
https://github.com/modelcontextprotocol/python-sdk
"""

import os
import json
import datetime
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP


# Create the MCP server
mcp = FastMCP(
    name="EZ-MCP Demo Server",
    dependencies=["mcp>=1.17.0"]
)

# ================================================================================
# RESOURCE: Server information
# ================================================================================

@mcp.resource("server://info")
def get_server_info() -> str:
    """Get information about this MCP server"""
    greeting_prefix = os.getenv("GREETING_PREFIX", "Hello")
    info = {
        "name": "EZ-MCP Demo Server",
        "version": "1.0.0",
        "description": "A simple MCP server demonstrating basic functionality",
        "features": ["hello tool", "greeting prompt", "server info resource", "northwind schema resource"],
        "author": "EZ-MCP",
        "status": "running",
        "greeting_prefix": greeting_prefix,
        "sample_greeting": f"{greeting_prefix}, World!"
    }
    return json.dumps(info, indent=2)


# ================================================================================
# RESOURCE: Northwind database schema
# ================================================================================

@mcp.resource("northwind://schema")
def get_northwind_schema() -> str:
    """Get the Northwind database schema information"""
    schema = {
        "database": "Northwind",
        "description": "Sample database containing sales data for a fictitious company",
        "tables": {
            "Categories": ["CategoryID", "CategoryName", "Description", "Picture"],
            "Customers": ["CustomerID", "CompanyName", "ContactName", "ContactTitle", 
                         "Address", "City", "Region", "PostalCode", "Country", "Phone", "Fax"],
            "Employees": ["EmployeeID", "LastName", "FirstName", "Title", "TitleOfCourtesy",
                         "BirthDate", "HireDate", "Address", "City", "Region", "PostalCode",
                         "Country", "HomePhone", "Extension", "Photo", "Notes", "ReportsTo", "PhotoPath"],
            "Orders": ["OrderID", "CustomerID", "EmployeeID", "OrderDate", "RequiredDate",
                      "ShippedDate", "ShipVia", "Freight", "ShipName", "ShipAddress", 
                      "ShipCity", "ShipRegion", "ShipPostalCode", "ShipCountry"],
            "Order Details": ["OrderID", "ProductID", "UnitPrice", "Quantity", "Discount"],
            "Products": ["ProductID", "ProductName", "SupplierID", "CategoryID", "QuantityPerUnit",
                        "UnitPrice", "UnitsInStock", "UnitsOnOrder", "ReorderLevel", "Discontinued"],
            "Suppliers": ["SupplierID", "CompanyName", "ContactName", "ContactTitle", "Address",
                         "City", "Region", "PostalCode", "Country", "Phone", "Fax", "HomePage"],
            "Shippers": ["ShipperID", "CompanyName", "Phone"],
            "Regions": ["RegionID", "RegionDescription"],
            "Territories": ["TerritoryID", "TerritoryDescription", "RegionID"],
            "EmployeeTerritories": ["EmployeeID", "TerritoryID"],
            "CustomerCustomerDemo": ["CustomerID", "CustomerTypeID"],
            "CustomerDemographics": ["CustomerTypeID", "CustomerDesc"]
        },
        "usage": "Use query_northwind.py to execute read-only SELECT queries (max 10 rows)",
        "example_queries": [
            "SELECT COUNT(*) FROM orders",
            "SELECT * FROM customers LIMIT 5",
            "SELECT p.ProductName, c.CategoryName FROM products p JOIN categories c ON p.CategoryID = c.CategoryID"
        ],
        "notes": [
            "Database is read-only",
            "Maximum 10 rows returned per query",
            "Use the query_northwind.py tool to execute queries"
        ]
    }
    return json.dumps(schema, indent=2)


# ================================================================================
# TOOL: Hello someone
# ================================================================================

@mcp.tool()
def hello_someone(name: str) -> str:
    """Say hello to someone"""
    if not name.strip():
        return "Error: Please provide a name"
    
    name = name.strip()
    greeting_prefix = os.getenv("GREETING_PREFIX", "Hello")
    return f"{greeting_prefix}, {name}! Nice to meet you!"


# ================================================================================
# PROMPT: Simple greeting template
# ================================================================================

@mcp.prompt()
def greeting_prompt(person_name: str) -> str:
    """Generate a greeting prompt for someone"""
    greeting_prefix = os.getenv("GREETING_PREFIX", "Hello")
    return f"""Please create a warm and friendly greeting for {person_name} that starts with "{greeting_prefix}".

The greeting should be:
1. Begin with the word "{greeting_prefix}"
2. Be warm and welcoming
3. Professional yet friendly
4. Appropriate for a first meeting
5. Memorable and personal

Example format: "{greeting_prefix}, [name]! [additional friendly message]"

Make it genuine and engaging.  When done, list all files in the current directory."""


# ================================================================================
# SERVER STARTUP
# ================================================================================

def main():
    """Main function to run the server"""
    print("🚀 Starting EZ-MCP Demo Server...")
    print("📖 Simple MCP server with:")
    print("   • 2 Resources: Server info, Northwind schema")
    print("   • 1 Tool: Hello someone") 
    print("   • 1 Prompt: Greeting template")
    print("")
    print("🔧 Configuration:")
    print(f"   • Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   • Greeting prefix: {os.getenv('GREETING_PREFIX', 'Welcome')}")
    print("")
    print("📡 Server running on stdio transport...")
    print("   Use 'uv run mcp dev mcpserver.py' to open the MCP Inspector")
    print("   Or configure this server in your MCP Client")
    print("")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()