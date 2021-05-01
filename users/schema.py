import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


user_model = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = user_model


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return user_model.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = user_model(username=kwargs.get(
            'username'), email=kwargs.get('email'))
        user.set_password(kwargs.get('password'))
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
