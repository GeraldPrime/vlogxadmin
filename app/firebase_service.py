# logistics_app/firebase_service.py
from firebase_admin import firestore
from typing import Dict, Any, Optional, List
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
            
            # Use the correct capitalized collection name
            drivers_ref = self.db.collection('Drivers')  # Note: capitalized
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
            doc_ref = self.db.collection('Drivers').document(driver_id)  # Capitalized
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
            doc_ref = self.db.collection('Drivers').document(driver_id)  # Capitalized
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating driver {driver_id}: {str(e)}")
            return False
    
    def create_driver(self, data: Dict[str, Any]) -> Optional[str]:
        """Create a new driver"""
        try:
            doc_ref = self.db.collection('Drivers').add(data)  # Capitalized
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating driver: {str(e)}")
            return None
    
    def delete_driver(self, driver_id: str) -> bool:
        """Delete a driver"""
        try:
            self.db.collection('Drivers').document(driver_id).delete()  # Capitalized
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
            
            # Use the correct capitalized collection name
            customers_ref = self.db.collection('Customers')  # Note: capitalized
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
            doc_ref = self.db.collection('Customers').document(customer_id)  # Capitalized
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
            doc_ref = self.db.collection('Customers').document(customer_id)  # Capitalized
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {str(e)}")
            return False
    
    def create_customer(self, data: Dict[str, Any]) -> Optional[str]:
        """Create a new customer"""
        try:
            doc_ref = self.db.collection('Customers').add(data)  # Capitalized
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            return None
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        try:
            self.db.collection('Customers').document(customer_id).delete()  # Capitalized
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
            
            return {
                'total_drivers': total_drivers,
                'active_drivers': active_drivers,
                'inactive_drivers': total_drivers - active_drivers
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
    def get_driver_trips(self, driver_id: str) -> List[Dict[str, Any]]:
        """Get all trips/delivery requests for a specific driver"""
        try:
            trips = []
            # Query DeliveryRequests where driverID matches (note: it's 'driverID' not 'driverId')
            trips_ref = self.db.collection('DeliveryRequests').where('driverID', '==', driver_id).stream()
            
            for doc in trips_ref:
                trip_data = doc.to_dict()
                trip_data['id'] = doc.id
                trips.append(trip_data)
            
            return trips
        except Exception as e:
            logger.error(f"Error fetching trips for driver {driver_id}: {str(e)}")
            return []

    def get_driver_current_trip(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get the driver's current active trip if any.

        Active statuses may include pending/accepted/picked_up/in_progress/started/ongoing.
        Falls back to the most recent ended/completed trip if no active one.
        """
        try:
            active_statuses = [
                'pending', 'accepted', 'picked_up', 'in_progress', 'started', 'ongoing'
            ]

            # First, search for an active trip
            query = (self.db.collection('DeliveryRequests')
                        .where('driverID', '==', driver_id)
                        .where('status', 'in', active_statuses)
                        .order_by('dateCreated', direction=firestore.Query.DESCENDING)
                        .limit(1))

            docs = list(query.stream())
            if docs:
                doc = docs[0]
                data = doc.to_dict()
                data['id'] = doc.id
                return data

            # If none active, return the most recent trip (optional)
            fallback_query = (self.db.collection('DeliveryRequests')
                                .where('driverID', '==', driver_id)
                                .order_by('dateCreated', direction=firestore.Query.DESCENDING)
                                .limit(1))
            fallback_docs = list(fallback_query.stream())
            if fallback_docs:
                doc = fallback_docs[0]
                data = doc.to_dict()
                data['id'] = doc.id
                return data

            return None
        except Exception as e:
            logger.error(f"Error fetching current trip for driver {driver_id}: {str(e)}")
            return None

    def get_driver_ratings(self, driver_id: str) -> List[Dict[str, Any]]:
        """Get all ratings for a specific driver"""
        try:
            ratings = []
            # Query DriverRatings where driverId matches (note: it's 'driverId' not 'driverID')
            ratings_ref = self.db.collection('DriversRatings').where('driverId', '==', driver_id).stream()
            
            for doc in ratings_ref:
                rating_data = doc.to_dict()
                rating_data['id'] = doc.id
                
                # Try to get customer info for this rating
                if 'customerId' in rating_data:
                    customer = self.get_customer_by_id(rating_data['customerId'])
                    if customer:
                        rating_data['customer_name'] = f"{customer.get('firstName', '')} {customer.get('lastName', '')}"
                
                # Try to infer trip info: use the latest DeliveryRequest for same driver and customer
                if not rating_data.get('tripId') and not rating_data.get('link_order_id'):
                    try:
                        if rating_data.get('customerId'):
                            query = (self.db.collection('DeliveryRequests')
                                        .where('driverID', '==', driver_id)
                                        .where('userID', '==', rating_data['customerId'])
                                        .limit(1))
                            trip_docs = list(query.stream())  # Avoid order_by to prevent index requirements
                            if trip_docs:
                                tdoc = trip_docs[0]
                                rating_data['tripId'] = tdoc.id
                                rating_data['link_order_id'] = tdoc.id
                        # Fallback: latest trip for driver regardless of customer
                        if not rating_data.get('tripId') and not rating_data.get('link_order_id'):
                            fallback_q = (self.db.collection('DeliveryRequests')
                                            .where('driverID', '==', driver_id)
                                            .limit(1))
                            fdocs = list(fallback_q.stream())  # Avoid order_by to prevent index requirements
                            if fdocs:
                                fdoc = fdocs[0]
                                rating_data['link_order_id'] = fdoc.id
                    except Exception:
                        # Best-effort enrichment; ignore failures
                        pass

                # Unified field used by templates for linking to order detail
                order_id = rating_data.get('tripId') or rating_data.get('link_order_id')
                if order_id:
                    rating_data['order_id'] = order_id
                
                ratings.append(rating_data)
            
            return ratings
        except Exception as e:
            logger.error(f"Error fetching ratings for driver {driver_id}: {str(e)}")
            return []

    def get_driver_balance(self, driver_id: str) -> Dict[str, Any]:
        """Get driver's balance information"""
        try:
            doc_ref = self.db.collection('DriverBalances').document(driver_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return {'balance': 0, 'pendingAmount': 0, 'totalEarned': 0}
        except Exception as e:
            logger.error(f"Error fetching balance for driver {driver_id}: {str(e)}")
            return {'balance': 0, 'pendingAmount': 0, 'totalEarned': 0}

    def get_rating_analytics(self, driver_id: str) -> Dict[str, Any]:
        """Get comprehensive rating analytics for a driver"""
        try:
            ratings = self.get_driver_ratings(driver_id)
            
            if not ratings:
                return {
                    'total_ratings': 0,
                    'average_rating': 0,
                    'rating_breakdown': {},
                    'recent_ratings': []
                }
            
            # Calculate analytics - handle both 'rating' and 'driverRating' field names
            total_ratings = len(ratings)
            total_score = 0
            for rating in ratings:
                # Try both field names
                rating_value = rating.get('rating') or rating.get('driverRating', 0)
                total_score += rating_value if rating_value else 0
            
            average_rating = total_score / total_ratings if total_ratings > 0 else 0
            
            # Rating breakdown (1-5 stars exact) and threshold breakdown (3+, 4+, 4.5+)
            rating_breakdown = {}
            thresholds = {
                '3_plus': 0,
                '4_plus': 0,
                '4_5_plus': 0,
            }

            for r in ratings:
                rating_value = r.get('rating') or r.get('driverRating', 0)
                # Exact bucket (rounded down to nearest int within 1..5 for visualization)
                try:
                    iv = int(rating_value)
                    if iv < 1:
                        iv = 1
                    if iv > 5:
                        iv = 5
                except Exception:
                    iv = 0
                if iv:
                    rating_breakdown[str(iv)] = rating_breakdown.get(str(iv), 0) + 1

                # Threshold buckets
                try:
                    rv = float(rating_value)
                    if rv >= 3.0:
                        thresholds['3_plus'] += 1
                    if rv >= 4.0:
                        thresholds['4_plus'] += 1
                    if rv >= 4.5:
                        thresholds['4_5_plus'] += 1
                except Exception:
                    pass
            
            # Recent ratings (last 10, sorted by date)
            recent_ratings = sorted(ratings, key=lambda x: x.get('dateCreated', ''), reverse=True)[:10]
            
            # Prepare a template-friendly distribution list for 1..5 stars
            rating_distribution = []
            for i in range(1, 6):
                count_i = rating_breakdown.get(str(i), 0)
                rating_distribution.append({'label': str(i), 'count': count_i})

            return {
                'total_ratings': total_ratings,
                'average_rating': round(average_rating, 2),
                'rating_breakdown': rating_breakdown,
                'rating_distribution': rating_distribution,
                'threshold_breakdown': thresholds,
                'recent_ratings': recent_ratings
            }
        except Exception as e:
            logger.error(f"Error getting rating analytics for driver {driver_id}: {str(e)}")
            return {
                'total_ratings': 0,
                'average_rating': 0,
                'rating_breakdown': {},
                'recent_ratings': []
            }

    def get_driver_earnings(self, driver_id: str) -> Dict[str, Any]:
        """Get comprehensive earnings information for a driver"""
        try:
            # Get all trips for the driver
            trips = self.get_driver_trips(driver_id)
            completed_trips = [trip for trip in trips if trip.get('status') in ['completed', 'ended', 'delivered']]
            
            # Calculate earnings - handle multiple possible field names
            total_earnings = 0
            for trip in completed_trips:
                # Try different field names for earnings
                earnings = (trip.get('driverEarnings') or 
                           trip.get('deliveryAmount') or 
                           trip.get('amount') or 
                           trip.get('totalAmount') or 0)
                # Convert string to float if needed
                if isinstance(earnings, str):
                    try:
                        earnings = float(earnings)
                    except (ValueError, TypeError):
                        earnings = 0
                total_earnings += earnings
            
            total_trips = len(completed_trips)
            avg_earnings_per_trip = total_earnings / total_trips if total_trips > 0 else 0
            
            # Get balance info
            balance_info = self.get_driver_balance(driver_id)
            
            return {
                'total_earnings': total_earnings,
                'total_trips': total_trips,
                'avg_earnings_per_trip': round(avg_earnings_per_trip, 2),
                'current_balance': balance_info.get('balance', 0),
                'pending_amount': balance_info.get('pendingAmount', 0),
                'total_withdrawals': balance_info.get('totalEarned', 0) - balance_info.get('balance', 0)
            }
        except Exception as e:
            logger.error(f"Error getting earnings for driver {driver_id}: {str(e)}")
            return {
                'total_earnings': 0,
                'total_trips': 0,
                'avg_earnings_per_trip': 0,
                'current_balance': 0,
                'pending_amount': 0,
                'total_withdrawals': 0
            }

    def get_driver_location(self, driver_id: str) -> Dict[str, Any]:
        """Get driver's current location information"""
        try:
            # Try to get location from DriverLocation collection (note: singular, not plural)
            location_ref = self.db.collection('DriverLocation').document(driver_id)
            location_doc = location_ref.get()
            
            if location_doc.exists:
                location_data = location_doc.to_dict()
                return {
                    'latitude': location_data.get('latitude', 0),
                    'longitude': location_data.get('longitude', 0),
                    'address': location_data.get('address', 'Location not available'),
                    'last_updated': location_data.get('updatedOn', ''),
                    'is_online': location_data.get('isOnline', False)
                }
            
            # Fallback: check if driver is online from driver document
            driver = self.get_driver_by_id(driver_id)
            if driver and driver.get('isDriverOnline', False):
                return {
                    'latitude': driver.get('latitude', 0),
                    'longitude': driver.get('longitude', 0),
                    'address': driver.get('address', 'Location not available'),
                    'last_updated': driver.get('lastLocationUpdate', ''),
                    'is_online': True
                }
            
            return {
                'latitude': 0,
                'longitude': 0,
                'address': 'Location not available',
                'last_updated': '',
                'is_online': False
            }
        except Exception as e:
            logger.error(f"Error getting location for driver {driver_id}: {str(e)}")
            return {
                'latitude': 0,
                'longitude': 0,
                'address': 'Location not available',
                'last_updated': '',
                'is_online': False
            }

    def get_customer_location(self, customer_id: str) -> Dict[str, Any]:
        """Get customer's current location information (if tracked)"""
        try:
            # Reuse DriverLocation collection pattern for customers if available
            location_ref = self.db.collection('CustomerLocation').document(customer_id)
            location_doc = location_ref.get()
            if location_doc.exists:
                location_data = location_doc.to_dict()
                return {
                    'latitude': location_data.get('latitude', 0),
                    'longitude': location_data.get('longitude', 0),
                    'address': location_data.get('address', 'Location not available'),
                    'last_updated': location_data.get('updatedOn', '')
                }

            # Fallback: sometimes location may be embedded on the customer doc
            customer = self.get_customer_by_id(customer_id)
            if customer and ('latitude' in customer or 'longitude' in customer):
                return {
                    'latitude': customer.get('latitude', 0),
                    'longitude': customer.get('longitude', 0),
                    'address': customer.get('address', 'Location not available'),
                    'last_updated': customer.get('lastLocationUpdate', '')
                }

            return {
                'latitude': 0,
                'longitude': 0,
                'address': 'Location not available',
                'last_updated': ''
            }
        except Exception as e:
            logger.error(f"Error getting location for customer {customer_id}: {str(e)}")
            return {
                'latitude': 0,
                'longitude': 0,
                'address': 'Location not available',
                'last_updated': ''
            }

    def get_customer_trips(self, customer_id: str) -> List[Dict[str, Any]]:
        """Get delivery requests created by a specific customer"""
        try:
            trips = []
            trips_ref = self.db.collection('DeliveryRequests').where('userID', '==', customer_id).stream()
            for doc in trips_ref:
                data = doc.to_dict()
                data['id'] = doc.id
                trips.append(data)
            return trips
        except Exception as e:
            logger.error(f"Error fetching trips for customer {customer_id}: {str(e)}")
            return []

    def get_driver_stats_enhanced(self) -> Dict[str, Any]:
        """Get enhanced driver statistics with more detailed breakdown"""
        try:
            drivers = self.get_all_drivers()
            total_drivers = len(drivers)
            
            # Categorize drivers by status
            active_drivers = len([d for d in drivers if d.get('isDriverOnline', False)])
            offline_drivers = total_drivers - active_drivers
            pending_drivers = len([d for d in drivers if not d.get('isApproved', False)])
            approved_drivers = len([d for d in drivers if d.get('isApproved', False)])
            
            return {
                'total_drivers': total_drivers,
                'active_drivers': active_drivers,
                'offline_drivers': offline_drivers,
                'pending_drivers': pending_drivers,
                'approved_drivers': approved_drivers
            }
        except Exception as e:
            logger.error(f"Error getting enhanced driver stats: {str(e)}")
            return {
                'total_drivers': 0,
                'active_drivers': 0,
                'offline_drivers': 0,
                'pending_drivers': 0,
                'approved_drivers': 0
            }

    def get_trip_analytics(self) -> Dict[str, Any]:
        """Get comprehensive trip analytics"""
        try:
            trips = self.get_all_trips(limit=1000)  # Get more trips for better analytics
            if not trips:
                return {
                    'total_trips': 0,
                    'completed_trips': 0,
                    'total_revenue': 0,
                    'completion_rate': 0
                }
            
            total_trips = len(trips)
            completed_trips = [trip for trip in trips if trip.get('status') in ['completed', 'ended', 'delivered']]
            completed_count = len(completed_trips)
            completion_rate = (completed_count / total_trips * 100) if total_trips > 0 else 0
            
            # Calculate total revenue - handle multiple possible field names
            total_revenue = 0
            for trip in completed_trips:
                revenue = (trip.get('totalAmount') or 
                          trip.get('deliveryAmount') or 
                          trip.get('amount') or 0)
                # Convert string to float if needed
                if isinstance(revenue, str):
                    try:
                        revenue = float(revenue)
                    except (ValueError, TypeError):
                        revenue = 0
                total_revenue += revenue
            
            return {
                'total_trips': total_trips,
                'completed_trips': completed_count,
                'total_revenue': total_revenue,
                'completion_rate': round(completion_rate, 2)
            }
        except Exception as e:
            logger.error(f"Error getting trip analytics: {str(e)}")
            return {
                'total_trips': 0,
                'completed_trips': 0,
                'total_revenue': 0,
                'completion_rate': 0
            }

    # def get_payment_modes(self) -> List[Dict[str, Any]]:
    #     """Get all available payment modes"""
    #     try:
    #         payment_modes_ref = self.db.collection('PaymentModes').stream()
    #         payment_modes = []
            
    #         for doc in payment_modes_ref:
    #             mode_data = doc.to_dict()
    #             mode_data['id'] = doc.id
    #             payment_modes.append(mode_data)
                
    #         return payment_modes
    #     except Exception as e:
    #         logger.error(f"Error fetching payment modes: {str(e)}")
    #         return []


    def get_payment_modes(self) -> List[Dict[str, Any]]:
        """Get all available payment modes"""
        try:
            payment_modes_ref = self.db.collection('PaymentMode').stream()  # Note: singular 'PaymentMode'
            payment_modes = []
            
            for doc in payment_modes_ref:
                mode_data = doc.to_dict()
                mode_data['id'] = doc.id
                payment_modes.append(mode_data)
                
            return payment_modes
        except Exception as e:
            logger.error(f"Error fetching payment modes: {str(e)}")
            return []


    def get_payment_mode_by_id(self, payment_mode_id: str) -> Optional[Dict[str, Any]]:
        """Get payment mode by ID"""
        try:
            doc_ref = self.db.collection('PaymentMode').document(payment_mode_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"Error fetching payment mode {payment_mode_id}: {str(e)}")
            return None

    def update_payment_mode(self, payment_mode_id: str, data: Dict[str, Any]) -> bool:
        """Update payment mode in Firestore"""
        try:
            doc_ref = self.db.collection('PaymentMode').document(payment_mode_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating payment mode {payment_mode_id}: {str(e)}")
            return False

    def create_payment_mode(self, data: Dict[str, Any]) -> Optional[str]:
        """Create new payment mode in Firestore"""
        try:
            # Add timestamp
            data['dateCreated'] = firestore.SERVER_TIMESTAMP
            
            # Add the document to Firestore
            doc_ref = self.db.collection('PaymentMode').document()
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating payment mode: {str(e)}")
            return None

    def delete_payment_mode(self, payment_mode_id: str) -> bool:
        """Delete payment mode from Firestore"""
        try:
            self.db.collection('PaymentMode').document(payment_mode_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting payment mode {payment_mode_id}: {str(e)}")
            return False

    # def get_payment_settings(self) -> List[Dict[str, Any]]:
    #     """Get all payment settings from Firestore"""
    #     try:
    #         payment_settings_ref = self.db.collection('PaymentSettings')
    #         docs = payment_settings_ref.stream()
    #         payment_settings = []
    #         for doc in docs:
    #             data = doc.to_dict()
    #             data['id'] = doc.id
    #             payment_settings.append(data)
    #         return payment_settings
    #     except Exception as e:
    #         logger.error(f"Error fetching payment settings: {str(e)}")
    #         return []



    def get_payment_settings(self) -> List[Dict[str, Any]]:
        """Get all payment settings from Firestore with vehicle type names"""
        try:
            payment_settings_ref = self.db.collection('PaymentSettings')
            docs = payment_settings_ref.stream()
            payment_settings = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                
                # Fetch vehicle type name if vehicleTypeId exists
                if data.get('vehicleTypeId'):
                    vehicle_type = self.get_vehicle_type_by_id(data['vehicleTypeId'])
                    if vehicle_type:
                        data['vehicle_type_name'] = vehicle_type.get('type', 'Unknown')
                        data['vehicle_type_icon'] = vehicle_type.get('vehicleIcon', 'car')
                    else:
                        data['vehicle_type_name'] = data['vehicleTypeId']  # Fallback to ID
                
                payment_settings.append(data)
                
            return payment_settings
        except Exception as e:
            logger.error(f"Error fetching payment settings: {str(e)}")
            return []


    def get_payment_setting_by_id(self, payment_setting_id: str) -> Optional[Dict[str, Any]]:
        """Get payment setting by ID"""
        try:
            doc_ref = self.db.collection('PaymentSettings').document(payment_setting_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"Error fetching payment setting {payment_setting_id}: {str(e)}")
            return None

    def update_payment_setting(self, payment_setting_id: str, data: Dict[str, Any]) -> bool:
        """Update payment setting in Firestore"""
        try:
            doc_ref = self.db.collection('PaymentSettings').document(payment_setting_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating payment setting {payment_setting_id}: {str(e)}")
            return False

    def create_payment_setting(self, data: Dict[str, Any]) -> Optional[str]:
        """Create new payment setting in Firestore"""
        try:
            # Add timestamp
            data['dateCreated'] = firestore.SERVER_TIMESTAMP
            
            # Add the document to Firestore
            doc_ref = self.db.collection('PaymentSettings').document()
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating payment setting: {str(e)}")
            return None

    def delete_payment_setting(self, payment_setting_id: str) -> bool:
        """Delete payment setting from Firestore"""
        try:
            self.db.collection('PaymentSettings').document(payment_setting_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting payment setting {payment_setting_id}: {str(e)}")
            return False
        
    # def get_all_trips(self, limit=50, status=None):
    #     """Get all delivery trips/requests with optional filtering"""
    #     try:
    #         trips_ref = self.db.collection('DeliveryRequests')
            
    #         # Apply status filter if provided
    #         if status:
    #             trips_ref = trips_ref.where('status', '==', status)
                
    #         # Apply limit
    #         trips_ref = trips_ref.limit(limit)
            
    #         # Get documents
    #         docs = trips_ref.stream()
            
    #         trips = []
    #         for doc in docs:
    #             trip_data = doc.to_dict()
    #             trip_data['id'] = doc.id
    #             trips.append(trip_data)
                
    #         return trips
    #     except Exception as e:
    #         logger.error(f"Error fetching trips: {str(e)}")
    #         return []


    def get_all_trips(self, limit=50, status=None):
        """Get all delivery trips/requests with optional filtering and driver names"""
        try:
            trips_ref = self.db.collection('DeliveryRequests')
            
            # Apply status filter if provided
            if status:
                trips_ref = trips_ref.where('status', '==', status)
                
            # Apply limit and order by date
            trips_ref = trips_ref.limit(limit).order_by('dateCreated', direction=firestore.Query.DESCENDING)
            
            # Get documents
            docs = trips_ref.stream()
            
            trips = []
            for doc in docs:
                trip_data = doc.to_dict()
                trip_data['id'] = doc.id
                
                # Fetch driver name if driverID exists
                if trip_data.get('driverID'):
                    driver = self.get_driver_by_id(trip_data['driverID'])
                    if driver:
                        # Combine first and last name
                        first_name = driver.get('firstName', '').strip()
                        last_name = driver.get('lastName', '').strip()
                        
                        if first_name and last_name:
                            trip_data['driver_name'] = f"{first_name} {last_name}"
                        elif first_name:
                            trip_data['driver_name'] = first_name
                        elif last_name:
                            trip_data['driver_name'] = last_name
                        else:
                            trip_data['driver_name'] = "Unknown Driver"
                    else:
                        trip_data['driver_name'] = "Driver Not Found"
                
                # Optionally fetch customer name as well for better display
                if trip_data.get('userID'):
                    customer = self.get_customer_by_id(trip_data['userID'])
                    if customer:
                        first_name = customer.get('firstName', '').strip()
                        last_name = customer.get('lastName', '').strip()
                        
                        if first_name and last_name:
                            trip_data['customer_name'] = f"{first_name} {last_name}"
                        elif first_name:
                            trip_data['customer_name'] = first_name
                        elif last_name:
                            trip_data['customer_name'] = last_name
                        else:
                            trip_data['customer_name'] = trip_data.get('userName', 'Unknown Customer')
                    else:
                        trip_data['customer_name'] = trip_data.get('userName', 'Customer Not Found')
                elif trip_data.get('userName'):
                    trip_data['customer_name'] = trip_data['userName']
                elif trip_data.get('recipientName'):
                    trip_data['customer_name'] = trip_data['recipientName']
                
                trips.append(trip_data)
                
            logger.info(f"Found {len(trips)} trips with driver names populated")
            return trips
            
        except Exception as e:
            logger.error(f"Error fetching trips: {str(e)}")
            return []



    # def get_trip_by_id(self, trip_id):
    #     """Get trip details by ID"""
    #     try:
    #         trip_ref = self.db.collection('DeliveryRequests').document(trip_id)
    #         trip = trip_ref.get()
            
    #         if not trip.exists:
    #             return None
                
    #         trip_data = trip.to_dict()
    #         trip_data['id'] = trip.id
            
    #         # Get customer and driver details
    #         if 'customerId' in trip_data:
    #             customer = self.get_customer_by_id(trip_data['customerId'])
    #             if customer:
    #                 trip_data['customer'] = customer
            
    #         if 'driverId' in trip_data:
    #             driver = self.get_driver_by_id(trip_data['driverId'])
    #             if driver:
    #                 trip_data['driver'] = driver
                
    #         return trip_data
    #     except Exception as e:
    #         logger.error(f"Error getting trip by ID: {str(e)}")
    #         return None

    def get_trip_by_id(self, trip_id):
        """Get trip details by ID with driver and customer names"""
        try:
            trip_ref = self.db.collection('DeliveryRequests').document(trip_id)
            trip = trip_ref.get()
            
            if not trip.exists:
                return None
                
            trip_data = trip.to_dict()
            trip_data['id'] = trip.id
            
            # Fetch driver name if driverID exists
            if trip_data.get('driverID'):
                driver = self.get_driver_by_id(trip_data['driverID'])
                if driver:
                    first_name = driver.get('firstName', '').strip()
                    last_name = driver.get('lastName', '').strip()
                    trip_data['driver_name'] = f"{first_name} {last_name}".strip()
            
            # Fetch customer name if userID exists
            if trip_data.get('userID'):
                customer = self.get_customer_by_id(trip_data['userID'])
                if customer:
                    first_name = customer.get('firstName', '').strip()
                    last_name = customer.get('lastName', '').strip()
                    trip_data['customer_name'] = f"{first_name} {last_name}".strip()
                    
            return trip_data
        except Exception as e:
            logger.error(f"Error getting trip by ID: {str(e)}")
            return None



    def update_trip_status(self, trip_id, status):
            """Update trip status"""
            try:
                trip_ref = self.db.collection('DeliveryRequests').document(trip_id)
                trip_ref.update({
                    'status': status,
                    'dateUpdated': firestore.SERVER_TIMESTAMP
                })
                return True
            except Exception as e:
                logger.error(f"Error updating trip status: {str(e)}")
                return False
        
    # def get_vehicle_type_by_id(self, type_id):
    #     """Get vehicle type by ID"""
    #     try:
    #         vehicle_type_ref = self.db.collection('vehicle_types').document(type_id)
    #         vehicle_type = vehicle_type_ref.get()
            
    #         if not vehicle_type.exists:
    #             return None
                
    #         data = vehicle_type.to_dict()
    #         data['id'] = vehicle_type.id
    #         return data
    #     except Exception as e:
    #         logger.error(f"Error getting vehicle type by ID: {str(e)}")
    #         return None


    def get_vehicle_type_by_id(self, type_id: str) -> Optional[Dict[str, Any]]:
        """Get vehicle type by ID"""
        try:
            doc_ref = self.db.collection('VehicleTypes').document(type_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"Error fetching vehicle type {type_id}: {str(e)}")
            return None
        
                
    # def get_vehicle_types(self):
    #     """Get all vehicle types"""
    #     try:
    #         vehicle_types = self.db.collection('vehicle_types').order_by('name').stream()
    #         result = []
    #         for vehicle_type in vehicle_types:
    #             data = vehicle_type.to_dict()
    #             data['id'] = vehicle_type.id
    #             result.append(data)
    #         return result
    #     except Exception as e:
    #         logger.error(f"Error getting vehicle types: {str(e)}")
    #         return []

    
    # def create_vehicle_type(self, data):
    #     """Create a new vehicle type"""
    #     try:
    #         # Add timestamp
    #         data['dateCreated'] = firestore.SERVER_TIMESTAMP
    #         data['dateUpdated'] = firestore.SERVER_TIMESTAMP
            
    #         # Create vehicle type
    #         vehicle_type_ref = self.db.collection('vehicle_types').document()
    #         vehicle_type_ref.set(data)
            
    #         return vehicle_type_ref.id
    #     except Exception as e:
    #         logger.error(f"Error creating vehicle type: {str(e)}")
    #         return None

    # def update_vehicle_type(self, type_id, data):
    #     """Update a vehicle type"""
    #     try:
    #         # Add timestamp
    #         data['dateUpdated'] = firestore.SERVER_TIMESTAMP
            
    #         # Update vehicle type
    #         self.db.collection('vehicle_types').document(type_id).update(data)
    #         return True
    #     except Exception as e:
    #         logger.error(f"Error updating vehicle type: {str(e)}")
    #         return False

    # def delete_vehicle_type(self, type_id):
    #     """Delete a vehicle type"""
    #     try:
    #         self.db.collection('vehicle_types').document(type_id).delete()
    #         return True
    #     except Exception as e:
    #         logger.error(f"Error deleting vehicle type: {str(e)}")
    #         return False

    def get_vehicle_types(self):
        """Get all vehicle types"""
        try:
            vehicle_types_ref = self.db.collection('VehicleTypes').stream()
            result = []
            for vehicle_type in vehicle_types_ref:
                data = vehicle_type.to_dict()
                data['id'] = vehicle_type.id
                result.append(data)
            return result
        except Exception as e:
            logger.error(f"Error getting vehicle types: {str(e)}")
            return []

    def create_vehicle_type(self, data):
        """Create a new vehicle type"""
        try:
            # Add timestamp
            data['dateCreated'] = firestore.SERVER_TIMESTAMP
            
            # Create vehicle type
            vehicle_type_ref = self.db.collection('VehicleTypes').document()
            vehicle_type_ref.set(data)
            
            return vehicle_type_ref.id
        except Exception as e:
            logger.error(f"Error creating vehicle type: {str(e)}")
            return None

    def update_vehicle_type(self, type_id, data):
        """Update a vehicle type"""
        try:
            self.db.collection('VehicleTypes').document(type_id).update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating vehicle type: {str(e)}")
            return False

    def delete_vehicle_type(self, type_id):
        """Delete a vehicle type"""
        try:
            self.db.collection('VehicleTypes').document(type_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting vehicle type: {str(e)}")
            return False



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
    
    # FAQ Management Methods
    def get_all_faqs(self) -> List[Dict[str, Any]]:
        """Get all FAQs from Firestore"""
        try:
            faqs_ref = self.db.collection('FAQs')
            docs = faqs_ref.stream()
            faqs = []
            for doc in docs:
                faq = doc.to_dict()
                faq['id'] = doc.id
                faqs.append(faq)
            return faqs
        except Exception as e:
            logger.error(f"Error fetching FAQs: {str(e)}")
            return []

    def get_faq_by_id(self, faq_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific FAQ by ID"""
        try:
            doc_ref = self.db.collection('FAQs').document(faq_id)
            doc = doc_ref.get()
            if doc.exists:
                faq = doc.to_dict()
                faq['id'] = doc.id
                return faq
            return None
        except Exception as e:
            logger.error(f"Error fetching FAQ {faq_id}: {str(e)}")
            return None

    def create_faq(self, data: Dict[str, Any]) -> Optional[str]:
        """Create a new FAQ"""
        try:
            doc_ref = self.db.collection('FAQs').add(data)
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error creating FAQ: {str(e)}")
            return None

    def update_faq(self, faq_id: str, data: Dict[str, Any]) -> bool:
        """Update FAQ information"""
        try:
            doc_ref = self.db.collection('FAQs').document(faq_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            logger.error(f"Error updating FAQ {faq_id}: {str(e)}")
            return False

    def delete_faq(self, faq_id: str) -> bool:
        """Delete a FAQ"""
        try:
            self.db.collection('FAQs').document(faq_id).delete()
            return True
        except Exception as e:
            logger.error(f"Error deleting FAQ {faq_id}: {str(e)}")
            return False