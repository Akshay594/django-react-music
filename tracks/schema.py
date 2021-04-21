import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import Track, Like
from users.schema import UserType


class TrackType(DjangoObjectType):

    class Meta:
        model = Track


class LikeType(DjangoObjectType):

    class Meta:
        model = Like


class Query(graphene.ObjectType):

    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None):
        if search:
            filters = (
                Q(title__icontains=search) |
                Q(url__icontains=search) |
                Q(description__icontains=search) |
                Q(posted_by__username__icontains=search)
            )
            Track.objects.filter(filters)
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Log in to add a track.")

        title = kwargs.get('title')
        description = kwargs.get('description')
        url = kwargs.get('url')
        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        track_id = kwargs.get('track_id')
        title = kwargs.get('title')
        description = kwargs.get('description')
        url = kwargs.get('url')
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception("Not permitted!!!")

        track.title = title
        track.description = description
        track.url = url
        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        track_id = kwargs.get('track_id')
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception("Not permitted to delete!!!")

        track.delete()
        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    track = graphene.Field(TrackType)
    user = graphene.Field(UserType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Log in to like tracks.")

        track_id = kwargs.get('track_id')
        track = Track.objects.get(id=track_id)
        if not track:
            raise Exception("Could not find track id.")
        Like.objects.create(track=track, user=user)
        return CreateLike(track=track, user=user)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
