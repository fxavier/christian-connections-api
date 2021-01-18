import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from core.models import Post, Like, Comment, User
from django.db.models import Q


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType, search=graphene.String())
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    all_comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.Int(required=True))
    all_likes = graphene.List(LikeType)

    def resolve_post(self, info, id):
        return Post.objects.get(id=id)

    def resolve_all_posts(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(posted_by_name__icontains=search)
            )
            return Post.objects.filter(filter)
        return Post.objects.all()

    def resolve_all_comments(self, info):
        return Comment.objects.all()

    def resolve_comment(self, info, id):
        return Comment.objects.get(id=id)

    def resolve_all_likes(self, info):
        return Like.objects.all()


class AddPost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        # The input arguments for this mutation
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        # user_id = graphene.String(required=True)

    # The class attributes define the response of the mutation
    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must login to add Post.')
        post = Post.objects.create(
            title=kwargs.get('title'),
            content=kwargs.get('content'),
            posted_by=user
        )
        post.save()
        # Notice we return an instance of this mutation
        return AddPost(post=post)


class AddComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    def mutate(self, info, content, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must login to add comment.')
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(
            content=content,
            post=post,
            commented_by=user
        )
        comment.save()
        return AddComment(comment=comment)


class AddLike(graphene.Mutation):
    like = graphene.Field(LikeType)

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must login to like this post!')
        post = Post.objects.get(id=post_id)
        like = Like.objects.create(
            post=post,
            liked_by=user
        )
        like.save()
        return AddLike(like=like)


class Mutation:
    add_post = AddPost.Field()
    add_comment = AddComment.Field()
    add_like = AddLike.Field()
