"""
Parking Lot System - Low Level Design

A comprehensive parking lot management system implementing:
- Design Patterns: Singleton, Strategy, Factory, Observer, State
- SOLID Principles: SRP, OCP, LSP, ISP, DIP
- Concurrency: Thread-safe spot allocation

Author: Senior Engineer Implementation
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Protocol
from threading import Lock, RLock
import uuid
import time
import threading


# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class VehicleType(Enum):
    """Enum representing different vehicle types."""
    MOTORCYCLE = auto()
    CAR = auto()
    TRUCK = auto()


class SpotType(Enum):
    """Enum representing parking spot types."""
    COMPACT = auto()    # For motorcycles
    REGULAR = auto()    # For cars
    LARGE = auto()      # For trucks


class SpotStatus(Enum):
    """State pattern: Spot status states."""
    AVAILABLE = auto()
    OCCUPIED = auto()
    RESERVED = auto()
    OUT_OF_SERVICE = auto()


class PaymentStatus(Enum):
    """Payment status enum."""
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
    REFUNDED = auto()


# Vehicle to Spot mapping - which vehicle fits in which spot
VEHICLE_SPOT_MAPPING: Dict[VehicleType, List[SpotType]] = {
    VehicleType.MOTORCYCLE: [SpotType.COMPACT, SpotType.REGULAR, SpotType.LARGE],
    VehicleType.CAR: [SpotType.REGULAR, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}

# Pricing rates per hour for each spot type
HOURLY_RATES: Dict[SpotType, float] = {
    SpotType.COMPACT: 10.0,
    SpotType.REGULAR: 20.0,
    SpotType.LARGE: 30.0,
}


# =============================================================================
# PROTOCOLS (Interface Segregation Principle)
# =============================================================================

class Parkable(Protocol):
    """Protocol for objects that can be parked."""
    def get_type(self) -> VehicleType: ...
    def get_license_plate(self) -> str: ...


class Observable(Protocol):
    """Protocol for observable objects."""
    def add_observer(self, observer: 'SpotObserver') -> None: ...
    def remove_observer(self, observer: 'SpotObserver') -> None: ...
    def notify_observers(self) -> None: ...


class SpotObserver(Protocol):
    """Protocol for spot observers (Observer Pattern)."""
    def update(self, spot: 'ParkingSpot') -> None: ...


# =============================================================================
# VEHICLE CLASSES (Liskov Substitution Principle - all subclasses interchangeable)
# =============================================================================

@dataclass
class Vehicle(ABC):
    """
    Abstract base class for vehicles.
    
    SRP: Responsible only for vehicle data and identification.
    OCP: New vehicle types can be added via inheritance.
    """
    license_plate: str
    
    @abstractmethod
    def get_type(self) -> VehicleType:
        """Return the vehicle type."""
        pass
    
    def get_license_plate(self) -> str:
        """Return the license plate."""
        return self.license_plate


@dataclass
class Motorcycle(Vehicle):
    """Motorcycle vehicle class."""
    
    def get_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE


@dataclass
class Car(Vehicle):
    """Car vehicle class."""
    
    def get_type(self) -> VehicleType:
        return VehicleType.CAR


@dataclass
class Truck(Vehicle):
    """Truck vehicle class."""
    
    def get_type(self) -> VehicleType:
        return VehicleType.TRUCK


# =============================================================================
# VEHICLE FACTORY (Factory Pattern)
# =============================================================================

class VehicleFactory:
    """
    Factory for creating vehicle instances.
    
    SRP: Single responsibility of creating vehicles.
    OCP: New vehicle types require minimal changes.
    """
    
    @staticmethod
    def create_vehicle(vehicle_type: VehicleType, license_plate: str) -> Vehicle:
        """Create a vehicle based on type."""
        vehicle_classes = {
            VehicleType.MOTORCYCLE: Motorcycle,
            VehicleType.CAR: Car,
            VehicleType.TRUCK: Truck,
        }
        
        vehicle_class = vehicle_classes.get(vehicle_type)
        if not vehicle_class:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        return vehicle_class(license_plate=license_plate)


# =============================================================================
# PARKING SPOT CLASSES
# =============================================================================

@dataclass
class ParkingSpot(ABC):
    """
    Abstract base class for parking spots.
    
    SRP: Manages a single parking spot's state.
    OCP: New spot types added via inheritance.
    """
    spot_id: str
    floor_number: int
    spot_type: SpotType = field(init=False)
    status: SpotStatus = SpotStatus.AVAILABLE
    vehicle: Optional[Vehicle] = None
    _observers: List[SpotObserver] = field(default_factory=list, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)
    
    @abstractmethod
    def get_spot_type(self) -> SpotType:
        """Return the spot type."""
        pass
    
    def __post_init__(self):
        self.spot_type = self.get_spot_type()
    
    def is_available(self) -> bool:
        """Check if spot is available."""
        return self.status == SpotStatus.AVAILABLE
    
    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        """Check if the vehicle can fit in this spot."""
        allowed_spots = VEHICLE_SPOT_MAPPING.get(vehicle.get_type(), [])
        return self.spot_type in allowed_spots
    
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Park a vehicle in this spot.
        Thread-safe operation.
        """
        with self._lock:
            if not self.is_available():
                return False
            if not self.can_fit_vehicle(vehicle):
                return False
            
            self.vehicle = vehicle
            self.status = SpotStatus.OCCUPIED
            self.notify_observers()
            return True
    
    def remove_vehicle(self) -> Optional[Vehicle]:
        """
        Remove vehicle from this spot.
        Thread-safe operation.
        """
        with self._lock:
            if self.status != SpotStatus.OCCUPIED:
                return None
            
            vehicle = self.vehicle
            self.vehicle = None
            self.status = SpotStatus.AVAILABLE
            self.notify_observers()
            return vehicle
    
    # Observer Pattern implementation
    def add_observer(self, observer: SpotObserver) -> None:
        """Add an observer."""
        self._observers.append(observer)
    
    def remove_observer(self, observer: SpotObserver) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self) -> None:
        """Notify all observers of state change."""
        for observer in self._observers:
            observer.update(self)


@dataclass
class CompactSpot(ParkingSpot):
    """Compact parking spot for motorcycles."""
    
    def get_spot_type(self) -> SpotType:
        return SpotType.COMPACT


@dataclass
class RegularSpot(ParkingSpot):
    """Regular parking spot for cars."""
    
    def get_spot_type(self) -> SpotType:
        return SpotType.REGULAR


@dataclass
class LargeSpot(ParkingSpot):
    """Large parking spot for trucks."""
    
    def get_spot_type(self) -> SpotType:
        return SpotType.LARGE


# =============================================================================
# SPOT FACTORY (Factory Pattern)
# =============================================================================

class SpotFactory:
    """Factory for creating parking spot instances."""
    
    @staticmethod
    def create_spot(spot_type: SpotType, spot_id: str, floor_number: int) -> ParkingSpot:
        """Create a parking spot based on type."""
        spot_classes = {
            SpotType.COMPACT: CompactSpot,
            SpotType.REGULAR: RegularSpot,
            SpotType.LARGE: LargeSpot,
        }
        
        spot_class = spot_classes.get(spot_type)
        if not spot_class:
            raise ValueError(f"Unknown spot type: {spot_type}")
        
        return spot_class(spot_id=spot_id, floor_number=floor_number)


# =============================================================================
# PRICING STRATEGY (Strategy Pattern)
# =============================================================================

class PricingStrategy(ABC):
    """
    Abstract pricing strategy.
    
    Strategy Pattern: Interchangeable pricing algorithms.
    OCP: New pricing strategies added without modifying existing code.
    """
    
    @abstractmethod
    def calculate_price(self, spot_type: SpotType, duration_hours: float) -> float:
        """Calculate the parking fee."""
        pass


class HourlyPricingStrategy(PricingStrategy):
    """Hourly pricing strategy."""
    
    def calculate_price(self, spot_type: SpotType, duration_hours: float) -> float:
        """Calculate price based on hourly rate."""
        hourly_rate = HOURLY_RATES.get(spot_type, 20.0)
        return round(hourly_rate * duration_hours, 2)


class FlatRatePricingStrategy(PricingStrategy):
    """Flat rate pricing strategy (daily rate)."""
    
    def __init__(self, daily_rate: float = 100.0):
        self.daily_rate = daily_rate
    
    def calculate_price(self, spot_type: SpotType, duration_hours: float) -> float:
        """Calculate price based on flat daily rate."""
        days = max(1, int(duration_hours / 24) + (1 if duration_hours % 24 > 0 else 0))
        return round(self.daily_rate * days, 2)


class WeekendPricingStrategy(PricingStrategy):
    """Weekend discounted pricing strategy."""
    
    def __init__(self, discount_percent: float = 20.0):
        self.discount_percent = discount_percent
    
    def calculate_price(self, spot_type: SpotType, duration_hours: float) -> float:
        """Calculate price with weekend discount."""
        base_rate = HOURLY_RATES.get(spot_type, 20.0)
        discount = 1 - (self.discount_percent / 100)
        return round(base_rate * duration_hours * discount, 2)


# =============================================================================
# OBSERVER PATTERN - Display Board
# =============================================================================

class DisplayBoard:
    """
    Display board showing parking availability.
    
    Observer Pattern: Updates when spot status changes.
    SRP: Only responsible for displaying information.
    """
    
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.available_compact: int = 0
        self.available_regular: int = 0
        self.available_large: int = 0
        self._lock = Lock()
    
    def update(self, spot: ParkingSpot) -> None:
        """Update display when spot status changes."""
        with self._lock:
            delta = 1 if spot.is_available() else -1
            
            if spot.spot_type == SpotType.COMPACT:
                self.available_compact = max(0, self.available_compact + delta)
            elif spot.spot_type == SpotType.REGULAR:
                self.available_regular = max(0, self.available_regular + delta)
            elif spot.spot_type == SpotType.LARGE:
                self.available_large = max(0, self.available_large + delta)
    
    def initialize_counts(self, compact: int, regular: int, large: int) -> None:
        """Initialize available spot counts."""
        with self._lock:
            self.available_compact = compact
            self.available_regular = regular
            self.available_large = large
    
    def show(self) -> str:
        """Return display information."""
        return (
            f"Floor {self.floor_number} Availability:\n"
            f"  Compact: {self.available_compact}\n"
            f"  Regular: {self.available_regular}\n"
            f"  Large: {self.available_large}"
        )


# =============================================================================
# TICKET & PAYMENT
# =============================================================================

@dataclass
class Ticket:
    """
    Parking ticket issued on entry.
    
    SRP: Only responsible for ticket data.
    """
    ticket_id: str
    vehicle: Vehicle
    spot: ParkingSpot
    entry_time: datetime
    exit_time: Optional[datetime] = None
    
    @staticmethod
    def generate_ticket(vehicle: Vehicle, spot: ParkingSpot) -> 'Ticket':
        """Generate a new parking ticket."""
        return Ticket(
            ticket_id=str(uuid.uuid4())[:8].upper(),
            vehicle=vehicle,
            spot=spot,
            entry_time=datetime.now()
        )
    
    def get_duration_hours(self) -> float:
        """Calculate parking duration in hours."""
        end_time = self.exit_time or datetime.now()
        delta = end_time - self.entry_time
        return delta.total_seconds() / 3600


@dataclass
class Payment:
    """
    Payment record for parking.
    
    SRP: Only responsible for payment data.
    DIP: Depends on PricingStrategy abstraction.
    """
    payment_id: str
    ticket: Ticket
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    payment_time: Optional[datetime] = None
    
    def process_payment(self) -> bool:
        """Process the payment."""
        # Simulate payment processing
        self.status = PaymentStatus.COMPLETED
        self.payment_time = datetime.now()
        return True


# =============================================================================
# ENTRY & EXIT PANELS
# =============================================================================

class EntryPanel:
    """
    Entry panel at parking lot entrance.
    
    SRP: Handles vehicle entry and ticket generation.
    """
    
    def __init__(self, panel_id: str, parking_lot: 'ParkingLot'):
        self.panel_id = panel_id
        self.parking_lot = parking_lot
    
    def process_entry(self, vehicle: Vehicle) -> Optional[Ticket]:
        """Process vehicle entry and return ticket."""
        return self.parking_lot.park_vehicle(vehicle)


class ExitPanel:
    """
    Exit panel at parking lot exit.
    
    SRP: Handles vehicle exit and payment processing.
    DIP: Depends on PricingStrategy abstraction.
    """
    
    def __init__(self, panel_id: str, parking_lot: 'ParkingLot', 
                 pricing_strategy: PricingStrategy):
        self.panel_id = panel_id
        self.parking_lot = parking_lot
        self.pricing_strategy = pricing_strategy
    
    def calculate_fee(self, ticket: Ticket) -> float:
        """Calculate the parking fee."""
        duration = ticket.get_duration_hours()
        return self.pricing_strategy.calculate_price(ticket.spot.spot_type, duration)
    
    def process_exit(self, ticket: Ticket) -> Optional[Payment]:
        """Process vehicle exit and return payment."""
        ticket.exit_time = datetime.now()
        
        # Calculate fee
        amount = self.calculate_fee(ticket)
        
        # Create payment
        payment = Payment(
            payment_id=str(uuid.uuid4())[:8].upper(),
            ticket=ticket,
            amount=amount
        )
        
        # Process payment
        if payment.process_payment():
            # Unpark the vehicle
            self.parking_lot.unpark_vehicle(ticket)
            return payment
        
        return None


# =============================================================================
# PARKING FLOOR
# =============================================================================

class ParkingFloor:
    """
    Represents a single floor in the parking lot.
    
    SRP: Manages spots on a single floor.
    """
    
    def __init__(self, floor_number: int, 
                 num_compact: int = 10, 
                 num_regular: int = 20, 
                 num_large: int = 5):
        self.floor_number = floor_number
        self.spots: Dict[str, ParkingSpot] = {}
        self.display_board = DisplayBoard(floor_number)
        self._lock = RLock()
        
        # Initialize spots
        self._initialize_spots(num_compact, num_regular, num_large)
        
        # Initialize display board counts
        self.display_board.initialize_counts(num_compact, num_regular, num_large)
    
    def _initialize_spots(self, num_compact: int, num_regular: int, num_large: int) -> None:
        """Initialize parking spots on this floor."""
        spot_configs = [
            (SpotType.COMPACT, num_compact, "C"),
            (SpotType.REGULAR, num_regular, "R"),
            (SpotType.LARGE, num_large, "L"),
        ]
        
        for spot_type, count, prefix in spot_configs:
            for i in range(count):
                spot_id = f"F{self.floor_number}-{prefix}{i+1:03d}"
                spot = SpotFactory.create_spot(spot_type, spot_id, self.floor_number)
                spot.add_observer(self.display_board)
                self.spots[spot_id] = spot
    
    def find_available_spot(self, vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        """
        Find an available spot for the given vehicle type.
        Thread-safe operation.
        """
        with self._lock:
            allowed_spot_types = VEHICLE_SPOT_MAPPING.get(vehicle_type, [])
            
            for spot in self.spots.values():
                if spot.is_available() and spot.spot_type in allowed_spot_types:
                    return spot
            
            return None
    
    def get_available_count(self) -> Dict[SpotType, int]:
        """Get count of available spots by type."""
        with self._lock:
            counts = {spot_type: 0 for spot_type in SpotType}
            for spot in self.spots.values():
                if spot.is_available():
                    counts[spot.spot_type] += 1
            return counts


# =============================================================================
# PARKING LOT (Singleton Pattern)
# =============================================================================

class ParkingLot:
    """
    Main parking lot class implementing Singleton pattern.
    
    SRP: Orchestrates parking operations.
    Singleton: Ensures single instance across the application.
    Thread-safe: Uses locks for concurrent access.
    """
    
    _instance: Optional['ParkingLot'] = None
    _lock: Lock = Lock()
    _initialized: bool = False
    
    def __new__(cls, *args, **kwargs) -> 'ParkingLot':
        """Thread-safe singleton implementation."""
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name: str = "Main Parking Lot", num_floors: int = 3):
        """Initialize the parking lot."""
        # Prevent re-initialization
        if ParkingLot._initialized:
            return
        
        with ParkingLot._lock:
            if ParkingLot._initialized:
                return
            
            self.name = name
            self.floors: List[ParkingFloor] = []
            self.active_tickets: Dict[str, Ticket] = {}
            self.entry_panels: List[EntryPanel] = []
            self.exit_panels: List[ExitPanel] = []
            self._operation_lock = RLock()
            
            # Initialize floors
            for i in range(num_floors):
                floor = ParkingFloor(floor_number=i + 1)
                self.floors.append(floor)
            
            # Initialize entry/exit panels
            self._setup_panels()
            
            ParkingLot._initialized = True
    
    def _setup_panels(self) -> None:
        """Set up entry and exit panels."""
        # Entry panels
        for i in range(2):
            panel = EntryPanel(f"ENTRY-{i+1}", self)
            self.entry_panels.append(panel)
        
        # Exit panels with different pricing strategies
        pricing_strategies = [
            HourlyPricingStrategy(),
            WeekendPricingStrategy(discount_percent=15.0),
        ]
        
        for i, strategy in enumerate(pricing_strategies):
            panel = ExitPanel(f"EXIT-{i+1}", self, strategy)
            self.exit_panels.append(panel)
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        with cls._lock:
            cls._instance = None
            cls._initialized = False
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        """
        Park a vehicle in the lot.
        Thread-safe operation.
        """
        with self._operation_lock:
            # Find available spot across all floors
            for floor in self.floors:
                spot = floor.find_available_spot(vehicle.get_type())
                if spot:
                    # Park the vehicle
                    if spot.park_vehicle(vehicle):
                        # Generate ticket
                        ticket = Ticket.generate_ticket(vehicle, spot)
                        self.active_tickets[ticket.ticket_id] = ticket
                        return ticket
            
            return None  # No available spot
    
    def unpark_vehicle(self, ticket: Ticket) -> bool:
        """
        Remove a vehicle from the lot.
        Thread-safe operation.
        """
        with self._operation_lock:
            if ticket.ticket_id not in self.active_tickets:
                return False
            
            # Remove vehicle from spot
            vehicle = ticket.spot.remove_vehicle()
            if vehicle:
                del self.active_tickets[ticket.ticket_id]
                return True
            
            return False
    
    def get_available_spots_count(self) -> Dict[int, Dict[SpotType, int]]:
        """Get available spots count per floor."""
        result = {}
        for floor in self.floors:
            result[floor.floor_number] = floor.get_available_count()
        return result
    
    def display_availability(self) -> None:
        """Display availability across all floors."""
        print(f"\n{'='*50}")
        print(f"  {self.name} - Availability")
        print(f"{'='*50}")
        for floor in self.floors:
            print(floor.display_board.show())
            print("-" * 30)


# =============================================================================
# DEMO & TESTING
# =============================================================================

def demo_basic_operations():
    """Demonstrate basic parking operations."""
    print("\n" + "="*60)
    print("  PARKING LOT SYSTEM DEMO - Basic Operations")
    print("="*60)
    
    # Get parking lot instance (Singleton)
    lot = ParkingLot(name="Downtown Parking", num_floors=2)
    
    # Create vehicles using factory
    car1 = VehicleFactory.create_vehicle(VehicleType.CAR, "ABC-1234")
    car2 = VehicleFactory.create_vehicle(VehicleType.CAR, "XYZ-5678")
    motorcycle = VehicleFactory.create_vehicle(VehicleType.MOTORCYCLE, "MOTO-001")
    truck = VehicleFactory.create_vehicle(VehicleType.TRUCK, "TRUCK-999")
    
    # Display initial availability
    print("\n--- Initial Availability ---")
    lot.display_availability()
    
    # Park vehicles
    print("\n--- Parking Vehicles ---")
    
    ticket1 = lot.entry_panels[0].process_entry(car1)
    if ticket1:
        print(f"✓ Parked {car1.license_plate} at {ticket1.spot.spot_id}")
        print(f"  Ticket ID: {ticket1.ticket_id}")
    
    ticket2 = lot.entry_panels[0].process_entry(motorcycle)
    if ticket2:
        print(f"✓ Parked {motorcycle.license_plate} at {ticket2.spot.spot_id}")
    
    ticket3 = lot.entry_panels[1].process_entry(truck)
    if ticket3:
        print(f"✓ Parked {truck.license_plate} at {ticket3.spot.spot_id}")
    
    # Display updated availability
    print("\n--- Updated Availability ---")
    lot.display_availability()
    
    # Simulate time passing (for demo, we'll manipulate the ticket time)
    ticket1.entry_time = datetime(2026, 1, 4, 20, 0, 0)  # 4 hours ago
    
    # Process exit and payment
    print("\n--- Processing Exit ---")
    exit_panel = lot.exit_panels[0]  # Hourly pricing
    payment = exit_panel.process_exit(ticket1)
    
    if payment:
        print(f"✓ Vehicle {car1.license_plate} exited")
        print(f"  Duration: {ticket1.get_duration_hours():.2f} hours")
        print(f"  Amount: ${payment.amount:.2f}")
        print(f"  Payment Status: {payment.status.name}")
    
    # Final availability
    print("\n--- Final Availability ---")
    lot.display_availability()
    
    return lot


def demo_concurrent_parking():
    """Demonstrate thread-safe concurrent parking."""
    print("\n" + "="*60)
    print("  PARKING LOT SYSTEM DEMO - Concurrent Operations")
    print("="*60)
    
    # Reset singleton for fresh test
    ParkingLot.reset_instance()
    lot = ParkingLot(name="Concurrent Test Lot", num_floors=1)
    
    successful_parks = []
    failed_parks = []
    lock = Lock()
    
    def park_vehicle(vehicle_id: int):
        """Worker function to park a vehicle."""
        vehicle = VehicleFactory.create_vehicle(
            VehicleType.CAR, 
            f"CAR-{vehicle_id:04d}"
        )
        ticket = lot.park_vehicle(vehicle)
        
        with lock:
            if ticket:
                successful_parks.append(vehicle.license_plate)
            else:
                failed_parks.append(vehicle.license_plate)
    
    # Create threads for concurrent parking
    threads = []
    num_vehicles = 25  # More than available regular spots (20)
    
    print(f"\nAttempting to park {num_vehicles} vehicles concurrently...")
    print(f"Available regular spots: 20")
    
    for i in range(num_vehicles):
        thread = threading.Thread(target=park_vehicle, args=(i,))
        threads.append(thread)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start_time
    
    print(f"\n--- Results (completed in {elapsed:.3f}s) ---")
    print(f"✓ Successful parks: {len(successful_parks)}")
    print(f"✗ Failed parks: {len(failed_parks)}")
    
    # Verify no race conditions
    availability = lot.get_available_spots_count()
    total_occupied = sum(
        20 - count  # 20 was the initial regular spot count
        for floor_counts in availability.values()
        for spot_type, count in floor_counts.items()
        if spot_type == SpotType.REGULAR
    )
    
    print(f"\nVerification:")
    print(f"  Parked vehicles count: {len(successful_parks)}")
    print(f"  Active tickets: {len(lot.active_tickets)}")
    print(f"  Match: {'✓ Yes' if len(successful_parks) == len(lot.active_tickets) else '✗ No'}")


def demo_pricing_strategies():
    """Demonstrate different pricing strategies."""
    print("\n" + "="*60)
    print("  PARKING LOT SYSTEM DEMO - Pricing Strategies")
    print("="*60)
    
    strategies = [
        ("Hourly Pricing", HourlyPricingStrategy()),
        ("Flat Rate (Daily)", FlatRatePricingStrategy(daily_rate=100)),
        ("Weekend Discount (20%)", WeekendPricingStrategy(discount_percent=20)),
    ]
    
    test_cases = [
        (SpotType.COMPACT, 2.0),
        (SpotType.REGULAR, 4.5),
        (SpotType.LARGE, 8.0),
        (SpotType.REGULAR, 26.0),  # Over a day
    ]
    
    for strategy_name, strategy in strategies:
        print(f"\n{strategy_name}:")
        print("-" * 40)
        for spot_type, hours in test_cases:
            price = strategy.calculate_price(spot_type, hours)
            print(f"  {spot_type.name:8} × {hours:5.1f}h = ${price:>8.2f}")


if __name__ == "__main__":
    # Run demos
    demo_basic_operations()
    demo_concurrent_parking()
    demo_pricing_strategies()
    
    print("\n" + "="*60)
    print("  All demos completed successfully!")
    print("="*60)
