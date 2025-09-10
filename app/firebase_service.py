# # logistics_app/firebase_service.py
# from firebase_admin import firestore
# from typing import List, Dict, Any, Optional
# import logging

# logger = logging.getLogger(__name__)

# class FirebaseService:
#     def __init__(self):
#         try:
#             self.db = firestore.client()
#             print("✅ Firebase connection established successfully")
#         except Exception as e:
#             print(f"❌ Firebase connection failed: {str(e)}")
#             self.db = None
    
#     # Driver Management Methods
#     def get_all_drivers(self) -> List[Dict[str, Any]]:
#         """Get all drivers from Firestore"""
#         try:
#             if not self.db:
#                 print("❌ Firebase not connected")
#                 return []
            
#             # Use the correct capitalized collection name
#             drivers_ref = self.db.collection('Drivers')  # Note: capitalized
#             docs = drivers_ref.stream()
            
#             drivers = []
#             for doc in docs:
#                 driver_data = doc.to_dict()
#                 driver_data['id'] = doc.id
#                 drivers.append(driver_data)
#                 print(f"📄 Driver found: {doc.id}")
            
#             print(f"✅ Found {len(drivers)} drivers")
#             return drivers
            
#         except Exception as e:
#             print(f"❌ Error fetching drivers: {str(e)}")
#             logger.error(f"Error fetching drivers: {str(e)}")
#             return []
    
#     def get_driver_by_id(self, driver_id: str) -> Optional[Dict[str, Any]]:
#         """Get a specific driver by ID"""
#         try:
#             doc_ref = self.db.collection('Drivers').document(driver_id)  # Capitalized
#             doc = doc_ref.get()
            
#             if doc.exists:
#                 driver_data = doc.to_dict()
#                 driver_data['id'] = doc.id
#                 return driver_data
#             return None
#         except Exception as e:
#             logger.error(f"Error fetching driver {driver_id}: {str(e)}")
#             return None
    
#     def update_driver(self, driver_id: str, data: Dict[str, Any]) -> bool:
#         """Update driver information"""
#         try:
#             doc_ref = self.db.collection('Drivers').document(driver_id)  # Capitalized
#             doc_ref.update(data)
#             return True
#         except Exception as e:
#             logger.error(f"Error updating driver {driver_id}: {str(e)}")
#             return False
    
#     def create_driver(self, data: Dict[str, Any]) -> Optional[str]:
#         """Create a new driver"""
#         try:
#             doc_ref = self.db.collection('Drivers').add(data)  # Capitalized
#             return doc_ref[1].id
#         except Exception as e:
#             logger.error(f"Error creating driver: {str(e)}")
#             return None
    
#     def delete_driver(self, driver_id: str) -> bool:
#         """Delete a driver"""
#         try:
#             self.db.collection('Drivers').document(driver_id).delete()  # Capitalized
#             return True
#         except Exception as e:
#             logger.error(f"Error deleting driver {driver_id}: {str(e)}")
#             return False
    
#     # Customer Management Methods
#     def get_all_customers(self) -> List[Dict[str, Any]]:
#         """Get all customers from Firestore"""
#         try:
#             if not self.db:
#                 print("❌ Firebase not connected")
#                 return []
            
#             # Use the correct capitalized collection name
#             customers_ref = self.db.collection('Customers')  # Note: capitalized
#             docs = customers_ref.stream()
            
#             customers = []
#             for doc in docs:
#                 customer_data = doc.to_dict()
#                 customer_data['id'] = doc.id
#                 customers.append(customer_data)
#                 print(f"📄 Customer found: {doc.id}")
            
#             print(f"✅ Found {len(customers)} customers")
#             return customers
            
#         except Exception as e:
#             print(f"❌ Error fetching customers: {str(e)}")
#             logger.error(f"Error fetching customers: {str(e)}")
#             return []
    
#     def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
#         """Get a specific customer by ID"""
#         try:
#             doc_ref = self.db.collection('Customers').document(customer_id)  # Capitalized
#             doc = doc_ref.get()
            
#             if doc.exists:
#                 customer_data = doc.to_dict()
#                 customer_data['id'] = doc.id
#                 return customer_data
#             return None
#         except Exception as e:
#             logger.error(f"Error fetching customer {customer_id}: {str(e)}")
#             return None
    
#     def update_customer(self, customer_id: str, data: Dict[str, Any]) -> bool:
#         """Update customer information"""
#         try:
#             doc_ref = self.db.collection('Customers').document(customer_id)  # Capitalized
#             doc_ref.update(data)
#             return True
#         except Exception as e:
#             logger.error(f"Error updating customer {customer_id}: {str(e)}")
#             return False
    
#     def create_customer(self, data: Dict[str, Any]) -> Optional[str]:
#         """Create a new customer"""
#         try:
#             doc_ref = self.db.collection('Customers').add(data)  # Capitalized
#             return doc_ref[1].id
#         except Exception as e:
#             logger.error(f"Error creating customer: {str(e)}")
#             return None
    
#     def delete_customer(self, customer_id: str) -> bool:
#         """Delete a customer"""
#         try:
#             self.db.collection('Customers').document(customer_id).delete()  # Capitalized
#             return True
#         except Exception as e:
#             logger.error(f"Error deleting customer {customer_id}: {str(e)}")
#             return False
    
#     # Analytics and Reporting Methods
#     def get_drivers_stats(self) -> Dict[str, Any]:
#         """Get driver statistics"""
#         try:
#             drivers = self.get_all_drivers()
#             total_drivers = len(drivers)
#             active_drivers = len([d for d in drivers if d.get('status') == 'active'])
            
#             return {
#                 'total_drivers': total_drivers,
#                 'active_drivers': active_drivers,
#                 'inactive_drivers': total_drivers - active_drivers
#             }
#         except Exception as e:
#             logger.error(f"Error getting driver stats: {str(e)}")
#             return {}
    
#     def get_customers_stats(self) -> Dict[str, Any]:
#         """Get customer statistics"""
#         try:
#             customers = self.get_all_customers()
#             total_customers = len(customers)
            
#             return {
#                 'total_customers': total_customers,
#             }
#         except Exception as e:
#             logger.error(f"Error getting customer stats: {str(e)}")
#             return {}
        
        
# # Add these methods to FirebaseService class

# def get_driver_documents(self, driver_id: str) -> Optional[Dict[str, Any]]:
#     """Get driver's documents"""
#     try:
#         doc_ref = self.db.collection('DriversDocuments').document(driver_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             return doc.to_dict()
#         return None
#     except Exception as e:
#         logger.error(f"Error fetching driver documents {driver_id}: {str(e)}")
#         return None

# def get_all_vehicles(self) -> List[Dict[str, Any]]:
#     """Get all vehicles from Firestore"""
#     try:
#         vehicles_ref = self.db.collection('VehicleDetails')
#         docs = vehicles_ref.stream()
#         vehicles = []
#         for doc in docs:
#             data = doc.to_dict()
#             data['id'] = doc.id
#             vehicles.append(data)
#         return vehicles
#     except Exception as e:
#         logger.error(f"Error fetching vehicles: {str(e)}")
#         return []

# def get_vehicle_by_id(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
#     """Get a specific vehicle by ID"""
#     try:
#         doc_ref = self.db.collection('VehicleDetails').document(vehicle_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             data = doc.to_dict()
#             data['id'] = doc.id
#             return data
#         return None
#     except Exception as e:
#         logger.error(f"Error fetching vehicle {vehicle_id}: {str(e)}")
#         return None

# def update_vehicle(self, vehicle_id: str, data: Dict[str, Any]) -> bool:
#     """Update vehicle information"""
#     try:
#         doc_ref = self.db.collection('VehicleDetails').document(vehicle_id)
#         doc_ref.update(data)
#         return True
#     except Exception as e:
#         logger.error(f"Error updating vehicle {vehicle_id}: {str(e)}")
#         return False

# def delete_vehicle(self, vehicle_id: str) -> bool:
#     """Delete a vehicle"""
#     try:
#         self.db.collection('VehicleDetails').document(vehicle_id).delete()
#         return True
#     except Exception as e:
#         logger.error(f"Error deleting vehicle {vehicle_id}: {str(e)}")
#         return False


from firebase_admin import firestore
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        try:
            self.db = firestore.client()
            print("✅ Firebase connection established successfully")
        except Exception as e:
            print(f"❌ Firebase connection failed: {str(e)}")
            self.db = None
    
    # Driver Management Methods
    def get_all_drivers(self) -> List[Dict[str, Any]]:
        """Get all drivers from Firestore"""
        try:
            if not self.db:
                print("❌ Firebase not connected")
                return []
            
            drivers_ref = self.db.collection('Drivers')
            docs = drivers_ref.stream()
            
            drivers = []
            for doc in docs:
                driver_data = doc.to_dict()
                driver_data['id'] = doc.id
                drivers.append(driver_data)
                print(f"📄 Driver found: {doc.id}")
            
            print(f"✅ Found {len(drivers)} drivers")
            return drivers
            
        except Exception as e:
            print(f"❌ Error fetching drivers: {str(e)}")
            logger.error(f"Error fetching drivers: {str(e)}")
            return []
    
    def get_driver_by_id(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific driver by ID"""
        try:
            doc_ref = self.db.collection('Drivers').document(driver_id)
            doc = doc_ref.get()
            
            if doc.exists:
                driver_data = doc.to_dict()
                driver_data['id'] = doc.id
                return driver_data
            return None
        except Exception as e:
            logger.error(f"Error fetching driver {driver_id}: {str(e)}")
            return None
    
    def update_driver(self, driver_id: str, data: Dict[str, Any]) -> bool:
        """Update driver information"""
        try:
            doc_ref = self.db.collection('Drivers').document(driver_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating driver {driver_id}: {str(e)}")
            return False
    
    def create_driver(self, data: Dict[str, Any]) -> Optional[str]:
        """Create a new driver"""
        try:
            doc_ref = self.db.collection('Drivers').add(data)
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating driver: {str(e)}")
            return None
    
    def delete_driver(self, driver_id: str) -> bool:
        """Delete a driver"""
        try:
            self.db.collection('Drivers').document(driver_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting driver {driver_id}: {str(e)}")
            return False
    
    # Customer Management Methods
    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers from Firestore"""
        try:
            if not self.db:
                print("❌ Firebase not connected")
                return []
            
            customers_ref = self.db.collection('Customers')
            docs = customers_ref.stream()
            
            customers = []
            for doc in docs:
                customer_data = doc.to_dict()
                customer_data['id'] = doc.id
                customers.append(customer_data)
                print(f"📄 Customer found: {doc.id}")
            
            print(f"✅ Found {len(customers)} customers")
            return customers
            
        except Exception as e:
            print(f"❌ Error fetching customers: {str(e)}")
            logger.error(f"Error fetching customers: {str(e)}")
            return []
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific customer by ID"""
        try:
            doc_ref = self.db.collection('Customers').document(customer_id)
            doc = doc_ref.get()
            
            if doc.exists:
                customer_data = doc.to_dict()
                customer_data['id'] = doc.id
                return customer_data
            return None
        except Exception as e:
            logger.error(f"Error fetching customer {customer_id}: {str(e)}")
            return None
    
    def update_customer(self, customer_id: str, data: Dict[str, Any]) -> bool:
        """Update customer information"""
        try:
            doc_ref = self.db.collection('Customers').document(customer_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {str(e)}")
            return False
    
    def create_customer(self, data: Dict[str, Any]) -> Optional[str]:
        """Create a new customer"""
        try:
            doc_ref = self.db.collection('Customers').add(data)
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            return None
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        try:
            self.db.collection('Customers').document(customer_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting customer {customer_id}: {str(e)}")
            return False
    
    # Analytics and Reporting Methods
    def get_drivers_stats(self) -> Dict[str, Any]:
        """Get driver statistics"""
        try:
            drivers = self.get_all_drivers()
            total_drivers = len(drivers)
            active_drivers = len([d for d in drivers if d.get('status') == 'active'])
            pending_drivers = len([d for d in drivers if not d.get('isApproved', False)])
            approved_drivers = total_drivers - pending_drivers
            
            return {
                'total_drivers': total_drivers,
                'active_drivers': active_drivers,
                'inactive_drivers': total_drivers - active_drivers,
                'pending_drivers': pending_drivers,
                'approved_drivers': approved_drivers,
            }
        except Exception as e:
            logger.error(f"Error getting driver stats: {str(e)}")
            return {}
    
    def get_customers_stats(self) -> Dict[str, Any]:
        """Get customer statistics"""
        try:
            customers = self.get_all_customers()
            total_customers = len(customers)
            
            return {
                'total_customers': total_customers,
            }
        except Exception as e:
            logger.error(f"Error getting customer stats: {str(e)}")
            return {}
    
    # Add these methods to FirebaseService class
    def get_driver_documents(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get driver's documents"""
        try:
            doc_ref = self.db.collection('DriversDocuments').document(driver_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error fetching driver documents {driver_id}: {str(e)}")
            return None

    def get_all_vehicles(self) -> List[Dict[str, Any]]:
        """Get all vehicles from Firestore"""
        try:
            vehicles_ref = self.db.collection('VehicleDetails')
            docs = vehicles_ref.stream()
            vehicles = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                vehicles.append(data)
            return vehicles
        except Exception as e:
            logger.error(f"Error fetching vehicles: {str(e)}")
            return []

    def get_vehicle_by_id(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific vehicle by ID"""
        try:
            doc_ref = self.db.collection('VehicleDetails').document(vehicle_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"Error fetching vehicle {vehicle_id}: {str(e)}")
            return None

    def update_vehicle(self, vehicle_id: str, data: Dict[str, Any]) -> bool:
        """Update vehicle information"""
        try:
            doc_ref = self.db.collection('VehicleDetails').document(vehicle_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating vehicle {vehicle_id}: {str(e)}")
            return False

    def delete_vehicle(self, vehicle_id: str) -> bool:
        """Delete a vehicle"""
        try:
            self.db.collection('VehicleDetails').document(vehicle_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting vehicle {vehicle_id}: {str(e)}")
            return False