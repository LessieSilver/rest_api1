from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.db_models import Advertisement
from app.models import (
    AdvertisementCreate,
    AdvertisementUpdate,
    AdvertisementOut,
)

router = APIRouter(prefix="/advertisement", tags=["advertisement"])


@router.post("", response_model=AdvertisementOut, status_code=201)
async def create_advertisement(
    data: AdvertisementCreate, session: AsyncSession = Depends(get_session)
):
    ad = Advertisement(**data.model_dump())
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad


@router.get("/{advertisement_id}", response_model=AdvertisementOut)
async def get_advertisement(
    advertisement_id: int, session: AsyncSession = Depends(get_session)
):
    ad = await session.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@router.patch("/{advertisement_id}", response_model=AdvertisementOut)
async def update_advertisement(
    advertisement_id: int,
    data: AdvertisementUpdate,
    session: AsyncSession = Depends(get_session),
):
    ad = await session.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ad, field, value)

    await session.commit()
    await session.refresh(ad)
    return ad


@router.delete("/{advertisement_id}", status_code=204)
async def delete_advertisement(
    advertisement_id: int, session: AsyncSession = Depends(get_session)
):
    ad = await session.get(Advertisement, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    await session.delete(ad)
    await session.commit()
    return None


@router.get("", response_model=List[AdvertisementOut])
async def search_advertisements(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """Поиск по полям через query string."""
    conditions = []
    if title is not None:
        conditions.append(Advertisement.title.ilike(f"%{title}%"))
    if description is not None:
        conditions.append(Advertisement.description.ilike(f"%{description}%"))
    if owner is not None:
        conditions.append(Advertisement.owner.ilike(f"%{owner}%"))
    if min_price is not None:
        conditions.append(Advertisement.price >= min_price)
    if max_price is not None:
        conditions.append(Advertisement.price <= max_price)

    stmt = select(Advertisement)
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    return result.scalars().all()
