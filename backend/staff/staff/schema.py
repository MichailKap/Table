import graphene
from graphene_django import DjangoObjectType

from staffapp.models import Occupation


class OccupationType(DjangoObjectType):
    class Meta:
        model = Occupation
        fields = ("__all__")

class Query(graphene.ObjectType):
    occupations = graphene.List(OccupationType)
    occupation_id = graphene.Field(OccupationType, id=graphene.String())
    
    def resolve_occupations(root, info, ** kwargs):
        return Occupation.objects.all()

    def resolve_occupation_id(root, info, id):
        return Occupation.objects.get(pk=id)


class AddOccupation(graphene.Mutation):
    id = graphene.ID()
    name = graphene.String(required=True)
    company_name = graphene.String(required=True)
    position_name = graphene.String(required=True)
    hire_date = graphene.Date(required=True)
    fire_date = graphene.Date()
    salary = graphene.Int(required=True)
    fraction = graphene.Int(required=True)
    base = graphene.Int(required=True)
    advance = graphene.Int(required=True)
    by_hours = graphene.Boolean(required=True)
    
    class Arguments:
        name = graphene.String()
        company_name = graphene.String(required=True)
        position_name = graphene.String(required=True)
        hire_date = graphene.Date(required=True)
        fire_date = graphene.Date()
        salary = graphene.Int(required=True)
        fraction = graphene.Int(required=True)
        base = graphene.Int(required=True)
        advance = graphene.Int(required=True)
        by_hours = graphene.Boolean(required=True)

    
    def mutate(
        self,
        info,
        name,
        company_name,
        position_name,
        hire_date,
        fire_date,
        salary,
        fraction,
        base,
        advance,
        by_hours
    ):
        occupation = Occupation(
            name=name,
            company_name=company_name,
            position_name=position_name,
            hire_date=hire_date,
            fire_date=fire_date,
            salary=salary,
            fraction=fraction,
            base=base,
            advance=advance,
            by_hours=by_hours
        )
        occupation.save()

        return AddOccupation(
            id=occupation.id,
            name=occupation.name,
            company_name=occupation.company_name,
            position_name=occupation.position_name,
            hire_date=occupation.hire_date,
            fire_date=occupation.fire_date,
            salary=occupation.salary,
            fraction=occupation.fraction,
            base=occupation.base,
            advance=occupation.advance,
            by_hours=occupation.by_hours
        )
        
class DeleteOccupation(graphene.Mutation):
    id = graphene.ID()
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        occupation = Occupation.objects.get(pk=id)
        occupation.delete()
        return cls(ok=True)
    

class Mutation(graphene.ObjectType):
    add_occupation = AddOccupation.Field()
    delete_occupation = DeleteOccupation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
