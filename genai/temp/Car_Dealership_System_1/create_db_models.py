# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Car(Base):
    """description: Represents a car model available in the dealership."""
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    model = Column(String)
    make = Column(String)
    year = Column(Integer)
    price = Column(Integer)
    in_stock = Column(Integer)

class Customer(Base):
    """description: Represents a customer who interacts with the dealership, purchasing cars."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    join_date = Column(Date)

class Purchase(Base):
    """description: Links customers and cars showing when a car was purchased and for how much."""
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    car_id = Column(Integer, ForeignKey('car.id'))
    purchase_date = Column(DateTime)
    price = Column(Integer)

class Salesperson(Base):
    """description: A salesperson employed by the dealership responsible for selling cars."""
    __tablename__ = 'salesperson'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)
    email = Column(String)

class Sale(Base):
    """description: Represents the sale transaction between customer, car, and salesperson."""
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    salesperson_id = Column(Integer, ForeignKey('salesperson.id'))

class MaintenanceRecord(Base):
    """description: Records maintenance activities performed on a car."""
    __tablename__ = 'maintenance_record'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    maintenance_date = Column(DateTime)
    description = Column(String)
    cost = Column(Integer)

class CarFeature(Base):
    """description: Describes additional features available for each car."""
    __tablename__ = 'car_feature'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    feature_name = Column(String)

class Employee(Base):
    """description: General table for employees that can be expanded to different positions."""
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)
    hire_date = Column(Date)

class Inventory(Base):
    """description: Tracks the inventory of cars available at different locations."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    location = Column(String)
    quantity = Column(Integer)

class Department(Base):
    """description: A department in the dealership, e.g., sales, inventory, management, etc."""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class Shift(Base):
    """description: Defines work hours for employees for the dealership operations."""
    __tablename__ = 'shift'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    shift_start = Column(DateTime)
    shift_end = Column(DateTime)

class Supplier(Base):
    """description: Describes suppliers who provide cars or parts to the dealership."""
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_name = Column(String)
    contact_phone = Column(String)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    car1 = Car(id=1, model="Model S", make="Tesla", year=2021, price=80000, in_stock=5)
    car2 = Car(id=2, model="Civic", make="Honda", year=2020, price=20000, in_stock=10)
    car3 = Car(id=3, model="Mustang", make="Ford", year=2021, price=55000, in_stock=3)
    car4 = Car(id=4, model="Corolla", make="Toyota", year=2019, price=18000, in_stock=7)
    customer1 = Customer(id=1, name="John Doe", email="john@example.com", phone="1234567890", address="123 Elm St", join_date=date(2021, 5, 17))
    customer2 = Customer(id=2, name="Jane Smith", email="jane@example.com", phone="0987654321", address="456 Oak St", join_date=date(2021, 6, 17))
    customer3 = Customer(id=3, name="Alan Walker", email="alan@example.com", phone="1029384756", address="789 Pine St", join_date=date(2021, 7, 17))
    customer4 = Customer(id=4, name="Emma Brown", email="emma@example.com", phone="1122334455", address="321 Cedar St", join_date=date(2021, 8, 17))
    purchase1 = Purchase(id=1, customer_id=1, car_id=1, purchase_date=datetime(2021, 5, 18, 10, 30), price=80000)
    purchase2 = Purchase(id=2, customer_id=2, car_id=2, purchase_date=datetime(2021, 6, 20, 11, 45), price=20000)
    purchase3 = Purchase(id=3, customer_id=3, car_id=3, purchase_date=datetime(2021, 7, 22, 16, 0), price=55000)
    purchase4 = Purchase(id=4, customer_id=4, car_id=4, purchase_date=datetime(2021, 8, 25, 14, 15), price=18000)
    salesperson1 = Salesperson(id=1, name="Alice Cooper", contact_number="2233445566", email="alice@dealership.com")
    salesperson2 = Salesperson(id=2, name="Bob Marley", contact_number="3344556677", email="bob@dealership.com")
    salesperson3 = Salesperson(id=3, name="Charlie Brown", contact_number="4455667788", email="charlie@dealership.com")
    salesperson4 = Salesperson(id=4, name="Diana Ross", contact_number="5566778899", email="diana@dealership.com")
    sale1 = Sale(id=1, purchase_id=1, salesperson_id=1)
    sale2 = Sale(id=2, purchase_id=2, salesperson_id=2)
    sale3 = Sale(id=3, purchase_id=3, salesperson_id=3)
    sale4 = Sale(id=4, purchase_id=4, salesperson_id=4)
    maint_record1 = MaintenanceRecord(id=1, car_id=1, maintenance_date=datetime(2021, 9, 1, 9, 0), description="Oil Change", cost=100)
    maint_record2 = MaintenanceRecord(id=2, car_id=2, maintenance_date=datetime(2021, 9, 15, 10, 0), description="Tire Rotation", cost=50)
    maint_record3 = MaintenanceRecord(id=3, car_id=3, maintenance_date=datetime(2021, 10, 5, 11, 0), description="Brake Inspection", cost=150)
    maint_record4 = MaintenanceRecord(id=4, car_id=4, maintenance_date=datetime(2021, 10, 20, 14, 0), description="Transmission Fluid Change", cost=120)
    feature1 = CarFeature(id=1, car_id=1, feature_name="Sunroof")
    feature2 = CarFeature(id=2, car_id=2, feature_name="Heated Seats")
    feature3 = CarFeature(id=3, car_id=3, feature_name="Bluetooth")
    feature4 = CarFeature(id=4, car_id=4, feature_name="Backup Camera")
    employee1 = Employee(id=1, name="Henry Ford", position="Manager", hire_date=date(2021, 5, 1))
    employee2 = Employee(id=2, name="Nikola Tesla", position="Sales Associate", hire_date=date(2021, 5, 15))
    employee3 = Employee(id=3, name="Thomas Edison", position="Technician", hire_date=date(2021, 6, 1))
    employee4 = Employee(id=4, name="Albert Einstein", position="Engineer", hire_date=date(2021, 7, 1))
    inventory1 = Inventory(id=1, car_id=1, location="Main Showroom", quantity=5)
    inventory2 = Inventory(id=2, car_id=2, location="Secondary Showroom", quantity=10)
    inventory3 = Inventory(id=3, car_id=3, location="Main Showroom", quantity=3)
    inventory4 = Inventory(id=4, car_id=4, location="Warehouse", quantity=7)
    department1 = Department(id=1, name="Sales", description="Handles car sales and customer service")
    department2 = Department(id=2, name="Service", description="Manages car maintenance and repair work")
    department3 = Department(id=3, name="Finance", description="Oversees financial operations and accounts")
    department4 = Department(id=4, name="Human Resources", description="Manages employee relations and recruitment")
    shift1 = Shift(id=1, employee_id=1, shift_start=datetime(2021, 10, 12, 9, 0), shift_end=datetime(2021, 10, 12, 17, 0))
    shift2 = Shift(id=2, employee_id=2, shift_start=datetime(2021, 10, 13, 9, 0), shift_end=datetime(2021, 10, 13, 17, 0))
    shift3 = Shift(id=3, employee_id=3, shift_start=datetime(2021, 10, 14, 9, 0), shift_end=datetime(2021, 10, 14, 17, 0))
    shift4 = Shift(id=4, employee_id=4, shift_start=datetime(2021, 10, 15, 9, 0), shift_end=datetime(2021, 10, 15, 17, 0))
    supplier1 = Supplier(id=1, name="Acme Cars Inc.", contact_name="Jim Beam", contact_phone="6677889900")
    supplier2 = Supplier(id=2, name="Fast Cars Ltd.", contact_name="Jack Daniels", contact_phone="7788990011")
    supplier3 = Supplier(id=3, name="Vehicles Unlimited", contact_name="Johnny Walker", contact_phone="8899001122")
    supplier4 = Supplier(id=4, name="Speed Motors LLC", contact_name="Jim Apple", contact_phone="9900112233"
    
    
    
    session.add_all([car1, car2, car3, car4, customer1, customer2, customer3, customer4, purchase1, purchase2, purchase3, purchase4, salesperson1, salesperson2, salesperson3, salesperson4, sale1, sale2, sale3, sale4, maint_record1, maint_record2, maint_record3, maint_record4, feature1, feature2, feature3, feature4, employee1, employee2, employee3, employee4, inventory1, inventory2, inventory3, inventory4, department1, department2, department3, department4, shift1, shift2, shift3, shift4, supplier1, supplier2, supplier3, supplier4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
