from core.flight_search import FlightSearch
from crud import crud_test
from fastapi import APIRouter, Depends, HTTPException
from model.database.database import get_session
from model.models.deal_model import Deal, DealBase, DealCreate, DealRead
from model.models.test_model import Test, TestCreate, TestRead
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from typing import Any, List

router = APIRouter()


@router.get("/", response_model=List[TestRead])
def get_tests(db: Session = Depends(get_session)) -> Any:
    # tests = crud_test.get_multi(db)
    tests = db.query(Test).all()
    return tests


@router.get("/test", response_model=TestRead)
def get_test(test_id: int, db: Session = Depends(get_session)) -> Any:
    test = db.query(Test).filter(Test.id == test_id).first()
    return test


@router.post("/", response_model=TestRead)
def create_test(test: TestCreate, db: Session = Depends(get_session)) -> Any:
    iata_code = FlightSearch(test).find_iata_code()
    if not iata_code:
        raise HTTPException(status_code=422,
                            detail={"message": f"Unable to find IATA code for {test.city}. Check your spelling."})
    test.iata_code = iata_code
    db_test = Test.from_orm(test)
    db.add(db_test)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail="A city with that IATA code is in the database already.")
    else:
        db.refresh(db_test)
        return db_test


@router.get("/search", response_model=DealRead)
def get_deal(test_id: int, db: Session = Depends(get_session)) -> Any:
    test = db.query(Test).filter(Test.id == test_id).first()
    deal_search = FlightSearch(test).search_flights()
    if deal_search is None:
        raise HTTPException(status_code=422, detail={"message": f"No deals were found for SEL to {test.city}"})
    itinerary = deal_search["data"][0]

    deal = DealCreate(
        fly_from=itinerary["flyFrom"],
        city_from=itinerary["cityFrom"],
        fly_to=itinerary["flyTo"],
        city_to=itinerary["cityTo"],
        date_from=itinerary["route"][0]["local_departure"].split("T")[0],
        date_to=itinerary["route"][-1]["local_departure"].split("T")[0],
        duration=itinerary["duration"],
        price=itinerary["price"],
        airlines=itinerary["airlines"],
        url=itinerary["deep_link"],
    )

    db_deal = Deal.from_orm(deal)
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.get("/deals", response_model=List[DealRead])
def get_deals(db: Session = Depends(get_session)) -> Any:
    # tests = crud_test.get_multi(db)
    deals = db.query(Deal).all()
    return deals
