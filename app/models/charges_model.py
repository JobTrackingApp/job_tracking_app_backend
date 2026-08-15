from pydantic import BaseModel


class CreateJobCharges(BaseModel):
    repair_charge: int = 0
    parts_charge: int = 0
    other_charge: int = 0

    parts_cost: int = 0
    technician_cost: int = 0
    other_cost: int = 0


class UpdateJobCharges(BaseModel):
    repair_charge: int | None = None
    parts_charge: int | None = None
    other_charge: int | None = None

    parts_cost: int | None = None
    technician_cost: int | None = None
    other_cost: int | None = None