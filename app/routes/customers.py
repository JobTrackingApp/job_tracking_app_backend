from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.customer_model import Customer, CustomerCreate, CustomerUpdate
from app.core.database import customers_collection

router = APIRouter(
    prefix = "/customers",
    tags = ["Customers"]
)

#Create a customer
@router.post("/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    #Generate customer id
    last_customer = await customers_collection.find_one(
        sort=[("customer_id", -1)])
    
    if last_customer:
        last_number = int(last_customer["customer_id"].split("-")[1])
        customer_id = f"CUS-{last_number + 1:06d}"
    else:
        customer_id = "CUS-000001"

    time_now = datetime.utcnow()

    customer_data = {
        "customer_id": customer_id,
        **customer.model_dump(),
        "created_at": time_now,
        "updated_at": time_now
    }

    await customers_collection.insert_one(customer_data)

    return customer_data

#Get the list of customers
@router.get("/", response_model=list[Customer])
async def get_customers():
    customers = await customers_collection.find().to_list(length=None)

    return customers

#Get customer by customer id
@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await customers_collection.find_one(
        {"customer_id": customer_id}
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    
    return customer

#Update customer info
@router.patch("/customer_id", response_model=Customer)
async def update_customer(customer_id: str,customer: CustomerUpdate):
    update_data = {
        key: value
        for key, value in customer.model_dump().items()
        if value is not None
    }
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to update customer details"
        )
    
    update_data["updated_at"] = datetime.utcnow()

    result = await customers_collection.update_one(
        {"customer_id": customer_id},
        {"$set": update_data}
    )

    if result.matched_count==0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    
    updated_customer = await customers_collection.find_one(
        {"customer_id": customer_id}
    )

    return updated_customer
