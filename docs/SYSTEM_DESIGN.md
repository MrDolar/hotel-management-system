# Hotel Management - System Design

## Tables
- rooms (id, room_number, room_type, price, capacity, is_available)
- bookings (id, room_id, guest_name, check_in, check_out, total_price, status)

## API
- /api/rooms - Room CRUD
- /api/bookings - Booking management
- /api/ai - AI features (pricing, prediction, chat)

## Security: JWT auth, env-only API keys
