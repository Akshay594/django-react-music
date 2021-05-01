import graphene
from graphene_django import DjangoObjectType
from .models import Track, Like
from users.schema import UserType


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info):
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Login to create a track")
        track = Track(title=kwargs.get('title'),
                      url=kwargs.get('url'), description=kwargs.get('description'),
                      posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Login to Create/Update a track")
        track = Track.objects.get(id=kwargs.get('track_id'))

        if track.posted_by == user:
            track.title = kwargs.get('title')
            track.url = kwargs.get('url')
            track.description = kwargs.get('description')
            track.save()
        else:
            raise Exception("Not allowed to update the track.")
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Login to delete a track")
        track = Track.objects.get(id=kwargs.get('track_id'))

        if track.posted_by == user:
            track.delete()
        else:
            raise Exception("Not allowed to delete the track.")
        return DeleteTrack(track_id=kwargs.get('track_id'))


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Please login to like the track.")
        track = Track.objects.get(id=kwargs.get('track_id'))
        if track is None:
            raise Exception("Track doesn't exists.")

        if Like.objects.filter(liked_by=user, track=track).exists():
            raise Exception("You have already liked the track.")

        like = Like(track=track, liked_by=user)
        like.save()
        return CreateLike(user=user, track=track)


class RemoveLikeTrack(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Please login to like/dislike the track.")
        track = Track.objects.get(id=kwargs.get('track_id'))
        if track is None:
            raise Exception("Track doesn't exists.")

        if Like.objects.filter(liked_by=user, track=track).exists():
            like = Like.objects.get(liked_by=user, track=track)
            like.delete()
        return RemoveLikeTrack(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    create_like = CreateLike.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    remove_like = RemoveLikeTrack.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
