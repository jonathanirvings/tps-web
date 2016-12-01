from django.core.urlresolvers import reverse
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from problems.forms.testcases import TestCaseAddForm

from .generics import ProblemObjectAddView, RevisionObjectView
from problems.models import TestCase

__all__ = ["TestCasesListView", "TestCaseAddView", "TestCaseInputDownloadView", "TestCaseOutputDownloadView"]


class TestCasesListView(RevisionObjectView):


    def get(self, request, problem_id, revision_slug):
        return render(request,
                      "problems/testcases_list.html",
                      context={
                          "testcases": self.revision.testcase_set.all()
                      })


class TestCaseAddView(ProblemObjectAddView):
    template_name = "problems/add_testcase.html"
    model_form = TestCaseAddForm

    def get_success_url(self, request, problem_id, revision_slug, obj):
        return reverse("problems:testcases", kwargs={
            "problem_id": problem_id,
            "revision_slug": revision_slug
        })


class TestCaseInputDownloadView(RevisionObjectView):

    def get(self, request, problem_id, revision_slug, testcase_id):
        testcase = get_object_or_404(TestCase, **{
            "problem_id": self.revision.id,
            "id": testcase_id
        })
        file = testcase.input_file
        if testcase.input_file_generated():
            return FileResponse(file.file, content_type="txt")
        else:
            return HttpResponse(content="A problem occurred during input generation:\n{}".format(
                                        testcase._input_generation_log),
                                content_type="txt")


class TestCaseOutputDownloadView(RevisionObjectView):

    def get(self, request, problem_id, revision_slug, testcase_id):
        testcase = get_object_or_404(TestCase, **{
            "problem_id": self.revision.id,
            "id": testcase_id
        })
        file = testcase.output_file
        if testcase.output_file_generated():
            return FileResponse(file.file, content_type="txt")
        elif testcase.input_file_generated():
            return HttpResponse(content="A problem occurred during output generation:\n{}".format(
                testcase._output_generation_log),
                content_type="txt")
        else:
            return HttpResponse(content="A problem occurred during output generation:\n{}".format(
                "Input generation failed"),
                content_type="txt")