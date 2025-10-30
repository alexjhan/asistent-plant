"""
Example: ERP system automation
Demonstrates automating tasks in an ERP system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant import DesktopAgent
import time


class ERPAutomation:
    """
    Example automation for ERP systems.
    This demonstrates how to use the agent to automate common ERP tasks.
    """
    
    def __init__(self):
        self.agent = DesktopAgent()
    
    def login_to_erp(self, username: str, password: str, erp_name: str = "ERP"):
        """
        Automate ERP login process.
        
        Args:
            username: ERP username
            password: ERP password
            erp_name: Name of the ERP application window
        """
        print(f"=== Logging into {erp_name} ===\n")
        
        # Open or activate ERP application
        print("1. Opening ERP application...")
        self.agent.execute_command(f"open {erp_name}")
        time.sleep(2)
        
        # Find and click username field
        print("2. Looking for username field...")
        result = self.agent.execute_command("click on username field")
        if result['success']:
            time.sleep(0.5)
            self.agent.execute_command(f"type '{username}'")
            print("   ✓ Username entered")
        
        # Find and click password field
        print("3. Looking for password field...")
        self.agent.execute_command("click on password field")
        time.sleep(0.5)
        self.agent.execute_command(f"type '{password}'")
        print("   ✓ Password entered")
        
        # Click login button
        print("4. Clicking login button...")
        self.agent.execute_command("click on login button")
        print("   ✓ Login submitted")
        
        # Wait for login to complete
        time.sleep(3)
        print("\n✓ Login process completed")
    
    def navigate_to_module(self, module_name: str):
        """
        Navigate to a specific ERP module.
        
        Args:
            module_name: Name of the module (e.g., "Sales", "Inventory")
        """
        print(f"\n=== Navigating to {module_name} Module ===\n")
        
        # Click on menu
        self.agent.execute_command("click on menu")
        time.sleep(1)
        
        # Click on module
        self.agent.execute_command(f"click on {module_name}")
        time.sleep(2)
        
        print(f"✓ Navigated to {module_name}")
    
    def create_sales_order(self, customer: str, product: str, quantity: int):
        """
        Create a sales order in the ERP system.
        
        Args:
            customer: Customer name
            product: Product name
            quantity: Order quantity
        """
        print("\n=== Creating Sales Order ===\n")
        
        # Click New Order button
        print("1. Opening new order form...")
        self.agent.execute_command("click on new order button")
        time.sleep(1)
        
        # Enter customer
        print("2. Selecting customer...")
        self.agent.execute_command("click on customer field")
        time.sleep(0.5)
        self.agent.execute_command(f"type '{customer}'")
        time.sleep(0.5)
        self.agent.execute_command("press enter")
        
        # Enter product
        print("3. Adding product...")
        self.agent.execute_command("click on product field")
        time.sleep(0.5)
        self.agent.execute_command(f"type '{product}'")
        time.sleep(0.5)
        self.agent.execute_command("press enter")
        
        # Enter quantity
        print("4. Entering quantity...")
        self.agent.execute_command("click on quantity field")
        time.sleep(0.5)
        self.agent.execute_command(f"type '{quantity}'")
        
        # Save order
        print("5. Saving order...")
        self.agent.execute_command("click on save button")
        time.sleep(2)
        
        print("\n✓ Sales order created successfully")
    
    def generate_report(self, report_type: str, date_range: str = "This Month"):
        """
        Generate a report in the ERP system.
        
        Args:
            report_type: Type of report (e.g., "Sales Report")
            date_range: Date range for the report
        """
        print(f"\n=== Generating {report_type} ===\n")
        
        # Navigate to reports
        print("1. Opening reports section...")
        self.agent.execute_command("click on reports")
        time.sleep(1)
        
        # Select report type
        print("2. Selecting report type...")
        self.agent.execute_command(f"click on {report_type}")
        time.sleep(1)
        
        # Select date range
        print("3. Setting date range...")
        self.agent.execute_command("click on date range")
        time.sleep(0.5)
        self.agent.execute_command(f"click on {date_range}")
        
        # Generate report
        print("4. Generating report...")
        self.agent.execute_command("click on generate button")
        time.sleep(3)
        
        # Export report
        print("5. Exporting report...")
        self.agent.execute_command("click on export button")
        time.sleep(1)
        
        print(f"\n✓ {report_type} generated and exported")
    
    def bulk_data_entry(self, data_list: list):
        """
        Perform bulk data entry.
        
        Args:
            data_list: List of dictionaries with data to enter
        """
        print("\n=== Bulk Data Entry ===\n")
        
        for i, data in enumerate(data_list, 1):
            print(f"Entry {i}/{len(data_list)}")
            
            # Click new entry
            self.agent.execute_command("click on new entry")
            time.sleep(0.5)
            
            # Fill fields
            for field, value in data.items():
                self.agent.execute_command(f"click on {field} field")
                time.sleep(0.3)
                self.agent.execute_command(f"type '{value}'")
                time.sleep(0.3)
            
            # Save entry
            self.agent.execute_command("click on save")
            time.sleep(1)
        
        print(f"\n✓ Completed {len(data_list)} entries")


def demo_erp_workflow():
    """Demonstrate a complete ERP workflow."""
    print("=== ERP Automation Demo ===\n")
    print("This is a demonstration of ERP automation capabilities.")
    print("Note: This is a simulation and requires actual ERP software.\n")
    
    erp = ERPAutomation()
    
    # Simulate workflow steps (in a real scenario, you would have actual ERP)
    print("Workflow steps:")
    print("1. Login to ERP")
    print("2. Navigate to Sales module")
    print("3. Create a sales order")
    print("4. Generate a report")
    print("\nNote: To use with real ERP, ensure the ERP is running")
    print("and customize the field names according to your ERP system.")
    
    # Example usage (commented out for demo)
    # erp.login_to_erp("username", "password", "MyERP")
    # erp.navigate_to_module("Sales")
    # erp.create_sales_order("ACME Corp", "Product A", 100)
    # erp.generate_report("Sales Report", "This Month")


if __name__ == "__main__":
    demo_erp_workflow()
