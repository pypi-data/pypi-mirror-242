from __future__ import annotations

from typing import List

from gapper.core.hook import HookBase, HookTypes
from gapper.core.test_result import TestResult
from gapper.gradescope.datatypes.gradescope_meta import GradescopeSubmissionMetadata


class PostTests(HookBase):
    """A decorator for post tests. Will be used as @post_tests() decorator."""

    _hook_type = HookTypes.POST_TESTS

    def _run(
        self,
        *args,
        result_proxy: TestResult,
        metadata: GradescopeSubmissionMetadata | None,
        tested_tests_results: List[TestResult],
    ) -> None:
        super()._run(tested_tests_results, result_proxy, metadata)


post_tests = PostTests


class PreTests(HookBase):
    _hook_type = HookTypes.PRE_TESTS

    def _run(
        self,
        *args,
        result_proxy: TestResult | None,
        metadata: GradescopeSubmissionMetadata | None,
    ) -> None:
        super()._run(result_proxy, metadata)


pre_tests = PreTests
