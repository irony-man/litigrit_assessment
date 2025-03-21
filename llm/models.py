import uuid

from django.db.models import (
    CharField,
    DateTimeField,
    FileField,
    Model,
    TextField,
    UUIDField,
)


class CreateUpdate(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Summary(CreateUpdate):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    extracted_text = TextField()
    attachment = FileField()
    title = CharField(max_length=255)
    summary = TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Summaries"
