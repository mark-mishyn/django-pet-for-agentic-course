Run the full test suite with `uv run python manage.py test -v2`.

If all tests pass, report the summary and stop.

If any tests fail:
1. Show which tests failed and the failure reason (keep it concise — don't dump the full traceback unless it's useful)
2. Read the failing test code and the relevant view/serializer/model code
3. Diagnose whether the bug is in the test or in the application code
4. Offer a fix — explain what's wrong and ask before applying changes
