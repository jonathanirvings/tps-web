# Amir Keivan Mohtashami
# Amirmohsen Ahanchi
import hashlib
import logging

from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from file_repository.models import FileModel
from problems.models.problem import ProblemRevision
from problems.models.version_control import RevisionObject
from runner import RUNNER_SUPPORTED_LANGUAGES as SUPPORTED_SOURCE_LANGUAGES
from runner import get_compilation_commands
from runner.actions.action import ActionDescription
from runner.actions.compile_source import compile_source
from tasks.models import Task


__all__ = ["Attachment", "SourceFile"]

logger = logging.getLogger(__name__)

FileNameValidator = RegexValidator(
    regex=r'^{character}(?:\.|{character})*$'.format(character=r'[a-zA-Z0-9_\-]'),
    message=_("please enter a valid file name."),
    code='invalid_file_name',
    inverse_match=False
)


class AttachmentBase(RevisionObject):

    problem = models.ForeignKey(ProblemRevision, verbose_name=_("problem"))
    name = models.CharField(max_length=256, verbose_name=_("name"), validators=[FileNameValidator])
    file = models.ForeignKey(FileModel, verbose_name=_("file"))

    @staticmethod
    def get_matching_fields():
        return ["name"]

    def diverged_from(self, other_object):
        return self.file != other_object.file

    class Meta:
        abstract = True


class Attachment(AttachmentBase):
    pass


# TODO: Source file can have multiple files (e.g. testlib.h)
class SourceFile(RevisionObject):
    problem = models.ForeignKey(ProblemRevision, verbose_name=_("problem"))
    name = models.CharField(max_length=50, verbose_name=_("name"), validators=[FileNameValidator])
    source_file = models.ForeignKey(FileModel, verbose_name=_("source file"), related_name="+")
    source_language = models.CharField(
        choices=[(x, x) for x in SUPPORTED_SOURCE_LANGUAGES],
        max_length=max([200] + [len(language) for language in SUPPORTED_SOURCE_LANGUAGES])
    )

    compile_jobs = GenericRelation("CompileJob", related_query_name='sourcefile')

    _compiled_file = models.ForeignKey(FileModel, verbose_name=_("compiled file"),
                                       related_name="+", null=True, blank=True)

    last_compile_log = models.TextField(verbose_name=_("last compile log"))

    class Meta:
        abstract = True
        unique_together = ("problem", "name")

    @staticmethod
    def get_matching_fields():
        return ["name"]

    def diverged_from(self, other_object):
        return self.source_file != other_object.source_file

    def compile(self):
        # TODO: Handling of simulataneous compilation of a single source file

        code_name = self.name
        compiled_file_name = self.name + ".out"
        compile_commands = get_compilation_commands(self.source_language, code_name,
                                                    compiled_file_name)
        action = ActionDescription(
            commands=compile_commands,
            files=[(code_name, self.source_file)],
            output_files=[compiled_file_name],
            time_limit=settings.DEFAULT_COMPILATION_TIME_LIMIT,
            memory_limit=settings.DEFAULT_COMPILATION_MEMORY_LIMIT
        )

        success, compilation_success, outputs, stdout, stderr, sandbox_data = compile_source(action)

        self._compiled_file = None

        if not success:
            logger.error("Running compilation command failed due to sandbox error")
        else:
            self.last_compile_log = "Standard output:\n" + stdout + "\n"
            self.last_compile_log += "Standard error:\n" + stderr + "\n"
            if compilation_success:
                self._compiled_file = outputs[compiled_file_name]
        self.save()

    def compiled_file(self):
        """
        return compiled_file, if _compiled_file is None it runs compile method to build _compiled_file
        """
        if self._compiled_file is None:
            self.compile()
        return self._compiled_file

    def is_compiled(self):
        return self._compiled_file is not None

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name == "":
            initial_prefix = "prefix_"
            self.name = initial_prefix
            for char in self.source_file.name:
                try:
                    FileNameValidator(self.name + char)
                except ValidationError:
                    continue
                self.name += char
            self.name = self.name[len(initial_prefix):]
            if self.name == "":
                self.name = "{}".format(hashlib.md5(self.source_file.name))

        super(SourceFile, self).save(*args, **kwargs)


class CompileJob(Task):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    source_file = GenericForeignKey('content_type', 'object_id')

    def run(self):
        self.source_file.compile()