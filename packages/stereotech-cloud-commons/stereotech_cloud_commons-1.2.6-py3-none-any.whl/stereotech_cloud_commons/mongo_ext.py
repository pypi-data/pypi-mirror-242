import datetime
import math
import random
import time
from typing import Optional
from mongoengine import *
from mongoengine import signals
from operator import itemgetter


def handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""
    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


@handler(signals.pre_save)
def update_date_tracking(sender, document):
    document.update_date = datetime.datetime.utcnow()


class ListQuerySet(QuerySet):
    def get_items(self, search: Optional[str] = None, sort_by: str = 'id', sort_desc: bool = False, skip: int = 0, limit: int = 10, **kwargs):
        query = self.order_by(
            f"{'-' if sort_desc else '+'}{sort_by}")[skip:limit]
        if search is not None:
            query = query.search_text(search)
        return query.count(), [i.to_mongo() for i in query]

    def get_item(self, id: str):
        return self.get(id=id)


class ItemFrequenciesQuerySet(ListQuerySet):
    def get_field_frequencies(self, field: str,  search: Optional[str] = None, sort_desc: bool = True, skip: int = 0, limit: int = 100, **kwargs):
        frqus = self.item_frequencies(field)
        if search is not None and len(search) > 0:
            frqus = {k: v for k, v in frqus.items() if search in str(k)}
        frqus_list = sorted(frqus.items(), key=itemgetter(1),
                            reverse=sort_desc)[skip:limit]
        return len(frqus_list), [{'id': kv[0], 'count': kv[1]} for kv in frqus_list]


class ListableDocument(Document):
    meta = {'allow_inheritance': True, 'queryset_class': ListQuerySet, 'abstract': True}
    creation_date = DateTimeField(default=datetime.datetime.utcnow())

    @queryset_manager
    def get_items(doc_cls, queryset: QuerySet, search: Optional[str] = None, sort_by: str = 'id', sort_desc: bool = False, skip: int = 0, limit: int = 100, **kwargs):
        return queryset.get_items(search, sort_by, sort_desc, skip, limit, **kwargs)

class RoleEntity(EmbeddedDocument):
    name = StringField(required=True)
    id = StringField(required=True)

class Role(ListableDocument):
    meta = {'allow_inheritance': True, 'queryset_class': ItemFrequenciesQuerySet, 'collection': 'roles'}

    entity = EmbeddedDocumentField(RoleEntity)
    name = StringField(required=True)
    scopes = ListField(StringField())

    @queryset_manager
    def get_scopes(doc_cls, queryset: QuerySet, search: Optional[str] = None, sort_desc: bool = True, skip: int = 0, limit: int = 100, **kwargs):
        return queryset.get_field_frequencies(
            'scopes', search, sort_desc, skip, limit, **kwargs)


class UserVerification(EmbeddedDocument):
    verified = BooleanField(default=False)
    verification_code = IntField(
        1000, 9999, default=random.randrange(1000, 9999))


class JwtData(EmbeddedDocument):
    jwt_id = StringField(required=True)
    jwt_secret = StringField(required=True)



class User(ListableDocument):
    meta = {'collection': 'users'}

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    username = StringField(min_length=1, max_length=50)
    avatar = URLField()
    role = ReferenceField(Role)
    verification = EmbeddedDocumentField(UserVerification)
    jwt_data = EmbeddedDocumentField(JwtData)
    salt = StringField(required=True)

    @queryset_manager
    def get_user(doc_cls, queryset: ListQuerySet, id: str):
        return queryset.get_item(id)

    @queryset_manager
    def get_users(doc_cls, queryset: ListQuerySet, **kwargs):
        return queryset.get_items(**kwargs)[1].exclude('verification', 'jwt_data')
