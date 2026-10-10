# Listings Service — Event Contract

**Transport:** NATS  
**Format:** JSON  
**Subject prefix:** `listing.*` (published), `moderation.*`, `user.*` (consumed)

---

## 📤 Published Events

### 1. `listing.created`
Published when a new listing is created.

**Payload:**
```json
{
  "event_id": "uuid-v4",
  "event_type": "listing.created",
  "timestamp": "2026-10-08T10:30:00Z",
  "data": {
    "listing_id": 123,
    "seller_id": 45,
    "title": "Calculus Textbook 8th Ed",
    "category": "textbook",
    "price_cents": 2500,
    "status": "active"
  }
}

**Subscribers:** Moderation Service, Search Indexer

---

### 2. `listing.updated`
Published when a listing's content changes.

**Payload:**
```json
{
  "event_id": "uuid-v4",
  "event_type": "listing.updated",
  "timestamp": "2026-10-08T10:35:00Z",
  "data": {
    "listing_id": 123,
    "changed_fields": ["price_cents", "description"],
    "status": "active"
  }
}
```

**Subscribers:** Search Indexer

---

### 3. `listing.sold`
Published when a listing is marked as sold.

**Payload:**
```json
{
  "event_id": "uuid-v4",
  "event_type": "listing.sold",
  "timestamp": "2026-10-08T11:00:00Z",
  "data": {
    "listing_id": 123,
    "seller_id": 45,
    "buyer_id": 67,
    "final_price_cents": 2400
  }
}
```

**Subscribers:** Chat Service, Analytics

---

### 4. `listing.flagged`
Published when a user flags a listing.

**Payload:**
```json
{
  "event_id": "uuid-v4",
  "event_type": "listing.flagged",
  "timestamp": "2026-10-08T11:15:00Z",
  "data": {
    "listing_id": 123,
    "reporter_id": 89,
    "reason": "spam",
    "notes": "Suspicious link in description"
  }
}
```

**Subscribers:** Moderation Service

---
## 📥 Consumed Events

### 1. `moderation.listing.hidden`
**Action:** Update listing status to `removed`.

```json
{
  "event_type": "moderation.listing.hidden",
  "data": {
    "listing_id": 123,
    "moderator_id": 5,
    "reason": "violates_policy"
  }
}
```

### 2. `moderation.listing.approved`
**Action:** Restore listing status to `active`.

### 3. `user.deleted`
**Action:** Mark all their listings as `removed`.

---

## 🔁 Subject Naming Convention

```
listing.created
listing.updated
listing.sold
listing.flagged
moderation.listing.hidden
moderation.listing.approved
user.deleted
```

**Rules:**
- lowercase + dots
- past tense (`created`, not `create`)
- service prefix for cross-service events (`moderation.*`, `user.*`)

---

## 🧪 Testing Events Locally

```bash
# Subscribe to all listing events
nats sub "listing.>"

# Publish a test event
nats pub listing.created '{"event_id":"test-1","data":{"listing_id":1}}'
```