#!/usr/bin/env python
"""
Script to check and migrate employee data from inventory app to employee app
Run this BEFORE running the migrations if you have important employee data in inventory app
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from django.db import connection
from employee.models import Employee as EmployeeEmployee, Unit, Department, Subdepartment, Position, EmployeeHistory
from inventory.models import ItemUnit
from django.utils import timezone


def check_inventory_tables():
    """
    Check if inventory employee tables exist and have data
    """
    with connection.cursor() as cursor:
        # Check if inventory_employee table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='inventory_employee';
        """)
        
        employee_table_exists = cursor.fetchone() is not None
        
        if employee_table_exists:
            # Check data in inventory_employee
            cursor.execute("SELECT COUNT(*) FROM inventory_employee")
            employee_count = cursor.fetchone()[0]
            
            print(f"inventory_employee table exists with {employee_count} records")
            
            if employee_count > 0:
                # Show employee data
                cursor.execute("SELECT id, employee_id, name, email, phone FROM inventory_employee LIMIT 10")
                employees = cursor.fetchall()
                
                print("\nInventory employees:")
                print("-" * 60)
                for emp in employees:
                    print(f"ID: {emp[0]} | Employee ID: {emp[1]} | Name: {emp[2]} | Email: {emp[3]}")
                
                return True, employee_count
        else:
            print("inventory_employee table does not exist")
            return False, 0
    
    return False, 0


def check_itemunit_references():
    """
    Check ItemUnit records that have current_user references
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM inventory_itemunit 
            WHERE current_user_id IS NOT NULL
        """)
        
        assigned_count = cursor.fetchone()[0]
        
        if assigned_count > 0:
            print(f"\nFound {assigned_count} ItemUnit records with current_user assignments")
            
            # Show some examples
            cursor.execute("""
                SELECT asset_number, current_user_id 
                FROM inventory_itemunit 
                WHERE current_user_id IS NOT NULL 
                LIMIT 10
            """)
            
            assignments = cursor.fetchall()
            print("\nCurrent assignments:")
            print("-" * 40)
            for asset, user_id in assignments:
                print(f"Asset: {asset} → User ID: {user_id}")
        else:
            print("\nNo ItemUnit records have current_user assignments")
        
        return assigned_count


def clear_itemunit_assignments():
    """
    Clear all current_user assignments in ItemUnit
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE inventory_itemunit SET current_user_id = NULL")
            affected_rows = cursor.rowcount
            
        print(f"Cleared current_user for {affected_rows} ItemUnit records")
        return True
    except Exception as e:
        print(f"Error clearing assignments: {e}")
        return False


def migrate_employees_from_db():
    """
    Migrate employees from inventory database table to employee app
    """
    print("Starting employee migration from inventory database to employee app...")
    
    # Get or create default organizational structure
    office_unit, _ = Unit.objects.get_or_create(name='office')
    general_dept, _ = Department.objects.get_or_create(
        name='General',
        defaults={'unit': office_unit}
    )
    general_subdept, _ = Subdepartment.objects.get_or_create(
        name='General',
        defaults={'department': general_dept}
    )
    general_position, _ = Position.objects.get_or_create(
        name='Employee',
        defaults={'level': '1', 'grade': 'A'}
    )
    
    migrated_count = 0
    skipped_count = 0
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, employee_id, name, email, phone 
            FROM inventory_employee
        """)
        
        inventory_employees = cursor.fetchall()
        
        for emp_data in inventory_employees:
            inv_id, emp_id, name, email, phone = emp_data
            
            try:
                # Check if employee already exists in employee app
                existing = EmployeeEmployee.objects.filter(
                    employee_id=emp_id
                ).first()
                
                if existing:
                    print(f"Employee {name} (ID: {emp_id}) already exists in employee app")
                    skipped_count += 1
                    continue
                
                # Create new employee in employee app
                new_employee = EmployeeEmployee.objects.create(
                    employee_id=emp_id,
                    name=name,
                    join_date=timezone.now().date(),
                    employment_status='tetap',
                    company_mail=email,
                    phone=phone,
                    is_active=True
                )
                
                # Create employee history
                EmployeeHistory.objects.create(
                    employee=new_employee,
                    subdepartment=general_subdept,
                    position=general_position,
                    start_date=timezone.now().date(),
                    is_active=True
                )
                
                print(f"Migrated employee: {name} (ID: {emp_id})")
                migrated_count += 1
                
            except Exception as e:
                print(f"Error migrating employee {name}: {e}")
    
    print(f"\nMigration completed!")
    print(f"Migrated: {migrated_count} employees")
    print(f"Skipped: {skipped_count} employees (already exist)")
    
    return migrated_count, skipped_count


def show_employee_employees():
    """
    Show all employees in employee app
    """
    print("Employees in employee app:")
    print("-" * 50)
    
    for emp in EmployeeEmployee.objects.all():
        print(f"ID: {emp.employee_id} | Name: {emp.name} | Email: {emp.company_mail}")
    
    print(f"\nTotal: {EmployeeEmployee.objects.count()} employees")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'check':
            table_exists, count = check_inventory_tables()
            check_itemunit_references()
        elif command == 'show-employee':
            show_employee_employees()
        elif command == 'migrate':
            table_exists, count = check_inventory_tables()
            if table_exists and count > 0:
                migrate_employees_from_db()
            else:
                print("No inventory employees to migrate")
        elif command == 'clear-assignments':
            clear_itemunit_assignments()
        else:
            print("Usage:")
            print("  python migrate_inventory_employees.py check             # Check inventory data")
            print("  python migrate_inventory_employees.py show-employee     # Show employee app employees")
            print("  python migrate_inventory_employees.py migrate           # Migrate employees")
            print("  python migrate_inventory_employees.py clear-assignments # Clear ItemUnit assignments")
    else:
        print("Available commands:")
        print("1. Check inventory data")
        print("2. Show employee app employees") 
        print("3. Migrate employees")
        print("4. Clear ItemUnit assignments")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            table_exists, count = check_inventory_tables()
            check_itemunit_references()
        elif choice == '2':
            show_employee_employees()
        elif choice == '3':
            table_exists, count = check_inventory_tables()
            if table_exists and count > 0:
                migrate_employees_from_db()
            else:
                print("No inventory employees to migrate")
        elif choice == '4':
            clear_itemunit_assignments()
        else:
            print("Invalid choice")