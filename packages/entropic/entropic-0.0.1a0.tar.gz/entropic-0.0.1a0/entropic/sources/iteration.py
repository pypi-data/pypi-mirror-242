from typing import Set, ClassVar, TypeAlias

from pydantic import BaseModel, Field, field_serializer

from entropic.db import default_database

from entropic.sources.sample import Sample


class Iteration(BaseModel):
    database: ClassVar = default_database()
    sample_class: ClassVar[TypeAlias] = Sample

    samples: Set[sample_class] = Field(default_factory=set)
    source_path: str

    @field_serializer("samples")
    def serialize_samples(self, samples):
        return list(samples)

    def save(self):
        self.database.upsert(
            self.model_dump(),
            key={"key": "source_path", "value": self.source_path},
        )

    def add_sample(self, sample=None, **kwargs):
        if not sample:
            sample = self.sample_class(**kwargs)
        self.samples.add(sample)
        return sample
