from judge.results import EvaluationResult, JudgeVerdict
from judge.tasktype import TaskType
from problems.models import ProblemRevision, TestCase
from runner import get_compilation_commands, get_execution_command, get_valid_extensions
from runner.actions.action import ActionDescription
from runner.actions.compile_source import compile_source
from runner.actions.execute_with_input import execute_with_input


class Batch(TaskType):


    def initialize_problem(self, problem_code, *args, **kwargs):
        status = ProblemRevision.objects.filter(pk=problem_code).exists()
        msg = "problem_code should be the primary key of an existing revision" if not status else ""
        return status, msg

    def add_testcase(self, problem_code, testcase_code, *args, **kwargs):
        status = TestCase.objects.filter(problem_id=problem_code, name=testcase_code).exists()
        msg = "testcase_code should be the name of a testcase in this revision" if not status else ""
        return status, msg

    def generate_output(self, problem_code, testcase_code, language, solution_file):
        if language not in self.judge.get_supported_languages():
            return EvaluationResult(
                success=False,
                verdict=JudgeVerdict.invalid_submission,
                message="Language not supported"
            )
        revision = ProblemRevision.objects.get(pk=problem_code)
        graders = [(grader.name, grader.code)
                   for grader in revision.grader_set.all()
                   if any([grader.name.endswith(x) for x in get_valid_extensions(language)])
                   ]
        name, file = solution_file
        code_name = name
        compiled_file_name = "code.out"
        compile_commands = get_compilation_commands(
            language,
            [code_name] + [name for name, _ in graders],
            compiled_file_name
        )

        action = ActionDescription(
            commands=compile_commands,
            files=[(code_name, file)] + graders,
            output_files=[compiled_file_name],
            time_limit=self.judge.compile_time_limit,
            memory_limit=self.judge.compile_memory_limit,
        )

        time_limit = revision.problem_data.time_limit
        memory_limit = revision.problem_data.memory_limit
        testcase = TestCase.objects.get(problem_id=problem_code, name=testcase_code)

        success, compilation_success, outputs, stdout, stderr, compilation_sandbox_data = compile_source(action)
        if not success or not compilation_success:
            compilation_message = "Compilation not successful"
            compilation_message += "Standard output:\n" + stdout
            compilation_message += "Standard error:\n" + stderr
            return EvaluationResult(
                success=False,
                message=compilation_message,
                verdict=JudgeVerdict.compilation_failed
            )

        compiled = outputs[compiled_file_name]

        execution_command = get_execution_command(language, "compiled")
        stdout_redirect = "output.txt"
        action = ActionDescription(
            commands=[execution_command],
            executables=[("compiled", compiled)],
            files=[("input.txt", testcase.input_file)],
            stdin_redirect="input.txt",
            stdout_redirect=stdout_redirect,
            output_files=[stdout_redirect],
            time_limit=time_limit,
            memory_limit=memory_limit
        )
        success, execution_success, outputs, execution_sandbox_datas = execute_with_input(action)

        if not success:
            evaluation_success = False
        else:
            evaluation_success = True

        if not execution_success:
            output_file = None
        else:
            output_file = outputs[stdout_redirect]

        return EvaluationResult(
                success=evaluation_success,
                output_file=output_file,
                execution_time=execution_sandbox_datas[0]["execution_time"],
                execution_memory=execution_sandbox_datas[0]["execution_memory"],
                verdict=self.judge.get_verdict_from_exit_status(execution_sandbox_datas[0]["exit_status"]),
        )
