from fastapi import HTTPException
from app.models.versioning import StrategyVersion

class DisciplineEnforcer:
    @staticmethod
    def enforce_lock(strategy: StrategyVersion):
        """
        The Bouncer:
        Checks if the user is allowed to touch this strategy.
        """
        # If the strategy is active/locked
        if strategy.locked:
            # Check if they fulfilled the contract
            if strategy.trades_completed < strategy.contract_size:
                
                remaining = strategy.contract_size - strategy.trades_completed
                
                # REJECT THE REQUEST
                raise HTTPException(
                    status_code=403, # Forbidden
                    detail=f"STRATEGY LOCKED. You must execute {remaining} more trades before you can edit or add rules."
                )

    @staticmethod
    def can_add_rule(strategy: StrategyVersion):
        """
        Explicitly blocks adding new rules.
        """
        if strategy.locked:
             raise HTTPException(
                status_code=403, 
                detail="NO ADDITIONS ALLOWED. Create a new strategy if you want to change the rules."
            )
