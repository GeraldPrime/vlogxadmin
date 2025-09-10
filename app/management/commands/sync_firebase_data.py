# app/management/commands/sync_firebase_data.py
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from firebase_admin import firestore
from django.utils import timezone
from datetime import datetime
import logging
from app.models import Driver, Customer, DeliveryOrder

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync data between Django and Firebase (matching your actual Firebase structure)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model', 
            type=str, 
            choices=['drivers', 'customers', 'orders', 'all'],
            default='all',
            help='Model to sync (drivers/customers/orders/all)'
        )
        parser.add_argument(
            '--direction', 
            type=str, 
            choices=['from_firebase', 'to_firebase', 'both'],
            default='from_firebase', 
            help='Sync direction (from_firebase/to_firebase/both)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synced without actually doing it'
        )

    def handle(self, *args, **options):
        model = options['model']
        direction = options['direction']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        try:
            # Test Firebase connection first
            self._test_firebase_connection()
            
            if model == 'drivers' or model == 'all':
                self._sync_drivers(direction, dry_run)
                
            if model == 'customers' or model == 'all':
                self._sync_customers(direction, dry_run)
                
            if model == 'orders' or model == 'all':
                self._sync_orders(direction, dry_run)
                
            self.stdout.write(
                self.style.SUCCESS(f'Successfully completed sync for {model}')
            )
            
        except Exception as e:
            logger.error(f'Error during sync: {str(e)}')
            raise CommandError(f'Sync failed: {str(e)}')

    def _test_firebase_connection(self):
        """Test Firebase connection"""
        try:
            db = firestore.client()
            collections = list(db.collections())
            collection_names = [c.id for c in collections]
            self.stdout.write(f"Firebase connected. Available collections: {collection_names}")
            return True
        except Exception as e:
            raise CommandError(f"Firebase connection failed: {str(e)}")

    def _sync_drivers(self, direction, dry_run):
        """Sync drivers data"""
        if direction in ['from_firebase', 'both']:
            self.stdout.write('Syncing drivers from Firebase...')
            if not dry_run:
                count = self._sync_drivers_from_firebase()
                self.stdout.write(
                    self.style.SUCCESS(f'Synced {count} drivers from Firebase')
                )
            else:
                count = self._count_firebase_drivers()
                self.stdout.write(f'Would sync {count} drivers from Firebase')
                
        if direction in ['to_firebase', 'both']:
            self.stdout.write('Syncing drivers to Firebase...')
            if not dry_run:
                count = self._sync_drivers_to_firebase()
                self.stdout.write(
                    self.style.SUCCESS(f'Synced {count} drivers to Firebase')
                )
            else:
                count = Driver.objects.count()
                self.stdout.write(f'Would sync {count} drivers to Firebase')

    def _sync_customers(self, direction, dry_run):
        """Sync customers data"""
        if direction in ['from_firebase', 'both']:
            self.stdout.write('Syncing customers from Firebase...')
            if not dry_run:
                count = self._sync_customers_from_firebase()
                self.stdout.write(
                    self.style.SUCCESS(f'Synced {count} customers from Firebase')
                )
            else:
                count = self._count_firebase_customers()
                self.stdout.write(f'Would sync {count} customers from Firebase')
                
        if direction in ['to_firebase', 'both']:
            self.stdout.write('Syncing customers to Firebase...')
            if not dry_run:
                count = self._sync_customers_to_firebase()
                self.stdout.write(
                    self.style.SUCCESS(f'Synced {count} customers to Firebase')
                )
            else:
                count = Customer.objects.count()
                self.stdout.write(f'Would sync {count} customers to Firebase')

    def _sync_orders(self, direction, dry_run):
        """Sync orders data"""
        if direction in ['from_firebase', 'both']:
            self.stdout.write('Syncing orders from Firebase...')
            if not dry_run:
                count = self._sync_orders_from_firebase()
                self.stdout.write(
                    self.style.SUCCESS(f'Synced {count} orders from Firebase')
                )
            else:
                count = self._count_firebase_orders()
                self.stdout.write(f'Would sync {count} orders from Firebase')

    def _count_firebase_drivers(self):
        """Count drivers in Firebase"""
        db = firestore.client()
        drivers_ref = db.collection('Drivers')
        docs = list(drivers_ref.stream())
        return len(docs)

    def _count_firebase_customers(self):
        """Count customers in Firebase"""
        db = firestore.client()
        customers_ref = db.collection('Customers')
        docs = list(customers_ref.stream())
        return len(docs)

    def _count_firebase_orders(self):
        """Count orders in Firebase"""
        db = firestore.client()
        orders_ref = db.collection('Orders')  # Assuming you have an Orders collection
        docs = list(orders_ref.stream())
        return len(docs)

    def _sync_drivers_from_firebase(self):
        """Sync drivers from Firebase to Django"""
        db = firestore.client()
        drivers_ref = db.collection('Drivers')
        docs = drivers_ref.stream()
        
        count = 0
        errors = 0
        
        for doc in docs:
            try:
                data = doc.to_dict()
                
                # Parse dateCreated - handle different formats
                date_created = timezone.now()
                if data.get('dateCreated'):
                    try:
                        # Try ISO format first
                        date_created = datetime.fromisoformat(
                            data['dateCreated'].replace('Z', '+00:00')
                        )
                    except (ValueError, AttributeError):
                        try:
                            # Try timestamp format
                            if hasattr(data['dateCreated'], 'seconds'):
                                date_created = datetime.fromtimestamp(
                                    data['dateCreated'].seconds
                                )
                            else:
                                date_created = timezone.now()
                        except:
                            date_created = timezone.now()
                
                # Extract geo position
                geo_position = data.get('geoPosition')
                latitude = None
                longitude = None
                if geo_position and isinstance(geo_position, dict):
                    latitude = geo_position.get('latitude')
                    longitude = geo_position.get('longitude')
                
                # Create or update driver
                driver, created = Driver.objects.update_or_create(
                    firebase_id=doc.id,
                    defaults={
                        'drivers_id': data.get('driversId', doc.id),
                        'first_name': data.get('firstName', ''),
                        'last_name': data.get('lastName', ''),
                        'email': data.get('email', ''),
                        'phone_number': data.get('phoneNumber', ''),
                        'profile_pic': data.get('profilePic'),
                        'is_approved': data.get('isApproved', False),
                        'is_driver_online': data.get('isDriverOnline', False),
                        'user_token': data.get('userToken', ''),
                        'latitude': latitude,
                        'longitude': longitude,
                        'date_created': date_created,
                    }
                )
                
                if created:
                    self.stdout.write(f"Created new driver: {driver.full_name}")
                else:
                    self.stdout.write(f"Updated driver: {driver.full_name}")
                
                count += 1
                
            except Exception as e:
                errors += 1
                logger.error(f"Error syncing driver {doc.id}: {str(e)}")
                self.stdout.write(
                    self.style.ERROR(f"Error syncing driver {doc.id}: {str(e)}")
                )
                continue
        
        if errors > 0:
            self.stdout.write(
                self.style.WARNING(f"Completed with {errors} errors out of {count + errors} drivers")
            )
        
        return count

    def _sync_customers_from_firebase(self):
        """Sync customers from Firebase to Django"""
        db = firestore.client()
        
        # Try to get customers collection
        try:
            customers_ref = db.collection('Customers')
            docs = list(customers_ref.stream())
            if not docs:
                self.stdout.write(self.style.WARNING("No customers found in Firebase"))
                return 0
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Customers collection not found: {str(e)}"))
            return 0
        
        count = 0
        errors = 0
        
        for doc in docs:
            try:
                data = doc.to_dict()
                
                # Parse dateCreated
                date_created = timezone.now()
                if data.get('dateCreated'):
                    try:
                        date_created = datetime.fromisoformat(
                            data['dateCreated'].replace('Z', '+00:00')
                        )
                    except:
                        try:
                            if hasattr(data['dateCreated'], 'seconds'):
                                date_created = datetime.fromtimestamp(
                                    data['dateCreated'].seconds
                                )
                        except:
                            date_created = timezone.now()
                
                # Extract geo position
                geo_position = data.get('geoPosition')
                latitude = None
                longitude = None
                if geo_position and isinstance(geo_position, dict):
                    latitude = geo_position.get('latitude')
                    longitude = geo_position.get('longitude')
                
                customer, created = Customer.objects.update_or_create(
                    firebase_id=doc.id,
                    defaults={
                        'customer_id': data.get('customerId', doc.id),
                        'first_name': data.get('firstName', ''),
                        'last_name': data.get('lastName', ''),
                        'email': data.get('email', ''),
                        'phone_number': data.get('phoneNumber', ''),
                        'profile_pic': data.get('profilePic'),
                        'user_token': data.get('userToken', ''),
                        'latitude': latitude,
                        'longitude': longitude,
                        'date_created': date_created,
                    }
                )
                
                if created:
                    self.stdout.write(f"Created new customer: {customer.full_name}")
                else:
                    self.stdout.write(f"Updated customer: {customer.full_name}")
                
                count += 1
                
            except Exception as e:
                errors += 1
                logger.error(f"Error syncing customer {doc.id}: {str(e)}")
                continue
        
        return count

    def _sync_orders_from_firebase(self):
        """Sync orders from Firebase to Django (if Orders collection exists)"""
        db = firestore.client()
        
        try:
            orders_ref = db.collection('Orders')
            docs = list(orders_ref.stream())
            if not docs:
                self.stdout.write(self.style.WARNING("No orders found in Firebase"))
                return 0
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Orders collection not found: {str(e)}"))
            return 0
        
        count = 0
        for doc in docs:
            try:
                data = doc.to_dict()
                
                # Find customer and driver by firebase_id or other identifiers
                customer = None
                driver = None
                
                if data.get('customerId'):
                    try:
                        customer = Customer.objects.get(
                            models.Q(firebase_id=data['customerId']) | 
                            models.Q(customer_id=data['customerId'])
                        )
                    except Customer.DoesNotExist:
                        continue
                
                if data.get('driverId'):
                    try:
                        driver = Driver.objects.get(
                            models.Q(firebase_id=data['driverId']) | 
                            models.Q(drivers_id=data['driverId'])
                        )
                    except Driver.DoesNotExist:
                        pass  # Driver is optional
                
                if customer:
                    order, created = DeliveryOrder.objects.update_or_create(
                        firebase_id=doc.id,
                        defaults={
                            'customer': customer,
                            'driver': driver,
                            'pickup_address': data.get('pickupAddress', ''),
                            'delivery_address': data.get('deliveryAddress', ''),
                            'pickup_latitude': data.get('pickupLatitude'),
                            'pickup_longitude': data.get('pickupLongitude'),
                            'delivery_latitude': data.get('deliveryLatitude'),
                            'delivery_longitude': data.get('deliveryLongitude'),
                            'status': data.get('status', 'pending'),
                            'fare': float(data.get('fare', 0)),
                        }
                    )
                    count += 1
                
            except Exception as e:
                logger.error(f"Error syncing order {doc.id}: {str(e)}")
                continue
                
        return count

    def _sync_drivers_to_firebase(self):
        """Sync drivers from Django to Firebase"""
        drivers = Driver.objects.all()
        count = 0
        
        for driver in drivers:
            try:
                driver.save_to_firebase()
                count += 1
            except Exception as e:
                logger.error(f"Error syncing driver {driver.id} to Firebase: {str(e)}")
                continue
            
        return count

    def _sync_customers_to_firebase(self):
        """Sync customers from Django to Firebase"""
        customers = Customer.objects.all()
        count = 0
        
        for customer in customers:
            try:
                customer.save_to_firebase()
                count += 1
            except Exception as e:
                logger.error(f"Error syncing customer {customer.id} to Firebase: {str(e)}")
                continue
            
        return count