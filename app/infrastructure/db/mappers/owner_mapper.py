from app.domain.entities.owner import Owner
from app.infrastructure.db.models import OwnerModel


class OwnerMapper:
    @staticmethod
    def to_model(entity: Owner) -> OwnerModel:
        return OwnerModel(**entity.__dict__)

    @staticmethod
    def to_entity(model: OwnerModel) -> Owner:
        return Owner.reconstitute(
            id=model.id,
            name=model.name,
            webhook_url=model.webhook_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
