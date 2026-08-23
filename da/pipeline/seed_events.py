"""Seed GA4-style analytics events (idempotent via event_id UNIQUE)."""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

from .db import run_psql


def _hash_user(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()


def _sql_str(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def seed_events(pipeline_run_id: str) -> int:
    base = datetime(2024, 3, 1, 10, 0, tzinfo=timezone.utc)
    user_hash = _hash_user("usr-user-001")
    admin_hash = _hash_user("usr-admin-001")
    rows = []

    def add(event_id, name, when, **kw):
        rows.append(
            {
                "event_id": event_id,
                "event_name": name,
                "occurred_at": when.isoformat(),
                "user_id_hash": kw.get("user_id_hash", user_hash),
                "session_id": kw.get("session_id"),
                "story_id": kw.get("story_id"),
                "region_id": kw.get("region_id"),
                "area_code": kw.get("area_code"),
                "source": kw.get("source"),
                "channel": kw.get("channel"),
                "sort_type": kw.get("sort_type"),
                "position": kw.get("position"),
                "action": kw.get("action"),
                "has_area_context": kw.get("has_area_context"),
                "has_image": kw.get("has_image"),
                "category": kw.get("category"),
                "zoom": kw.get("zoom"),
            }
        )

    stories = [
        ("story-002", "reg-002", True, "A100001"),
        ("story-003", "reg-003", True, "A100002"),
        ("story-004", "reg-004", True, "A100003"),
        ("story-005", "reg-005", True, "A100004"),
        ("story-001", "reg-001", False, None),
        ("story-006", "reg-006", False, None),
    ]
    for i, (story_id, region_id, has_area, area_code) in enumerate(stories):
        sid = f"sess-{region_id}-{i}"
        add(f"evt-map-{i:03d}", "map_view", base + timedelta(hours=i), session_id=sid, region_id=region_id, zoom=14)
        add(
            f"evt-detail-{i:03d}",
            "story_detail_view",
            base + timedelta(hours=i, minutes=5),
            session_id=sid,
            story_id=story_id,
            region_id=region_id,
            source="map",
            has_area_context=has_area,
        )
        if has_area:
            add(
                f"evt-area-{i:03d}",
                "area_context_view",
                base + timedelta(hours=i, minutes=6),
                session_id=sid,
                story_id=story_id,
                region_id=region_id,
                area_code=area_code,
                source="detail",
                has_area_context=True,
            )
        add(
            f"evt-like-{i:03d}",
            "like_toggle",
            base + timedelta(hours=i, minutes=8),
            session_id=sid,
            story_id=story_id,
            region_id=region_id,
            action="add",
            has_area_context=has_area,
        )
        if i % 2 == 0:
            add(
                f"evt-share-{i:03d}",
                "share",
                base + timedelta(hours=i, minutes=10),
                session_id=sid,
                story_id=story_id,
                region_id=region_id,
                channel="link",
                has_area_context=has_area,
            )

    for pos, story_id in enumerate(["story-002", "story-003", "story-004", "story-001"], start=1):
        add(
            f"evt-cur-imp-{pos:03d}",
            "curation_impression",
            base + timedelta(days=1, minutes=pos),
            session_id="sess-curation",
            story_id=story_id,
            source="curation",
            sort_type="popular",
            position=pos,
        )
    for pos, story_id in enumerate(["story-002", "story-003"], start=1):
        add(
            f"evt-cur-click-{pos:03d}",
            "story_detail_view",
            base + timedelta(days=1, minutes=20 + pos),
            session_id="sess-curation",
            story_id=story_id,
            source="curation",
            sort_type="popular",
            position=pos,
            has_area_context=story_id != "story-001",
        )

    add(
        "evt-register-001",
        "story_register",
        base - timedelta(days=2),
        session_id="sess-reg",
        story_id="story-002",
        region_id="reg-002",
        has_image=True,
        category="상점",
    )
    add(
        "evt-admin-001",
        "admin_review",
        base - timedelta(days=1),
        user_id_hash=admin_hash,
        session_id="sess-admin",
        story_id="story-002",
        region_id="reg-002",
        action="approve",
    )

    statements = [
        f"""
INSERT INTO raw_events (
  event_id, event_name, occurred_at, user_id_hash, session_id, story_id, region_id,
  area_code, source, channel, sort_type, position, action, has_area_context,
  has_image, category, zoom, pipeline_run_id
) VALUES (
  {_sql_str(r['event_id'])}, {_sql_str(r['event_name'])}, {_sql_str(r['occurred_at'])}::timestamptz,
  {_sql_str(r['user_id_hash'])}, {_sql_str(r['session_id'])}, {_sql_str(r['story_id'])},
  {_sql_str(r['region_id'])}, {_sql_str(r['area_code'])}, {_sql_str(r['source'])},
  {_sql_str(r['channel'])}, {_sql_str(r['sort_type'])}, {_sql_str(r['position'])},
  {_sql_str(r['action'])}, {_sql_str(r['has_area_context'])}, {_sql_str(r['has_image'])},
  {_sql_str(r['category'])}, {_sql_str(r['zoom'])}, {_sql_str(pipeline_run_id)}
) ON CONFLICT (event_id) DO NOTHING;
""".strip()
        for r in rows
    ]
    run_psql("BEGIN;\n" + "\n".join(statements) + "\nCOMMIT;\n", tuples_only=False)
    return len(rows)
