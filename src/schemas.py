from typing import Literal
from pydantic import BaseModel, Field

# Allowed values used across triage and resolution stages

Category = Literal[
    "billing",
    "technical",
    "account",
    "cancellation_refund",
    "order_delivery",
    "general",
]

Priority = Literal["low","medium","high","critical"]


ResolutionType = Literal[
    "self_service",
    "resolve",
    "escalate",
    "request_information",
]


class TicketTriage(BaseModel):
    category: Category = Field(description="support ticket category ")
    priority : Priority = Field(description="Urgency of the ticket")
    language: str = Field(description="Language used in the customer ticket")
    
    
class BillingAnalysis(BaseModel):
    issue: str = Field(description=" Short summary of the billing problem")
    amount : str = Field(description="Money amount mentioned, or 'unknown")
    transaction_count : int = Field(description="Number of charges mentioned")
    refund_required : bool = Field(description="Whether a refund appears needed")
    
class TechnicalAnalysis(BaseModel):
    issue: str = Field(description=" Short summary of the technical problem")
    affected_feature : str = Field(description="Feature or area that is broken")
    error_message : str = Field(description="Error text if mentioned else 'none'")
    troubleshooting_required : bool = Field(description="Whether torubleshooting are still needed")
    
class AccountAnalysis(BaseModel):
    issue: str = Field(description=" Short summary of the account problem")
    access_problem : str = Field(description="Whether login/access is blocked")
    verification_required : bool = Field(description="Whether identity verification is needed")
    account_status : str = Field(description="Likely account status, for example active,locked, or unknown")
    
class CancellationRefundAnalysis(BaseModel):
    request_type: str = Field(description="What the customer wants, for example cancel/refund/both")
    reason : str = Field(description="Reason given by the customer")
    refund_required : bool = Field(description="Whether the refund is needed or requested")
    retention_oppurtunity : bool = Field(description="Whether there may be a chance to retain the customer")
    
class OrderDeliveryAnalysis(BaseModel):
    issue: str = Field(description=" Short summary of the order/delivery problem")
    order_status : str = Field(description="Current status if mentioned, otherwise unknown")
    delivery_problem : bool = Field(description="Whether delivery is the main problem")
    customer_request : str = Field(description="What the customer wants to be done")
    

class GeneralAnalysis(BaseModel):
    issue: str = Field(description=" Short summary of the customer problem")
    customer_request : str = Field(description="Waht the customer is asking for")
    additional_context : str = Field(description="Any extra useful context from the ticket")
   


    
class ResolutionDecision(BaseModel):
    resolution_type : ResolutionType = Field(description=" Chosen next-step type for the support system") # type: ignore
    recommended_action : str = Field(description="Concrete action to take next")
    requires_human : bool = Field(description="True if human agent is needed")
    reason : str = Field(description="Why this resolution was chosen")
    

class TicketResult(BaseModel):
    ticket_id : str
    customer_name : str
    category : str
    priority : str
    language : str
    case_summary : str
    resolution_type : str
    recommended_action : str
    requires_human : bool
    resolution_reason : str
    response : str
    